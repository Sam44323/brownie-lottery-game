from brownie import Lottery, accounts, network


def deploy_lottery():
    account = accounts[0]
    print(account)


def main():
    deploy_lottery()
