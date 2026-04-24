const {
  escapeHtml,
  isAllowedOrigin,
  isValidEmail,
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

  const email = sanitizeText(body.email, 180).toLowerCase();
  const formSource = sanitizeText(body.form_source, 80) || "Website";

  if (!isValidEmail(email)) {
    return sendJson(res, 400, { error: "Please provide a valid email address." });
  }

  const result = await sendResendEmail({
    to: process.env.NEWSLETTER_TO_EMAIL || process.env.CONTACT_TO_EMAIL,
    subject: `Newsletter subscription - ${formSource}`,
    html: `
      <h2>Newsletter Subscription</h2>
      <p><strong>Email:</strong> ${escapeHtml(email)}</p>
      <p><strong>Source:</strong> ${escapeHtml(formSource)}</p>
      <p><strong>Submitted at:</strong> ${new Date().toISOString()}</p>
    `,
    text: [
      "Newsletter Subscription",
      `Email: ${email}`,
      `Source: ${formSource}`,
      `Submitted at: ${new Date().toISOString()}`,
    ].join("\n"),
    replyTo: email,
    tags: [
      { name: "form", value: "newsletter" },
      { name: "source", value: formSource.replaceAll(/[^A-Za-z0-9_-]/g, "-") || "website" },
    ],
    idempotencyPrefix: "newsletter",
  });

  if (!result.ok) {
    return sendJson(res, result.status, { error: result.error || "Could not submit newsletter request." });
  }

  return sendJson(res, 200, { ok: true });
};
