## Cointegration strategy

<br>

### tl; dr

* search for all possible cryptos that we can long or short using some CEX api (e.g. [bybit testnet](https://testnet.bybit.com/), with their perpetual derivatives contracts. 
* then find what pairs are cointegrated.
* check latest zscore signal (long when zscore is negative).
* if "hot": confirm long vs. short tokens and confirm initial capital.
* in any case, average in limit postonly orders or place market orders.
* monitor zscore for close signal.


> A perpetual contract is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.

<br>

![Figure_1](https://user-images.githubusercontent.com/1130416/200736166-a8672149-7e49-4522-8cfa-f72f891ca00f.png)



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
