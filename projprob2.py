from probo.marketdata import *
from probo.payoff import *
from probo.engine import *
from probo.facade import *


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
    replications = 100
    
    the_data = MarketData(rate, spot, volatility, dividend)

    the_call = StrangePayoff(expiry, strike, sSquared_payoff)
    the_call2 = StrangePayoff(expiry, strike, sSqrt_payoff)
    the_call3 = StrangePayoff(expiry, strike, sFrac_payoff)

    """Naive Monte Carlo"""    

    mc_engine = MonteCarloPricingEngine(time_steps, replications, Naive_Monte_Carlo_Pricer)
    mc_option = OptionFacade(the_call, mc_engine, the_data)
    MC_price = mc_option.price()
    print("The Naive Monte Carlo Call Price for S squared is {0:.3f}".format(MC_price))
    
    mc2_engine = MonteCarloPricingEngine(time_steps, replications, Naive_Monte_Carlo_Pricer)
    mc_option2 = OptionFacade(the_call2, mc2_engine, the_data)
    MC_price2 = mc_option2.price()
    print("The Naive Monte Carlo Call Price for square root of S is {0:.3f}".format(MC_price2))
    
    mc3_engine = MonteCarloPricingEngine(time_steps, replications, Naive_Monte_Carlo_Pricer)
    mc_option3 = OptionFacade(the_call3, mc3_engine, the_data)
    MC_price3 = mc_option3.price()
    print("The Naive Monte Carlo Call Price for 1/S is {0:.3f}".format(MC_price3))
    
    """Antithetic Monte Carlo"""
    anti_mc_engine = MonteCarloPricingEngine(time_steps, replications, Antithetic_Monte_Carlo_Pricer)
    anti_option = OptionFacade(the_call, anti_mc_engine, the_data)
    anti_price = anti_option.price()
    print("The Antithetic Monte Carlo Call Price is {0:.3f}".format(anti_price))
    
    anti_mc2_engine = MonteCarloPricingEngine(time_steps, replications, Antithetic_Monte_Carlo_Pricer)
    anti_option2 = OptionFacade(the_call2, anti_mc2_engine, the_data)
    anti_price2 = anti_option2.price()
    print("The Antithetic Monte Carlo Call Price is {0:.3f}".format(anti_price2))
    
    anti_mc3_engine = MonteCarloPricingEngine(time_steps, replications, Antithetic_Monte_Carlo_Pricer)
    anti_option3 = OptionFacade(the_call3, anti_mc3_engine, the_data)
    anti_price3 = anti_option3.price()
    print("The Antithetic Monte Carlo Call Price is {0:.3f}".format(anti_price3))
    
    """Stratified Monte Carlo"""
    strat_mc_engine = MonteCarloPricingEngine(time_steps, replications, Stratified_Monte_Carlo_Pricer)
    strat_option = OptionFacade(the_call, strat_mc_engine, the_data)
    strat_price = strat_option.price()
    print("The Stratified Monte Carlo Call Price is {0:.3f}".format(strat_price))
    
    strat_mc_engine2 = MonteCarloPricingEngine(time_steps, replications, Stratified_Monte_Carlo_Pricer)
    strat_option2 = OptionFacade(the_call2, strat_mc_engine2, the_data)
    strat_price2 = strat_option2.price()
    print("The Stratified Monte Carlo Call Price is {0:.3f}".format(strat_price2))
    
    strat_mc_engine3 = MonteCarloPricingEngine(time_steps, replications, Stratified_Monte_Carlo_Pricer)
    strat_option3 = OptionFacade(the_call3, strat_mc_engine3, the_data)
    strat_price3 = strat_option3.price()
    print("The Stratified Monte Carlo Call Price is {0:.3f}".format(strat_price3))

if __name__ == "__main__":
    main()