class Strategy:
    def __init__(self, short_open, short_close, long_open, long_close):
        self.short_open = short_open
        self.short_close = short_close
        self.long_open = long_open
        self.long_close = long_close

    def entryRule (self):
        if self.short_close > self.short_open and self.long_close > self.long_open:
            return ("BUY", 1)

        else:
            return ("HOLD", 0)
    
    def exitRule (self):
        if self.short_close < self.short_open:
            return ("EXIT", 1)

        else:
            return ("HOLD", 0)
