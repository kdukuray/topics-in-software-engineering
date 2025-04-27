import { useState } from "react";

function SubscribeToBusiness() {
  const [formData, setFormData] = useState({
    client_name: "",
    client_email: "",
    client_phone: "",
    plan_name: "",
    total_price: "",
    business_name: "", // required to match with Django User
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:8000/api/subscriptions/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

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
    return <p>✅ Subscription successful! You’ll receive a payment link soon.</p>;
  }

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Subscribe to a Business</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="client_name"
          placeholder="Your Name"
          onChange={handleChange}
          required
        /><br />
        <input
          name="client_email"
          type="email"
          placeholder="Email"
          onChange={handleChange}
          required
        /><br />
        <input
          name="client_phone"
          placeholder="Phone (optional)"
          onChange={handleChange}
        /><br />
        <input
          name="plan_name"
          placeholder="Plan Name"
          onChange={handleChange}
          required
        /><br />
        <input
          name="total_price"
          placeholder="Price in SOL"
          onChange={handleChange}
          required
        /><br />
        <input
          name="business_name"
          placeholder="Business Username"
          onChange={handleChange}
          required
        /><br /><br />
        <button type="submit">Subscribe</button>
      </form>
    </div>
  );
}

export default SubscribeToBusiness;
