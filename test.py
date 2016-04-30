#Edits needed
from probo.marketData import MarketData
from probo.payoff import VanillaPayoff, call_payoff
from probo.pricingEngine import BinomialPricingEngine, EuropeanBinomialPricer
from probo. import Facade


def main():
    strike = 40.0
    expiry = .25 
    
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    steps = 500 

    call = Vanilla_Payoff(expiry, strike, call_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    binom_engine = BinomialPricingEngine(steps, EuropeanBinomialPricer)
    
    the_option = OptionFacade(call, binom_engine, data)
    price = the_option.price()
    print("The Call Price is {0:.3f}".format(price))
    
if __name__ == "__main__":
    main()
