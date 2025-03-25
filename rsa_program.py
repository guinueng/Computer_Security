import sys

# Euclidean Algorithm to get gcd.
def gcd(a, b):
   # If base case(b = 0) occurs, return a which is gcd of first input.
   if(b == 0):
      return a
   else: # Else, pursue Euclidean Algorithm.
      q = a % b
      rst = gcd(b, q)
      return rst

# RSA function. Returns m^key mod n.
def rsa(msg, key, n):
   return (msg ** key) % n

def rsa_encrypt(p_txt, e, n):
   c_txt = ""

   for i in p_txt:
      t_str = ord(i)   # ord function converts input character into corresponding ascii.
      # Reference: https://www.quora.com/How-do-you-convert-ascii-to-integer-in-Python
      c_txt += (str(hex(rsa(t_str, e, n))) + " ")

   return c_txt

def rsa_decrypt(c_txt, d, n):
   p_txt = ""

   tmp_str = ""
   for i in c_txt:
      if(i == " "):  # If space occur, calculate hex part of cipher text into corresponding plain text.
         t_str = int(tmp_str, 16)
         p_txt += str(chr(rsa(t_str, d, n)))
         tmp_str = ""   # And need to flush tmp_str buffer to store new hex number.
      else: # If before space part, collect chunk of hex number due to hex number is saved in string manner.
         tmp_str += i

   return p_txt

if(sys.argv[1] == "--generate-key"):
   # Get required file name on argv.
   # Reference: https://wikidocs.net/26

   p = int(sys.argv[3])
   q = int(sys.argv[5])

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
            # # During usage of extended euclidean algorithm, example case does not worked.
            # # Due to this problem, I decided to use brute-force algorithm.
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

   # Concat n and e into two line and write it into public_key.txt file.
   pub_str = "n=" + str(n) + "\ne=" + str(e)
   pub_txt_file = open("public_key.txt", "w")
   pub_txt_file.write(pub_str)
   pub_txt_file.close()

   # Concat n and d into two line and write it into private_key.txt file.
   pri_str = "n=" + str(n) + "\nd=" + str(d)
   pri_txt_file = open("private_key.txt", "w")
   pri_txt_file.write(pri_str)
   pri_txt_file.close()

if(sys.argv[1] == "--encrypt"):
   # Get required file name on argv.
   p_txt_name = sys.argv[2]
   pub_key_name = sys.argv[4]
   c_txt_name = sys.argv[6]

   # Open, read and close plain text and public key file.
   p_txt_file = open(p_txt_name, "r")
   p_txt = p_txt_file.read()
   p_txt_file.close()

   pub_key_file = open(pub_key_name, "r")
   pub_key_txt = pub_key_file.read()
   pub_key_file.close()

   c_txt = ""
   n = ""
   e = ""

   # Parsing n and e into given public_key.txt file.
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

   # Encrypt plain text into cipher text by using rsa method.
   # Delete unnecessary space in last of cipher text.
   c_txt = rsa_encrypt(p_txt, int(e), int(n))[:-1]

   # Print converted cipher text result and write it into ciphertext.txt file.
   print("Ciphertext:", c_txt)
   c_txt_file = open(c_txt_name, "w")
   c_txt_file.write(c_txt)
   c_txt_file.close()

if(sys.argv[1] == "--decrypt"):
   # Get required file name on argv.
   c_txt_name = sys.argv[2]
   pri_key_name = sys.argv[4]
   p_txt_name = sys.argv[6]

   # Open, read, and close cipher text and private key files.
   c_txt_file = open(c_txt_name, "r")
   c_txt = c_txt_file.read()
   c_txt_file.close()

   pri_key_file = open(pri_key_name, "r")
   pri_key_txt = pri_key_file.read()
   pri_key_file.close()

   
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

   # Decrypt cipher text into plain text by using rsa method.
   p_txt = rsa_decrypt(c_txt, int(d), int(n))

   # Print converted plain text and save it into plaintext.txt file.
   print("Decrypted plaintext:", p_txt)
   p_txt_file = open(p_txt_name, "w")
   p_txt_file.write(p_txt)
   p_txt_file.close()

if(sys.argv[1] == "--sign"):
   # Get required file name on argv.
   sign = sys.argv[2]
   pri_key_name = sys.argv[4]
   sign_txt_name = sys.argv[6]

   # Open, read, and close required files.
   pri_key_file = open(pri_key_name, "r")
   pri_key_txt = pri_key_file.read()
   pri_key_file.close()

   n = ""
   d = ""

   # Parsing n and d into given private_key.txt file.
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

   # Encrypt signature text into cipher text by using rsa method.
   digi_sign = rsa_encrypt(sign, int(d), int(n))

   # Delete unnecessary space in last of signature text.
   digi_sign = digi_sign[:-1]

   # Print created digital signature result, open signature.txt,
   # write result into file, and close it.
   print("Signature:", digi_sign)
   sign_txt_file = open(sign_txt_name, "w")
   sign_txt_file.write(digi_sign)
   sign_txt_file.close()

if(sys.argv[1] == "--verify"):
   # Get required file name and string on argv.
   verify_str = sys.argv[2]
   sign_txt_name = sys.argv[4]
   pub_key_name = sys.argv[6]

   # Open, read and close signature file.
   sign_txt_file = open(sign_txt_name, "r")
   sign_txt = sign_txt_file.read()
   sign_txt_file.close()

   # Open, read and close public_key file.
   pub_key_file = open(pub_key_name, "r")
   pub_key_txt = pub_key_file.read()
   pub_key_file.close()

   # Add space on last part of signature text to be surely converted last hex number into text.
   sign_txt += " "
   n = ""
   e = ""

   # Parsing n and e into given public_key.txt file.
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

   compare_str = rsa_decrypt(sign_txt, int(e), int(n))

   if(verify_str == compare_str):
      print("Signature is valid")
   else:
      print("Signature is invalid")