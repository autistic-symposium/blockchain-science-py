## Transfer events analysis through `eth_getLogs`

<br>

In this notebook, we leverage [Infura API](https://app.infura.io/dashboard/ethereum/), particularly [`eth_getLogs`](https://docs.infura.io/infura/networks/ethereum/json-rpc-methods/eth_getlogs), to retrieve and parse transfer events logs for a given erc20 token, calculating balances and token holders.


To run this notebook locally, follow the steps below:

### Install dependencies:

```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Add API keys:

Please add your env info to the `.env` file:

```
cp .env_example .env
vim .env
```

### Start Jupyter server:

```
jupyter notebook
```

<br>

◼️

