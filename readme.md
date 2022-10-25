# Delta Neutral MLP
This is a basic DN strategy.

It takes a position in MLP - which is an index holding a basket of assets. It earns yield through trading rewards as well as through MYC rewards.

The strategy does not remain perfectly DN - it holds some crypto market exposure. It does this to reduce the cost of hedging. It only hedges the major crypto holdings of MLP (ETH and BTC) and does not hedge the long tail assets held by the index.

The strategy will rebalance its position every 6 hours if needed.

Any earned MYC will unlocked and then be sold for USDC and redeposited into MLP. Any earned ETH will be deposited back into MLP.

# Strategy details
- exposure rebalancing: every 6 hours
- reward claiming: every 24 hours
- MYC claiming: every 7 days