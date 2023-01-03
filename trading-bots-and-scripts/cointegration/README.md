## Cointegration bot

<br>

> *A **perpetual contract** is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.*


<br>

### strategy tl; dr

```
1. search for possible crypto perpetual derivative contracts that can be longed/shorted
2. calculate what pairs are cointegrated (by price history)
3. check the latest z-score signal, longing when zscore < 0
4. if the asset is "hot", confirm the tokens that are longing vs. shorting, and initial capital
5. in any case, average in limit orders or place market orders
6. also, continue monitoring the z-score for close signals in the future
```



<br>

---

### strategy code


We are using [bybit testnet](https://testnet.bybit.com/) for this example.

The code basically does the following:

```
1. get tradeable symbols
2. get price history and save to JSON
3. calculate and plot cointegration
4. backtest on a testnet
```

<br>

An example of a result:

![Figure_1](https://user-images.githubusercontent.com/1130416/200736166-a8672149-7e49-4522-8cfa-f72f891ca00f.png)





<br>


---
### setting up

Add info to an `.env` file:

```
cp .env.example .env
vim .env
```


Install with:

```
virtualenv venv
source venv/bin/activate
make install_deps
make install
```

<br>

----

### usage

<br>

<img width="732" alt="Screen Shot 2023-01-02 at 4 35 53 PM" src="https://user-images.githubusercontent.com/1130416/210287522-124f344d-5bf1-442a-849b-eb505b08d722.png">


<br>

#### getting data for a derivative 

``` 
cointbot -d usdt
```


<br>

example of output:

```

[   {   'alias': '10000NFTUSDT',
        'base_currency': '10000NFT',
        'funding_interval': 480,
        'leverage_filter': {   'leverage_step': '0.01',
                               'max_leverage': 12,
                               'min_leverage': 1},
        'lot_size_filter': {   'max_trading_qty': 370000,
                               'min_trading_qty': 10,
                               'post_only_max_trading_qty': '3700000',
                               'qty_step': 10},
        'maker_fee': '0.0001',
        'name': '10000NFTUSDT',
        'price_filter': {   'max_price': '9.999990',
                            'min_price': '0.000005',
                            'tick_size': '0.000005'},
        'price_scale': 6,
        'quote_currency': 'USDT',
        'status': 'Trading',
        'taker_fee': '0.0006'},

(...)
```

<br>

----

#### Save price history for a derivative

``` 
cointbot -p usdt
```


<br>

example of output:

```
```

<br>

---

#### Get cointegration for a pair of assets

``` 
cointbot -i ethusdt btcusdt
```


<br>

example of output:

```
```

<br>

---

#### Get latest z-core signal for a pair of assets.

<br>

> *In the context of trading, **z-score** is the number of **standard deviations** separating the **current price** from the **mean price**, so that traders can look at the **momentum of the average z-score** and takes a **contrarian approach** to trading to generate **buy and sell signals**.*

<br>

To see the latest z-score for an asset, run:

``` 
cointbot -z ethusdt btcusdt
```


<br>

example of output:

```
```

<br>

---

#### Run backtests

<br>

> *I*n the context of crypto trading, **backtesting** is accomplished by **reconstructing**, with **historical data**, trades that would have occurred in the past using rules defined by a given strategy, gauging the **effectiveness of the strategy**.*

<br>


To run backtests, run:

``` 
cointbot -t
```


<br>

example of output:

```
```

<br>

---

#### Deploy and start bot

``` 
cointbot -b
```


<br>

example of output:

```
```

<br>

---


### resources

<br>


* [pair trading](https://robotwealth.com/practical-pairs-trading/)
* [interpreting cointegration results](https://www.aptech.com/blog/how-to-interpret-cointegration-test-results/)

