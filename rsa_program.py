import sys

def gcd(a, b): # Euclidean Algorithm to get gcd.
   if(b == 0):
      return a
   else:
      q = a % b
      rst = gcd(b, q)
      return rst

def rsa(msg, key, n):
   return (msg ** key) % n

print(sys.argv)
print(sys.argv[1])

if(sys.argv[1] == "--generate-key"):
   print("-–generate-key case")
   if sys.argv[2] == "--p":   # Get required file name on argv.
      p = int(sys.argv[3])
      q = int(sys.argv[5])
   
   if sys.argv[2] == "--q":
      q = int(sys.argv[3])
      p = int(sys.argv[5])

   # print(p, q)
 
   n = p * q               # Calculate n, phi.
   phi = (p - 1) * (q - 1)
   # gcd_rst = gcd(p, q)

   for e in range (2, phi): # Finding e by using property of 1 < e < phi and gcd(phi, e) == 1.
      gcd_rst = gcd(phi, e)

      if(gcd_rst == 1): # If found candidate e,
            # print(e, "has gcd_rst = 1")
            a = phi
            b = e
            # s_1 = 1
            # s_2 = 0
            # t_1 = 0
            # t_2 = 1

            d = 2
            while(d < phi): # Find candidate d by checking e*d mod phi == 1.
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

            if(d > 1 and d < phi):  # If proper d is found(1 < d < phi and e*d mod phi == 1), break function and print result.
               break

   print("RSA key pair generated:")
   print("n=", n)
   print("e=", e)
   print("d=", d)
   print("phi=",phi)

   pub = open("public_key.txt", "w")   # Print result into screen and file.
   pri = open("private_key.txt", "w")

   pub_txt = "n=" + str(n) + "\ne=" + str(e)
   pri_txt = "n=" + str(n) + "\nd=" + str(d)
   pub.write(pub_txt)
   pri.write(pri_txt)

   pub.close()
   pri.close()

if(sys.argv[1] == "--encrypt"):
   print("--encrypt case")
   p_txt_name = sys.argv[2]   # Get required file name on argv.
   pub_key_name = sys.argv[4]
   c_txt_name = sys.argv[6]

   print(p_txt_name, pub_key_name, c_txt_name)

   p_txt_file = open(p_txt_name, "r")     # Open required files.
   pub_key_file = open(pub_key_name, "r")
   c_txt_file = open(c_txt_name, "w")

   p_txt = p_txt_file.read()
   pub_key_txt = pub_key_file.read()

   c_txt = ""
   n = ""
   e = ""

   e_line = False
   for i in pub_key_txt: # Parsing n and e into given public_key.txt file.
      if(i == "\n"):
         e_line = True
         continue

      if(not(e_line)):
         if(i != "n" and i != "="):
            n += i
      else:
         if(i != "e" and i != "="):
            e += i

   n = int(n)  # Conv parsed n and e str to int.
   e = int(e)

   for i in p_txt:
      t_str = ord(i)   # Need to find how to conv target str into ascii int value.
      c_txt += (hex(rsa(t_str, e, n)) + " ")

   c_txt = c_txt[:-1]
   print(c_txt)
   print(len(c_txt))
   # 0x43f 0xbff 0x755 0x755 0xc6f 0x469 0xad6 0x435 0x721 0x525 0x971

   c_txt_file.write(c_txt)

   p_txt_file.close()
   pub_key_file.close()
   c_txt_file.close()

if(sys.argv[1] == "-–decrypt"):
   print("-–decrypt case")

if(sys.argv[1] == "-–sign"):
   print("-–sign case")

if(sys.argv[1] == "-–verify"):
   print("-–verify case")

if(sys.argv[1] == "a"):
   print("test")