from brownie import accounts, network, config, Contract, MockV3Aggregator

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimal=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(
        decimal, initial_value, {"from": account})
    print("Deployed!")


def get_account(index=None, id=None):
    if id:
        # returns the account with the id stored in brownie
        return accounts.load(id)
    elif index:
        # returning a particular account from the accounts array
        return accounts[index]
    elif(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    # returning the account derived from the key
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": MockV3Aggregator,
}


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the brownie config if defined, otherwise, it will deploy a mock version of that contract and return that mock address

    Args:
        contract_name: (string)
    Return:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        # getting the latest deployed contract for that type
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )]["eth_usd_price_feed"]
        # getting a deployed contract from the abi
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi)
    return contract
