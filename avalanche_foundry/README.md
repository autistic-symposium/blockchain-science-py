## 🧱👵🏽 inspecting blockchains with foundry's vm

<br>

### tl; dr

<br>

##### 🛠 in this project, we leverage [foundry](https://github.com/foundry-rs/foundry) to analyze evm-based blockchains. foundry provides **["vm cheatcodes"](https://www.paradigm.xyz/2021/12/introducing-the-foundry-ethereum-development-toolbox#you-should-be-able-to-override-vm-state-in-your-tests)** that allow easy methods to modify the state at test runtime (for instance, simulating previous blocks).


##### 🕹 although this boilerplate contains only one test (looking at sandwich attacks in historical blocks data from avalanche c-chain), it could be expanded to be used for several purposes, including testing vulnerabilities or extracting mev data.

##### 🚨 disclaimer: i am not responsible for anything you do with my free code.


<br>

----
### simulating sandwich attacks on avalanche c-chain

<br>

#### gathering input data

<br>

1. define the **desired assets and/or protocols** you want to research. in this example, we are looking at **[gmx](https://github.com/gmx-io/gmx-contracts)** and running the test `test/testHistoricalGmx()`.

2. find out the **methods that trigger prices updates** (*e.g.* `swap()` on gmx's **[router](https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/Router.sol#L88)**).

2. add/clone all the contracts need for the methods above to `contracts/`. the main code we will be running is actually located inside `test/` (foundry is a solidity testing toolkit).

3. use any **blockchain analytics tools** (*e.g.,* **[dune](https://dune.com/home)** or **[avax apis](https://docs.avax.network/apis/avalanchego/public-api-server)**) to search for **past blocks** with a suspecting price movement (*e.g.,* set a threshold that could be interesting to look at). 

4. create a **list with all the blocks** you found and add them to `data/blocks.txt`. there is already one example to get you started (on avalanche c-chain).

<br>


#### installing deps

<br>

1. install **[foundry](https://book.getfoundry.sh/getting-started/installation)** (this will create a `lib/forge-std`). besides running `forge`, the tests import `forge-std/Test.sol` from there.

2. install a **[solidity compiler](https://docs.soliditylang.org/en/latest/installing-solidity.html#installing-the-solidity-compiler)**. you need to look at which solidity version your protocol is using. for instance, for gmx we have to use **[0.6.12](https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/VaultPriceFeed.sol#L11)**).

3. create an env variable for avalanche c-chain's RPC url (*e.g.*, from **[infura's](https://avalanche-mainnet.infura.io/v3/)** or **[ankr's](https://www.ankr.com/rpc/avalanche/)** or **your own node**):

```
export URL=<URL>
```

<br>

#### running the test (the simulation)

<br>

to build the contracts and run the test(s), run:

```
> make run

[⠢] Compiling...
[⠔] Compiling 17 files with 0.6.12
[⠑] Solc 0.6.12 finished in 2.31s
Compiler run successful

Running 1 test for test/Gmx.sol:getHistorical
[PASS] testHistoricalGmx() (gas: 81654567)
Logs:
  🧱 block number: 19443666
  🪙 token 1: USDC
  🪙 token 2: WETH.e
  💰 possible $ profit: 9674

Test result: ok. 1 passed; 0 failed; finished in 2.01s
```

<br>


----

### useful links

<br>

* [foudry book](https://book.getfoundry.sh/)


