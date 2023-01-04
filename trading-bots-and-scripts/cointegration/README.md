## Cointegration bot

<br>

> *A **perpetual contract** is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.*


<br>

### tl; dr

* we are using [bybit testnet](https://testnet.bybit.com/) for backtesting.
* this bot does the following:

```
        1. search for possible crypto perpetual derivative contracts that can be longed/shorted
        2. calculate what pairs are cointegrated (by price history)
        3. check the latest z-score signal, backtest, and long when z-score < 0
        4. if the asset is "hot", confirm the tokens that are longing vs. shorting, and initial capital
        5. average in limit orders or place market orders
        6. continue monitoring the z-score for close signals in the future
```



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


<img width="1117" alt="Screen Shot 2023-01-03 at 5 59 35 PM" src="https://user-images.githubusercontent.com/1130416/210470901-024191a3-7a93-4e3e-9c1d-af60fa6bf25d.png">



<br>

<br>

#### getting derivatives data for a derivative currency

<br>

> ***Crypto derivatives** are financial contracts that derive their values from underlying assets.*

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

#### saving price history for a derivative currency

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

#### getting cointegration history data for a derivative currency

With the price history data (e.g., directly generated in the previous option, inside `OUTPUTDIR/PRICE_HISTORY_FILE`), we can generate a cointegration data frame (in Pandas).

For that, set the desired `PLIMIT` (p-value limit that defines a "hot" pair) and run:

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
ℹ️ Cointegration saved to results/cointegration_results.csv
ℹ️ Zscore saved to results/zscore_results.csv

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

This table is saved in `OUTPUTDIR/COINTEGRATION_FILE`.

<br>

---

#### getting z-score signal for a cointegrated pair and a derivative currency

<br>

> *In the context of trading, **z-score** is the number of **standard deviations** separating the **current price** from the **mean price**, so that traders can look at the **momentum of the average z-score** and takes a **contrarian approach** to trade to generate **buy and sell signals**.*

<br>

Run:

``` 
cointbot -z 
```


<br>

example of output:

```
ℹ️ Zscore loaded from results/zscore_results.csv
             0         1         2         3         4         5         6         7         8         9        10  ...       189       190       191       192       193       194       195       196       197       198       199
0    -0.841478 -0.954716 -0.503403 -0.840932 -0.540967 -0.880135 -0.766897 -1.067955 -1.105519 -1.293338 -1.029298  ... -1.549728 -1.098961 -0.949252 -0.874124 -0.873577 -1.212199 -1.512711 -0.759246 -0.947066 -0.608991 -0.834374
1     1.280295  1.330660  1.202023  0.794668  0.934925  0.897796  0.767361  0.843417  0.862282  0.876535  0.745500  ... -0.266424 -0.275466 -0.448659 -0.566457 -0.708930 -0.785585 -0.966386 -1.170064 -1.224442 -1.188329 -1.361104
2    -1.805839 -1.742938 -1.734276 -1.768212 -1.695584 -1.780209 -1.734276 -1.788871 -2.403184 -1.789936 -1.721214  ... -0.227997 -0.148128 -0.122853 -0.215785  0.070606  0.085798 -0.071099  0.051862 -0.018990 -0.087357 -0.010684
3    -0.496911 -0.334074 -0.496991 -0.469418 -0.773009 -0.874205 -0.666722 -0.711288 -0.724995 -0.716378 -0.935766  ... -0.914445 -1.027705 -1.000372 -1.543870 -0.868315 -1.219759 -1.437423 -1.130466 -1.368730 -1.523110 -1.528200
4     0.135408  0.234355  0.220202  0.069457 -0.271648 -0.247513 -0.438351 -0.501376 -0.640976 -0.573220 -0.700431  ... -0.036896 -0.061675  0.011331 -0.084689  0.377734  0.550330  0.306491  0.468504  0.505630  0.391327  0.442004
...        ...       ...       ...       ...       ...       ...       ...       ...       ...       ...       ...  ...       ...       ...       ...       ...       ...       ...       ...       ...       ...       ...       ...
9169  1.338721  1.301523  1.268954  1.321006  1.200505  1.142184  1.186648  1.232206  1.149547  1.053899  0.998536  ... -0.074680 -0.327255 -0.176919 -0.333299 -0.050245 -0.178237 -0.740839 -0.573013 -0.542310 -0.607350 -0.665350
9170  0.956325  0.956325  1.046668  1.028473  1.196818  1.179256  1.227355  1.239063  1.070717  1.016132  0.895885  ... -0.391706 -0.469709 -0.583469 -0.679034 -0.505467 -0.751182 -0.841525 -0.799913 -0.770010 -0.799913 -0.931869
9171  1.472142  1.522843  1.551008  1.731278  1.812022  1.840187  2.029844  2.073035  2.110593  1.806392  1.763204  ... -1.303227 -1.643109 -1.419651 -1.359563 -1.333272 -1.314495 -1.579263 -1.656251 -1.522927 -1.537950 -1.691929
9172  1.776555  1.822700  1.850263  1.831867  1.862486  1.890049  1.896161  1.819334  1.770257  1.659694  1.607499  ... -0.664547 -0.556854 -0.439994 -0.378570 -0.233898 -0.396966 -0.470675 -0.384433 -0.313656 -0.301371 -0.267511
9173  0.473118  0.523284  0.545284  0.504641  0.490024  0.562190  0.621210  0.557897  0.549711  0.491627  0.501417  ... -2.490448 -2.285091 -2.344645 -2.372676 -2.299173 -2.057600 -2.403397 -2.703723 -2.548532 -2.589710 -2.598697

[9174 rows x 200 columns]
```

<br>

---

#### generate backtest metrics for a cointegrated pair and a derivative currency

<br>

> *In the context of crypto trading, **backtesting** is accomplished by **reconstructing**, with **historical data**, trades that would have occurred in the past using rules defined by a given strategy, gauging the **effectiveness of the strategy**.*

<br>


Run:

``` 
cointbot -t <coin1> <coin2>
```


<br>

example of output for ETHUSDT vs. BTCUSDT:

```
ℹ️ Cointegration loaded from results/cointegration_results.csv
ℹ️ Price history loaded from results/price_history.json
ℹ️ Metrics loaded from results/ETHUSDT_BTCUSDT_backtest.csv
     ETHUSDT   BTCUSDT  ETHUSDT_perc  BTCUSDT_perc    spread    zscore
0    1218.23  16832.82      1.000000      1.000000  2.214971       NaN
1    1216.79  16824.00      0.998818      0.999476  1.412135       NaN
2    1217.95  16834.47      0.999770      1.000098  1.815774       NaN
3    1217.98  16832.03      0.999795      0.999953  2.022042       NaN
4    1220.95  16857.36      1.002233      1.001458  3.162184       NaN
..       ...       ...           ...           ...       ...       ...
195  1215.65  16697.00      0.997882      0.991931  9.446706  0.533320
196  1214.21  16678.00      0.996700      0.990802  9.379280  0.443960
197  1214.18  16673.12      0.996676      0.990513  9.701814  0.499004
198  1215.70  16692.62      0.997923      0.991671  9.813120  0.685415
199  1213.82  16688.65      0.996380      0.991435  8.219916 -1.210695

[200 rows x 6 columns]
ℹ️ Saving plot to results/ETHUSDT_BTCUSDT_cointegration.png
```

<br>

The pair plot is saved at `OUTPUTDIR/{coin1}_{coin2}_cointegration.png` and backtest file is saved at `OUTPUTDIR/{coin1}_{coin2}_BACKTEST_FILE`.

<br>


<img width="1391" alt="Screen Shot 2023-01-02 at 11 44 09 PM" src="https://user-images.githubusercontent.com/1130416/210318333-4542e096-74fd-4381-8aae-886893a875c6.png">


<br>

<br>

> 💡If you are starting a new run (i.e., an entirely new timeframe and setup), clean up the result directory with `make clean`.

<br>

---

#### testing orderbook connection through websockets for a cointegrated pair


<br>


To open a websocket subscribed to the cointegration pairs (either for spot, linear, or inverse markets), run:

``` 
cointbot -n <coin1> <coin2> <spot, linear, or inverse>
```


<br>

example of output for ETHUSD and BTCUSD (spot):

<br>

```
WebSocket Spot attempting connection...
websocket connected
WebSocket Spot connected
    [{
    "e": 301,
    "s": "BTCUSDT",
    "t": 1565600357643,
    "v": "112801745_18",
    "o": 0,
    "b": [
      ["11371.49", "0.0014"],
      ["11371.12", "0.2"],
      ["11369.97", "0.3523"],
      ["11369.96", "0.5"],
      ["11369.95", "0.0934"],
      ["11369.94", "1.6809"],
      ["11369.6", "0.0047"],
      ["11369.17", "0.3"],
      ["11369.16", "0.2"],
      ["11369.04", "1.3203"]],
    "a": [
      ["11375.41", "0.0053"],
      ["11375.42", "0.0043"],
      ["11375.48", "0.0052"],
      ["11375.58", "0.0541"],
      ["11375.7", "0.0386"],
      ["11375.71", "2"],
      ["11377", "2.0691"],
      ["11377.01", "0.0167"],
      ["11377.12", "1.5"],
      ["11377.61", "0.3"]],
(...)
```

<br>

> 💡 In these results, `a` is the ask prices and quantities, and `b` is the bid prices and quantities (both in descending order).

<br>

---

#### deploying a trading bot using the cointegrated strategy

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
* [pybit documentation](https://openbase.com/python/pybit/documentation)
* [bybit documentation](https://pub.dev/documentation/bybit/latest/bybit/bybit-library.html)
* [interpreting cointegration results](https://www.aptech.com/blog/how-to-interpret-cointegration-test-results/)
