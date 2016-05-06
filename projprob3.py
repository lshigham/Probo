from probo.marketdata import MarketData
from probo.payoff import *
from probo.engine import *
from probo.facade import OptionFacade

def main():
    """Set up the option!"""
    strike = 40.0
    expiry = .25 
    
    """Set up the Market Data!"""
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    
    """Set up the Pricing Engine!"""
    time_steps = 50
    replications =100
    
    call = ExoticPayoff(expiry, strike, arithmetic_asian_call_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    
    Arithmetic_A_engine = MonteCarloPricingEngine(time_steps, replications, Asian_Option_Pricer)
    AA_option = OptionFacade(call, Arithmetic_A_engine, data)
    AA_price = AA_option.price()
    print("The call price for an Arithmetic Asian Call Option using a Geometric Asian control Variate is:  {0:.3f}".format(AA_price))
    
if __name__ == "__main__":
    main()