from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import time


def test_get_entrance_fee():
    lottery = deploy_lottery()
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entranceFee = lottery.getEntranceFee()
    assert expected_entrance_fee == entranceFee
