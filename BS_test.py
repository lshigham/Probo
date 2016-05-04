from marketdata import MarketData
from payoff import VanillaPayoff, call_payoff
from engine import BlackScholesPricingEngine, BlackScholesPricer
from facade import OptionFacade

def main():
    """Set up the option!"""
    expiry = 0.25
    strike = 40.0
    
    """Set up the data!"""
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
 
    """set up the engine!"""
    #steps = 500 
    #type = "Put"


    bs_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    the_data = MarketData(rate, spot, volatility, dividend)
    the_call = VanillaPayoff(expiry, strike, call_payoff)
    option2 = OptionFacade(the_call, bs_engine, the_data)
    price2 = option2.price()
    print("The call price via Black-Scholes is: {0:.3f}".format(price2))
    
    
if __name__ == "__main__":
    main()