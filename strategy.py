import mlp_helpers
import position_helpers
import execution
class Strategy():
    # class for managing the stategy.
    # will hold initial state and allow execution of updates / update internal balances when this happens
    
    def __init__(self, vault, reader, router, mlp, tokens, tokens_to_hedge, tokens_as_collateral, account, w3):
        self.vault = vault
        self.reader = reader
        self.router = router
        self.mlp = mlp
        self.mlp_tokens = tokens
        self.mlp_tokens_to_hedge = tokens_to_hedge
        self.tokens_as_collateral = tokens_as_collateral
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

        # todo compute target exposure
        target_exposure = {
            "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": -35000000000000000000000000000000,
            "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": -35000000000000000000000000000000
        }

        # get current exposure for ETH and BTC
        exposure = position_helpers.get_current_exposure(self.vault, self.reader, self.account.address, self.tokens_as_collateral, self.mlp_tokens_to_hedge)
        
        # compute required delta
        exposure_delta = position_helpers.get_hedge_delta(self.vault, exposure, target_exposure)

        # perform update using execution.py
        for asset in exposure_delta.keys():
            # make trade of size exposure_delta[asset]
            raw_size = exposure_delta[asset][0]

            if raw_size != 0:

                size = int(abs(raw_size))
                is_long = True if raw_size > 0 else False

                if (abs(raw_size) > abs(target_exposure[asset])):
                    # decrease exposure
                    print("decreasing exposure")
                    print(asset)
                    print(exposure_delta)
                    print(exposure_delta[asset][1])
                    print(size)
                    print(is_long)
                    execution.decreasePositionToken(
                        self.router,
                        self.vault,
                        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
                        asset,
                        exposure_delta[asset][1],
                        size,
                        is_long,
                        self.account,
                        self.w3
                    )
                else:
                    # increase exposure
                    print("increasing exposure")
                    print(asset)
                    print(exposure_delta)
                    print(exposure_delta[asset][1])
                    print(size)
                    print(is_long)
                    execution.increasePositionToken(
                        self.router,
                        self.vault,
                        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
                        asset,
                        exposure_delta[asset][1],
                        size,
                        is_long,
                        self.account,
                        self.w3
                    )

