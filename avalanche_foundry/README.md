## [WIP] 🧱👵🏽 inspecting old blocks in avalanche

<br>

### tl; dr

<br>

##### 🛠 in this project, we use [foundry](https://github.com/foundry-rs/foundry) to analyze blocks history in the avalanche blockchain. this can be used for several purposes, including testing vulnerabilities or extracting mev data.

##### 📚 for more details, check my mirror post ["foundry, avalanche, and historical shenanigans"](https://mirror.xyz/steinkirch.eth/Nzlw7ub7HFVa-LnP4kEKeiDtPcmzUkYlI2BJG_StVX8).

##### 🚨 disclaimer: i am not responsible for anything you do with my free code.


<br>

----

### installing

<br>

1. install [foundry](https://book.getfoundry.sh/getting-started/installation)
2. install a [solidity compiler](https://docs.soliditylang.org/en/latest/installing-solidity.html#installing-the-solidity-compiler)
3. create an env variable for the RPC url for avalanche (*e.g.*, [infura's](https://avalanche-mainnet.infura.io/v3/) or [ankr's](https://www.ankr.com/rpc/avalanche/) or your own node):

```
export URL=<URL>
```


<br>

---

### simulating sandwich attacks

<br>

#### gathering data

<br>

1. define the desired assets and/or protocols you want to research research, and find out the methods that update their prices.
3. use any blockchain analytic tool (*e.g.,* [dune](https://dune.com/home) or [avax apis](https://docs.avax.network/apis/avalanchego/public-api-server)) to search for past blocks with a considerable price movement. 
4. create a list of the block numbers you want to analyze and add them to `data/blocks.txt`. there is one example there already to get you started (on avalanche c-chain).

<br>

#### running

<br>

build the contracts and check test pass:

```
make run
```


