//SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    uint256 public usdEntryFee;
    address[] public players;
    AggregatorV3Interface internal ethUsdPriceFee;

    // declaring a state of type LOTTERY_STATE
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18); // storing the entry whenever  we initilized an instance of the contract
        ethUsdPriceFee = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    // entering a lottery
    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(
            msg.value >= getEntranceFee(),
            "Not enought ETH to enter the Lottery!"
        );
        players.push(msg.sender);
    }

    // returns the latest price for eth in usd
    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFee.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (10**10);
        uint256 costToEnter = (usdEntryFee * (10**18)) / adjustedPrice;
        return costToEnter;
    }

    // method for starting a lottery(admin)
    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "The lottery is already open! close it before starting a new one."
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    // method for ending a lottery(admin)
    function endLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "You can end a lottery that's not even started!"
        );
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}
