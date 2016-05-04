from probo.marketdata import MarketData
from probo.payoff import VanillaPayoff, call_payoff
from probo.engine import BinomialPricingEngine, EuropeanBinomialPricer, BlackScholesPricingEngine, BlackScholesPricer
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
    
    """Set up the European Binomial Pricing Engine!"""
    steps = 500 
    call = VanillaPayoff(expiry, strike, call_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    binom_engine = BinomialPricingEngine(steps, EuropeanBinomialPricer)
    
    """Calculate the Price"""
    the_option = OptionFacade(call, binom_engine, data)
    price = the_option.price()
    print("The European Binomial Call Price is {0:.3f}".format(price))
    
    """Set up Black Scholes Price!"""
    the_call = VanillaPayoff(expiry, strike, call_payoff)
    BS_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_option = OptionFacade(the_call, BS_engine, data)
    BS_price = BS_option.price()
    print("The call price via BLack Scholes is:  {0:.3f}".format(BS_price))
    
if __name__ == "__main__":
    main()
