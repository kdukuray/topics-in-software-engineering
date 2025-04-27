import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Change 'Switch' to 'Routes'
import Home from './pages/Home';
import Checkout from './pages/checkout';
import Invoice from "./pages/Invoice"
import SubscribeToBusiness from './pages/SubscribeToBusiness';

function App() {
  return (
    <Router>
      <div>
        <Routes>  {/* Replace 'Switch' with 'Routes' */}
          <Route path="/" element={<Home />} />  {/* Use 'element' prop instead of 'component' */}
          <Route path="/checkout" element={<Checkout />} /> {/* Use 'element' prop */}
          <Route path="/invoice" element={<Invoice />} />
          <Route path="/subscribe" element={<SubscribeToBusiness />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
