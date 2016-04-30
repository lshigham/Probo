import abc

class OptionFacade(object, metaclass=abc.ABCMeta):
    """An option. -- Using Facade design pattern.  This instantiates the price method for the price engine.
    Also requires a payoff method to be used.  Requires an option, a pricing engine, and the data.

    """

    @property
    @abc.abstractmethod
    def expiry(self):
        """Get the expiry date."""
        pass

    @expiry.setter
    @abc.abstractmethod
    def expiry(self, newExpiry):
        """Set the expiry date."""
        pass
    
    @abc.abstractmethod
    def payoff(self):
        """Get the option's payoff value."""
        pass

    def __init__(self, option, engine, data):
        self.option = option
        self.engine = engine
        self.data = data


    def price(self):
        return self.engine.calculate(self.option, self.data)
        
      



        
