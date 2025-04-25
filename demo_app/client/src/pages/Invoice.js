
import { Transaction, Connection, PublicKey, clusterApiUrl, SystemProgram } from '@solana/web3.js';
import { useState } from 'react';
import { Buffer } from 'buffer';


function Invoice() {
  const queryParams = new URLSearchParams(window.location.search);

  const [connectionStatus, setConnectionStatus] = useState();
  const [userPublicKey, setUserPublicKey] = useState(false);
  const [items, setItems] = useState(queryParams.get("items"));
  const [prices, setPrices] = useState(queryParams.get("prices"));
  const [counts, setCounts] = useState(queryParams.get("counts"))
  const [paymentToken, setPaymentToken] = useState(queryParams.get("paymenttoken"))
  const [walletConnected, setWalletConnected] = useState(false);
  // const [tax, setTax] = useState(Number(queryParams.get("tax")));
  const [paymentType, setPaymentType] = useState("One Time Payment");

  const itemNames = items.split(" ");
  const itemPrices = prices.split(" ");
  const itemCounts = counts.split(" ");  // fixed typo: 'ittemCounts' to 'itemCounts'

  const totalPrice = itemPrices
    .map((price, index) => parseFloat(price) * parseInt(itemCounts[index] || "1"))
    .reduce((sum, subtotal) => sum + subtotal, 0);


  window.Buffer = Buffer;
  const wallet = window.solana;

  async function initiateWalletConnection() {
    if (wallet?.isPhantom) {
      await wallet.connect();
      setConnectionStatus(true);
      setUserPublicKey(wallet.publicKey.toBase58());
      setWalletConnected(true)
    }
  }

  async function get_wallet_address(){
    const resp = await fetch(`http://127.0.0.1:8000/get-wallet-address/?payment_token=${paymentToken}`, {
      method: "GET",
    })
    if (resp.ok){
      let data = await resp.json()
      return data["wallet_address"]
    }

  }

  async function pingLedgerPayWithNewTransaction(transaction_signature){
    const payload = new FormData();
    
    const sellerWalletAddress = await get_wallet_address();
    payload.append("user_wallet_address", sellerWalletAddress)
    payload.append("amount", `${totalPrice}`)
    payload.append("transaction_signature", transaction_signature)
    const resp = await fetch(`http://127.0.0.1:8000/new-transaction/`, {
      method: "POST",
      body: payload,
    })
    if (resp.ok){
      let transactionLedgerPayId = await resp.json()
      alert(`Your transaction with ID: ${transactionLedgerPayId['new_transaction_id']} has been has been submitted.`)

    }

  }

  async function makeAndSendTransation() {
    if (!walletConnected){
      alert("Please Connect your wallet first")
      return;
    }
    // use the payment token to get the sellers public wallet address
    const sellerWalletAddress = await get_wallet_address();

    // establish a blockchain connection
    const blockchainConnection = new Connection(clusterApiUrl("devnet"), "confirmed");
    await wallet.connect();

    // Attempt to send transaction to the blockchain
    try {
      const fromPubkey = new PublicKey(wallet.publicKey);
      const toPubkey = new PublicKey(sellerWalletAddress);

      // Convert price from SOL to lamports (1 SOL = 1_000_000_000 lamports)
      const lamports = totalPrice * 1_000_000_000;

      // Create a new transaction obect
      let transaction = new Transaction().add(
        SystemProgram.transfer({
          fromPubkey,
          toPubkey,
          lamports,
        })
      );

      transaction.feePayer = fromPubkey;
      transaction.recentBlockhash = (await blockchainConnection.getLatestBlockhash()).blockhash;

      const signedTransaction = await wallet.signTransaction(transaction);
      const txid = await blockchainConnection.sendRawTransaction(signedTransaction.serialize());
      await blockchainConnection.confirmTransaction(txid, "confirmed");

      alert(`Transaction successful! \nTransaction Signature:\n${txid}`);
      pingLedgerPayWithNewTransaction(txid)
    } catch (error) {
      console.error("Transaction failed:", error);
      alert("Transaction failed. See console for details.");
    }
  }


  return (
    <div className="app-container">
      <div className="card">
        <h2 className="card-heading">Connect Phantom Wallet</h2>
        <p className="card-subtext">To make payments, first connect to your Phantom Wallet.</p>
        <p className="status">Connection status: <strong>{connectionStatus ? "Successful" : "Pending"}</strong></p>
        {connectionStatus && (
          <p className="wallet-address">
            Connected to wallet: <br />
            <strong>{wallet.publicKey.toBase58()}</strong>
          </p>
        )}
        <button onClick={initiateWalletConnection} className="btn btn-green">Connect Wallet</button>
      </div>

      <div className="card">
        <h2 className="card-heading">Transaction Details</h2>
        <div className="transaction-details">
          <p><strong>Cart Details:</strong></p>
          <div>
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Price</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                {itemNames.map((cartItem, index) => (
                  <tr key={index}>
                    <td>{cartItem}</td>
                    <td>{itemPrices[index]}</td>
                    <td>{itemCounts[index]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p><strong>Total: {totalPrice} SOL</strong></p>
          <p><strong>Payment Type:</strong> {paymentType}</p>
        </div>
        <button onClick={makeAndSendTransation} className="btn btn-purple" title="You must connect your wallet">Make Transaction</button>        
      </div>
    </div>
  );
}

export default Invoice;
