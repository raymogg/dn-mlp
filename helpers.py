# get token target weights (USD value)
# simply read from contract
from fractions import Fraction

def getMLPTokens(vault):
    num_tokens = vault.functions.allWhitelistedTokensLength().call()
    tokens = []
    for i in range(int(num_tokens)):
        token = vault.functions.allWhitelistedTokens(i).call()
        tokens.append(token)
    return tokens

def getTokensTargetWeights(vault, tokens):
    weights = []
    total_weights = vault.functions.totalTokenWeights().call()
    for token in tokens:
        target_weight = vault.functions.tokenWeights(token).call()
        weight = Fraction(target_weight, total_weights)
        weights.append([token, weight])
    return weights

def getTokenTargetWeight(vault, token):
    target = vault.functions.tokenWeights(token).call()
    total = vault.functions.totalTokenWeights().call()
    return Fraction(target, total)

# get token current weights (USD value)
# get token USD value and div by USD supply
def getTokenPrice(vault, token):
    # todo this seems wrong - this should probably call the oracle of the token
    price = vault.functions.getMaxPrice(token).call()
    return price

def getTokenCurrentWeight(vault, token):
    # todo return the tokens USDG weight
    print("getTokenCurrentWeight")

def getTokensCurrentWeights(vault, tokens):
    total = 0
    raw_amounts = []
    target_weights = []
    for token in tokens:
        token_usdg = getTokenUSDGAmount(vault, token)
        total += token_usdg
        raw_amounts.append([token, token_usdg])
    for raw in raw_amounts:
        target_weights.append([raw[0], Fraction(raw[1], total)])
    return target_weights

def getTokenUSDGAmount(vault, token):
    usdg_amount = vault.functions.usdgAmounts(token).call()
    return usdg_amount



# calculate hedge amount for asset