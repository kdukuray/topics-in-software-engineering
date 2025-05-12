import { useState } from "react";

function SubscribeToBusiness() {
  const [formData, setFormData] = useState({
    client_name: "",
    client_email: "",
    client_phone: "",
    plan_name: "",
    total_price: "",
    business_name: "",
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(
        "https://ledger-pay-demo-spring-fff5fa203a7c.herokuapp.com/api/subscriptions/create/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        }
      );

      if (res.ok) {
        setSubmitted(true);
      } else {
        const error = await res.json();
        alert("Failed: " + error.error);
      }
    } catch (err) {
      console.error(err);
      alert("Error submitting form");
    }
  };

  if (submitted) {
    return (
      <div className="success-message">
        ✅ Subscription successful! You’ll receive a payment link soon.
      </div>
    );
  }

  return (
    <div className="subscription-container">
      <h2 className="subscription-title">Subscribe to a Business</h2>
      <form onSubmit={handleSubmit} className="subscription-form">
        <input
          className="form-input"
          name="client_name"
          placeholder="Your Name"
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          name="client_email"
          type="email"
          placeholder="Email"
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          name="client_phone"
          placeholder="Phone (optional)"
          onChange={handleChange}
        />
        <input
          className="form-input"
          name="plan_name"
          placeholder="Plan Name"
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          name="total_price"
          placeholder="Price in SOL"
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          name="business_name"
          placeholder="Business Username"
          onChange={handleChange}
          required
        />
        <button type="submit" className="submit-button">Subscribe</button>
      </form>
    </div>
  );
}

export default SubscribeToBusiness;
