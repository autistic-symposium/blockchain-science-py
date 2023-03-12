## transfer events analysis through `eth_getLogs`

<br>

in this notebook, we leverage [Infura API](https://app.infura.io/dashboard/ethereum/), particularly [`eth_getLogs`](https://docs.infura.io/infura/networks/ethereum/json-rpc-methods/eth_getlogs), to retrieve and parse transfer events logs for a given erc20 token, calculating balances and token holders.


<br>

#### install dependencies

```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

<br>

#### add API keys

please add your env info to the `.env` file:

```
cp .env_example .env
vim .env
```

<br>

#### start jupyter server

```
jupyter notebook
```

<br>

◼️

<br>

----

### resources

* [keccak encode/decode online](https://emn178.github.io/online-tools/keccak_256.html)


<br>


