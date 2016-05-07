from probo.marketdata import MarketData
from probo.payoff import VanillaPayoff, call_payoff
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
    time_steps = 10
    replications =1000
    
    call = VanillaPayoff(expiry, strike, call_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    
    """Set up Black Scholes Price!"""
    the_call = VanillaPayoff(expiry, strike, call_payoff)
    BS_engine = BlackScholesPricingEngine("call", BlackScholesPricer)
    BS_option = OptionFacade(the_call, BS_engine, data)
    BS_price = BS_option.price()
    print("The call price via BLack Scholes is:  {0:.3f}".format(BS_price))

    """Naive Monte Carlo"""    
    the_call = VanillaPayoff(expiry, strike, call_payoff)
    the_data = MarketData(rate, spot, volatility, dividend)
    mc_engine = MonteCarloPricingEngine(replications, time_steps, Naive_Monte_Carlo_Pricer)
    
    the_option = OptionFacade(the_call, mc_engine, the_data)
    MC_price = the_option.price()
    print("The Naive Monte Carlo Call Price is {0:.3f}".format(MC_price))
    
    """Antithetic Monte Carlo"""
    anti_mc_engine = MonteCarloPricingEngine(time_steps, replications, Antithetic_Monte_Carlo_Pricer)
    anti_option = OptionFacade(the_call, anti_mc_engine, the_data)
    anti_price = anti_option.price()
    print("The Antithetic Monte Carlo Call Price is {0:.3f}".format(anti_price))
    
    """Stratified Monte Carlo"""
    strat_mc_engine = MonteCarloPricingEngine(time_steps, replications, Stratified_Monte_Carlo_Pricer)
    strat_option = OptionFacade(the_call, strat_mc_engine, the_data)
    strat_price = strat_option.price()
    print("The Stratified Monte Carlo Call Price is {0:.3f}".format(strat_price))
    
    """Control Variate Monte Carlo"""
    convar_mc_engine = MonteCarloPricingEngine(time_steps, replications, ControlVariatePricer)
    convar_option = OptionFacade(the_call, convar_mc_engine, the_data)
    convar_price = convar_option.price()
    print("The Call Price via Control Variate Monte Carlo is {0:.3f}".format(convar_price))

    
if __name__ == "__main__":
    main()