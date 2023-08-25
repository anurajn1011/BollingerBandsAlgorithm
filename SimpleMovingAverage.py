from linked_list import SLinkedList
import statistics

class SimpleMovingAverage:
    def __init__(self, days_of_average):
        self.days_of_average = days_of_average
        self.list = SLinkedList()
        self.current_close = 0
        self.closing_price_sum = 0
        self.moving_average = 0
        self.sd = 0
    #adds closing price of the new day; the tail will be the new day while the head is the earliest date
    def add_new_day(self, closing_price):
        if self.list.getLength() == self.days_of_average:
            removed_val = self.list.head.value
            self.list.remove(0)
            self.list.append(closing_price)
            self.current_close = closing_price
            self.closing_price_sum -= removed_val
            self.moving_average = self.closing_price_sum / self.days_of_average
            dataset = self.list.getNodes()
            self.sd = statistics.stdev(dataset)
        else:
            self.list.append(closing_price)
            self.current_close = closing_price
        self.closing_price_sum += closing_price
        return 0
    #Private; get moving average 
    def get_moving_average(self):
        return self.moving_average 
    #Private; get the standard deviation of the moving average
    def get_standard_deviation(self):
        return self.sd
    def get_current_close(self):
        return self.current_close
