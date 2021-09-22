from brownie import Lottery
from helpful_scripts import get_account


def deploy_lottery():
    account = get_account()
    print(account)


def main():
    deploy_lottery()
