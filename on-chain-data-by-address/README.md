## Extracting on-chain data from a list of Ethereum public addresses

In this notebook, we leverage Etherscan API to extract the following information from a list of public addresses (retrieved from the file defined on `ADRESS_LIST`):

* Current ETH balance
* Token transfers and swaps
* Current tokens balance


### Install dependencies:

```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Add API keys:

Please add your Etherscan API info and the public address list to the `.env` file:

```
mv .env_example .env
vim .env
```

### Run:

```
jupyter notebook
```

### Output:

The three dataframes for this exercise are saved into `.csv` files inside the directory `./output`.


◼️
