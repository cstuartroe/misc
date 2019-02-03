def increment(x,y = None):
    if type(x) == int:
        x += 1
    elif type(x) == list:
        if y is None:
            x[0] += 1
        elif type(y) == list:
            x[0] += 1
            y[0] += 1

num1 = [5]
increment(num1)
print(num1[0])

num2 = 5
increment(num2)
print(num2)

increment(num1[0])
print(num1[0])

num3 = [5]
increment(num1,num3)
print(num1[0])
print(num3[0])

increment(num1,num1)
print(num1[0])

num3 = num1
increment(num3)
print(num1[0])
print(num3[0])

increment(num1,num3)
print(num1[0])
print(num3[0])
