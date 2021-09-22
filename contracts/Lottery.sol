//SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    uint256 public usdEntryFee;
    address[] public players;
    AggregatorV3Interface internal ethUsdPriceFee;
    bytes32 public keyhash;
    uint256 public fee;

    // declaring a state of type LOTTERY_STATE
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18); // storing the entry whenever  we initilized an instance of the contract
        ethUsdPriceFee = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
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
    // we'll call this one
    function endLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "You can end a lottery that's not even started!"
        );
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    // once the chainlink node has created a provely random number then it's going to call this function
    // for the transaction
}
