## 🧱🥪 gmx sandwiches

<br>

### tl; dr

<br>

#### in this project, we inspect historical data on avalanche c-chain to simulate sandwich attacks in the gmx protocol.


<br>

---

### gathering input data

<br>

1. define the **desired assets and/or protocols** you want to research. in this example, we are looking at **[gmx](https://github.com/gmx-io/gmx-contracts)** and running the test `test/testGmx()`.

2. find out the **methods that trigger prices updates** (*e.g.* `swap()` on gmx's **[router](https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/Router.sol#L88)**).

2. add/clone all the contracts needed for the methods above to `contracts/`. the main code we will be running is located inside `test/` (foundry is a solidity testing platform).

3. use any **blockchain analytics tools** (*e.g.,* **[dune](https://dune.com/home)** or **[avax apis](https://docs.avax.network/apis/avalanchego/public-api-server)**) to search for **past blocks** with a suspecting price movement (*e.g.,* set a threshold that could be interesting to look at). 

4. create a **list with all the blocks** you found and add them to `data/blocks.txt`. there is already one example to get you started.

<br>

---

### installing deps

<br>

1. install **[foundry](https://book.getfoundry.sh/getting-started/installation)** (this will create `lib/forge-std`). this is not only needed for running `forge` per se, but also because our tests import `forge-std/Test.sol`. note that our directory setup is defined inside `foundry.toml`:

```
[profile.default]
src = 'data'
out = 'out'
libs = ['lib']
fs_permissions = [{ access = "read", path = "./"}]
```


2. install a **[solidity compiler](https://docs.soliditylang.org/en/latest/installing-solidity.html#installing-the-solidity-compiler)**. you need to look at which solidity version your protocol is using. for instance, for gmx we have to use **[0.6.12](https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/VaultPriceFeed.sol#L11)**.

3. export an env variable for avalanche c-chain's RPC url (*e.g.*, from **[infura's](https://avalanche-mainnet.infura.io/v3/)** or **[ankr's](https://www.ankr.com/rpc/avalanche/)** or **your own node**):

```
> export URL=<URL>
```

<br>

---

### running the simulation

<br>

1. adjust [the constants in the beginning of the test file](https://github.com/go-outside-labs/blockchain-science-py/blob/main/historical-with-foundry/avalanche-c-chain/test/Gmx.sol#L19)

2. build the contracts and run with:

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
  🔂 loops in the simulation: 12
  🥪 possible $ profit: 9720

Test result: ok. 1 passed; 0 failed; finished in 2.01s
```

<br>


