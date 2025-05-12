from solana.rpc.api import Client, Signature
from solders.solders import TransactionConfirmationStatus
import base58

def check_transaction_status(transaction_signature):
    http_client = Client("https://api.devnet.solana.com")
    tx_sig = Signature(base58.b58decode(transaction_signature))
    res = http_client.get_signature_statuses([tx_sig], search_transaction_history=True)  # Use tx_sig, not tx_sig_str
    status_info  = res.value[0]
    status = status_info.confirmation_status
    status_as_str = ""
    match status:
        case TransactionConfirmationStatus.Processed:
            status_as_str = "processed"
        case TransactionConfirmationStatus.Confirmed:
            status_as_str = "confirmed"
        case TransactionConfirmationStatus.Finalized:
            status_as_str = "finalized"
        case _:
            status_as_str = "pending"

    return status_as_str