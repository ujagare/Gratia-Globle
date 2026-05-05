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

    // Send email to info@gratiaglobal.com (Premium Golden Template)
    const data = await resend.emails.send({
      from: 'onboarding@resend.dev',  // Using Resend's default verified sender
      to: ['info@gratiaglobal.com'],
      subject: `New Inquiry: ${subject || 'Contact Form'} - ${name}`,
      reply_to: email,
      html: `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body { font-family: 'Manrope', 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background: #f7f1e8; }
            .container { max-width: 600px; margin: 0 auto; background: #ffffff; }
            .header { background: linear-gradient(135deg, #c8911d 0%, #9f6810 100%); padding: 30px; text-align: center; }
            .header h1 { color: #ffffff; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 28px; margin: 0; font-weight: 400; letter-spacing: 0.02em; }
            .content { padding: 35px 30px; }
            .section-title { color: #2b3518; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 22px; margin-bottom: 20px; }
            .details-box { background: linear-gradient(135deg, rgba(201, 145, 29, 0.08), rgba(255, 248, 231, 0.5)); border-left: 4px solid #c8911d; padding: 20px 22px; margin: 20px 0; border-radius: 0 12px 12px 0; }
            .details-box p { margin: 8px 0; color: #4d4a43; font-size: 15px; }
            .details-box strong { color: #2b2515; min-width: 80px; display: inline-block; }
            .message-box { background: #faf6ef; border: 1px solid rgba(201, 145, 29, 0.2); padding: 20px; border-radius: 12px; margin: 20px 0; }
            .message-box p { color: #4d4a43; line-height: 1.8; margin: 0; white-space: pre-wrap; }
            .footer { background: #2b3518; padding: 25px; text-align: center; }
            .footer p { color: rgba(255, 246, 231, 0.8); font-size: 13px; margin: 5px 0; }
            .badge { display: inline-block; background: rgba(255, 248, 231, 0.2); color: #f0c96d; padding: 6px 14px; border-radius: 999px; font-size: 12px; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 15px; }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <div style="color: #f0c96d; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 20px; margin-bottom: 8px;">Gratia Global</div>
              <h1>New Contact Inquiry</h1>
            </div>
            <div class="content">
              <div class="badge">NEW MESSAGE</div>
              <h2 class="section-title">Contact Details</h2>
              <div class="details-box">
                <p><strong>Name:</strong> ${name}</p>
                <p><strong>Email:</strong> <a href="mailto:${email}">${email}</a></p>
                ${phone ? `<p><strong>Phone:</strong> <a href="tel:${phone}">${phone}</a></p>` : ''}
                <p><strong>Subject:</strong> ${subject || 'General Inquiry'}</p>
                <p><strong>Source:</strong> ${req.body.form_source || 'Contact Page'}</p>
              </div>
              
              <h2 class="section-title">Message</h2>
              <div class="message-box">
                <p>${message.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>')}</p>
              </div>
              
              <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(201, 145, 29, 0.2);">
                <p style="color: #6f6658; font-size: 13px;">⏱ Submitted: ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}</p>
              </div>
            </div>
            <div class="footer">
              <p style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 18px; color: #f0c96d;">Gratia Global</p>
              <p>Premium Agro & Herbal Exports</p>
              <p style="margin-top: 12px;">📧 info@gratiaglobal.com | 📞 +91 98765 43210</p>
            </div>
          </div>
        </body>
        </html>
      `,
    });

    // Send confirmation email to user (Premium Golden Template)
    await resend.emails.send({
      from: 'onboarding@resend.dev',  // Using Resend's verified sender
      to: [email],
      subject: 'Thank You for Contacting Gratia Global | We Received Your Message',
      html: `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body { font-family: 'Manrope', 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(180deg, #fdfaf5 0%, #fbf6ef 100%); }
            .container { max-width: 600px; margin: 0 auto; background: #ffffff; }
            .header { background: linear-gradient(135deg, #c8911d 0%, #9f6810 100%); padding: 40px 30px; text-align: center; }
            .header h1 { color: #ffffff; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 32px; margin: 0; font-weight: 400; letter-spacing: 0.02em; }
            .content { padding: 40px 30px; }
            .greeting { font-size: 20px; color: #2b3518; font-family: 'Cormorant Garamond', Georgia, serif; margin-bottom: 20px; }
            .message { color: #4d4a43; line-height: 1.8; font-size: 15px; margin-bottom: 25px; }
            .info-box { background: linear-gradient(135deg, rgba(201, 145, 29, 0.08), rgba(255, 248, 231, 0.5)); border-left: 4px solid #c8911d; padding: 18px 20px; margin: 25px 0; border-radius: 0 12px 12px 0; }
            .info-box p { margin: 5px 0; color: #5a4b33; font-size: 14px; }
            .divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(201, 145, 29, 0.4), transparent); margin: 30px 0; }
            .footer { background: linear-gradient(180deg, #2b3518 0%, #1a2210 100%); padding: 30px; text-align: center; }
            .footer p { color: rgba(255, 246, 231, 0.8); font-size: 13px; margin: 5px 0; }
            .logo-text { color: #f0c96d; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 24px; margin-bottom: 10px; }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <div class="logo-text">Gratia Global</div>
              <h1>Thank You for Contacting Us!</h1>
            </div>
            <div class="content">
              <p class="greeting">Dear ${name},</p>
              <p class="message">We have successfully received your message and appreciate you reaching out to us. Our team is reviewing your inquiry and will respond within <strong>24-48 business hours</strong>.</p>
              
              <div class="info-box">
                <p><strong>Your Submission Details:</strong></p>
                <p>📧 Email: ${email}</p>
                ${phone ? `<p>📞 Phone: ${phone}</p>` : ''}
                <p>📝 Subject: ${subject || 'General Inquiry'}</p>
              </div>
              
              <p class="message">In the meantime, feel free to explore our premium range of herbal and agro products on our website.</p>
              
              <div class="divider"></div>
              
              <p style="color: #6f6658; font-size: 14px; text-align: center;">We export trust, quality, and excellence worldwide.</p>
            </div>
            <div class="footer">
              <p class="logo-text">Gratia Global</p>
              <p>Premium Agro & Herbal Exports</p>
              <p style="margin-top: 15px;">📧 info@gratiaglobal.com | 📞 +91 98765 43210</p>
              <p>A-1, Export House, Indore, Madhya Pradesh, India</p>
            </div>
          </div>
        </body>
        </html>
      `,
    });

    return res.status(200).json({ success: true, data });
  } catch (error) {
    console.error('Error sending email:', error);
    return res.status(500).json({ error: 'Failed to send email. Please try again.' });
  }
};
