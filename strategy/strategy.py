class EMAStrategy:

    def __init__(self):
        self.prices = []
        self.ema_9 = None
        self.ema_44 = None
        self.ema_100 = None

    def eval(self, new_price):
        self.prices.append(new_price)

        ema_9_old = self.ema_9
        ema_44_old = self.ema_44
        ema_100_old = self.ema_100

        self.ema_9 = self.EMA(9, self.ema_9, new_price)
        self.ema_44 = self.EMA(44, self.ema_44, new_price)
        self.ema_100 = self.EMA(100, self.ema_100, new_price)
        
        if len(self.prices) < 100:
            return ("HOLD", 0)

        if new_price > self.ema_100 and self.ema_9 > self.ema_44 and ema_9_old <= ema_44_old:
            return ("BUY", 1)
        elif new_price < self.ema_100 and self.ema_9 < self.ema_44 and ema_9_old >= ema_44_old:
            return ("EXIT", 1)
        else:
            return ("HOLD", 0)

    def EMA(self, period, ema_old, new_price):
        alpha = 2/(period+1)

        if ema_old is None:
            if len(self.prices) < period:
                return None
            return sum(self.prices[-period:])/period
        
        return (alpha * new_price) + ((1-alpha) * ema_old)
            
