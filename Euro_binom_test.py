from marketdata import MarketData
from payoff import VanillaPayoff, call_payoff
from engine import BinomialPricingEngine, EuropeanBinomialPricer
from facade import OptionFacade

def main():
    strike = 40.0
    expiry = .25 
    
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    steps = 500 

    the_call = VanillaPayoff(expiry, strike, call_payoff)
    the_data = MarketData(rate, spot, volatility, dividend)
    binom_engine = BinomialPricingEngine(steps, EuropeanBinomialPricer)
    
    the_option = OptionFacade(the_call, binom_engine, the_data)
    price = the_option.price()
    print("The Call Price is {0:.3f}".format(price))
    
if __name__ == "__main__":
    main()
