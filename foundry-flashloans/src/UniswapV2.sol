// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.16;

import {IERC20} from "./interfaces.sol";

interface IUniswapPair {
    function swap(
        uint256,
        uint256,
        address,
        bytes calldata
    ) external;
}

contract UniswapV2 {

    ////////////////////////
    // define all constants 
    ////////////////////////
    // WETH-USDC
    address constant PAIR_ADDRESS = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;
    address constant WETH_ADDRESS = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    IUniswapPair constant pair = IUniswapPair(PAIR_ADDRESS);
    IERC20 constant weth = IERC20(WETH_ADDRESS);

    function flashLoan(uint256 amount) public {
        // WETH is token1
        pair.swap(0, amount, address(this), hex"00");
    }

    function uniswapV2Call(
        address sender,
        uint256, /* amount0 */
        uint256 amount1,
        bytes calldata /* data */
    ) public {
        if (msg.sender != PAIR_ADDRESS) revert();
        if (sender != address(this)) revert();

        weth.transfer(msg.sender, (amount1 * 1000) / uint256(997) + 1);
    }
}