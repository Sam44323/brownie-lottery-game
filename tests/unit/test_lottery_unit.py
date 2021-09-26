from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3
import time
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entranceFee = lottery.getEntranceFee()
    assert expected_entrance_fee == entranceFee
