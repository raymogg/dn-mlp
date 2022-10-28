import mlp_helpers
class Strategy():
    # class for managing the stategy.
    # will hold initial state and allow execution of updates / update internal balances when this happens
    
    def __init__(self, vault, mlp, tokens, account, w3):
        self.vault = vault
        self.mlp = mlp
        self.mlp_tokens = tokens
        self.account = account
        self.mlp_balance = 0
        self.total_exposure = []
        self.w3 = w3

        # load in balances
        self.update_mlp_balance()
        self.update_mlp_exposure()
        

    def update_mlp_exposure(self):
        # compute total exposure per asset
        self.total_exposure = mlp_helpers.usdExposure(self.vault, self.mlp_tokens, self.mlp, self.mlp_balance)
        for exposure in self.total_exposure:
            print(str(exposure[0]) + ": " + str(self.w3.fromWei(float(exposure[1]), "ether"))) 
    
    def update_mlp_balance(self):
        # todo uncomment when ready
        # self.mlp_balance = account.getMLPBalance(self.mlp, "0x2bb8ab3c2a9837de97a83c228a07e16928b4f07f")
        self.mlp_balance = 1000000000000000000