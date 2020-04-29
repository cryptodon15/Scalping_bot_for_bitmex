import threading
import time
import datetime
from itertools import chain
from market_maker.utils import log, constants, errors, math
from market_maker import bitmex
from market_maker import settings
from market_maker import get_indicator

logger = log.setup_custom_logger('root')

class Main():
    def __init__(self, dry_run=False):
        print("====main.py start====")
        self.is_change_value=0
        self.my_elemensts = [self.is_change_value]
        self.dry_run = dry_run
        self.symbol = settings.SYMBOL
        self.bitmex = bitmex.BitMEX(base_url=settings.BASE_URL, symbol=self.symbol,
                                    apiKey=settings.API_KEY, apiSecret=settings.API_SECRET,
                                    orderIDPrefix=settings.ORDERID_PREFIX, postOnly=settings.POST_ONLY,
                                    timeout=settings.TIMEOUT)
        self.get_indicator = get_indicator.Get_Indicator()
        self.run()
    
    def cancel_all_orders(self):
        if self.dry_run:
            return

        logger.info("Resetting current position. Canceling all existing orders.")
        tickLog = self.get_instrument()['tickLog']
        orders = self.bitmex.http_open_orders()

        for order in orders:
            logger.info("Canceling: %s %d @ %.*f" % (order['side'], order['orderQty'], tickLog, order['price']))

        if len(orders):
            self.bitmex.cancel([order['orderID'] for order in orders])
        time.sleep(0.0001)
                
    def create_bulk_orders(self, orders):
        if self.dry_run:
            return orders
        return self.bitmex.create_bulk_orders(orders)
        # ticker = self.get_ticker()
        # return print(orders,ticker)
        
    def get_instrument(self, symbol=None):
        if symbol is None:
            symbol = self.symbol
        return self.bitmex.instrument(symbol)
        
    def get_ticker(self, symbol=None):
        if symbol is None:
            symbol = self.symbol
        self.instrument = self.get_instrument()
        ticker = self.bitmex.ticker_data(symbol)
        self.start_position_mid = ticker["mid"]
        return ticker
        
    def get_orders(self):
        if self.dry_run:
            return []
        return self.bitmex.open_orders()
    
    def switching(self, my_switch, arg):
        if my_switch:
            my_switch[1] = my_switch[0]
            my_switch[0] = arg
        else:
            my_switch.append(arg)
            my_switch.append(arg)

    def get_position(self, symbol=None):
        if symbol is None:
            symbol = self.symbol
        return self.bitmex.position(symbol)
        
    def func_order_strategy(self):
        prices = []
        order = {'price': 0, 'orderQty': 0, 'side': "Buy"}
        self.HL_band = self.get_HL_band()
        open_orders = self.get_orders
        while True:
            try:
                ticker = self.get_ticker()
                position = self.get_position()['currentQty']
                self.switching(prices, ticker['last'])
                # buy and exit
                if prices[1] <= self.HL_band[0] and prices[0] > self.HL_band[0]:
                    if position < settings.LOT:
                        orders = []
                        self.status = "buy"
                        self.cancel_all_orders()
                        ticker = self.get_ticker()
                        order['price'] = ticker['sell']
                        order['orderQty'] = -position + settings.LOT
                        order['side'] = "Buy"
                        orders.append(order.copy())
                        self.create_bulk_orders(orders)
                        time.sleep(1)
                if prices[1] >= self.HL_band[2] and prices[0] < self.HL_band[2]:
                    if self.status == "buy":
                        orders = []
                        self.status = "exit"
                        ticker = self.get_ticker()
                        order['price'] = ticker['buy']
                        order['orderQty'] = position
                        order['side'] = "Sell"
                        orders.append(order.copy())
                        self.create_bulk_orders(orders)
                        time.sleep(1)
                # sell and exit
                if prices[1] >= self.HL_band[1] and prices[0] < self.HL_band[1]:
                    if position > -settings.LOT:
                        orders = []
                        self.status = "sell"
                        self.cancel_all_orders()
                        ticker = self.get_ticker()
                        order['price'] = ticker['buy']
                        order['orderQty'] = -position - settings.LOT
                        order['side'] = "Sell"
                        orders.append(order.copy())
                        self.create_bulk_orders(orders)
                        time.sleep(1)
                if prices[1] <= self.HL_band[2] and prices[0] > self.HL_band[2]:
                    if self.status == "sell":
                        orders = []
                        self.status = "exit"
                        ticker = self.get_ticker()
                        order['price'] = ticker['sell']
                        order['orderQty'] = -position
                        order['side'] = "Buy"
                        orders.append(order.copy())
                        self.create_bulk_orders(orders)
                        time.sleep(1)
                # MM
                if prices[0] <= self.HL_band[0] and prices[0] >= self.HL_band[1]:
                    if self.status == "exit" or self.status == "init" or self.status == "mm":
                        orders = []
                        self.status = "mm"
                        print(prices)
                        ticker = self.get_ticker()
                        # import pdb; pdb.set_trace()
                        order['price'] = ticker['buy']
                        order['orderQty'] = settings.LOT
                        order['side'] = "Buy"
                        orders.append(order.copy())
                        ticker = self.get_ticker()
                        order['price'] = ticker['sell']
                        order['orderQty'] = settings.LOT
                        order['side'] = "Sell"
                        orders.append(order)
                        self.create_bulk_orders(orders)
                        time.sleep(5)
                if len(open_orders()) > 100:
                    time.sleep(10)
                if len(open_orders()) > 150:
                    time.sleep(15)
                if len(open_orders()) > 180:
                    time.sleep(20)
                if len(open_orders()) > 190:
                    time.sleep(25)
            except:
                print("restart!!")
                time.sleep(5)
                self.func_order_strategy()
                
    def get_HL_band(self):
        df_ohlcv = self.get_indicator.df_ohlcv(time_range=1, bar_no=500)
        df_hl = self.get_indicator.ta_hl(df_ohlcv, ma_range=15)
        H_band = df_hl[0].tail(1).values[0]
        L_band = df_hl[1].tail(1).values[0]
        M_band = (H_band + L_band)/2
        return (H_band.tolist() + L_band.tolist() + M_band.tolist())
    
    
    def func_get_HL_band(self):
        while True:
            self.HL_band = self.get_HL_band()
            time.sleep(60)
    
    def func_monitor(self):
        while True:
            ticker = self.get_ticker()
            open_orders = self.get_orders()
            date = datetime.datetime.now()
            position = self.get_position()['currentQty']
            print(date, ticker, self.status, self.HL_band, position, len(open_orders))
            time.sleep(1)

    def run(self):
        self.status = "init"
        self.orders = []
        self.HL_band = []
        self.thread_1 = threading.Thread(target=self.func_order_strategy)
        self.thread_2 = threading.Thread(target=self.func_get_HL_band)
        self.thread_3 = threading.Thread(target=self.func_monitor)

        self.thread_1.start()
        self.thread_2.start()
        self.thread_3.start()
