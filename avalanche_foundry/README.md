## 🧱👵🏽 inspecting old blocks in avalanche

<br>

### tl; dr

<br>

##### 🛠 in this project, we use [foundry](https://github.com/foundry-rs/foundry) to analyze blocks history in the avalanche blockchain. this can be used for several purposes, including testing vulnerabilities or extracting mev data.

##### 📚 for more details, check [this mirror post](https://mirror.xyz/steinkirch.eth/e-gsChe2GxfadHeBnMDsWe_4eQar9JJHJKlWqIE-jKY).

##### 🚨 disclaimer: i am not responsible for anything you do with my free code.


<br>

----

### installing

<br>

install [foundry](https://book.getfoundry.sh/getting-started/installation)



add config info to `.env`, including an RPC for avalanche (*e.g.*, [ankr's](https://www.ankr.com/rpc/avalanche/)):

```
cp .env_example .env
vim .env
```


<br>

---

### examples

<br>

#### simulating sandwich attack

<br>

1. follow the installation and setup above.
2. define the desired assets and/or protocols to research, and find out the methods that update price.
3. use any blockchain analytic tool (*e.g.,* [dune](https://dune.com/home) or [avax apis](https://docs.avax.network/apis/avalanchego/public-api-server)) to search for past blocks with a considerable price movement. 
4. take note of the block numbers you want to analyze and add them to `data/blocks.txt`. there is one example there already to get you started.
5. run this code by following the instructions above, and check the results in `results/`.


