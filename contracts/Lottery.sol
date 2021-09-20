//SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFee;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18); // storing the entry whenever  we initilized an instance of the contract
        ethUsdPriceFee = AggregatorV3Interface(_priceFeedAddress);
    }

    // entering a lottery
    function enter() public payable {}

    // returns the latest price for eth in usd
    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFee.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (10**10);
        uint256 costToEnter = (usdEntryFee * (10**18)) / adjustedPrice;
        return costToEnter;
    }

    // method for starting a lottery(admin)
    function startLottery() public {}

    // method for ending a lottery(admin)
    function endLottery() public {}
}
