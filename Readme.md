# Brownie Lottery App

**Pseudo-Decentralized lottery system with real-time usd**

### Tech-stack

- Brownie
- Python
- Ganache/Ganache-cli
- Web3
- Py-test
- Solidity
- ChainLink
- Etherscan-versioning

**Features**

1. Users can enter lottery with ETH based on USD
2. An admin will choose when the lottery is over
3. The lottery will select a random user

---

---

Wanna contribute? You're welcome. Follow these steps to add your contribution after you fork the repo.

---

**After your're done adding your updated code or adding a new contract, run the following commands in order**

_For compiling the contract_

```bash
brownie compile
```

_For deploying the contract_

- For ganache local network

```bash
brownie run scripts/deploy.py
```

- For a particular network

```bash
brownie run scripts/deploy.py --network <network-name>
```

_For testing the contract_

```bash
brownie test
```

_For test the contract in a specific network_

```bash
brownie test --network <network-name>
```

---
