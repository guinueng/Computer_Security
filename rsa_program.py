import sys

def gcd(a, b): # Euclidean Algorithm to get gcd.
   if(b == 0):
      return a
   else:
      q = a % b
      rst = gcd(b, q)
      return rst

print (sys.argv)

if(sys.argv[1] == "–generate-key"):
   print("–generate-key case")
   if sys.argv[2] == "-p":
      p = int(sys.argv[3])
      q = int(sys.argv[5])
   
   if sys.argv[2] == "-q":
      q = int(sys.argv[3])
      p = int(sys.argv[5])

   # print(p, q)
 
   n = p * q
   phi = (p - 1) * (q - 1)
   gcd_rst = gcd(p, q)

   for e in range (2, phi):
      gcd_rst = gcd(phi, e)

      if(gcd_rst == 1):
            # print(e, "has gcd_rst = 1")
            a = phi
            b = e
            # s_1 = 1
            # s_2 = 0
            # t_1 = 0
            # t_2 = 1

            d = 2
            while(d < phi):
               if( (e * d) % phi == 1):
                  break               
               d += 1

            # while(b > 0): # Extended Euclidean Algorithm to get e, d values.
            # During usage of extended euclidean algorithm, example case does not worked.
            # Due to this problem, I decided to use brute-force algorithm.
            #    # print(b)
            #    q = a // b # quotient
            #    r = a % b # remainder
            #    a = b # update value.
            #    b = r
            # 
            #    s = s_1 - q * s_2 
            #    s_1 = s_2
            #    s_2 = s
            # 
            #    t = t_1 - q * t_2
            #    t_1 = t_2
            #    t_2 = t
            #    print(q, r, a, b, s_1, s_2, t_1, t_2)
            
            # k = s_1
            # d = t_1
            # print(e, d)

            if(d > 1 and d < phi):
               break

   print("RSA key pair generated:")
   print("n=", n)
   print("e=", e)
   print("d=", d)
   print("phi=",phi)

   pub = open("public_key.txt", "w")
   pri = open("private_key.txt", "w")

   pub_txt = "n=" + str(n) + "\ne=" + str(e)
   pri_txt = "n=" + str(n) + "\nd=" + str(d)
   pub.write(pub_txt)
   pri.write(pri_txt)

if(sys.argv[1] == "–encrypt"):

   print("–encrypt case")

if(sys.argv[1] == "–decrypt"):
   print("–decrypt case")

if(sys.argv[1] == "–sign"):
   print("–sign case")

if(sys.argv[1] == "–verify"):
   print("–verify case")