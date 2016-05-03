import numpy as np
from scipy.stats import norm
import Facade

class Vanilla_Payoff(Facade.OptionFacade):
    def __init__(self, expiry, strike, payoff):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff
        
    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry
    
    @property 
    def strike(self):
        return self.__strike
    
    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike

    def payoff(self, spot):
        return self.__payoff(self, spot)
    
def call_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0)

def put_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0)
    
class BS_Payoff(Facade.OptionFacade):
    def __init__(self, expiry, strike, dividend, rate, volatility, payoff):
        self.__expiry = expiry
        self.__strike = strike
        self.__dividend = dividend
        self.__rate = rate
        self.__volatility = volatility
        self.__payoff = payoff
        
    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry
    
    @property 
    def strike(self):
        return self.__strike
    
    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike
        
    @property 
    def dividend(self):
        return self.__dividend
    
    @dividend.setter
    def dividend(self, new_dividend):
        self.__dividend = new_dividend
        
    @property 
    def rate(self):
        return self.__rate
    
    @rate.setter
    def rate(self, new_rate):
        self.__rate = new_rate
        
    @property 
    def volatility(self):
        return self.__volatility
    
    @volatility.setter
    def volatility(self, new_volatility):
        self.__volatility = new_volatility

    def payoff(self, engine, spot):
        return self.__payoff(self, engine, spot)
    
def bs_call_payoff(option, engine, spot):
    return spot * np.exp(-engine.dividend * engine.expiry) * norm.cdf(engine.d1) - option.strike * np.exp(-engine.rate * engine.expiry) * norm.cdf(engine.d2)

def bs_put_payoff(option, engine, spot):
    return option.strike * np.exp(-engine.rate * engine.expiry) * norm.cdf(-engine.d2) - spot * np.exp(-engine.dividend * engine.expiry) * norm.cdf(-engine.d1) 

class Exotic_Payoff(Facade.OptionFacade):
    def __init__(self, expiry, strike, payoff):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff
        
    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry
    
    @property 
    def strike(self):
        return self.__strike
    
    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike

    def payoff(self, spot):
        return self.__payoff(self, spot)
        
def arithmetic_asian_call_payoff(option, spot):
    pass

def arithmetic_asian_put_payoff(option, spot):
    pass