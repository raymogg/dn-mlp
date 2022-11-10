
# returns current positional exposure to given asset
def get_current_exposure(vault, reader, account, collateral_tokens, index_tokens):
    # todo generalise this.
    # WETH:DAI (short), WBTC:DAI (short), WETH:WETH (long), WBTC: WBTC (long)
    _collateral_tokens = ["0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1", "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1", "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"]
    _index_tokens = ["0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f", "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"]
    positions = reader.functions.getPositions(
        vault.address,
        account,
        _collateral_tokens,
        _index_tokens,
        [False, False, True, True]
    ).call()

    # positions is an array corresponding to the ordered query
    # returns results as a single array so needs to be serialised back out
    # this could be generalised but we only care about eth and btc for now
    exposure = {}
    eth_shorts = positions[0: 9]
    btc_shorts = positions[9: 18]
    eth_longs = positions[18: 27]
    btc_longs = positions[27: 36]

    # net eth exposure and collateral
    # todo what more info will be needed
    net_eth = [eth_longs[0] - eth_shorts[0], eth_longs[1] + eth_shorts[1]]
    net_btc = [btc_longs[0] - btc_shorts[0], btc_longs[1] + btc_shorts[1]]
    exposure["0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"] = net_eth
    exposure["0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"] = net_btc
    print(exposure)
    return exposure


# given current exposure and target exposure, returns the required positional update
def get_hedge_delta(vault, current_exposures, target_exposures):
    exposure_deltas = {}
    for asset in current_exposures.keys():
        if (current_exposures[asset][0] != 0):
            # todo this is messy. current_exposures[0] is because this is returned from get_current_exposure
            exposure_deltas[asset] = []
            target_size = target_exposures[asset] - current_exposures[asset][0]
            exposure_deltas[asset].append(int(target_size))
            # compute amount of stablecoins in or out to keep same leverage
            current_leverage = abs(current_exposures[asset][0]) / current_exposures[asset][1]
            print("current leverage: " + str(current_leverage))
            # todo all positions will need a target leverage to be opened with
            new_collateral_amount = (abs(target_exposures[asset])) / current_leverage
            print("new collat amount: " + str(new_collateral_amount))
            collat_delta = (current_exposures[asset][1]) - new_collateral_amount
            print("collat delta: " + str(collat_delta))
            exposure_deltas[asset].append(int(collat_delta))
        else:
            exposure_deltas[asset] = [0, 0]


    print(exposure_deltas)
    return exposure_deltas

