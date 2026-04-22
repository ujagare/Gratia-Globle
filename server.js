const path = require("path");
const express = require("express");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const { Resend } = require("resend");
require("dotenv").config();

const app = express();
app.disable("x-powered-by");
app.set("trust proxy", 1);

const isProduction = process.env.NODE_ENV === "production";
const resendApiKey = process.env.RESEND_API_KEY || "";
const resend = resendApiKey ? new Resend(resendApiKey) : null;

const contactFromEmail = process.env.CONTACT_FROM_EMAIL || "";
const contactToEmail = process.env.CONTACT_TO_EMAIL || "";
const newsletterToEmail = process.env.NEWSLETTER_TO_EMAIL || contactToEmail;
const allowedOrigins = (process.env.APP_ORIGIN || "")
  .split(",")
  .map((value) => value.trim())
  .filter(Boolean);

app.use(
  helmet({
    crossOriginEmbedderPolicy: false,
    contentSecurityPolicy: false,
  }),
);

app.use(express.urlencoded({ extended: false, limit: "20kb" }));
app.use(express.json({ limit: "20kb" }));

const createLimiter = (max) =>
  rateLimit({
    windowMs: 15 * 60 * 1000,
    max,
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: "Too many requests. Please try again later." },
  });

const contactLimiter = createLimiter(20);
const newsletterLimiter = createLimiter(40);

const isAllowedOrigin = (origin) => {
  if (!origin || allowedOrigins.length === 0 || !isProduction) {
    return true;
  }
  return allowedOrigins.includes(origin);
};

const sanitizeText = (value, maxLength) => String(value || "").trim().slice(0, maxLength);
const escapeHtml = (value) =>
  String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
const isValidPhone = (phone) => /^[0-9+\-()\s]{7,20}$/.test(phone);

const validateBotGuards = (body) => {
  const honeypot = sanitizeText(body.company, 200);
  if (honeypot) {
    return "Bot request blocked.";
  }

  const loadedAt = Number(body.form_loaded_at || 0);
  if (!loadedAt || Number.isNaN(loadedAt)) {
    return "Invalid form request.";
  }

  if (Date.now() - loadedAt < 1800) {
    return "Please wait a moment and submit again.";
  }

  return null;
};

const ensureServiceIsConfigured = (res) => {
  if (!resend || !contactFromEmail || !contactToEmail) {
    res.status(500).json({ error: "Email service is not configured." });
    return false;
  }
  return true;
};

app.post("/api/newsletter", newsletterLimiter, async (req, res) => {
  if (!isAllowedOrigin(req.get("origin"))) {
    return res.status(403).json({ error: "Origin not allowed." });
  }

  if (!ensureServiceIsConfigured(res)) {
    return undefined;
  }

  const guardError = validateBotGuards(req.body);
  if (guardError) {
    return res.status(400).json({ error: guardError });
  }

  const email = sanitizeText(req.body.email, 180).toLowerCase();
  const formSource = sanitizeText(req.body.form_source, 80) || "Website";

  if (!isValidEmail(email)) {
    return res.status(400).json({ error: "Please provide a valid email address." });
  }

  try {
    await resend.emails.send({
      from: contactFromEmail,
      to: newsletterToEmail,
      subject: `Newsletter subscription - ${formSource}`,
      html: `
        <h2>Newsletter Subscription</h2>
        <p><strong>Email:</strong> ${escapeHtml(email)}</p>
        <p><strong>Source:</strong> ${escapeHtml(formSource)}</p>
        <p><strong>Submitted at:</strong> ${new Date().toISOString()}</p>
      `,
      replyTo: email,
    });

    return res.status(200).json({ ok: true });
  } catch (error) {
    return res.status(500).json({ error: "Could not submit newsletter request." });
  }
});

app.post("/api/contact", contactLimiter, async (req, res) => {
  if (!isAllowedOrigin(req.get("origin"))) {
    return res.status(403).json({ error: "Origin not allowed." });
  }

  if (!ensureServiceIsConfigured(res)) {
    return undefined;
  }

  const guardError = validateBotGuards(req.body);
  if (guardError) {
    return res.status(400).json({ error: guardError });
  }

  const name = sanitizeText(req.body.name, 120);
  const email = sanitizeText(req.body.email, 180).toLowerCase();
  const phone = sanitizeText(req.body.phone, 24);
  const subject = sanitizeText(req.body.subject, 160);
  const message = sanitizeText(req.body.message, 3000);
  const formSource = sanitizeText(req.body.form_source, 80) || "Contact Page";

  if (name.length < 2) {
    return res.status(400).json({ error: "Name is too short." });
  }
  if (!isValidEmail(email)) {
    return res.status(400).json({ error: "Please provide a valid email address." });
  }
  if (!isValidPhone(phone)) {
    return res.status(400).json({ error: "Please provide a valid phone number." });
  }
  if (subject.length < 3) {
    return res.status(400).json({ error: "Subject is too short." });
  }
  if (message.length < 10) {
    return res.status(400).json({ error: "Message is too short." });
  }

  try {
    await resend.emails.send({
      from: contactFromEmail,
      to: contactToEmail,
      subject: `Website Inquiry: ${subject}`,
      html: `
        <h2>New Contact Inquiry</h2>
        <p><strong>Name:</strong> ${escapeHtml(name)}</p>
        <p><strong>Email:</strong> ${escapeHtml(email)}</p>
        <p><strong>Phone:</strong> ${escapeHtml(phone)}</p>
        <p><strong>Source:</strong> ${escapeHtml(formSource)}</p>
        <p><strong>Message:</strong></p>
        <p>${escapeHtml(message).replaceAll("\n", "<br/>")}</p>
        <p><strong>Submitted at:</strong> ${new Date().toISOString()}</p>
      `,
      replyTo: email,
    });

    return res.status(200).json({ ok: true });
  } catch (error) {
    return res.status(500).json({ error: "Could not send your message." });
  }
});

app.use(express.static(path.join(__dirname)));

app.use((req, res) => {
  res.status(404).json({ error: "Not found." });
});

const port = Number(process.env.PORT || 3000);
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
