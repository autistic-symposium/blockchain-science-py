## Cointegration bot

<br>

> A **perpetual contract** is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.


<br>

### tl; dr

```
1. search for possible crypto perpetual derivative contracts that can be longed/shorted
2. calculate what pairs are cointegrated (by price history)
3. check the latest z-score signal, longing when zscore < 0
4. if the asset is "hot", confirm the tokens that are longing vs. shorting, and initial capital
5. in any case, average in limit orders or place market orders
6. continue monitoring the z-score for close signals in the future
```



<br>

---

### code


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

```
virtualenv venv
source venv/bin/activate
make install_deps
make install
```

<br>

----

### usage

``` 
cointbot -s buybit usdt
```


<br>

---


### resources

<br>


* [pair trading](https://robotwealth.com/practical-pairs-trading/)
* [interpreting cointegration results](https://www.aptech.com/blog/how-to-interpret-cointegration-test-results/)

