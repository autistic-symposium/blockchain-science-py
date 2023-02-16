// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.16;

import "forge-std/Test.sol";
import "../src/AaveV2.sol";
import "../src/Balancer.sol";
import "../src/Euler.sol";
import "../src/UniswapV2.sol";
import "../src/UniswapV3.sol";


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
    uint256 constant INTEREST_RATE = 0;
    uint256 constant AMOUNT = 1 ether;
    address constant WETH_ADDRESS = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    AAVE aave;
    Balancer balancer;
    Euler euler;
    UniswapV2 uniswapv2;
    UniswapV3 uniswapv3;


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
        aave = new AAVE();
        create_weth_storage(address(aave));

        balancer = new Balancer();
        create_weth_storage(address(balancer));

        euler = new Euler();
        create_weth_storage(address(euler));

        uniswapv2 = new UniswapV2();
        create_weth_storage(address(uniswapv2));

        uniswapv3 = new UniswapV3();
        create_weth_storage(address(uniswapv3));
    }

   
    ///////////////
    // TESTS: run
    //////////////

    function testAAVE() public {
        address[] memory assets = new address[](1);
        assets[0] = WETH_ADDRESS;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = AMOUNT;

        uint256[] memory modes = new uint256[](1);
        modes[0] = INTEREST_RATE; 

        for (uint32 i; i < SIMULATION_CUTOFF; i++) {
            aave.flashLoan(assets, amounts, modes);
        }
    }

    function testBalancer() public {
        address[] memory assets = new address[](1);
        assets[0] = WETH_ADDRESS;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = AMOUNT;

        for (uint32 i; i < SIMULATION_CUTOFF; i++) {
            balancer.flashLoan(assets, amounts);
        }
    }

    function testEulerFinance() public {
        for (uint32 i; i < SIMULATION_CUTOFF; i++) {
            euler.flashLoan(AMOUNT);
        }
    }

    function testUniswapV2() public {
        for (uint32 i; i < SIMULATION_CUTOFF; i++) {
            uniswapv2.flashLoan(AMOUNT);
        }
    }
        
    function testUniswapV3() public {
        for (uint32 i; i < SIMULATION_CUTOFF; i++) {
            uniswapv3.flashLoan(AMOUNT);
        }
    }

}
