# Helper class for executing trades against Mycelium Perp Swaps
referral_code = "todo"

# increases position usign ERC20 as collat per https://swaps.docs.mycelium.xyz/developer-resources/contract-interactions
def increasePositionToken(router, token_in, target_token, collateral_amount, is_long, price):
    size_delta = collateral_amount * price
    execution_fee = 0 #todo
    router.functions.createIncreasePosition(
        [token_in],
        target_token,
        collateral_amount,
        0,
        size_delta,
        is_long,
        price,
        execution_fee,
        referral_code
    ).call()

# decreases position using ERC20 as collat per https://swaps.docs.mycelium.xyz/developer-resources/contract-interactions
def decreasePositionToken(router, token_out, target_token, collateral_amount_out, is_long, price, receiver):
    size_delta = collateral_amount * price
    execution_fee = 0 #todo
    router.functions.createDecreasePosition(
        [token_out],
        target_token,
        collateral_amount_out,
        size_delta,
        0,
        is_long,
        receiver,
        price,
        0,
        execution_fee,
        False
    ).call()