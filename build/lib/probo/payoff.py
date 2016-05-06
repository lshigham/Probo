import abc
from numpy import sqrt, maximum 


class Payoff(object, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def expiry(self):
        """Get the expiry date"""
        pass
        
    @expiry.setter
    @abc.abstractmethod
    def expiry(self, newExpiry):
        """Set the expiry date"""
        self.__expiry = newExpiry
        pass
    
    @abc.abstractmethod
    def payoff(self):
        pass
    
class VanillaPayoff(Payoff):
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
    return maximum(spot - option.strike, 0.0)

def put_payoff(option, spot):
    return maximum(option.strike - spot, 0.0)
    
    
class StrangePayoff(Payoff):
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
    
def sSquared_payoff(option, spot):
    return spot ** 2.0
    
def sSqrt_payoff(option, spot):
    return spot ** 0.5
    
def sFrac_payoff(option, spot):
    return spot ** -1.0
    
    # Needs edits 
#class Exotic_Payoff(Facade.OptionFacade):
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