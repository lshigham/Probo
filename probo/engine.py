import abc
import enum
import numpy as np
from numpy import matlib
from scipy.stats import binom, norm, mstats
from matplotlib.pyplot import *

class PricingEngine(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def calculate(self):
        """A method to implement a pricing model.  Called from Facade, passed through here.  instantiated in the specific Pricing Engines.
           The pricing method may be either an analytic model (i.e.
           Black-Scholes), a PDF solver such as the finite difference method,
           or a Monte Carlo pricing algorithm.
        """
        pass
        
class BinomialPricingEngine(PricingEngine):
    def __init__(self, steps, pricer):
        self.__steps = steps
        self.__pricer = pricer

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, new_steps):
        self.__steps = new_steps
    
    def calculate(self, option, data):
        return self.__pricer(self, option, data)

    
def EuropeanBinomialPricer(engine, option, data):
    """Price Engine for European Call and Put options via a binomial (tree) pricing method.
    Collecting inputs from option and data classes plus the inputs necessary to build tree."""
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    nodes = steps + 1
    delta_t = expiry / steps 
    u = np.exp((rate * delta_t) + volatility * np.sqrt(delta_t)) 
    d = np.exp((rate * delta_t) - volatility * np.sqrt(delta_t))
    pu = (np.exp(rate * delta_t) - d) / (u - d)
    pd = 1 - pu
    discount_rate = np.exp(-rate * expiry)
    spot_T = 0.0
    payoff_T = 0.0
    
    for i in range(nodes):
        spot_T = spot * (u ** (steps - i)) * (d ** (i))
        payoff_T += option.payoff(spot_T)  * binom.pmf(steps - i, steps, pu)  
    price = discount_rate * payoff_T 
     
    return price 


def AmericanBinomialPricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    nodes = steps + 1
    delta_t = expiry / steps
    discount_rate = np.exp(-rate * delta_t)
    u = np.exp((rate * delta_t) + volatility * np.sqrt(delta_t))
    d = np.exp((rate * delta_t) - volatility * np.sqrt(delta_t))
    pu = (np.exp(rate * delta_t) - d) / (u - d)
    pd = 1 - pu
    disc_pu = discount_rate * pu
    disc_pd = discount_rate * pd
    spot_t = np.zeros((nodes, ))
    payoff_t = np.zeros((nodes, ))
    
    for i in range(nodes):
        spot_t[i] = spot * (u ** (steps - i)) * (d ** i)
        payoff_t[i] = option.payoff(spot_t[i])

    """Backwards Recursion portion of the American Binomial Model"""
    for i in range((steps - 1), -1, -1):
        for j in range(i + 1):
            payoff_t[j] = disc_pu * payoff_t[j] + disc_pd * payoff_t[j+1]
            spot_t[j] = spot_t[j] / u
            payoff_t[j] = np.maximum(payoff_t[j], option.payoff(spot_t[j])) 
            
    price = payoff_t[0]
    return price


               
class BlackScholesPricingEngine(PricingEngine):
    def __init__(self, payoff_type, pricer):
        self.__payoff_type = payoff_type
        self.__pricer = pricer

    @property
    def payoff_type(self):
        return self.__payoff_type

    def calculate(self, option, data):
        return self.__pricer(self, option, data)

def BlackScholesPricer(pricing_engine, option, data):
    strike = option.strike
    expiry = option.expiry
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5 * volatility * volatility) * expiry) / (volatility * np.sqrt(expiry))
    d2 = d1 - volatility * np.sqrt(expiry) 

    if pricing_engine.payoff_type == "call":
        price = (spot * np.exp(-dividend * expiry) * norm.cdf(d1)) - (strike * np.exp(-rate * expiry) * norm.cdf(d2)) 
    elif pricing_engine.payoff_type == "put":
        price = (strike * np.exp(-rate * expiry) * norm.cdf(-d2)) - (spot * np.exp(-dividend * expiry) * norm.cdf(-d1))
    else:
        raise ValueError("You must pass either a call or a put option.")
    return price
    
    
    

class MonteCarloPricingEngine(PricingEngine):
    def __init__(self, replications, time_steps, pricer):
        self.__replications = replications
        self.__time_steps = time_steps
        self.__pricer = pricer

    @property
    def replications(self):
        return self.__replications

    @replications.setter
    def replications(self, new_replications):
        self.__replications = new_replications

    @property
    def time_steps(self):
        return self.__time_steps

    @time_steps.setter
    def time_steps(self, new_time_steps):
        self.__time_steps = new_time_steps
    
    def calculate(self, option, data):
        return self.__pricer(self, option, data)     
        
def Naive_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    time_steps = engine.time_steps
    replications = engine.replications
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry
    z = np.random.normal(size = replications)
    
    nudt = (rate - dividend - 0.5 * volatility * volatility) * expiry
    sidt = volatility * np.sqrt(expiry)
    
    spot_t = np.zeros((replications, ))
    payoff_t = np.zeros((replications, ))
    spot_t = spot * np.exp(nudt + sidt * z)
        
    payoff_t = option.payoff(spot_t)
    
    #title("Naive Monte Carlo")
    #hist(spot_t, bins=50)
    standard_error = payoff_t.std() / np.sqrt(replications)
    price = discount_rate * payoff_t.mean()
    print("The standard error for Naive Monte Carlo is: {}".format(standard_error))
    
    return price
    
def Stratified_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    time_steps = engine.time_steps
    replications = engine.replications
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry 
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)
    
    spot_t = np.zeros((replications, ))
    payoff_t = np.zeros((replications, ))
    
    """stratified portion"""
    for i in range(replications):
        u = np.random.uniform(size = 1)
        u_hat = (i + u) / replications
        z = norm.ppf(u_hat)
        spot_t[i] = spot * np.exp(nudt + sidt * z)
        payoff_t[i] = option.payoff(spot_t[i])
        
    price = discount_rate * payoff_t.mean()
    #title("Stratified Monte Carlo")
    #hist(spot_t, bins=50)
    standard_error = payoff_t.std(dtype = np.float64) / np.sqrt(replications)
    print("Standard error for the stratified Monte Carlo Call is: {0:3f}".format(standard_error))

    
    return price
    
def Antithetic_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()   
    time_steps = engine.time_steps
    replications = engine.replications
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry 
    z = np.random.normal(size = replications)
    z = np.concatenate((z, -z))

    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)    
    
    spot_t_antithetic = np.zeros((replications, ))
    payoff_t_antithetic = np.zeros((replications, ))
    for i in range(replications):
        spot_t_antithetic[i] = spot * np.exp(nudt + sidt * z[i])
        payoff_t_antithetic[i] = option.payoff(spot_t_antithetic[i])
    
    price = discount_rate * payoff_t_antithetic.mean()
    stderr = payoff_t_antithetic.std() / np.sqrt(replications)
    #title("Antithetic Monte Carlo")
    #hist(spot_t_antithetic, bins=50)
    print("The standard error for Antithetic Monte Carlo is: {}".format(stderr))
    
    return price

def BlackScholesDelta(spot, t, strike, expiry, volatility, rate, dividend):
    tau = expiry - t
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5 * volatility * volatility) * tau) / (volatility * np.sqrt(tau))
    BS_delta = np.exp(-dividend * tau) * norm.cdf(d1) 
    return BS_delta
    
def ControlVariatePricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    time_steps = engine.time_steps
    replications = engine.replications
    delta_t = expiry / time_steps    
    nudt = (rate - dividend - 0.5 * volatility * volatility) * delta_t
    sigsdt = volatility * np.sqrt(delta_t)
    erddt = np.exp((rate - dividend) * delta_t)    
    beta = -1.0
    cash_flow_t = np.zeros((replications, ))
    price = 0.0

    for j in range(replications):
        spot_t = spot
        convar = 0.0
        z = np.random.normal(size = replications)

        for i in range(int(time_steps)):
            t = i * delta_t
            BS_delta = BlackScholesDelta(spot, t, strike, expiry, volatility, rate, dividend)
            spot_tn = spot_t * np.exp(nudt + sigsdt * z[i])
            convar = convar + BS_delta * (spot_tn - spot_t * erddt)
            spot_t = spot_tn

        cash_flow_t[j] = option.payoff(spot_t) + beta * convar

    title("Control Variate Monte Carlo")
    hist(cash_flow_t, bins=50)
    price = np.exp(-rate * expiry) * cash_flow_t.mean()
    stderr = cash_flow_t.std() / np.sqrt(replications)
    print("The standard error for Control Variate Monte Carlo is: {}".format(stderr))
    return price


def GeometricAsian(spot, volatility, strike, rate, expiry, time_steps):
    vol_hat = volatility * np.sqrt((2.0 * time_steps + 1.0) / (6.0 * (time_steps + 1)))
    rho = 0.5 * (rate - 0.5 *(volatility * volatility) + vol_hat * vol_hat)
    d1 = (np.log(spot / strike) + (rho + 0.5 *vol_hat * vol_hat) * expiry) / (vol_hat * np.sqrt(expiry))
    d2 = d1 - volatility * np.sqrt(expiry)
    G_Asian = np.exp(-rate * expiry) * (spot * np.exp(rho * expiry) * norm.cdf(d1) - strike * norm.cdf(d2))
    return G_Asian
  

def Asian_Option_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    time_steps = engine.time_steps
    replications = engine.replications
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry / time_steps
    z = np.random.normal(size = (replications, ))
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)    

    """Path Dependent Portion"""
    expected_return = rate - 0.5 * (volatility * volatility)
    deterministic = np.matlib.repmat(expected_return * delta_t * time_steps, time_steps, 1)
    stochastic = volatility * np.sqrt(delta_t) * np.cumsum(z)
    spots = np.matlib.repmat(spot, 1, replications)
    sim_paths = spots * np.exp(deterministic + stochastic)

    spot_t = np.mean(sim_paths, 1)
    payoff_t = discount_rate * option.payoff(spot_t)
    convar = GeometricAsian(spot, volatility, strike, rate, expiry, time_steps)
    G_average = np.exp((1/(time_steps +1)) * np.sum(np.log(sim_paths),1))
    payoff_gavg = discount_rate * np.maximum(G_average - strike, 0)
    convar_price = payoff_t + convar - payoff_gavg

    price = np.mean(convar_price)
    stderr = np.std(convar_price)
    title("Geometric Asian Control Variate -- Arithmetic Asian Monte Carlo")    
    hist(z, bins=50)

    print("The standard error for Control Variate Monte Carlo simulation for an Arithmetic Asian Call option is: {}".format(stderr))
    
    return price
    
    
def Lookback_Option_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry
    z = np.random.normal(size = steps)
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)    
    
    spot_t = np.zeros((steps, ))
    payoff_t = np.zeros((steps, ))
    
    for i in range(steps):
        spot_t[i] = spot * nudt + sidt * z[i]
        payoff_t[i] = option.payoff(spot_t[i])
        
    price = discount_rate * payoff_t.max()   
    
    return price
