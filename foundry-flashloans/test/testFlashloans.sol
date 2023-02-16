// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.16;

import "forge-std/Test.sol";
import "../src/Balancer.sol";


/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
// note: this test is not meant to be optimized for gas
// it is meant to be a easy to read test for this problem
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////



contract getFlashloansData is Test {

    ////////////////////////////////////
    // define all constants in the test
    ///////////////////////////////////

    uint32 constant SIMULATION_CUTOFF = 20;
    address constant WETH_ADDRESS = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    Balancer balancer;


    ////////////////////
    // utils: logging
    ////////////////////

    function log_protocol_info(string memory protocol, uint256 data) internal 
    {
        emit log_named_uint(protocol, data);
    }

    ////////////////////////////////////////////////////////////////
    // simulation: create a vm storage for testing weth flashloans
    ////////////////////////////////////////////////////////////////

    function create_weth_storage(address addr) internal {
        // https://github.com/foundry-rs/forge-std/blob/master/src/StdStorage.sol#L6
        vm.store(
            WETH_ADDRESS,
            keccak256(abi.encode(addr, uint256(3))),
            bytes32(uint256(10 ether))
        );
    }


    //////////////////
    // TESTS: setup
    //////////////////

    function setUp() public {
        balancer = new Balancer();
        create_weth_storage(address(balancer));

    }

   
    ///////////////
    // TESTS: run
    //////////////

    function testBalancer() public {
        address[] memory assets = new address[](1);
        assets[0] = WETH_ADDRESS;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 1 ether;

        for (uint32 i; i < SIMULATION_CUTOFF; i++) {
            balancer.flashLoan(assets, amounts);
        }
    }
}
