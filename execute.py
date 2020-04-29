from market_maker import main

class Execute():
    def __init__(self):
        print("====execute.py start====")
        print("====market_maker/high_frequency_trade_bot start====")

    def run(self):
        main.Main()
        
    def test(self):
        from market_maker.auth import AccessTokenAuth

if __name__ == "__main__":
    my_execute = Execute()
    my_execute.run()
    # my_execute.test()
