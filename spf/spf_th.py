from threading import Thread, Semaphore


class SPFThread(Thread):
    def __init__(self, target, args):
        super(SPFThread, self).__init__(target=target, args=args)
        self._target = target
        self._args = args
        self._result = None

    def run(self):
        self._result = self._target(*self._args)

    def getResult(self):
        return self._result


class SPFSemaphore(Semaphore):
    def getValue(self):
        return self._value
