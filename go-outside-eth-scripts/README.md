## 📚 goe: go-outside-eth-scripts

An on-going development of a library and set of scripts with my fav on-chain queries.

<br>


### installing

0. create and source a virtual environment 
1. install `requirements.txt`
2. create and fill `.env`
3. any output is saved to `data/`

<br>


----

### scripts

<br>

####  get contracts deployed to mainnet and testnets

run `./get_contracts_deployed.py`



<br>

---

### troubleshoot

#### ethereum-etl not compatible to m1

If you run on this error, runL

```
pip uninstall ethereum-etl 
pip install --no-binary ethereum-etl 
```

<br>

---

### resources

* [ethereum etl library](https://ethereum-etl.readthedocs.io/en/latest/quickstart/)
