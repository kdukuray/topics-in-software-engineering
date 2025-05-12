import { Transaction, Connection, PublicKey, clusterApiUrl, SystemProgram } from '@solana/web3.js';
import { useState } from 'react';
import { Buffer } from 'buffer';

function SubsInvoice() {
  const queryParams = new URLSearchParams(window.location.search);

  const clientName = queryParams.get("client_name");
  const clientEmail = queryParams.get("client_email");
  const planName = queryParams.get("plan_name");
  const price = parseFloat(queryParams.get("price"));
  const businessWallet = queryParams.get("wallet");

  const [connectionStatus, setConnectionStatus] = useState(false);
  const [userPublicKey, setUserPublicKey] = useState(null);
  const [paid, setPaid] = useState(false);

  window.Buffer = Buffer;
  const wallet = window.solana;

  async function connectWallet() {
    if (wallet?.isPhantom) {
      try {
        await wallet.connect();
        setConnectionStatus(true);
        setUserPublicKey(wallet.publicKey.toBase58());
      } catch (error) {
        console.error("Wallet connection failed:", error);
        alert("Wallet connection failed.");
      }
    } else {
      alert("Phantom Wallet not found. Please install it.");
    }
  }

  async function sendTransaction() {
    const connection = new Connection(clusterApiUrl("devnet"), "confirmed");

    try {
      const fromPubkey = new PublicKey(wallet.publicKey);
      const toPubkey = new PublicKey(businessWallet);
      const lamports = price * 1_000_000_000;

      const transaction = new Transaction().add(
        SystemProgram.transfer({
          fromPubkey,
          toPubkey,
          lamports,
        })
      );

      transaction.feePayer = fromPubkey;
      transaction.recentBlockhash = (await connection.getLatestBlockhash()).blockhash;

      const signed = await wallet.signTransaction(transaction);
      const txid = await connection.sendRawTransaction(signed.serialize());
      await connection.confirmTransaction(txid, "confirmed");

      alert(`✅ Subscription payment successful!\nTransaction ID:\n${txid}`);
      console.log("Transaction ID:", txid);
      setPaid(true);
    } catch (err) {
      console.error("❌ Transaction failed:", err);
      alert("Transaction failed. See console for details.");
    }
  }

  return (
    <div className="app-container">
      <div className="card">
        <h2>Subscription Invoice</h2>
        <p><strong>Client:</strong> {clientName}</p>
        <p><strong>Email:</strong> {clientEmail}</p>
        <p><strong>Plan:</strong> {planName}</p>
        <p><strong>Amount Due:</strong> {price} SOL</p>
        <p><strong>Pay To Wallet:</strong> {businessWallet}</p>

        {!connectionStatus && (
          <button onClick={connectWallet} className="btn btn-green">Connect Phantom Wallet</button>
        )}

        {connectionStatus && (
          <div>
            <p className="wallet-address">
              Connected Wallet: <strong>{userPublicKey}</strong>
            </p>
            {!paid && (
              <button onClick={sendTransaction} className="btn btn-purple">Pay Now</button>
            )}
            {paid && <p>✅ Payment Completed. Thank you!</p>}
          </div>
        )}
      </div>
    </div>
  );
}

export default SubsInvoice;
