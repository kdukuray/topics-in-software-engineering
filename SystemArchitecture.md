## LedgerPay Architecture

### High-Level Component Diagram

![High-Level Component Diagram](./component_diagram.png)

This diagram illustrates the core components of the LedgerPay system and how they interact with 
each other during a transaction. A client store redirects the user to an invoice page, which serves as the payment
interface. The user connects their Solana wallet and signs the transaction, which is then sent to the Solana network via 
an RPC call. The invoice page also communicates with the LedgerPay backend through an API, providing transaction details. 
The backend, built using Django, processes this data and stores it using an ORM in the SQLlite database. This setup 
allows the client to track payments and manage transactions securely from the dashboard.

---
