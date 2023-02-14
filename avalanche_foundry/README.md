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

1. define the desired assets and/or protocols you want to research, and find out the methods that update their prices. in this example, we will be using [gmx](https://github.com/gmx-io/gmx-contracts).

2. the main code of this work is inside `test\` (foundry is a solidity testing toolkit), so add/clone the desired protocol's contracts inside `lib\`.

3. use any blockchain analytic tool (*e.g.,* [dune](https://dune.com/home) or [avax apis](https://docs.avax.network/apis/avalanchego/public-api-server)) to search for past blocks with a considerable price movement. 

4. create a list of the block numbers you want to analyze and add them to `data/blocks.txt`. there is one example there already to get you started (on avalanche c-chain).

<br>


#### installing 

<br>

1. install [foundry](https://book.getfoundry.sh/getting-started/installation)

2. install a [solidity compiler](https://docs.soliditylang.org/en/latest/installing-solidity.html#installing-the-solidity-compiler)

3. create an env variable for avalanche c-chain's RPC url (*e.g.*, from [infura's](https://avalanche-mainnet.infura.io/v3/) or [ankr's](https://www.ankr.com/rpc/avalanche/) or your own node):

```
export URL=<URL>
```


#### running

<br>

build the contracts and check test pass:

```
make run
```


