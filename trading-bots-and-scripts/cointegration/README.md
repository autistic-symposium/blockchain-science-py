## Cointegration bot

<br>

> *A **perpetual contract** is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.*


<br>

### strategy tl; dr

```
1. search for possible crypto perpetual derivative contracts that can be longed/shorted
2. calculate what pairs are cointegrated (by price history)
3. check the latest z-score signal, longing when z-score < 0
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
2. get price history and save it to JSON
3. calculate and plot cointegration
4. backtest on a testnet
```

<br>

An example of a result:

![Figure_1](https://user-images.githubusercontent.com/1130416/200736166-a8672149-7e49-4522-8cfa-f72f891ca00f.png)



<br>


---
### setting up

Add info to a `.env` file:

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


<img width="598" src="https://user-images.githubusercontent.com/1130416/210302882-9c74be58-a2f2-4fd6-8ff6-7112f2c63667.png">




<br>

<br>

#### getting derivatives data for a currency 

<br>

> **Crypto derivatives** are financial contracts that derive their values from underlying assets.

<br>


Run API calls to bybit to query the market price k-line for all assets, in a given `TIMEFRAME` and `KLINE-LIMIT`. 

``` 
cointbot -c usdt
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

#### saving price history for a derivative

Retrieve market price kline for all assets, in a given `TIMEFRAME` and `KLINE-LIMIT`, and save them to `OUTPUTDIR/PRICE_HISTORY_FILE`:
``` 
cointbot -p usdt
```


<br>

example of output:

```
ℹ️ Retriving k-lines for 10000NFTUSDT
ℹ️ Retriving k-lines for 1000BTTUSDT
ℹ️ Retriving k-lines for 1000LUNCUSDT
ℹ️ Retriving k-lines for 1000XECUSDT
ℹ️ Retriving k-lines for 1INCHUSDT
(...)
ℹ️ Retriving k-lines for ZILUSDT
ℹ️ Retriving k-lines for ZRXUSDT
ℹ️ Price history saved to results/price_history.json
```

<br>

---

#### getting cointegration data

With the price history data (e.g., directly generated in the previous option, inside `OUTPUTDIR/PRICE_HISTORY_FILE`), we can generate a cointegration data frame (in Pandas).

For that, set the desired `PLIMIT` (p-value limit) and run:

``` 
cointbot -i 
```


<br>

example of output:

```
ℹ️ Price history loaded from results/price_history.json
ℹ️ Calculating cointegration for 10000NFTUSDT...
ℹ️    ✅ Found a hot pair: 10000NFTUSDT and AAVEUSDT
ℹ️    ✅ Found a hot pair: 10000NFTUSDT and XRPUSDT
ℹ️    ✅ Found a hot pair: 10000NFTUSDT and ZRXUSDT
ℹ️ Calculating cointegration for 1000BTTUSDT...
ℹ️    ✅ Found a hot pair: 1000BTTUSDT and 1INCHUSDT
ℹ️    ✅ Found a hot pair: 1000BTTUSDT and ACHUSDT
ℹ️    ✅ Found a hot pair: 1000BTTUSDT and XNOUSDT
ℹ️ Calculating cointegration for 1000LUNCUSDT...
ℹ️    ✅ Found a hot pair: 1000LUNCUSDT and LUNA2USDT
ℹ️ Calculating cointegration for 1000XECUSDT...
ℹ️    ✅ Found a hot pair: 1000XECUSDT and BATUSDT
ℹ️    ✅ Found a hot pair: 1000XECUSDT and BICOUSDT
(...)
ℹ️ Price history loaded from results/cointration_results.csv
      hot  pvalue  cointegration_value  critical_value  hedge_ratio  zero_crossings    symbol1       symbol2
299  True   0.039            -3.427942       -3.367006   186.709153              47    DARUSDT   1000BTTUSDT
569  True   0.008            -3.952940       -3.367006   814.468122              46   QTUMUSDT      REEFUSDT
99   True   0.002            -4.403082       -3.367006     0.374482              46   ASTRUSDT      CTSIUSDT
61   True   0.007            -3.992374       -3.367006     0.002553              45    ADAUSDT       BCHUSDT
80   True   0.034            -3.480315       -3.367006    37.053379              43  ALICEUSDT       XEMUSDT
..    ...     ...                  ...             ...          ...             ...        ...           ...
320  True   0.039            -3.427692       -3.367006     1.118496               1   DUSKUSDT     ALPHAUSDT
322  True   0.039            -3.426715       -3.367006     0.073619               1   DUSKUSDT      API3USDT
258  True   0.004            -4.211679       -3.367006  9955.362104               1    BNXUSDT  SHIB1000USDT
265  True   0.030            -3.523876       -3.367006    50.182586               1    BNXUSDT     WAVESUSDT
172  True   0.003            -4.288047       -3.367006  4335.680819               1    BNBUSDT      COTIUSDT

[662 rows x 8 columns]
```

<br>

This table is saved in `OUTPUTDIR/COINTEGRATION_FILE `.

<br>

---

#### getting the latest z-core signal for a pair of assets.

<br>

> *In the context of trading, **z-score** is the number of **standard deviations** separating the **current price** from the **mean price**, so that traders can look at the **momentum of the average z-score** and takes a **contrarian approach** to trade to generate **buy and sell signals**.*

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

#### running backtests

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

#### deploying and starting bot

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
* [pybit documentation](https://openbase.com/python/pybit/documentation)
* [bybit documentation](https://pub.dev/documentation/bybit/latest/bybit/bybit-library.html)

