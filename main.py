import abis
from web3 import Web3

DECIMAL_PRECISION = 1e18
USDM_TO_WITHDRAW = 100

rpcs = [
    "https://fuse.liquify.com",
    "https://rpc.fuse.io"]
        

def check_provider(network_providers):
    for provider in network_providers:
        if network_provider := Web3(Web3.HTTPProvider(provider)):
            return network_provider


def fetch_redemption_rate():
    trove_manager = w3.eth.contract(address="0xCD413fC3347cE295fc5DB3099839a203d8c2E6D9", abi=abis.trove_manager())
    return trove_manager.functions.getRedemptionRate().call() 


def fetch_oracle_price():
    price_feed = w3.eth.contract(address="0x5d377B319d9E343B8c547160936eBb870036e867", abi=abis.price_feed())
    return price_feed.functions.fetchPrice().call()

w3 = check_provider(rpcs)

price = fetch_oracle_price() / DECIMAL_PRECISION
collateral_withdrawn = USDM_TO_WITHDRAW / price

redemption_rate = fetch_redemption_rate()
redemptionFee = redemption_rate * collateral_withdrawn / DECIMAL_PRECISION
amount_out = collateral_withdrawn - redemptionFee

usdm_price = amount_out / collateral_withdrawn
print(usdm_price)
