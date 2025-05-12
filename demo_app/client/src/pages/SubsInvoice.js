import { Transaction, Connection, PublicKey, clusterApiUrl, SystemProgram } from '@solana/web3.js';
import { useState, useEffect } from 'react';
import { Buffer } from 'buffer';

function SubsInvoice() {
  const queryParams = new URLSearchParams(window.location.search);

  const clientName = queryParams.get("client_name");
  const clientEmail = queryParams.get("client_email");
  const planName = queryParams.get("plan_name");
  const price = parseFloat(queryParams.get("price"));
  const paymentToken = queryParams.get("wallet"); // actually the payment token

  const [connectionStatus, setConnectionStatus] = useState(false);
  const [userPublicKey, setUserPublicKey] = useState(null);
  const [receiverWallet, setReceiverWallet] = useState(null);
  const [walletConnected, setWalletConnected] = useState(false);
  const [paid, setPaid] = useState(false);
  const [loadingWallet, setLoadingWallet] = useState(true);
  const [walletError, setWalletError] = useState(null);

  window.Buffer = Buffer;
  const wallet = window.solana;

  useEffect(() => {
    async function fetchWalletAddress() {
      try {
        const res = await fetch(`https://ledger-pay-demo-spring-fff5fa203a7c.herokuapp.com/get-wallet-address/?payment_token=${paymentToken}`);
        if (!res.ok) throw new Error("Failed to fetch wallet address.");
        const data = await res.json();
        const pubkey = new PublicKey(data.wallet_address);
        setReceiverWallet(pubkey);
        setLoadingWallet(false);
      } catch (err) {
        console.error(err);
        setWalletError("❌ Could not retrieve business wallet address.");
        setLoadingWallet(false);
      }
    }

    fetchWalletAddress();
  }, [paymentToken]);

  async function connectWallet() {
    if (wallet?.isPhantom) {
      try {
        await wallet.connect();
        setConnectionStatus(true);
        setUserPublicKey(wallet.publicKey.toBase58());
        setWalletConnected(true);
      } catch (error) {
        console.error("Wallet connection failed:", error);
        alert("Wallet connection failed.");
      }
    } else {
      alert("Phantom Wallet not found. Please install it.");
    }
  }

  async function pingLedgerPayWithNewTransaction(txid) {
    const formData = new FormData();
    formData.append("user_wallet_address", receiverWallet.toBase58());
    formData.append("amount", `${price}`);
    formData.append("transaction_signature", txid);

    try {
      const res = await fetch("https://ledger-pay-demo-spring-fff5fa203a7c.herokuapp.com/new-transaction/", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        alert(`🧾 Your transaction with ID: ${data.new_transaction_id} has been submitted.`);
      }
    } catch (err) {
      console.error("Failed to notify backend of transaction:", err);
    }
  }

  async function sendTransaction() {
    if (!walletConnected) {
      alert("Please connect your wallet first.");
      return;
    }

    if (!receiverWallet) {
      alert("Recipient wallet address is not ready.");
      return;
    }

    const connection = new Connection(clusterApiUrl("devnet"), "confirmed");

    try {
      const fromPubkey = new PublicKey(wallet.publicKey);
      const toPubkey = receiverWallet;
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

      alert(`✅ Subscription payment successful!\nTransaction Signature:\n${txid}`);
      setPaid(true);
      await pingLedgerPayWithNewTransaction(txid);
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
        {loadingWallet ? (
          <p>Loading wallet info...</p>
        ) : walletError ? (
          <p style={{ color: "red" }}>{walletError}</p>
        ) : (
          <p><strong>Pay To Wallet:</strong> {receiverWallet.toBase58()}</p>
        )}

        {!connectionStatus && !walletError && (
          <button onClick={connectWallet} className="btn btn-green">Connect Phantom Wallet</button>
        )}

        {connectionStatus && !walletError && (
          <div>
            <p className="wallet-address">
              Connected Wallet: <strong>{userPublicKey}</strong>
            </p>
            {!paid && (
              <button onClick={sendTransaction} className="btn btn-purple">
                Pay Now
              </button>
            )}
            {paid && <p>✅ Payment Completed. Thank you!</p>}
          </div>
        )}
      </div>
    </div>
  );
}

export default SubsInvoice;
