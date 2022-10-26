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
mlp_address = os.getenv("MLP")
mlp_file = open("./contracts/MLP.json")
mlp_abi = json.load(mlp_file)["abi"]
mlp = w3.eth.contract(abi=mlp_abi, address=mlp_address)

# get array of all tokens held in MLP
mlp_tokens = helpers.getMLPTokens(vault)

# Vault
# test get token weights
# token_weights = helpers.getTokensTargetWeights(vault, mlp_tokens)
# print(token_weights)

# # test get current weights
# target_weights = helpers.getTokensCurrentWeights(vault, mlp_tokens)
# print(target_weights)

total_exposure = helpers.usdExposure(vault, mlp_tokens, mlp, 1000000000000000000)
print(total_exposure)

# testing convert to raw dollar values
# appears to be working accurately -> this gives exposure per asset
for exposure in total_exposure:
    print(str(exposure[0]) + ": " + str(w3.fromWei(float(exposure[1]), "ether")))

# - getMaxPrice / getMinPrice
# - token balances (exact tokens held by index?)


# setup connection to hedging facility
