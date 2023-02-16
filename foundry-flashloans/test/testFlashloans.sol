// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.16;

import "forge-std/Test.sol";
import "../src/Balancer.sol";


contract FlashloansTest is Test {
    Balancer balancer;

    address constant wethAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    function setUp() public {

        balancer = new Balancer();


        giveWeth(address(balancer));

    }

   

    function testBalancer() public {
        address[] memory assets = new address[](1);
        assets[0] = wethAddress;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 1 ether;

        for (uint256 i; i < 10; i++) {
            balancer.flashLoan(assets, amounts);
        }
    }


    function giveWeth(address addr) internal {
        vm.store(
            wethAddress,
            keccak256(abi.encode(addr, uint256(3))),
            bytes32(uint256(10 ether))
        );
    }
}