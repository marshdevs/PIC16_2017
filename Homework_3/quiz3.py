import turtle as t

def threeqsq(n, L):
    if n == 0:
        t.done()
    else:
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        threeqsq(n-1, 3*float(L)/4.0)
        
def main():
    threeqsq(6, 100)    
    
if __name__ == "__main__": main()