class Engine:
    def __init__(self):
        self.in_position = False

    def exec (self, signal, qty):
        if signal == "BUY" and not self.in_position:
            self.placeOrder(qty)
            self.in_position = True

        elif signal == "EXIT" and self.in_position:
            self.closeOrder(qty)
            self.in_position = False

    def placeOrder (self,qty):
        print(f"Placing Order for {qty} quantity")

    def closeOrder (self,qty):
        print(f"Closing Order for {qty} quantity")
