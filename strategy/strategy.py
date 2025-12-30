class EMAStrategy:

    def __init__(self):
        # Initialization of EMA strategy with tracking for three moving averages
        self.prices = []
        self.ema_9 = None
        self.ema_44 = None
        self.ema_100 = None

    def eval(self, new_price):
        """
        Evaluating trading signal based on EMA crossover strategy
        
        Returns:
            tuple: (signal, quantity) where signal is "BUY", "EXIT", or "HOLD"
        """
        self.prices.append(new_price)

        # Storing previous EMA values for crossover detection
        ema_9_old = self.ema_9
        ema_44_old = self.ema_44
        ema_100_old = self.ema_100

        # Updating all EMAs
        self.ema_9 = self.EMA(9, self.ema_9, new_price)
        self.ema_44 = self.EMA(44, self.ema_44, new_price)
        self.ema_100 = self.EMA(100, self.ema_100, new_price)
        
        # Check to wait for sufficient data before generating signals
        if len(self.prices) < 100:
            return ("HOLD", 0)

        # Buy signal: price above EMA100 and EMA9 shows posetive crossover with respect to EMA44
        if new_price > self.ema_100 and self.ema_9 > self.ema_44 and ema_9_old <= ema_44_old:
            return ("BUY", 1)

        # Exit signal: price below EMA100 and EMA9 shows negetive crossover with respect to EMA44
        elif new_price < self.ema_100 and self.ema_9 < self.ema_44 and ema_9_old >= ema_44_old:
            return ("EXIT", 1)


        else:
            return ("HOLD", 0)

    def EMA(self, period, ema_old, new_price):
        """
        Calculation of exponential moving average.
        
        Args:
            period: EMA period
            ema_old: Previous EMA value (None if first calculation)
            new_price: Current price
            
        Returns:
            float: Updated EMA value or None if insufficient data
        """
        alpha = 2/(period+1)

        if ema_old is None:
            if len(self.prices) < period:
                return None
            # Return EMA = simple moving average if old EMA doesnt exist
            return sum(self.prices[-period:])/period
        
        return (alpha * new_price) + ((1-alpha) * ema_old)
            
