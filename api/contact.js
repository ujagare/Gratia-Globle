const {
  escapeHtml,
  isAllowedOrigin,
  isValidEmail,
  isValidPhone,
  parseRequestBody,
  sanitizeText,
  sendJson,
  sendResendEmail,
  validateBotGuards,
} = require("./_lib/email");

module.exports = async (req, res) => {
  res.setHeader("X-Robots-Tag", "noindex, nofollow");

  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return sendJson(res, 405, { error: "Method not allowed." });
  }

  const origin = req.headers.origin || "";
  if (!isAllowedOrigin(origin)) {
    return sendJson(res, 403, { error: "Origin not allowed." });
  }

  const body = await parseRequestBody(req);
  const guardError = validateBotGuards(body);
  if (guardError) {
    return sendJson(res, 400, { error: guardError });
  }

  const name = sanitizeText(body.name, 120);
  const email = sanitizeText(body.email, 180).toLowerCase();
  const phone = sanitizeText(body.phone, 40);
  const subject = sanitizeText(body.subject, 160) || "Contact Form";
  const message = sanitizeText(body.message, 3000);
  const formSource = sanitizeText(body.form_source, 80) || "Contact Page";

  if (!name || !email || !message) {
    return sendJson(res, 400, { error: "Please complete all required fields." });
  }

  if (!isValidEmail(email)) {
    return sendJson(res, 400, { error: "Please provide a valid email address." });
  }

  if (phone && !isValidPhone(phone)) {
    return sendJson(res, 400, { error: "Please provide a valid phone number." });
  }

  const result = await sendResendEmail({
    to: process.env.CONTACT_TO_EMAIL,
    subject: `New Inquiry: ${subject} - ${name}`,
    html: `
      <h2>New Contact Inquiry</h2>
      <p><strong>Name:</strong> ${escapeHtml(name)}</p>
      <p><strong>Email:</strong> ${escapeHtml(email)}</p>
      ${phone ? `<p><strong>Phone:</strong> ${escapeHtml(phone)}</p>` : ""}
      <p><strong>Subject:</strong> ${escapeHtml(subject)}</p>
      <p><strong>Source:</strong> ${escapeHtml(formSource)}</p>
      <p><strong>Message:</strong></p>
      <p>${escapeHtml(message).replaceAll("\n", "<br>")}</p>
      <p><strong>Submitted at:</strong> ${new Date().toISOString()}</p>
    `,
    text: [
      "New Contact Inquiry",
      `Name: ${name}`,
      `Email: ${email}`,
      phone ? `Phone: ${phone}` : "",
      `Subject: ${subject}`,
      `Source: ${formSource}`,
      "",
      message,
      "",
      `Submitted at: ${new Date().toISOString()}`,
    ]
      .filter(Boolean)
      .join("\n"),
    replyTo: email,
    tags: [
      { name: "form", value: "contact" },
      { name: "source", value: formSource.replaceAll(/[^A-Za-z0-9_-]/g, "-") || "website" },
    ],
    idempotencyPrefix: "contact",
  });

  if (!result.ok) {
    return sendJson(res, result.status, { error: result.error || "Could not submit contact request." });
  }

  return sendJson(res, 200, { ok: true, success: true });
};
