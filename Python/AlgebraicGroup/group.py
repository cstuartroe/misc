def modexp(base,exp,mod):
    total = 1
    while exp > 0:
        if exp%2 == 0:
            base = base*base%mod
            exp = exp//2
        else:
            total = total*base%mod
            exp = exp - 1
    return total

def op(x,y,e):
    z = modexp(2*x+1,2*y+1,2**(e+1))
    return (z-1)//2

def table(e):
    w = len(str(2**e))+1
    
    heads = [str(i).ljust(w,' ') for i in range(2**e)]
    
    print(''.join(heads))
    
    print('#'*(w*2**e + 1))
    
    for row in range(2**e):
        line = " "*w*0
        
        for col in range(0,2**e):
            line += str(op(row,col,e)).ljust(w,' ')

        line += '# ' + str(row)
        print(line)

table(4)
