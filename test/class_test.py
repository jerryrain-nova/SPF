class Father:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def run(self):
        print("a + b = ", self.a+self.b)


class Son(Father):
    def __init__(self, a, b, c):
        super(Son, self).__init__(a, b)
        self.c = c
        self.result = None

    def run(self):
        print("a * b + c = ", self.a*self.b+self.c)


if __name__ == '__main__':
    son1 = Son(2, 2, 1)
    son1.run()