from marketdata import MarketData
from payoff import VanillaPayoff, call_payoff
from engine import MonteCarloPricingEngine, Antithetic_Monte_Carlo_Pricer
from facade import OptionFacade


def main():
    strike = 40.0
    expiry = .25 
    
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    time_steps = 100
    replications = 1000

    the_call = VanillaPayoff(expiry, strike, call_payoff)
    the_data = MarketData(rate, spot, volatility, dividend)
    anti_mc_engine = MonteCarloPricingEngine(time_steps, replications, Antithetic_Monte_Carlo_Pricer)
    
    the_option = OptionFacade(the_call, anti_mc_engine, the_data)
    price = the_option.price()
    print("The Call Price is {0:.3f}".format(price))
    
if __name__ == "__main__":
    main()
