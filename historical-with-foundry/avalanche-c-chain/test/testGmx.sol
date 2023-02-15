// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.6.12;

import "forge-std/Test.sol";
import "contracts/Router.sol";


/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
// note: this test is not meant to be optimized for gas
// it is meant to be a easy to read test for this problem
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////


contract getHistorical is Test {

    ////////////////////////////////////
    // define all constants in the test
    ///////////////////////////////////

    uint256 constant T1_VALUE = 1560;
    uint256 constant T2_VALUE = 1;
    uint256 constant T1_QTY = 1;
    uint256 constant T2_QTY = 1e6;
    uint32 constant SIMULATION_CUTOFF = 20;
    uint32 constant SIMULATION_STEP = 3;
    string constant blocks_path = 'data/blocks.txt';

    // define all erc20 tokens you would like to analyze
    // (you can add all tokens from glp or any intermediaries)
    IERC20 constant USDC  = IERC20(0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E);
    IERC20 constant WETH = IERC20(0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB);

    // gmx contracts
    Router constant router = Router(0x5F719c2F1095F7B9fc68a68e35B51194f4b6abe8);
    uint32 constant ROUTER_MIN_OUT = 0;


    ////////////////////
    // utils: logging
    ////////////////////

    function log_tokens(swapStruct memory this_swap) internal 
    {
        log_named_string("🪙 token 1", this_swap.t1.symbol());
        log_named_string("🪙 token 2", this_swap.t2.symbol());
    }

    function log_profit(uint256 profit) internal 
    {
        log_named_uint("🥪 possible $ profit (usd)", profit);
    }

    function log_block(uint256 this_block) internal 
    {
        log_named_uint("🧱 block number", this_block);
    }

    function log_simulation_info(uint32 simulation_loop_num) internal 
    {
        log_named_uint("🔂 loops in the simulation", simulation_loop_num);
    }

    ////////////////////////////////
    // utils: forge storage methods
    ////////////////////////////////

    function createStorage(address token, address signer, uint256 qty) internal 
    {
        // https://github.com/foundry-rs/forge-std/blob/master/src/StdStorage.sol#L6
        stdstore
            .target(token)
            .sig(IERC20(token).balanceOf.selector)
            .with_key(signer)
            .checked_write(qty);
    }


    ////////////////////
    // utils: maths
    ////////////////////

    function uint2str(string memory s) internal pure returns (uint) 
    {
        bytes memory b = bytes(s);
        uint result = 0;
        for (uint256 i = 0; i < b.length; i++) 
        {
            uint256 c = uint256(uint8(b[i]));
            if (c >= 48 && c <= 57) 
            {
                result = result * 10 + (c - 48);
            }
        }
        return result;
    }


    ///////////////////////////////////////////////////////////
    // simulation: simulate swap() for this and previous block
    ////////////////////////////////////////////////////////

    function extractBlockData(uint256 this_block, uint256 qty, IERC20 t1, IERC20 t2) external returns (uint256)
    {
        // 1) what was the chain state in the previous block?
        // https://book.getfoundry.sh/cheatcodes/roll-fork?highlight=vm.rollfork#rollfork
        vm.rollFork(this_block - 1);

        // 2) what was token balance in the previous block?
        uint256 _amountIn = qty * (10 ** uint256(t1.decimals()));
        createStorage(address(t1), address(this), _amountIn);
        t1.approve(address(router), _amountIn);

        // 3) run gmx swap()
        address[] memory _path_before = new address[](2);
        _path_before[0] = address(t1);
        _path_before[1] = address(t2);
        //https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/Router.sol#L88
        router.swap(_path_before, _amountIn, ROUTER_MIN_OUT, address(this));
        uint256 _amountOut = t2.balanceOf(address(this));

        // 4) back to this block
        vm.rollFork(this_block);
        t2.approve(address(router), _amountOut);
        createStorage(address(t2), address(this), _amountOut);

        // 5) run gmx swap() after oracle update
        address[] memory _path = new address[](2);
        _path[0] = address(t2);
        _path[1] = address(t1);
        router.swap(_path, _amountOut, ROUTER_MIN_OUT, address(this));
        uint256 t1_balance = t1.balanceOf(address(this));

        return t1_balance;
    }


    ////////////////////////////////////////////////////////////////
    // simulation: extract the profit data from the block simulation
    ////////////////////////////////////////////////////////////////
    
    function simulateProfit(uint256 this_block) private returns(uint256)
    {
        // start a snapshot of the state of the chain, and revert to it at the end of the function
        // https://book.getfoundry.sh/cheatcodes/snapshots?highlight=vm.snapshot#snapshot-cheatcodes
        uint256 vm_id = vm.snapshot();
        uint256 result = 0;
        uint32 simulation_loop_num = 0;

        // run this loop for each token in our list 
        // (for now only USDC and WETH, but more if more tokens are added)
        for (uint token_i = 0; token_i < swapDict.length; token_i++) 
        {
            bool simulation_stop = false;
        
            swapStruct memory this_swap = swapDict[token_i];
            uint256 this_amount = this_swap.quantity;
            uint256 this_t1_balance = 10 ** uint256(this_swap.t1.decimals());
            
            uint256 _amountOut = 0;
            uint256 _amountOutBefore = 0;

            while (!simulation_stop && simulation_loop_num < SIMULATION_CUTOFF)
            {
                try this.extractBlockData(this_block, this_amount, this_swap.t1, this_swap.t2) returns (uint256 t1_balance)
                {
                    _amountOut = t1_balance;
                    _amountOutBefore = this_amount;
                    this_amount *= SIMULATION_STEP;
                }
                catch
                {
                    simulation_stop = true; 
                    _amountOutBefore *= this_t1_balance;
                    // sandwich
                    if (_amountOut > _amountOutBefore)
                    {
                        log_tokens(this_swap);
                        result = this_swap.value * (_amountOut - _amountOutBefore) / this_t1_balance;
                    }
                }  
                simulation_loop_num += 1;  
                vm.revertTo(vm_id);        
            }
        }
        log_simulation_info(simulation_loop_num);
        return result;
    }


    //////////////////
    // TESTS: setup
    //////////////////

    struct swapStruct 
    {
        IERC20 t1;
        IERC20 t2;
        uint256 value;
        uint256 quantity;
    }
    swapStruct[] public swapDict;

    function setUp() public
    {
        swapDict.push(swapStruct({t1: WETH, t2: USDC, value: T1_VALUE, quantity: T1_QTY }));
        swapDict.push(swapStruct({t1: USDC, t2: WETH, value: T2_VALUE, quantity: T2_QTY }));
    }


    ///////////////
    // TESTS: run
    //////////////

    function testHistoricalGmx() public
    {
        uint256 profit;
        uint256 this_block = 1;
    
        while (this_block > 0)
        {
            // https://book.getfoundry.sh/cheatcodes/fs?highlight=readline#file-cheat-codes
            this_block = uint2str(vm.readLine(blocks_path));
            if (this_block != 0)
            {
                log_block(this_block);
                profit += simulateProfit(this_block);
            }
        }

        log_profit(profit);
        
    }

}

