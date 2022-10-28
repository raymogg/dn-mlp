from time import sleep
from web3 import Web3
import os
from dotenv import load_dotenv
import json
import mlp_helpers
from strategy import Strategy

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
mlp_tokens = mlp_helpers.getMLPTokens(vault)

# Initialise strategy
# todo replace with actual account, placeholder for now
strategy = Strategy(vault, mlp, mlp_tokens, "0x2bb8ab3c2a9837de97a83c228a07e16928b4f07f")

# Strategy
# Hedging -> check and hedge every 6 hours

# MLP Rewards -> claim every 24 hours

# MYC Rewards -> claim every 7 days

# setup connection to hedging facility
