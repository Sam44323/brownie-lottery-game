from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


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


def get_contract():
    """
    This function will grab the contract addresses from the brownie config if defined, otherwise, it will deploy a mock version of that contract and return that mock address

    Args:
        contract_name: (string)
    Return:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract.
    """
