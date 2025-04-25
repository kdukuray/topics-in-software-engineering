/*import React, { useState } from 'react';
import axios from 'axios';

const Checkout = () => {
  const [paymentMethod, setPaymentMethod] = useState('');
  const [paymentLink, setPaymentLink] = useState('');

  const handlePayment = async () => {
    if (paymentMethod === 'ledgerpay') {
      try {
        // Example request to create a LedgerPay invoice
        const response = await axios.post('http://localhost:5000/api/create-invoice', {
          amount: 1500, // Example amount (adjust based on cart total)
          currency: 'USD', // Example currency
        });

        setPaymentLink(response.data.paymentLink); // Return payment link from backend
      } catch (error) {
        console.error('Error creating invoice with LedgerPay:', error);
      }
    }
  };

  return (
    <div>
      <h1>Checkout</h1>
      <div>
        <button onClick={() => setPaymentMethod('ledgerpay')}>Pay with LedgerPay</button>
        <button onClick={() => setPaymentMethod('paypal')}>Pay with PayPal</button>
      </div>

      {paymentMethod === 'ledgerpay' && (
        <div>
          <button onClick={handlePayment}>Generate LedgerPay Invoice</button>
        </div>
      )}

      {paymentLink && (
        <div>
          <h3>Payment Link</h3>
          <a href={paymentLink} target="_blank" rel="noopener noreferrer">
            Click to Pay with LedgerPay
          </a>
        </div>
      )}
    </div>
  );
};

export default Checkout;
*/
import React from 'react';
import { useLocation } from 'react-router-dom'; // To access passed state
import axios from 'axios';

const Checkout = () => {
  const location = useLocation();
  const cart = location.state?.cart || [];  // Getting cart from state or defaulting to an empty array
  console.log(cart)
  const [paymentMethod, setPaymentMethod] = React.useState('');
  const [paymentLink, setPaymentLink] = React.useState('');
  const paymentToken = "sdjfknwejdfncwoe";


  function getInvoiceUrl() {
    const itemMap = {};
  
    // Aggregate duplicates
    cart.forEach(item => {
      const name = item.name;
      const price = item.price;
      const count = item.count || 1;
  
      if (itemMap[name]) {
        itemMap[name].count += count;
      } else {
        itemMap[name] = { price, count };
      }
    });
  
    const items = Object.keys(itemMap).join(' ');
    const prices = Object.values(itemMap).map(i => i.price).join(' ');
    const counts = Object.values(itemMap).map(i => i.count).join(' ');
  
    const url = `http://localhost:3000/invoice/?items=${encodeURIComponent(items)}&prices=${encodeURIComponent(prices)}&counts=${encodeURIComponent(counts)}&paymenttoken=${encodeURIComponent(paymentToken)}`;
    return url;
  }
  

  const handlePayment = async () => {
    if (paymentMethod === 'ledgerpay') {
      try {
        const response = await axios.post('http://localhost:5000/api/create-invoice', {
          amount: cart.reduce((total, product) => total + product.price, 0),  // Total price of the cart
          currency: 'USD',
        });
        setPaymentLink(response.data.paymentLink);
      } catch (error) {
        console.error('Error creating invoice with LedgerPay:', error);
      }
    }
  };

  function goToInvoice(){
    


  }

  return (
    <div>
      <h1>Checkout</h1>

      <h2>Your Cart</h2>
      <ul>
        {cart.map((product, index) => (
          <li key={index}>
            {product.name} - ${product.price}
          </li>
        ))}
      </ul>
      <h3>Total: ${cart.reduce((total, product) => total + product.price, 0)}</h3>

      <div>
        <button onClick={() => window.location.href = getInvoiceUrl()}>Pay with LedgerPay</button>
        <button onClick={() => setPaymentMethod('paypal')}>Pay with PayPal</button>
      </div>

      {paymentMethod === 'ledgerpay' && (
        <div>
          <button onClick={handlePayment}>Generate LedgerPay Invoice</button>
        </div>
      )}

      {paymentLink && (
        <div>
          <h3>Payment Link</h3>
          <a href={paymentLink} target="_blank" rel="noopener noreferrer">
            Click to Pay with LedgerPay
          </a>
        </div>
      )}
    </div>
  );
};

export default Checkout;
