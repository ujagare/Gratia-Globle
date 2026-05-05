const { Resend } = require('resend');
const resend = new Resend(process.env.RESEND_API_KEY);

module.exports = async function handler(req, res) {
  // Log all request details
  console.log('Request method:', req.method);
  console.log('Environment RESEND_API_KEY exists:', !!process.env.RESEND_API_KEY);
  
  // Set CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, phone, subject, message } = req.body;
    console.log('Received data:', { name, email, subject });

    if (!name || !email || !message) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Send to info@gratiaglobal.com
    const data = await resend.emails.send({
      from: 'onboarding@resend.dev',
      to: ['info@gratiaglobal.com'],
      subject: `New Inquiry: ${subject || 'Contact Form'} - ${name}`,
      html: `<h2>New Contact</h2><p>Name: ${name}</p><p>Email: ${email}</p>${phone ? `<p>Phone: ${phone}</p>` : ''}<p>Message: ${message}</p>`
    });
    
    console.log('Email sent successfully:', data);
    
    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Full error:', error);
    return res.status(500).json({ error: error.message || 'Failed to send email' });
  }
};
