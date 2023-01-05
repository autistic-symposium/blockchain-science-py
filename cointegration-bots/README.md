## 🤖✨ Cointegration Trading Bots

<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/1130416/210710893-9fe299e3-96cf-4f99-9bf1-1bf3bea1c944.png" width="30%" align="center" style="padding:1px;border:1px solid black;"/>
 </p>

<br>

### TL; DR statistical arbitrage

<br>

* When 2 or more **non-stationary series** can be **combined** to make a **stationary series**, they are said to be cointegrated. The coefficients that define this stationary combination are called **hedge ratio**, describing the **amount of B to buy or sell for every of A**.

<br>

| 😎 **PROS** 😎                           | 😭 **CONS** 😭                                             |
| -----------                              | -----------                                            |
| profit in up, down, or sideways markets  | behaviors are not guaranteed to continue               |
| use rebates on two assets                | high entry barrier 🧠                                   |
| clear signals for entry and exit         | involves shorting                                      |
| mathematical edge                        | market-based orders, costs double                      |
| scale for larger capital                 | entry and exit in parallel with limit-orders is tricky |

<br>


* 📚 For more details, check **[my Mirror post, bot #2: cointbot, a cointegration trader]()**.

<br>



### TL; DR this package

<br>

* This package consists of a libraries for different market types, statistical algorithmic decisions, and bots (end-to-end) deployment. Here is its directory's structure:

```
📂 cointegration-bots
    ┣ 📂 src
        ┣ main.py
        ┣ 📂 markets
            ┣ bybit.py
            ┣ (...)
        ┣ 📂 bots
            ┣ bot1.py
            ┣ (...)
        ┣ 📂 strategies
            ┣ cointegration.py
            ┣ (...)
        ┣ 📂 utils
            ┣ os.py
            ┣ (...)
    ┣ 📂 results
    ┣ 📂 docker
```

* For example, `bot1` has the following strategy:
```
        1. search for possible crypto perpetual derivative contracts that can be longed/shorted
        2. calculate pairs that are cointegrated (by price history)
        3. check the spread and latest z-score signal, backtest, and then long when z-score < 0
        4. if asset is "hot", confirm tokens that are longing vs. shorting with the initial capital
        5. average in limit orders or place market orders
        6. continue monitoring the z-score for close signals in the future
```


<br>

#### 🚨 Disclaimer: my projects are boilerplates to get you started; you might or might not profit from it: in the mev world, nobody is going to handle you the alpha. i am not responsible for anything you do with my free code.




<br>


---
### Setting up cointbot

<br>

Add system and trading config to a `.env` file:

<br>

```
cp .env.example .env
vim .env
```

<br>

Install with:

```
virtualenv venv
source venv/bin/activate
make install_deps
make install
```

<br>

Run with:

```
cointbot
```

<br>

Usage:


<br>

<img width="1182" alt="Screen Shot 2023-01-04 at 2 54 38 PM" src="https://user-images.githubusercontent.com/1130416/210665313-b9b51fb5-e3f1-4030-ac20-ae8814477384.png">



<br>

----

### Running on bybit cex

<br>

> 💡 *You can test these strategies on [bybit's testnet](https://testnet.bybit.com/).*

<br>


#### Getting data for a derivative currency

<br>

> 💡 ***Crypto derivatives** are financial contracts that derive their values from underlying assets. A **perpetual contract** is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.*



<br>


Run API calls to bybit to query the market data for all assets, in a given `TIMEFRAME` and `KLINE-LIMIT`. Example:

``` 
cointbot -c usdt
```


<br>

Example of output:

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

#### Saving price history for a derivative currency

<br>

> 💡 *In the context of trading, a **k-line** represents the **fluctuation** of an asset prices in a give time frame. It shows **close price**, **open price**, **high price**, and **low price**. If the **close price > open price**, the k-line has a **positive line**. Otherwise, it is a **negative line**.*

<br>

Run API calls to bybit to query the market price k-line for all assets, in a given `TIMEFRAME` and `KLINE-LIMIT`. Save them to `OUTPUTDIR/PRICE_HISTORY_FILE`. Example:
``` 
cointbot -p usdt
```


<br>

Example of output:

```
(...)
ℹ️ Retrieving k-lines for ZRXUSDT: [{'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1655596800, 'open': 0.2478, 'high': 0.2691, 'low': 0.2314, 'close': 0.2644}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1655683200, 'open': 0.2644, 'high': 0.2857, 'low': 0.2507, 'close': 0.2755}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1655769600, 'open': 0.2755, 'high': 0.2987, 'low': 0.273, 'close': 0.2798}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1655856000, 'open': 0.2798, 'high': 0.3043, 'low': 0.2664, 'close': 0.2703}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1655942400, 'open': 0.2703, 'high': 0.2942, 'low': 0.2691, 'close': 0.2902}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656028800, 'open': 0.2902, 'high': 0.3067, 'low': 0.2878, 'close': 0.302}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656115200, 'open': 0.302, 'high': 0.3132, 'low': 0.2895, 'close': 0.311}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656201600, 'open': 0.311, 'high': 0.3463, 'low': 0.3039, 'close': 0.3154}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656288000, 'open': 0.3154, 'high': 0.3523, 'low': 0.3093, 'close': 0.3235}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656374400, 'open': 0.3235, 'high': 0.3427, 'low': 0.3147, 'close': 0.3175}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656460800, 'open': 0.3175, 'high': 0.3678, 'low': 0.3119, 'close': 0.3509}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656547200, 'open': 0.3509, 'high': 0.352, 'low': 0.3133, 'close': 0.3288}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656633600, 'open': 0.3288, 'high': 0.3351, 'low': 0.2977, 'close': 0.3054}, {'symbol': 'ZRXUSDT', 'period': 'D', 'start_at': 1656720000, 'open': 0.3054, 'high': 0.309, 'low': 0.2942, 'close': 0.3003}, 
(...)
ℹ️ 200 k-lines retrieved for ZRXUSDT.
ℹ️ Price history saved to results/USDT_price_history.json
```

<br>

> 💡 *Bybit employs a **[dual-price mechanism](https://www.bybit.com/en-US/help-center/bybitHC_Article?id=360039261074&language=en_US) to prevent market manipulations** (when the market price on a futures exchange deviates from the spot price, causing mass liquidation of traders' positions). The dual-price mechanism consists of **mark price** and **last traded price**. "Mark price" refers to a **global spot price index plus a decaying funding basis rate**, and it's used as a trigger for liquidation and to measure **unrealized profit and loss**. "Last traded price" is the **current market price**, anchored to the **spot price** using the funding mechanism.*



<br>


---

#### Getting cointegration for a derivative currency's history data 

<br>

> 💡 *In statistics, **p-value** is the probability of obtaining results at least as extreme as the results of a **hypothesis test**, assuming that the **null hypothesis is correct**. A p-value of **0.05 or lower** is generally considered statistically **significant**.*

<br>

With the price history data (which was generated in the previous step inside `OUTPUTDIR/PRICE_HISTORY_FILE`), we can generate a cointegration `DataFrame`.

For the desired `PLIMIT` (p-value limit that defines a "hot" pair), this is an example:

``` 
cointbot -i usdt
```


<br>

Example of output:

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
ℹ️ Cointegration saved to results/USDT_cointegration_results.csv
ℹ️ Zscore saved to results/USDT_zscore_results.csv

      hot  pvalue  cointegration_value  critical_value  hedge_ratio  zero_crossings      coin1           coin2
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

This `DataFrame` is saved at `OUTPUTDIR/COINTEGRATION_FILE`, sorted by `zero_crossing`.

<br>

> 💡 *In statistics, **zero crossing** is a point where the sign of function changes. In the context of trading, it determines an **entry point** (using the price in relation to the moving average as a **direction confirmation**).*


<br>



---

#### Getting the z-score signal for a cointegrated pair in a derivative currency's history data

<br>

> 💡 *In the context of trading, **z-score** is the number of **standard deviations** separating the **current price** from the **mean price**, so that traders can look at the **momentum of the average z-score** and takes a **contrarian approach** to trade to generate **buy and sell signals**. Graphically, **positive z-scores lie to the right** of the mean, and **negative Z-scores lie to the left** of the mean.*

<br>

Example:

``` 
cointbot -z  usdt
```


<br>

Example of output:

```
ℹ️ Zscore loaded from results/USDT_zscore_results.csv
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



#### Generate backtest metrics for a cointegrated pair in a derivative currency's history data

<br>

> 💡 *In the context of crypto trading, **backtesting** is accomplished by **reconstructing**, with **historical data**, trades that would have occurred in the past using rules defined by a given strategy, gauging the **effectiveness of the strategy**.*

<br>

Select your favorite asset pair to generate the data and the plot on their cointegration:

Example:

``` 
cointbot -t uniusdt c98usdt usdt  
```


<br>

Example of output for `ETHUSDT` vs. `BTCUSDT`:

```
ℹ️ Cointegration loaded from results/USDT_cointegration_results.csv
ℹ️ Price history loaded from results/USDT_price_history.json
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

Their plot will be saved at `OUTPUTDIR/{coin1}_{coin2}_cointegration.png`. Their backtest file will be saved at `OUTPUTDIR/{coin1}_{coin2}_BACKTEST_FILE`.

<br>

![BCHUSDT_LINKUSDT_W_cointegration](https://user-images.githubusercontent.com/1130416/210667745-98395c53-f4ce-4330-8bbf-93abc0b778c1.png)







<br>

<br>

> 💡 *If you are **starting a new run**, **clean up** the current setup with* `make clean_data`.

<br>

---

#### Getting top cointegrated pairs for a derivative currency's history data 

<br>

Once the cointegration pairs for a given derivative currency's history data is calculated, we can look at the top best cointegrated pairs for the given `TIMEFRAME`.

<br>

Example:

``` 
cointbot -o usdt 10
```

<br>

Example of output:

```
ℹ️ Metrics loaded from results/USDT_cointegration.csv

'Top 10 cointegrated pairs for USDT:'


     pvalue  cointegration_value  critical_value  hedge_ratio  zero_crossings      coin1        coin2
388   0.046            -3.368619       -3.367006     0.061731              15  MATICUSDT      AXSUSDT
499   0.046            -3.372177       -3.367006   104.198594              11    AXSUSDT      RENUSDT
340   0.046            -3.371256       -3.367006    74.784234              17   LINKUSDT     COTIUSDT
402   0.046            -3.371678       -3.367006    29.610067              15   AAVEUSDT      SNXUSDT
626   0.046            -3.372086       -3.367006    30.392953               7    TRBUSDT    1INCHUSDT
409   0.046            -3.371230       -3.367006     1.042626              15    BELUSDT    1INCHUSDT
454   0.046            -3.368308       -3.367006    16.127011              13    UNIUSDT      C98USDT
616   0.046            -3.370103       -3.367006   576.820067               7    BITUSDT  1000BTTUSDT
465   0.046            -3.370326       -3.367006   162.653323              13   AAVEUSDT      ENJUSDT
521   0.046            -3.369336       -3.367006     3.250135              11    UNIUSDT    ALICEUSDT
```

<br>

Note that this command automatically generates the backtesting data and plots (similar to the previous option).

<br>

---

#### Testing connection to orderbooks through websockets



<br>


To open a websocket subscribed to a cointegration pair (either for spot, linear, or inverse markets), run:

``` 
cointbot -n <coin1> <coin2> <spot, linear, or inverse>
```


<br>

###### [Topics for spot market](https://bybit-exchange.github.io/docs/spot/v1/#t-websocket)

Spot market topics are implemented with `trade_v1_stream()`, which pushes raw data for each trade.

After a successful subscription message, the first data message (`f: true`), consists of the last 60 trades. After (`f: false`), only new trades are pushed (at a frequency of 300ms, where the message received has a maximum delay of 400ms).

Example of output for `ETHUSDT` and `BTCUSDT` for spot market:

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


###### [Topics for inverse perpetual/futures market](https://bybit-exchange.github.io/docs/futuresV2/inverse/#t-websocketresponse)

Inverse market topics are implemented with `orderbook_25_stream()`, which fetches the orderbook with a depth of 25 orders per side.

After the subscription response, the first response will be the snapshot response, showing the entire orderbook. The data is ordered by price (starting with the lowest buys). Push frequency is 20 ms.

Example of output for `ETHUSD` and `BTCUSD for inverse market:

<br>

```
WebSocket Inverse Perp attempting connection...
websocket connected
WebSocket Inverse Perp connected
[   {   'id': 12638500,
        'price': '1263.85',
        'side': 'Buy',
        'size': 4310,
        'symbol': 'ETHUSD'},
    {   'id': 12637500,
        'price': '1263.75',
        'side': 'Buy',
        'size': 1310,
        'symbol': 'ETHUSD'}]

[   {   'id': 166250000,
        'price': '16625.00',
        'side': 'Buy',
        'size': 600,
        'symbol': 'BTCUSD'},
    {   'id': 166410000,
        'price': '16641.00',
        'side': 'Buy',
        'size': 18,
        'symbol': 'BTCUSD'},
(...)
```

<br>


###### [Topics for USDT linear perpetual](https://bybit-exchange.github.io/docs/futuresV2/linear/#t-websocketresponse)



`USDT` Linear market topics are implemented with `orderbook_25_stream()`, which fetches the orderbook with a depth of 25 orders per side.

The first response is the snapshot response, showing the entire orderbook. The data is ordered by price, starting with the lowest buys and ending with the highest sells. Push frequency is 20ms.


Example of output for `ETHUSDT` and `BTCUSDT` for linear market:

<br>

```
WebSocket USDT Perp attempting connection...
websocket connected
WebSocket USDT Perp connected

[   {   'is_block_trade': 'false',
        'price': '1249.90',
        'side': 'Sell',
        'size': 0.03,
        'symbol': 'ETHUSDT',
        'tick_direction': 'MinusTick',
        'timestamp': '2023-01-04T04:11:30.000Z',
        'trade_id': '4c104034-c298-59b9-82de-5cb82d104f86',
        'trade_time_ms': '1672805490378'}]

[   {   'is_block_trade': 'false',
        'price': '1249.95',
        'side': 'Buy',
        'size': 0.03,
        'symbol': 'ETHUSDT',
        'tick_direction': 'PlusTick',
        'timestamp': '2023-01-04T04:11:32.000Z',
        'trade_id': 'af3c770a-bc0d-540a-bc3f-4de17ce80194',
        'trade_time_ms': '1672805492380'}]

(...)
```

<br>




---

#### Deploying trading bots using several cointegrated strategies and setups

<br>

Several bots with different strategies are found inside  `src/bots/`.

Each bot has a different number and configuration settings in the `.env` file (*e.g.*, `BOT_COINS`, `BOT_MARKET_TYPE`, `BOT_ORDER_TYPE`, `BOT_STOP_LOSS`, `BOT_TRADEABLE_CAPITAL`, and others).


<br>


##### 🤖 `BbBotOne`


<br>

`Bot1`'s setup:

```
1. check constants inside .env
2. connect to REST API and Websockets
3. set leverage
4. start a loop with "while True"
```

<br>

`Bot1`'s execution (inside a `while True` loop)

```
5. check positions
6. check active orders
7. manage new trades
  a. check latest z-score signal:
    - if hot:
        i. get ticker liquidity
        ii. confirm short vs. long tickers
        iii. confirm initial capital
    - in any case:
        i. average in Limit PostOnly orders
        ii. or place Market orders
        iii. monitor z-score for close signal
8. close existing trades
9. repeat
```


<br>


Run with:

``` 
cointbot -b 1
```

<br>

To have this bot running inside a docker container, run:

```
make bot1
```


<br>

##### 🤖 `BbBotTwo`


<br>

`Bot2`'s setup:

```
1. check constants inside .env
2. connect to REST API and Websockets
3. set leverage
4. start a loop with "while True"
```

<br>

`Bot2`'s execution (inside a `while True` loop)

```
5. get z-score
6. check open positions and net P&L
7. close all positions if z-score is not relevant or if poor P&L performance
8. check how much capital is invested
9. open new positions
10. repeat each time period
```

<br>


Run with:

``` 
cointbot -b 2
```

<br>

To have this bot running inside a docker container, run:

```
make bot2
```



<br>

---


### Resources

<br>


* [Notes on pair trading](https://robotwealth.com/practical-pairs-trading/)
* [Pybit documentation](https://openbase.com/python/pybit/documentation)
* [Bybit documentation](https://pub.dev/documentation/bybit/latest/bybit/bybit-library.html)
* [Bybit postman setup](https://github.com/bybit-exchange/QuickStartWithPostman)
* [Interpreting cointegration](https://www.aptech.com/blog/how-to-interpret-cointegration-test-results/)
