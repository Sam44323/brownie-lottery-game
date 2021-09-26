from _pytest.config import exceptions
from brownie import network, reverts
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_links, get_contract
from web3 import Web3
import pytest


def network_checker():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    else:
        return


def test_get_entrance_fee():
    network_checker()
    lottery = deploy_lottery()
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entranceFee = lottery.getEntranceFee()
    assert expected_entrance_fee == entranceFee


def test_cant_enter_unless_started():
    network_checker()
    lottery = deploy_lottery()
    with reverts("Lottery is not open yet!"):
        lottery.enter({
            "from": get_account(),
            "value": lottery.getEntranceFee()
        })


def test_can_start_and_enter_lottery():
    network_checker()
    account = get_account()
    lottery = deploy_lottery()
    start_tx = lottery.startLottery({
        "from": account
    })
    start_tx.wait(1)  # waiting for the transaction to complete
    value = lottery.getEntranceFee() + 100000000
    transact = lottery.enter({
        "from": account,
        "value": value
    })
    transact.wait(1)
    assert lottery.players(0) == account


def test_can_end_lottery():
    network_checker()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_links(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    network_checker()
    account = get_account()
    lottery = deploy_lottery()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1),
                  "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2),
                  "value": lottery.getEntranceFee()})
    fund_with_links(lottery)
    transaction = lottery.endLottery({"from": account})
    # getting the request id for the contract
    request_id = transaction.events["RequestRandomness"]["requestId"]
    STATIC_RNG = 777
    # calling the function posing as a vrf node with that request id value
    get_contract(
        "vrf_coordinator").callBackWithRandomness(request_id, STATIC_RNG, lottery.address, {"from": account})
    starting_balance = account.balance()
    lottery_balance = lottery.balance()
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance + lottery_balance
