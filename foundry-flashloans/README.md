## 🧱💸 comparisons of flashloans on ethereum


<br>

### tl; dr

<br>

##### 🛠 we leverage [foundry](https://github.com/foundry-rs/foundry) to compare flashloans from **lending protocols on ethereum**, including fees, deployment cost, and deployment size. 


##### 🕹 these boilerplates can be expanded for several purposes, including testing vulnerabilities or extracting mev data. this particular work is based on **[jeiwan's code](https://github.com/Jeiwan/flash-loans-comparison)**.

##### 🚨 disclaimer: i am not responsible for anything you do with my free code.


<br>

----

### installing deps

<br>

1. install **[foundry](https://book.getfoundry.sh/getting-started/installation)** (this will create `lib/forge-std`) and a **[solidity compiler](https://docs.soliditylang.org/en/latest/installing-solidity.html#installing-the-solidity-compiler)** (we are using **^0.8.16** in this project).


3. export an env variable foran **ethereum RPC URL** (*e.g.*, from **[infura's](https://app.infura.io/dashboard)**, **[alchemy](https://www.alchemy.com/)**, **[ankr's](https://www.ankr.com/rpc/avalanche/)**, or **your own node**):

```
> export RPC_URL=<RPC_URL>
```

<br>

---

### running the simulation

<br>

1. adjust [the constants in the beginning of the test file](https://github.com/go-outside-labs/blockchain-science-py/blob/main/historical-with-foundry/avalanche-c-chain/test/Gmx.sol#L19)

2. build the contracts and run with:

```
>  make test 

[⠆] Compiling...
No files changed, compilation skipped

Running 1 test for test/testFlashloans.sol:FlashloansTest
[PASS] testBalancer() (gas: 264732)
Test result: ok. 1 passed; 0 failed; finished in 1.66s
| src/Balancer.sol:Balancer contract |                 |       |        |       |         |
|------------------------------------|-----------------|-------|--------|-------|---------|
| Deployment Cost                    | Deployment Size |       |        |       |         |
| 247087                             | 1266            |       |        |       |         |
| Function Name                      | min             | avg   | median | max   | # calls |
| flashLoan                          | 24407           | 25727 | 24407  | 37608 | 10      |
| receiveFlashLoan                   | 4150            | 4150  | 4150   | 4150  | 10      |

```

<br>


