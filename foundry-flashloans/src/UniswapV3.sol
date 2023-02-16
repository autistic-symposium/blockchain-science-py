// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.16;

import {IERC20} from "./interfaces.sol";

interface IUniswapV3Pool {
    function flash(
        address recipient,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) external;
}

contract UniswapV3 {

    ////////////////////////////////////
    // define all constants in the test
    ///////////////////////////////////
    // WETH-USDC
    address constant PAIR_ADDRESS = 0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8;
    address constant WETH_ADDRESS = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    IERC20 constant weth = IERC20(WETH_ADDRESS);
    IUniswapV3Pool constant pair = IUniswapV3Pool(PAIR_ADDRESS);

    ////////////////////////
    // run flashloan 
    ////////////////////////
    
    function flashLoan(uint256 amount) public {
        // WETH is token1
        pair.flash(address(this), 0, amount, abi.encodePacked(amount));
    }

    function uniswapV3FlashCallback(
        uint256, /* fee0 */
        uint256 fee1,
        bytes calldata data
    ) public {
        if (msg.sender != PAIR_ADDRESS) revert();
        uint256 amount = abi.decode(data, (uint256));
        weth.transfer(msg.sender, amount + fee1);
    }
}