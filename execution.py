# Helper class for executing trades against Mycelium Perp Swaps
from mlp_helpers import getTokenPriceWithSpread


referral_code = "0x0000000000000000000000000000000000000000000000000000000000000000"

# increases position usign ERC20 as collat per https://swaps.docs.mycelium.xyz/developer-resources/contract-interactions
# token_in -> token being used to take the position (use stablecoin ERC20 with best borrowing rate)
# target_token -> asset to take the position on (ETH or BTC)
# collateral_amount -> amount of collat (stablecoin) going in (units 10^18)
# leverage -> integer amount of leverage being taken -> todo might be better ways to pass in this param
# size_delta -> USD value of change in position size. 10^30 units
# price -> USD price in 10^30 units
def increasePositionToken(router, vault, token_in, target_token, collateral_amount_in, size_delta, is_long, account, w3):
    execution_fee = 150000000000000 #todo
    nonce = w3.eth.get_transaction_count(account.address)

    price_with_spread = getTokenPriceWithSpread(vault, target_token, is_long)

    transaction = router.functions.createIncreasePosition(
        [token_in],
        target_token,
        collateral_amount_in,
        0,
        size_delta,
        is_long,
        int(price_with_spread),
        execution_fee,
        referral_code
    ).build_transaction({
        'chainId': 42161,
        'gas': 3000000,
        'maxFeePerGas': w3.toWei('0.1', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('0.1', 'gwei'),
        'nonce': nonce,
        'value': execution_fee
    })

    signed = account.sign_transaction(transaction)
    result = w3.eth.send_raw_transaction(signed.rawTransaction)
    # return txn hash
    return result




# decreases position using ERC20 as collat per https://swaps.docs.mycelium.xyz/developer-resources/contract-interactions
def decreasePositionToken(router, vault, token_out, target_token, collateral_amount_out, size_delta, is_long, account, w3):
    execution_fee = 150000000000000 #todo
    nonce = w3.eth.get_transaction_count(account.address)

    # use current oracle price + accepted deviation to price order
    # todo improve pricing here / verify safety
    oracle_price = vault.functions.getMinPrice(target_token).call()
    price_with_slippage = oracle_price + (oracle_price * 0.005)
    print(int(price_with_slippage))
    print(oracle_price)
    # invert is long because closing a short -> want max price. Closing a long -> want min price to avoid issues.
    price_with_spread = getTokenPriceWithSpread(vault, target_token, not is_long)

    transaction = router.functions.createDecreasePosition(
        [token_out],
        target_token,
        collateral_amount_out,
        size_delta,
        is_long,
        account.address,
        int(price_with_spread),
        0,
        execution_fee,
        False
    ).build_transaction({
        'chainId': 42161,
        'gas': 3000000,
        'maxFeePerGas': w3.toWei('0.15', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('0.15', 'gwei'),
        'nonce': nonce,
        'value': execution_fee
    })

    signed = account.sign_transaction(transaction)
    result = w3.eth.send_raw_transaction(signed.rawTransaction)
    # return txn hash
    return result