import mlp_helpers
import position_helpers
class Strategy():
    # class for managing the stategy.
    # will hold initial state and allow execution of updates / update internal balances when this happens
    
    def __init__(self, vault, mlp, tokens, tokens_to_hedge, account, w3):
        self.vault = vault
        self.mlp = mlp
        self.mlp_tokens = tokens
        self.mlp_tokens_to_hedge = tokens_to_hedge
        self.account = account
        self.mlp_balance = 0
        # map from asset to USD exposure in MLP
        self.total_exposure = {}
        self.w3 = w3

        # load in balances
        self.update_mlp_balance()
        self.update_mlp_exposure()
        

    def update_mlp_exposure(self):
        # compute total exposure per asset
        exposures = mlp_helpers.usdExposure(self.vault, self.mlp_tokens, self.mlp, self.mlp_balance)
        for exposure in exposures:
            self.total_exposure[str(exposure[0])] = exposure[1]
            print(str(exposure[0]) + ": " + str(self.w3.fromWei(float(exposure[1]), "ether"))) 
    
    def update_mlp_balance(self):
        # todo uncomment when ready
        # self.mlp_balance = account.getMLPBalance(self.mlp, "0x2bb8ab3c2a9837de97a83c228a07e16928b4f07f")
        self.mlp_balance = 1000000000000000000
    
    def update_hedges(self):
        # update mlp exposure
        self.update_mlp_exposure()

        # for each asset being hedged, update position
        for asset in self.mlp_tokens_to_hedge:
            print("---- HEDGING ----")
            print(asset)
            print("USD Value: $" + str(self.total_exposure[asset]))
            exposure = position_helpers.get_current_exposure(self.vault, asset)
            # get hedge delta for asset

            # perform update using execution.py
        
