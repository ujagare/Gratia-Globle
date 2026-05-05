const crypto = require("crypto");
const querystring = require("querystring");

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_REGEX = /^[0-9+\-()\s]{7,20}$/;

const sendJson = (res, status, payload, extraHeaders = {}) => {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Content-Type-Options", "nosniff");
  Object.entries(extraHeaders).forEach(([key, value]) => {
    res.setHeader(key, value);
  });
  res.end(JSON.stringify(payload));
};

const parseRequestBody = async (req) => {
  if (typeof req.body === "string") {
    return querystring.parse(req.body);
  }

  if (req.body && typeof req.body === "object" && !Buffer.isBuffer(req.body)) {
    return req.body;
  }

  return await new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => {
      const raw = Buffer.concat(chunks).toString("utf8");
      const parsed = querystring.parse(raw);
      resolve(parsed);
    });
    req.on("error", reject);
  });
};

const sanitizeText = (value, maxLength) =>
  String(value ?? "")
    .trim()
    .slice(0, maxLength);

const escapeHtml = (value) =>
  String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

const isValidEmail = (email) => EMAIL_REGEX.test(email);
const isValidPhone = (phone) => PHONE_REGEX.test(phone);

const getAllowedOrigins = () => {
  const configuredOrigins = sanitizeText(process.env.APP_ORIGIN, 2000)
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean);

  const previewOrigin = process.env.VERCEL_URL
    ? `https://${sanitizeText(process.env.VERCEL_URL, 300)}`
    : "";

  const productionOrigins = [
    "https://gratiaglobal.com",
    "https://www.gratiaglobal.com",
  ];

  return new Set([...configuredOrigins, previewOrigin, ...productionOrigins].filter(Boolean));
};

const isAllowedOrigin = (origin) => {
  if (!origin) {
    return process.env.NODE_ENV !== "production";
  }

  const allowedOrigins = getAllowedOrigins();
  if (allowedOrigins.size === 0) {
    return process.env.NODE_ENV !== "production";
  }

  return allowedOrigins.has(origin);
};

const getSubmittedAt = (value) => {
  const timestamp = Number(value || 0);
  if (!Number.isNaN(timestamp) && timestamp > 0) {
    return timestamp;
  }

  const parsedDate = Date.parse(String(value || ""));
  return Number.isNaN(parsedDate) ? 0 : parsedDate;
};

const validateBotGuards = (fields) => {
  const honeypot = sanitizeText(fields.contact_website || fields.website_url, 200);
  if (honeypot) {
    return "Bot request blocked.";
  }

  const loadedAt = getSubmittedAt(fields.form_loaded_at);
  if (!loadedAt) {
    return "Invalid form request.";
  }

  if (Date.now() - loadedAt < 1800) {
    return "Please wait a moment and submit again.";
  }

  return null;
};

const getResendConfig = () => {
  const apiKey = sanitizeText(process.env.RESEND_API_KEY, 200);
  const fromEmail = sanitizeText(process.env.CONTACT_FROM_EMAIL, 180);
  const contactToEmail = sanitizeText(process.env.CONTACT_TO_EMAIL, 180);
  const newsletterToEmail = sanitizeText(
    process.env.NEWSLETTER_TO_EMAIL || contactToEmail,
    180,
  );

  if (!apiKey || !fromEmail || !contactToEmail) {
    return null;
  }

  return {
    apiKey,
    fromEmail,
    contactToEmail,
    newsletterToEmail,
  };
};

const createIdempotencyKey = (prefix, fields) => {
  const normalized = Object.keys(fields)
    .sort()
    .map((key) => `${key}:${String(fields[key] ?? "")}`)
    .join("|");

  return `${prefix}-${crypto.createHash("sha256").update(normalized).digest("hex").slice(0, 48)}`;
};

const sendResendEmail = async ({ to, subject, html, text, replyTo, tags, idempotencyPrefix }) => {
  const config = getResendConfig();
  if (!config) {
    return {
      ok: false,
      status: 500,
      error: "Email service is not configured.",
    };
  }

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${config.apiKey}`,
      "Content-Type": "application/json",
      "Idempotency-Key": createIdempotencyKey(idempotencyPrefix, {
        to,
        subject,
        html,
        text,
        replyTo,
      }),
    },
    body: JSON.stringify({
      from: config.fromEmail,
      to,
      subject,
      html,
      text,
      reply_to: replyTo,
      tags,
    }),
  });

  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = payload && payload.message ? String(payload.message) : "Could not send email.";
    return {
      ok: false,
      status: response.status || 500,
      error: detail,
    };
  }

  return {
    ok: true,
    status: 200,
    data: payload,
  };
};

module.exports = {
  escapeHtml,
  getAllowedOrigins,
  getResendConfig,
  isAllowedOrigin,
  isValidEmail,
  isValidPhone,
  parseRequestBody,
  sanitizeText,
  sendJson,
  sendResendEmail,
  validateBotGuards,
};
