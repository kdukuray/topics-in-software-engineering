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
  const [paymentMethod, setPaymentMethod] = React.useState('');
  const [paymentLink, setPaymentLink] = React.useState('');

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
