## 📚 go-outside-eth-scripts

<br>

an on-going development of a library and set of scripts with my fav on-chain queries.

<br>


### installing

```
virtualenv venv
make install_deps
cp .env.example
vim .env
```
<br>

any output is saved to `data/`.

<br>


----

### scripts

<br>

#### get contracts deployed to mainnet and testnets

run `./get_contracts_deployed.py`



<br>


#### get reserve history by block for a pair of addresses

run `./get_reserve_history_by_block.py`



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

### lexicon

##### providers
 
- providers are how libraries such as `web3.py` talk to the blockchain. 
- providers take `JSON-RPC` requests and return responses
- the most common ways to connect to your node are:
   - IPC (uses local filesystem, fastest and most secure)
   - Websockets (works remotely, faster than HTTP)
   - HTTP (more nodes support it)