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
  const phone = sanitizeText(body.phone, 24);
  const subject = sanitizeText(body.subject, 160);
  const message = sanitizeText(body.message, 3000);
  const formSource = sanitizeText(body.form_source, 80) || "Contact Page";

  if (name.length < 2) {
    return sendJson(res, 400, { error: "Name is too short." });
  }
  if (!isValidEmail(email)) {
    return sendJson(res, 400, { error: "Please provide a valid email address." });
  }
  if (!isValidPhone(phone)) {
    return sendJson(res, 400, { error: "Please provide a valid phone number." });
  }
  if (subject.length < 3) {
    return sendJson(res, 400, { error: "Subject is too short." });
  }
  if (message.length < 10) {
    return sendJson(res, 400, { error: "Message is too short." });
  }

  const result = await sendResendEmail({
    to: process.env.CONTACT_TO_EMAIL,
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
    text: [
      "New Contact Inquiry",
      `Name: ${name}`,
      `Email: ${email}`,
      `Phone: ${phone}`,
      `Source: ${formSource}`,
      "Message:",
      message,
      `Submitted at: ${new Date().toISOString()}`,
    ].join("\n"),
    replyTo: email,
    tags: [
      { name: "form", value: "contact" },
      { name: "source", value: formSource.replaceAll(/[^A-Za-z0-9_-]/g, "-") || "contact-page" },
    ],
    idempotencyPrefix: "contact",
  });

  if (!result.ok) {
    return sendJson(res, result.status, { error: result.error || "Could not send your message." });
  }

  return sendJson(res, 200, { ok: true });
};
