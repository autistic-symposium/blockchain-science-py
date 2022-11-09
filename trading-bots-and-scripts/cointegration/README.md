## Cointegration strategy

<br>

### tl; dr

* search for all possible cryptos that we can long or short using some CEX api (e.g. [bybit testnet](https://testnet.bybit.com/), bitwithin their perpetual derivatives contracts. 
* then find what pairs are cointegrated.

<br>

> A perpetual contract is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.

<br>

---
### Strategy steps

1. Get tradeable symbols
2. Get price history and save to `JSON`
3. Calculate and plot cointegration
4. Backtest on some testnet


<br>


---
### Installing

```
virtualenv venv
source venv/bin/activate
make install_deps
make install
```

<br>



#### CLI usage

``` 
cointbot
```

<br>

#### Deploying the bot


<br>