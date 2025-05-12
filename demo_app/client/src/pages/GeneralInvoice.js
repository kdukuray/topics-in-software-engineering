import { Transaction, Connection, PublicKey, clusterApiUrl, SystemProgram } from '@solana/web3.js';
import { useState } from 'react';
import { Buffer } from 'buffer';

function GeneralInvoice() {
  const queryParams = new URLSearchParams(window.location.search);

  const [connectionStatus, setConnectionStatus] = useState(false);
  const [userPublicKey, setUserPublicKey] = useState(null);
  const [walletConnected, setWalletConnected] = useState(false);
  const [paymentType] = useState("One Time Payment");

  const paymentName = queryParams.get("payment_name");
  const amount = parseFloat(queryParams.get("amount"));
  const paymentToken = queryParams.get("payment_token");

  window.Buffer = Buffer;
  const wallet = window.solana;

  async function initiateWalletConnection() {
    if (wallet?.isPhantom) {
      await wallet.connect();
      setConnectionStatus(true);
      setUserPublicKey(wallet.publicKey.toBase58());
      setWalletConnected(true);
    }
  }

  async function get_wallet_address() {
    const resp = await fetch(`https://ledger-pay-demo-spring-fff5fa203a7c.herokuapp.com/get-wallet-address/?payment_token=${paymentToken}`, {
      method: "GET",
    });
    if (resp.ok) {
      const data = await resp.json();
      return data["wallet_address"];
    }
  }

  async function pingLedgerPayWithNewTransaction(transaction_signature) {
    const payload = new FormData();
    const sellerWalletAddress = await get_wallet_address();
    payload.append("user_wallet_address", sellerWalletAddress);
    payload.append("amount", `${amount}`);
    payload.append("transaction_signature", transaction_signature);

    const resp = await fetch(`https://ledger-pay-demo-spring-fff5fa203a7c.herokuapp.com/new-transaction/`, {
      method: "POST",
      body: payload,
    });

    if (resp.ok) {
      const transactionLedgerPayId = await resp.json();
      alert(`Your transaction with ID: ${transactionLedgerPayId['new_transaction_id']} has been submitted.`);
    }
  }

  async function makeAndSendTransaction() {
    if (!walletConnected) {
      alert("Please connect your wallet first.");
      return;
    }

    const sellerWalletAddress = await get_wallet_address();
    const blockchainConnection = new Connection(clusterApiUrl("devnet"), "confirmed");

    try {
      const fromPubkey = new PublicKey(wallet.publicKey);
      const toPubkey = new PublicKey(sellerWalletAddress);
      const lamports = amount * 1_000_000_000;

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

      alert(`Transaction successful!\nSignature: ${txid}`);
      pingLedgerPayWithNewTransaction(txid);
    } catch (error) {
      console.error("Transaction failed:", error);
      alert("Transaction failed. See console for details.");
    }
  }

  return (
    <div className="app-container">
      <div className="card">
        <h2>Connect Phantom Wallet</h2>
        <p>Connect your wallet to continue with payment.</p>
        <p>Status: <strong>{connectionStatus ? "Connected" : "Disconnected"}</strong></p>
        {connectionStatus && (
          <p><strong>{userPublicKey}</strong></p>
        )}
        <button className="btn btn-green" onClick={initiateWalletConnection}>Connect Wallet</button>
      </div>

      <div className="card">
        <h2>General Payment</h2>
        <p><strong>For:</strong> {paymentName}</p>
        <p><strong>Amount:</strong> {amount} SOL</p>
        <p><strong>Type:</strong> {paymentType}</p>
        <button className="btn btn-purple" onClick={makeAndSendTransaction}>Make Payment</button>
      </div>
    </div>
  );
}

export default GeneralInvoice;
