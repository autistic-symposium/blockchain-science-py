## 📚 eth-python-scripts

<br>

an on-going development of a library and set of python scripts with my fav on-chain ops.

<br>


### installing

```
brew install poetry
make install
cp .env.example .env
```


<br>


----

### scripts


#### get contracts deployed to mainnet and testnets

1. add info to `.env`
2. run 
   `poetry run python  get_contracts_deployed.py`
3. any output is saved to `data/`.



<br>


#### get reserve history by block for a pair of addresses

1. add the pair abi to `abi`
2. add info to `.env`
3. run 
   `poetry run python get_reserve_history_by_block.py`



<br>

#### get deep block data

1. add info to `.env`
3. run 
   `poetry run python get_deep_block_data.py`



<br>

---

### troubleshoot

##### if you see `ethereum-etl not compatible to m1` run:

```
pip uninstall ethereum-etl 
pip install --no-binary ethereum-etl 
```

<br>

---

### resources

* [web3.py library](https://web3py.readthedocs.io/en/v5/)
* [ethereum etl library](https://ethereum-etl.readthedocs.io/en/latest/quickstart/)

<br>

---

### relevant info

##### providers
 
- providers are how libraries such as `web3.py` talk to the blockchain. 
- providers take `JSON-RPC` requests and return responses
- the most common ways to connect to your node are:
   - IPC (uses local filesystem, fastest and most secure)
   - Websockets (works remotely, faster than HTTP)
   - HTTP (more nodes support it)

<br>

##### middleware

* a web3.py instance can be configured via middleware (sitting between the web3 methods and the provider).
* middlewares use an onion metaphor: each layer may affect both the request and response from the provider.
* each middleware layer gets invoked before the request reaches the provider, and then processes the result after the provider returns, in reverse order.
* we often use `geth_poa_middleware`, to run with geth's Proof-of-Authority (PoA) consensus. this adds support for more than 32 bytes in each block (the `extraData` field).