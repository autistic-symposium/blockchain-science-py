## 🧱👵🏽 inspecting old blocks on avalanche

<br>

### tl; dr

<br>

##### 🛠 in this project, we use [foundry](https://github.com/foundry-rs/foundry) to analyze blocks history in the avalanche blockchain. this can be used for several purposes, including testing vulnerabilities or extracting mev data.

##### 🚨 disclaimer: i am not responsible for anything you do with my free code.


<br>

----
### example I: simulating sandwich attacks on avalanche c-chain

<br>

#### gathering data

<br>

1. define the **desired assets and/or protocols** you want to research, in this example, we looking at **[gmx](https://github.com/gmx-io/gmx-contracts)** and writing the test `testHistoricalGmx()`.

2. find out the **methods that trigger prices updates** (e.g. `swap()` on gmx's **[router](https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/Router.sol#L88)**).

2. add/clone all the contracts need for the methods above to `lib/`. the main code we will be running is actually located inside `test/` (foundry is a solidity testing toolkit).

3. use any **blockchain analytics tools** (*e.g.,* **[dune](https://dune.com/home)** or **[avax apis](https://docs.avax.network/apis/avalanchego/public-api-server)**) to search for **past blocks** with a suspecting price movement (*e.g.,* set a threshold that could be interesting to look at). 

4. create a **list with all the block** you found and add them to `data/blocks.txt`. there is one example there already to get you started (on avalanche c-chain).

<br>


#### installing 

<br>

1. install **[foundry](https://book.getfoundry.sh/getting-started/installation)**.

2. install a **[solidity compiler](https://docs.soliditylang.org/en/latest/installing-solidity.html#installing-the-solidity-compiler)**. you need to look at which solidity version your protocol is using. for instance, for gmx we have to use **[0.6.12](https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/VaultPriceFeed.sol#L11)**).

3. create an env variable for avalanche c-chain's RPC url (*e.g.*, from **[infura's](https://avalanche-mainnet.infura.io/v3/)** or **[ankr's](https://www.ankr.com/rpc/avalanche/)** or **your own node**):

```
export URL=<URL>
```

<br>

#### running

<br>

to build the contracts and run the test, run:

```
> make run

[⠆] Compiling...
[⠆] Compiling 1 files with 0.6.12
[⠰] Solc 0.6.12 finished in 889.97ms
Compiler run successful

Running 1 test for test/Gmx.t.sol:getHistorical
[PASS] Gmx() (gas: 91522784)
Logs:
  🧱 block number: 19443666
  🪙 token 1: USDC
  🪙 token 2: WETH.e
  💰 possible $ profit: 9674

Test result: ok. 1 passed; 0 failed; finished in 2.33s
```

<br>


----

### useful links

<br>

* [foudry book](https://book.getfoundry.sh/)


