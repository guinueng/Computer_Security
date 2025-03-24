import sys

def gcd(a, b):
    print(a, b)
    if(b == 0):
       return a
    else:
        q = a % b
        gcd(b, q)

print (sys.argv)

if(sys.argv[1] == "–generate-key"):
    print("–generate-key case")
    if sys.argv[2] == "-p":
      p = int(sys.argv[3])
      q = int(sys.argv[5])
    
    if sys.argv[2] == "-q":
      q = int(sys.argv[3])
      p = int(sys.argv[5])

    print(p, q)
    
    n = p * q
    phi = (p - 1) * (q - 1)

    gcd = gcd(p, q)
    print(gcd)
    for i in range (2, n):
       gcd_rst = gcd(phi, i)
       if(gcd_rst == 1):
            



    print("RSA key pair generated:")
    print("n=", n)
    print("e=", e)
    print("d=", d)
    print("phi=",phi)

if(sys.argv[1] == "–encrypt"):
   print("–encrypt case")

if(sys.argv[1] == "–decrypt"):
   print("–decrypt case")

if(sys.argv[1] == "–sign"):
   print("–sign case")

if(sys.argv[1] == "–verify"):
   print("–verify case")