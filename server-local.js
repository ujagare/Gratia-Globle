const express = require('express');
const { Resend } = require('resend');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static(__dirname));

const resend = new Resend(process.env.RESEND_API_KEY);

app.post('/api/contact', async (req, res) => {
  try {
    const { name, email, phone, subject, message } = req.body;
    
    if (!name || !email || !message) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    await resend.emails.send({
      from: 'info@gratiaglobal.com',
      to: ['info@gratiaglobal.com'],
      subject: `New Inquiry: ${subject || 'Contact Form'} - ${name}`,
      html: `<h2>New Contact</h2><p>Name: ${name}</p><p>Email: ${email}</p>`
    });

    await resend.emails.send({
      from: 'info@gratiaglobal.com',
      to: [email],
      subject: 'Thank You',
      html: `<h2>Thank you!</h2><p>Dear ${name}, we received your message.</p>`
    });

    res.json({ success: true });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to send email' });
  }
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
