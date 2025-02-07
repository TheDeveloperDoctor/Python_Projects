def swap_num(a,b):
    a = a+b
    b = a-b
    a = a-b
    return(a,b)


print(swap_num(5,4))