from probo.marketdata import MarketData
from probo.payoff import VanillaPayoff, call_payoff
from probo.engine import BinomialPricingEngine, AmericanBinomialPricer
from probo.facade import OptionFacade


def main():
    strike = 40.0
    expiry = 0.25 
    
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    steps = 3 

    the_call = VanillaPayoff(expiry, strike, call_payoff)
    the_data = MarketData(rate, spot, volatility, dividend)
    A_binom_engine = BinomialPricingEngine(steps, AmericanBinomialPricer)
    
    the_option = OptionFacade(the_call, A_binom_engine, the_data)
    price = the_option.price()
    print("The call price is {0:.3f}".format(price))
    
if __name__ == "__main__":
    main()

