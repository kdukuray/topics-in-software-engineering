import React, { useState } from "react";
import "/Users/faye/topics-in-software-engineering/demo_app/client/src/App.css";
import { useSearchParams } from "react-router-dom";
const paymentOptions = [
  { id: "credit-card", name: "Credit Card", icon: "💳" },
  { id: "paypal", name: "PayPal", icon: "PP" },
  { id: "bank-transfer", name: "Bank Transfer", icon: "🏦" },
  { id: "cash", name: "Cash on Delivery", icon: "💵" },
  { id: "bitcoin", name: "Bitcoin", icon: "₿" },
  { id: "ethereum", name: "Ethereum", icon: "Ξ" },
  { id: "usdt", name: "Tether (USDT)", icon: "₮" },
  { id: "litecoin", name: "Litecoin", icon: "Ł" },
  { id: "binance", name: "Binance Coin", icon: "BNB" },
];
export function PaymentSelector() {
  const [selectedPayments, setSelectedPayments] = useState([]);
  const [searchParam] = useSearchParams();
  const storeId = searchParam.get("storeId");


  function handleSubmit() {
    if (selectedPayments.length === 0) {
      alert("Please select at least one payment method");
      return;
    }
    // Here you can send selectedPayments to your backend or handle it as needed
    console.log("Submitted payment methods:", selectedPayments);
  }

  function handleClear() {
    setSelectedPayments([]);
  }
  function handlePaymentToggle(paymentId) {
    if (selectedPayments.includes(paymentId)) {
      setSelectedPayments(selectedPayments.filter((id) => id !== paymentId));
    } else {
      setSelectedPayments([...selectedPayments, paymentId]);
    }
  }

  return (
    <div className="payment-selector">
      <h2>Preferred payment selection console</h2>
      <h3 style={{ color: "gray" }}>
        Under here you can select all the payment you would like to accept
      </h3>
      <div className="payment-options">
        {paymentOptions.map((option) => (
          <div
            key={option.id}
            className={`payment-option ${
              selectedPayments.includes(option.id) ? "selected" : ""
            }`}
            onClick={() => handlePaymentToggle(option.id)}
          >
            <span className="payment-icon">{option.icon}</span>
            <span className="payment-name">{option.name}</span>
          </div>
        ))}
      </div>
      {selectedPayments.length > 0 && (
        <div className="selected-summary">
          <h3>Selected Methods:</h3>
          <ul>
            {selectedPayments.map((paymentId) => (
              <li key={paymentId}>
                {paymentOptions.find((option) => option.id === paymentId).name}
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="payment-buttons">
        <button className="submit-btn" onClick={handleSubmit}>
          Submit
        </button>
        <button className="clear-btn" onClick={handleClear}>
          Clear
        </button>
      </div>
    </div>
  );
}

export default PaymentSelector;
