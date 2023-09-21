class test:
    def __init__(self,  a) -> None:
        self.a = a

b = []
for i in range(10):
    b.append(test(i))
print(b)
c = b[0: 4] + [test(10)]
b[0].a = 10
print(c)
print(c[0].a)