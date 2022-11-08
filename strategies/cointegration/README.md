## Cointegration strategy

<br>

#### tl; dr

* search for all possible cryptos that we can long or short using some CEX api within their perpetual derivatives contracts. 
* then find what pairs are cointegrated.

<br>

> A perpetual contract is a contract that can be held in perpetuity, *i.e.,* indefinitely until the trader closes their position.

<br>

#### Steps

1. Get tradeable symbols
2. Get price history
3. Calculate cointegration
4. Backtest on testnet