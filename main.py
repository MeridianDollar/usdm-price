import abis
from web3 import Web3

DECIMAL_PRECISION = 1e18
USDM_TO_WITHDRAW = 100

rpcs = [
    "https://mainnet.telos.net/evm",
    "https://api.kainosbp.com/evm",
    "https://rpc1.eu.telos.net/evm"]
        

def check_provider(network_providers):
    for provider in network_providers:
        if network_provider := Web3(Web3.HTTPProvider(provider)):
            return network_provider


def fetch_redemption_rate():
    trove_manager = w3.eth.contract(address="0xb1F92104E1Ad5Ed84592666EfB1eB52b946E6e68", abi=abis.trove_manager())
    return trove_manager.functions.getRedemptionRate().call() 


def fetch_oracle_price():
    price_feed = w3.eth.contract(address="0xE421fC686099C4Dec31c9D58B51DE9608665FBF2", abi=abis.price_feed())
    return price_feed.functions.fetchPrice().call()


network = "telos"
w3 = check_provider(rpcs)

price = fetch_oracle_price() / DECIMAL_PRECISION
tlos_withdrawn = USDM_TO_WITHDRAW / price

redemption_rate = fetch_redemption_rate()
redemptionFee = redemption_rate * tlos_withdrawn / DECIMAL_PRECISION
amount_out = tlos_withdrawn - redemptionFee

usdm_price = amount_out / tlos_withdrawn
print(usdm_price)
