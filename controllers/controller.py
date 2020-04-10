
class Controller:
    
    def __init__(self, wp):

        self.wp = wp

    def __call__(self, *args, **kwargs):
        print("class called")
        self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        pass

    def on_init(self):
        pass

    def on_calc_ready(self):
        pass

    def on_results_ready(self):
        pass

    def update(self):
        pass
