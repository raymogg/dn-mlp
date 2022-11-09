from time import sleep
from web3 import Web3
import os
from dotenv import load_dotenv
import json
from execution import decreasePositionToken, increasePositionToken
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

router_address = os.getenv("ROUTER")
router_file = open("./contracts/PositionRouter.json")
router_abi = json.load(router_file)["abi"]
router = w3.eth.contract(abi=router_abi, address=router_address)

reader_address = os.getenv("READER")
reader_file = open("./contracts/Reader.json")
reader_abi = json.load(reader_file)["abi"]
reader = w3.eth.contract(abi=reader_abi, address=reader_address)

private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)
print("Running with account: " + account.address)

# get array of all tokens held in MLP
mlp_tokens = mlp_helpers.getMLPTokens(vault)
# hedge WETH and WBTC
tokens_to_hedge = ["0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"]
# WETH, WBTC and DAI for collateral
tokens_as_collateral = ["0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f", "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"]
# Initialise strategy
strategy = Strategy(vault, reader, router, mlp, mlp_tokens, tokens_to_hedge, tokens_as_collateral, account, w3)

# increasePositionToken(
#     router,
#     vault,
#     "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
#     "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
#     10000000000000000000,
#     2,
#     False,
#     account,
#     w3
# )

# sleep(30)

# decreasePositionToken(
#     router,
#     vault,
#     "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
#     "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
#     10000000000000000000,
#     False,
#     account,
#     w3
# )



# Strategy
# Hedging -> check and hedge every 6 hours
strategy.update_hedges()

# MLP Rewards -> claim every 24 hours

# MYC Rewards -> claim every 7 days

# setup connection to hedging facility
