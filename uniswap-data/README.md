## Leveraging Uniswap subgraph to extract token pair information

<br>

In this notebook, we are using the following subgraph:
```
ENDPOINT = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
```

<br>


### Steps

0. Define private methods for querying
1. Query to find all token IDs for $UNI
2. Query to find all token IDs for $WETH
3. Query to find IDs of all combinations of a pair of tokens
4. Query to find recent swaps between the pairs (by their pair IDs)
5. Data cleaning and plotting


<br>

### Installing dependencies

```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```



◼️
