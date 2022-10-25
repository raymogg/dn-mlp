# get token target weights (USD value)
# simply read from contract
from fractions import Fraction

# Returns the addresses of all assets currently in MLP
def getMLPTokens(vault):
    num_tokens = vault.functions.allWhitelistedTokensLength().call()
    tokens = []
    for i in range(int(num_tokens)):
        token = vault.functions.allWhitelistedTokens(i).call()
        tokens.append(token)
    return tokens

# Returns the target weights of every asset in the tokens list
def getTokensTargetWeights(vault, tokens):
    weights = []
    total_weights = vault.functions.totalTokenWeights().call()
    for token in tokens:
        target_weight = vault.functions.tokenWeights(token).call()
        weight = Fraction(target_weight, total_weights)
        weights.append([token, weight])
    return weights

# Returns the target weight of a given token
def getTokenTargetWeight(vault, token):
    target = vault.functions.tokenWeights(token).call()
    total = vault.functions.totalTokenWeights().call()
    return Fraction(target, total)

# Returns the token price reported by the MYC oracle for a given token
def getTokenPrice(vault, token):
    # todo this seems wrong - this should probably call the oracle of the token
    price = vault.functions.getMaxPrice(token).call()
    return price

# Returns the token weight for agiven token
def getTokenCurrentWeight(vault, token):
    # todo return the tokens USDG weight
    print("getTokenCurrentWeight")

# Returns the token weights of every asset in the tokens list
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

# Returns the amount of tokens held by the MLP vault for each token in the vault
def getTokensUSDGAmounts(vault, tokens):
    amounts = []
    for token in tokens:
        amount = getTokenUSDGAmount(vault, token)
        amounts.append([token, amount])
    return amounts

# gets the amount of tokens held by the MLP vault denominated in USDG (USD)
def getTokenUSDGAmount(vault, token):
    usdg_amount = vault.functions.usdgAmounts(token).call()
    return usdg_amount

# Compute USD exposure to each asset for a given amount of mlp
def usdExposure(vault, tokens, mlp, mlp_balance):
    # compute share of MLP
    mlp_supply = mlp.functions.totalSupply().call()
    share = Fraction(mlp_balance, mlp_supply)
    # get amount of each asset held by vault denominated in USDG
    token_amounts = getTokensUSDGAmounts(vault, tokens)
    token_shares = []
    # for each token compute net USDG exposure for holding mlp_balance units of MLP.
    for token_amount_pair in token_amounts:
        token_shares.append([token_amount_pair[0], token_amount_pair[1] * share])
    return token_shares