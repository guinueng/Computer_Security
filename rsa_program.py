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
   # Get required file name on argv.
   # Reference: https://wikidocs.net/26
   if sys.argv[2] == "--p":
      p = int(sys.argv[3])
      q = int(sys.argv[5])
   
   if sys.argv[2] == "--q":
      q = int(sys.argv[3])
      p = int(sys.argv[5])
 
   # Calculate n, phi.
   n = p * q
   phi = (p - 1) * (q - 1)

   # Finding e by using property of 1 < e < phi and gcd(phi, e) == 1.
   for e in range (2, phi):
      gcd_rst = gcd(phi, e)

      # If found candidate e,
      if(gcd_rst == 1):
            a = phi
            b = e

            # Find candidate d by checking e*d mod phi == 1.
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
            #
            # k = s_1
            # d = t_1

            # If proper d is found(1 < d < phi and e*d mod phi == 1), break function and print result.
            if(d > 1 and d < phi):
               break

   # Print calculated result.
   # By using {0} and .format, we can print decimal and string together.
   # Reference: https://wikidocs.net/164969
   print("RSA key pair generated:")
   print("n={0}".format(n))
   print("e={0}".format(e))
   print("d={0}".format(d))
   print("phi={0}".format(phi))

   pub = open("public_key.txt", "w")   # Print result into screen and file.
   pri = open("private_key.txt", "w")

   # Concat n and e into two line and write it into public_key.txt file.
   pub_txt = "n=" + str(n) + "\ne=" + str(e)
   pub.write(pub_txt)

   # Concat n and d into two line and write it into private_key.txt file.
   pri_txt = "n=" + str(n) + "\nd=" + str(d)   
   pri.write(pri_txt)

   # Close public_key.txt and private_key.txt file.
   pub.close()
   pri.close()

if(sys.argv[1] == "--encrypt"):
   # Get required file name on argv.
   p_txt_name = sys.argv[2]
   pub_key_name = sys.argv[4]
   c_txt_name = sys.argv[6]

   # Open required files.
   p_txt_file = open(p_txt_name, "r")
   pub_key_file = open(pub_key_name, "r")
   c_txt_file = open(c_txt_name, "w")

   # Read plain text and public_key file.
   p_txt = p_txt_file.read()
   pub_key_txt = pub_key_file.read()

   c_txt = ""
   n = ""
   e = ""

   # Parsing n and d into given public_key.txt file.
   e_line = False
   for i in pub_key_txt:
      if(i == "\n"):
         e_line = True
         continue

      if(not(e_line)):
         if(i != "n" and i != "="):
            n += i
      else:
         if(i != "e" and i != "="):
            e += i

   # Conv parsed n and e str to int.
   n = int(n)
   e = int(e)

   for i in p_txt:
      t_str = ord(i)   # ord function converts input character into corresponding ascii.
      # Reference: https://www.quora.com/How-do-you-convert-ascii-to-integer-in-Python
      c_txt += (str(hex(rsa(t_str, e, n))) + " ")

   # Delete unnecessary space in last of cipher text.
   c_txt = c_txt[:-1]

    # Print calculated cipher text result and write it into ciphertext.txt file.
   print("Ciphertext:", c_txt) 
   c_txt_file.write(c_txt)

   p_txt_file.close()
   pub_key_file.close()
   c_txt_file.close()

if(sys.argv[1] == "--decrypt"):
   # Get required file name on argv.
   c_txt_name = sys.argv[2]
   pri_key_name = sys.argv[4]
   p_txt_name = sys.argv[6]

   # Open required files.
   c_txt_file = open(c_txt_name, "r")
   pri_key_file = open(pri_key_name, "r")
   p_txt_file = open(p_txt_name, "w")

   # Read plain text and public_key file.
   c_txt = c_txt_file.read()
   pri_key_txt = pri_key_file.read()

   # Add space on last part of cipher text to be sure calculate last hex number into text.
   c_txt += " "
   p_txt = ""
   n = ""
   d = ""

   # Parsing n and e into given public_key.txt file.
   d_line = False
   for i in pri_key_txt:
      if(i == "\n"):
         d_line = True
         continue

      if(not(d_line)):
         if(i != "n" and i != "="):
            n += i
      else:
         if(i != "d" and i != "="):
            d += i

   # Conv parsed n and e str to int.
   n = int(n)
   d = int(d)

   print(c_txt)

   tmp_str = ""
   for i in c_txt:
      if(i == " "):  # If space occur, calculate hex part of cipher text into corresponding plain text.
         t_str = int(tmp_str, 16)
         p_txt += str(chr(rsa(t_str, d, n)))
         tmp_str = ""   # And need to flush tmp_str buffer to store new hex number.
      else: # If before space part, collect chunk of hex number due to hex number is saved in string manner.
         tmp_str += i

   # Print calculated plain text and save it into plaintext.txt file.
   print("Decrypted plaintext:",p_txt)
   p_txt_file.write(p_txt)

   # Close public_key.txt and private_key.txt file.
   c_txt_file.close()
   pri_key_file.close()
   p_txt_file.close()

if(sys.argv[1] == "--sign"):
   print("-–sign case")
   sign = sys.argv[2]   # Get required file name on argv.
   pri_key_name = sys.argv[4]
   sign_txt_name = sys.argv[6]

   print(sign, pri_key_name, sign_txt_name)

   # Open required files.
   pri_key_file = open(pri_key_name, "r")
   sign_txt_file = open(sign_txt_name, "w")




   # Close public_key.txt and private_key.txt file.
   sign.close()
   pri_key_name.close()
   p_txt_file.close()

if(sys.argv[1] == "--verify"):
   print("-–verify case")

# –