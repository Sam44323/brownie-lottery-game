from _pytest.config import exceptions
from brownie import network, reverts
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
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
