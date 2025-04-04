const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = 5000;

app.use(cors());
app.use(bodyParser.json());

// Placeholder LedgerPay API URL
const ledgerPayAPIUrl = 'https://ledgerpay.com/create-invoice'; // this end point is the bridge to ledgerpay

// Mock API Key for LedgerPay (you should replace with actual API keys)
const ledgerPayAPIKey = 'YOUR_LEDGERPAY_API_KEY';

// Create invoice route (for LedgerPay payment)
app.post('/api/create-invoice', async (req, res) => {
  try {
    const { amount, currency } = req.body;

    // Send request to LedgerPay API to create an invoice
    const response = await axios.post(
      ledgerPayAPIUrl,
      {
        amount,
        currency,
      },
      {
        headers: {
          'Authorization': `Bearer ${ledgerPayAPIKey}`,
        },
      }
    );

    // Return the payment link
    res.json({ paymentLink: response.data.paymentLink });
  } catch (error) {
    console.error('Error generating invoice with LedgerPay:', error);
    res.status(500).json({ error: 'Error generating invoice' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
