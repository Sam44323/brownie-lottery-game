from brownie import Lottery, network, config
from scripts.helpful_scripts import get_account, get_contract


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


def main():
    deploy_lottery()
    start_lottery()
