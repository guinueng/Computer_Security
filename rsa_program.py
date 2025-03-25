import sys

def gcd(a, b): # Euclidean Algorithm to get gcd.
   if(b == 0): # If base case(b = 0) occurs, return a which is gcd of first input.
      return a
   else: # Else, pursue Euclidean Algorithm.
      q = a % b
      rst = gcd(b, q)
      return rst

def rsa(msg, key, n):   # RSA function. Returns m^key mod n.
   return (msg ** key) % n

print(sys.argv)
print(sys.argv[1])

if(sys.argv[1] == "--generate-key"):
   if sys.argv[2] == "--p":   # Get required file name on argv.
      # Reference: https://wikidocs.net/26
      p = int(sys.argv[3])
      q = int(sys.argv[5])
   
   if sys.argv[2] == "--q":
      q = int(sys.argv[3])
      p = int(sys.argv[5])
 
   n = p * q               # Calculate n, phi.
   phi = (p - 1) * (q - 1)
   # gcd_rst = gcd(p, q)

   for e in range (2, phi): # Finding e by using property of 1 < e < phi and gcd(phi, e) == 1.
      gcd_rst = gcd(phi, e)

      if(gcd_rst == 1): # If found candidate e,
            a = phi
            b = e

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
            #
            # k = s_1
            # d = t_1

            if(d > 1 and d < phi):  # If proper d is found(1 < d < phi and e*d mod phi == 1), break function and print result.
               break

   print("RSA key pair generated:")
   print("n={0}".format(n))         # By using {0} and .format, we can print decimal and string together.
   print("e={0}".format(e))         # Reference: https://wikidocs.net/164969
   print("d={0}".format(d))
   print("phi={0}".format(phi))

   pub = open("public_key.txt", "w")   # Print result into screen and file.
   pri = open("private_key.txt", "w")

   pub_txt = "n=" + str(n) + "\ne=" + str(e) # Concat n and e into two line.
   pri_txt = "n=" + str(n) + "\nd=" + str(d) # Concat n and d into two line.
   pub.write(pub_txt)   # Write public_key line into public_key.txt
   pri.write(pri_txt)   # Write public_key line into private_key.txt

   pub.close() # Close public_key.txt and private_key.txt file.
   pri.close()

if(sys.argv[1] == "--encrypt"):
   p_txt_name = sys.argv[2]   # Get required file name on argv.
   pub_key_name = sys.argv[4]
   c_txt_name = sys.argv[6]

   p_txt_file = open(p_txt_name, "r")     # Open required files.
   pub_key_file = open(pub_key_name, "r")
   c_txt_file = open(c_txt_name, "w")

   p_txt = p_txt_file.read()        # Read plain text and public_key fille
   pub_key_txt = pub_key_file.read()

   c_txt = ""
   n = ""
   e = ""

   e_line = False
   for i in pub_key_txt: # Parsing n and d into given public_key.txt file.
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
      t_str = ord(i)   # ord function converts input character into corresponding ascii.
      # Reference: https://www.quora.com/How-do-you-convert-ascii-to-integer-in-Python
      c_txt += (str(hex(rsa(t_str, e, n))) + " ")

   c_txt = c_txt[:-1]      # Delete unnecessary space in last of cipher text.
   print("Ciphertext:", c_txt)  # Print calculated cipher text result.
   c_txt_file.write(c_txt) # Write calculated cipher text into ciphertext.txt file.

   p_txt_file.close()
   pub_key_file.close()
   c_txt_file.close()

if(sys.argv[1] == "--decrypt"):
   print("-–decrypt case")
   c_txt_name = sys.argv[2]   # Get required file name on argv.
   pri_key_name = sys.argv[4]
   p_txt_name = sys.argv[6]

   print(c_txt_name, pri_key_name, p_txt_name)

   c_txt_file = open(c_txt_name, "r")     # Open required files.
   pri_key_file = open(pri_key_name, "r")
   p_txt_file = open(p_txt_name, "w")

   c_txt = c_txt_file.read()        # Read plain text and public_key fille
   pri_key_txt = pri_key_file.read()

   c_txt += " "
   p_txt = ""
   n = ""
   d = ""

   d_line = False
   for i in pri_key_txt: # Parsing n and e into given public_key.txt file.
      if(i == "\n"):
         d_line = True
         continue

      if(not(d_line)):
         if(i != "n" and i != "="):
            n += i
      else:
         if(i != "d" and i != "="):
            d += i

   n = int(n)  # Conv parsed n and e str to int.
   d = int(d)

   print(c_txt)

   tmp_str = ""
   tmp_num = 0
   for i in c_txt:
      if(i == " "):
         print(tmp_str)
         t_str = int(tmp_str, 16)
         print("conv hex:",hex(t_str))
         print(t_str)
         p_txt += str(chr(rsa(t_str, d, n)))
         print("rst:",str(chr(rsa(t_str, d, n))))
         tmp_str = ""
      else:
         tmp_str += i

   # p_txt = p_txt[:-1]
   print("Decrypted plaintext:",p_txt)
   print(len(p_txt))
   # Hello, RSA!

   p_txt_file.write(p_txt)

   c_txt_file.close()
   pri_key_file.close()
   p_txt_file.close()

if(sys.argv[1] == "-–sign"):
   print("-–sign case")

if(sys.argv[1] == "-–verify"):
   print("-–verify case")

# –