## Moraris Token and Transactions

<br>

In this notebook, we leverage Moralis API to extract lots of juicy data from tokens, transactions, balances, etc.

<br>

----

### Features

#### tokens

1. Get all ERC20 tokens owned by an address
2. Get the price of an ERC20 token
3. Get the all ERC20 transfers by wallet
4. Get all ERC20 transactions by contract
5. Get ERC20 metadata by contract

#### balances

6. Get the native balance of an address
7. Get the native balance of a multi-signature wallet

#### transactions

8. Get all transactions of an address
9. Get transaction by tx hash
10. Get the verbose transaction of an address

#### events

11. Get the logs for a contract

#### blocks

12. Get block content by block number

#### resolve

13. Reverse Resolve ENS name

<br>

---

### Installing

To run this notebook locally, first install dependencies:


```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Then add your Moralis API info to an `.env` file:

```
cp .env_example .env
vim .env
```

<br>

----

### Start Jupyter server:

```
jupyter notebook
```

◼️
