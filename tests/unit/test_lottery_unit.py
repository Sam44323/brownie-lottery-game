from _pytest.config import exceptions
from brownie import network, reverts
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_links
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
