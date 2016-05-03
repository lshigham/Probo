import abc
import numpy as np
from scipy.stats import binom, norm
import Facade

class Pricing_Engine(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def calculate(self):
        """A method to implement a pricing model.
           The pricing method may be either an analytic model (i.e.
           Black-Scholes), a PDF solver such as the finite difference method,
           or a Monte Carlo pricing algorithm.
        """
        pass
        
class BinomialPricingEngine(Pricing_Engine):
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
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    nodes = steps + 1
    dt = expiry / steps 
    u = np.exp((rate * dt) + volatility * np.sqrt(dt)) 
    d = np.exp((rate * dt) - volatility * np.sqrt(dt))
    pu = (np.exp(rate * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-rate * expiry)
    spotT = 0.0
    payoffT = 0.0
    
    for i in range(nodes):
        spotT = spot * (u ** (steps - i)) * (d ** (i))
        payoffT += option.payoff(spotT)  * binom.pmf(steps - i, steps, pu)  
    price = disc * payoffT 
     
    return price 


# Need to fix bugs
def AmericanBinomialPricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    #nodes = steps + 1
    delta_t = expiry / steps
    discount_rate = np.exp(-rate * delta_t)
    u = np.exp((rate * delta_t) + volatility * np.sqrt(delta_t))
    d = np.exp((rate * delta_t) - volatility * np.sqrt(delta_t))
    pu = (np.exp(rate * delta_t) - d) / (u - d)
    pd = 1 - pu
    spot_t = []
    payoff_t = []
    
    for i in range(steps+1):
        spot_t.append(spot * (u ** (steps - i)) * (d ** i))
        
    for j in range(steps+1):
        payoff_t.append(option.payoff(spot_t[j]))

    payoff_tree = np.zeros([steps+1,steps+1])
    payoff_tree[:,-1] = payoff_t    
    for i in range(steps-1,-1,-1):
        for j in range(i+1):
            payoff_tree[j,i] = (payoff_tree[j,i+1]*pu+payoff_tree[j+1,i+1]*pd)*discount_rate
            payoff_tree[j,i] = np.maximum( payoff_tree[j,i], option.payoff(spot*(u**(i-j)*(d**(j)))))

    price = payoff_tree[0,0]  
    return price
      
class BlackScholesPricingEngine(Pricing_Engine):
    def __init__(self, pricer):
        self.__pricer = pricer
   
    def calculate(self, option, data):
        return self.__pricer(self, option, data)

# Need to fix bugs
def Black_Scholes_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5 * volatility * volatility) * expiry) / (volatility * np.sqrt(expiry))
    d2 = d1 - volatility * np.sqrt(expiry)
    price = option.payoff(spot, rate, volatility, dividend, d1, d2)
    return price
    
class MonteCarloPricingEngine(Pricing_Engine):
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
    discount_rate = np.exp(rate * expiry)
    delta_t = expiry / engine.time_steps
    z = np.random.normal(size = time_steps)
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)
    
    spot_t = np.zeros((engine.replications, ))
    payoff_t = np.zeros((engine.replications, ))
    spot_t = spot * np.exp(nudt + sidt * z)
    payoff_t = option.payoff(spot_t)
    price = discount_rate * payoff_t.mean()
    
    return price
    
def Stratified_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    time_steps = engine.time_steps
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry / time_steps
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)
    
    spot_t = np.zeros((engine.replications, ))
    payoff_t = np.zeros((engine.replications, ))
    
    for i in range(time_steps):
        u = np.random.uniform(size = 1)
        u_hat = (i + u) / time_steps
        z = norm.ppf(u_hat)
        spot_t[i] = spot * np.exp(nudt + sidt * z)
        payoff_t[i] = option.payoff(spot_t[i])
        
    price = discount_rate * payoff_t.mean()
    
    return price
    
def Antithetic_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()   
    time_steps = engine.time_steps
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry / time_steps
    z = np.random.normal(size = time_steps)
    z = np.concatenate((z, -z))

    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)    
    
    spot_t_antithetic = np.zeros((engine.replications, ))
    payoff_t_antithetic = np.zeros((engine.replications, ))
    spot_t_antithetic = spot * np.exp(nudt + sidt * z)
    payoff_t_antithetic = option.payoff(spot_t_antithetic)
    
    price = discount_rate * payoff_t_antithetic.mean()
    
    return price

def BlackScholesDelta(spot, t, strike, expiry, volatility, rate, dividend):
    tau = expiry - t
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5 * volatility * volatility) * tau) / (volatility * np.sqrt(tau))
    delta = np.exp(-dividend * tau) * norm.cdf(d1) 
    return delta
    
def ControlVariatePricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    dt = expiry / engine.time_steps
    nudt = (rate - dividend - 0.5 * volatility * volatility) * dt
    sigsdt = volatility * np.sqrt(dt)
    erddt = np.exp((rate - dividend) * dt)    
    beta = -1.0
    cash_flow_t = np.zeros((engine.replications, ))
    price = 0.0

    for j in range(engine.replications):
        spot_t = spot
        convar = 0.0
        z = np.random.normal(size=int(engine.time_steps))

        for i in range(int(engine.time_steps)):
            t = i * dt
            delta = BlackScholesDelta(spot, t, strike, expiry, volatility, rate, dividend)
            spot_tn = spot_t * np.exp(nudt + sigsdt * z[i])
            convar = convar + delta * (spot_tn - spot_t * erddt)
            spot_t = spot_tn

        cash_flow_t[j] = option.payoff(spot_t) + beta * convar

    price = np.exp(-rate * expiry) * cash_flow_t.mean()
    #stderr = cash_flow_t.std() / np.sqrt(engine.replications)
    return price

# Do I want to make a path dependent class?
# If so, what will I want to include?



##### Extensions  
  
def Asian_Option_Pricer(engine, option, data):
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
        spot_t[i] = spot_t[i-1] * nudt + sidt * z[i]
        payoff_t[i] = option.payoff(spot_t[i])
        
    price = discount_rate * payoff_t.mean()
    
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