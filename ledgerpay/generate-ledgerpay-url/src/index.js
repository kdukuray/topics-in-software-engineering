/**
 * Generates a LedgerPay invoice URL with encoded item data.
 *
 * @param {Array} cart - Array of items. Each item must have: name (string), price (string|number), count (number).
 * @param {string} paymentToken - Token used to identify the payment destination.
 * @returns {string} - A full LedgerPay invoice URL.
 */
function generateLedgerPayUrl(cart, paymentToken) {
    const itemMap = {};
  
    cart.forEach(({ name, price, count = 1 }) => {
      if (itemMap[name]) {
        itemMap[name].count += count;
      } else {
        itemMap[name] = { price, count };
      }
    });
  
    const items = Object.keys(itemMap).join(' ');
    const prices = Object.values(itemMap).map(i => i.price).join(' ');
    const counts = Object.values(itemMap).map(i => i.count).join(' ');
  
    const baseUrl = 'https://steady-melba-a90a8a.netlify.app/invoice/';
    const queryParams = new URLSearchParams({
      items,
      prices,
      counts,
      paymenttoken: paymentToken,
    });
  
    return `${baseUrl}?${queryParams.toString()}`;
  }
  
  module.exports = generateLedgerPayUrl;