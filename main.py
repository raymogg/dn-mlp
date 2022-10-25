from time import sleep
from web3 import Web3
import os
from dotenv import load_dotenv
import json
load_dotenv()

# setup web3
rpc = os.getenv("RPC")
w3 = Web3(Web3.HTTPProvider(rpc))

# setup MLP contracts

# setup connection to hedging facility
