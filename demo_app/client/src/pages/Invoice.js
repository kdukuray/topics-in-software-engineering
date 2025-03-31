import logo from './logo.svg';
import { Transaction, Connection, PublicKey, clusterApiUrl,  SystemProgram } from '@solana/web3.js';
import { useState } from 'react';
import { Buffer } from 'buffer';
import './App.css';

function Invoice() {
  const queryParams = new URLSearchParams(window.location.search);

  const [connectionStatus, setConnectionStatus] = useState();
  const [userPublicKey, setUserPublicKey] = useState(false);
  const [item, setItem] = useState(queryParams.get("item_name"));
  const [price, setPrice] = useState(Number(queryParams.get("price")));
  const [tax, setTax] = useState(Number(queryParams.get("tax")));
  const [paymentType, setPaymentType] = useState("One Time Payment");

  window.Buffer = Buffer;
  const wallet = window.solana;

  async function initiateWalletConnection() {
    if (wallet?.isPhantom) {
      await wallet.connect();
      setConnectionStatus(true);
      setUserPublicKey(wallet.publicKey.toBase58());
    }
  }

  async function makeAndSendTransation() {
    const blockchainConnection = new Connection(clusterApiUrl("devnet"), "confirmed");
    await wallet.connect();

    try {
      const fromPubkey = new PublicKey(wallet.publicKey);
      const toPubkey = new PublicKey("5hM386Bx7DeyWTP3VvePE5TAYTxMU4s9jvSWQcPbhuE7");

      // Convert price from SOL to lamports (1 SOL = 1_000_000_000 lamports)
      const lamports = price * 1_000_000_000;

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

      alert(`Transaction successful! \nTransaction ID:\n${txid}`);
      console.log("Transaction ID:", txid);
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
          <p><strong>Item:</strong> {item}</p>
          <p><strong>Price:</strong> {price} SOL</p>
          <p><strong>Tax:</strong> {tax}</p>
          <p><strong>Payment Type:</strong> {paymentType}</p>
        </div>
        <button onClick={makeAndSendTransation} className="btn btn-purple">Make Transaction</button>
      </div>
    </div>
  );
}

export default App;
