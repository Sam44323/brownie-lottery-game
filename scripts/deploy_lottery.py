from brownie import Lottery, network, config
from scripts.helpful_scripts import get_account, get_contract, fund_with_links


def deploy_lottery():
    account = get_account()
    Lottery.deploy(
        get_contract(
            "eth_usd_price_feed").address,
        get_contract(
            "vrf_coordinator").address,
        get_contract(
            "link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify", False)  # if verify key is not there then set it to false
    )
    print("Deployed the lottery!")


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    start_tx = lottery.startLottery({
        "from": account
    })
    start_tx.wait(1)  # waiting for the transaction to complete
    print("The lottery is open!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    transact = lottery.enter({
        "from": account,
        "value": value
    })
    transact.wait(1)
    print("Entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # funding the contract with link and then ending the lottery
    fund_with_links(contract_address=lottery.address)
    transaction = lottery.endLottery({
        "from": account
    })
    transaction.wait(1)
    print("Ended the lottery!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
