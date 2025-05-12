# 🧾 generate-ledgerpay-url

Generate a LedgerPay invoice URL from a shopping cart array and payment token.  
Useful for creating pre-filled payment links in LedgerPay-powered applications.

---

## 📦 Installation

```
bash
npm install generate-ledgerpay-url
```
🚀 Usage
```
const generateLedgerPayUrl = require('generate-ledgerpay-url');

const cart = [
  { name: 'T-shirt', price: 25, count: 2 },
  { name: 'Mug', price: 10, count: 1 },
  { name: 'T-shirt', price: 25, count: 1 }
];

const paymentToken = 'abc123';

const url = generateLedgerPayUrl(cart, paymentToken);
console.log(url);
```
🧾 Sample Output:
```
https://steady-melba-a90a8a.netlify.app/invoice/?items=T-shirt Mug&prices=25 10&counts=3 1&paymenttoken=abc123
```
---
🧠 Function Signature
```
generateLedgerPayUrl(
  cart: Array<{ name: string; price: number|string; count?: number }>,
  paymentToken: string
): string
```
🛠 How It Works
Accepts an array of items (name, price, count).

Combines duplicate items by name.

Constructs query string:

items: space-separated item names

prices: space-separated prices

counts: space-separated quantities

paymenttoken: your LedgerPay destination token

Returns a full invoice URL ready to use in a browser or payment flow.

🧪 Example Test
```
const url = generateLedgerPayUrl(
  [
    { name: 'Notebook', price: 5, count: 2 },
    { name: 'Pen', price: 1.5, count: 3 },
    { name: 'Notebook', price: 5, count: 1 }
  ],
  'myToken123'
);
```
```
// Output: 
// https://steady-melba-a90a8a.netlify.app/invoice/?items=Notebook Pen&prices=5 1.5&counts=3 3&paymenttoken=myToken123
```
📄 License
MIT © [Ledger Pay Team]