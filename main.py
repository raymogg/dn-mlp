from time import sleep
from web3 import Web3
import os
from dotenv import load_dotenv
import json
import helpers

load_dotenv()

# setup web3
rpc = os.getenv("RPC")
w3 = Web3(Web3.HTTPProvider(rpc))

# setup MLP contracts
vault_address = os.getenv("VAULT")
vault_file = open("./contracts/Vault.json")
vault_abi = json.load(vault_file)["abi"]
vault = w3.eth.contract(abi=vault_abi, address=vault_address)
mlp_tokens = helpers.getMLPTokens(vault)

# Vault
# test get token weights
token_weights = helpers.getTokensTargetWeights(vault, mlp_tokens)
print(token_weights)

# test get current weights
target_weights = helpers.getTokensCurrentWeights(vault, mlp_tokens)
print(target_weights)
# - getMaxPrice / getMinPrice
# - token balances (exact tokens held by index?)


# setup connection to hedging facility
