from threading import Thread


class RepeatedTimer(Thread):
    def __init__(self, event, interval, function, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def run(self):
        self.is_running = True
        while not self.stopped.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def cancel(self):
        self.stopped.set()
        self.is_running = False

