const { Resend } = require('resend');
const resend = new Resend(process.env.RESEND_API_KEY);

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, phone, subject, message } = req.body;

    // Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Send email to info@gratiaglobal.com
    const data = await resend.emails.send({
      from: 'contact@gratiaglobal.com',
      to: ['info@gratiaglobal.com'],
      subject: subject || 'New Contact Form Submission - Gratia Global',
      reply_to: email,
      html: `
        <h2>New Contact Form Submission</h2>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Phone:</strong> ${phone || 'N/A'}</p>
        <p><strong>Subject:</strong> ${subject || 'N/A'}</p>
        <p><strong>Message:</strong></p>
        <p>${message.replace(/\n/g, '<br>')}</p>
        <p><em>Submitted from: ${req.body.form_source || 'Contact Page'}</em></p>
      `,
    });

    // Send confirmation email to user
    await resend.emails.send({
      from: 'info@gratiaglobal.com',
      to: [email],
      subject: 'Thank you for contacting Gratia Global',
      html: `
        <h2>Thank you for contacting us!</h2>
        <p>Dear ${name},</p>
        <p>We have received your message and will get back to you soon.</p>
        <p>Our team typically responds within 24-48 business hours.</p>
        <p>Best regards,<br>The Gratia Global Team</p>
      `,
    });

    return res.status(200).json({ success: true, data });
  } catch (error) {
    console.error('Error sending email:', error);
    return res.status(500).json({ error: 'Failed to send email. Please try again.' });
  }
};
