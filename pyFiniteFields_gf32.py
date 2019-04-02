import string, random

letters = "".join(string.ascii_lowercase)
punctuation = " ?!@.,"
msgString = letters + punctuation  # Creates a string of all letters and punctuation
message = 'encrypt me' # Original Plaintext
decoded_string = []

# Adds two values
def GF32_add(b1,b2):
  x = int(b1,2)^int(b2,2)
  return(format(x,'05b'))

# Multiplies two values
def GF32_mult(b1,b2):
    x = format(int(b1,2), '05b')
    y='0'
    for i in range(5):
        if x[i] == '1':
            y=int(y)^(int(b2,2)<<(4-i))

    r=len(format(y,'b'))
    while r>5:
        y = y^(int('100101',2)<<(r-5-1))
        r=len(format(y,'b'))
    return(format(y,'05b'))

# Encodes a string into elements within GF(2^5)
def encode(message):
    encoded = ""
    for x in range(len(message)):
        for i in range(len(msgString)):
            if message[x] == msgString[i]:
                if i <= len(message)-1:
                    encoded += "0" + str(i)
                else:
                    encoded += str(i)
    return(encoded)

# Decodes the elements within GF(2^5) back to a string
def decode(message):
    temp_string = msgString[int(int(message,2))]
    decoded_string.append(temp_string)

# Multipacitive Inverse in GF(2^5)
def gf_invert(a, mod=0x25):
  v = mod
  g1 = 1
  g2 = 0
  j = gf_degree(a) - 5

  while (a != 1) :
    if (j < 0) :
      a, v = v, a
      g1, g2 = g2, g1
      j = -j

    a ^= v << j
    g1 ^= g2 << j

    a %= 32  # Emulating 5-bit overflow
    g1 %= 32 # Emulating 5-bit overflow

    j = gf_degree(a) - gf_degree(v)

  return g1

# Calculates the degree of the polynomial
def gf_degree(a):
  res = 0
  a >>= 1
  while (a != 0):
    a >>= 1;
    res += 1;
  return res

# Performs ElGamal Cryptosystem within GF(2^5)
def elgamal(message):
    p = '100101'
    g = '00010'
    x = random.randint(1, (int(p) - 1)) # Random value between 1 and p-1 (Private Key)
    y = g

    # y = (g ** x) mod p
    for i in range(int(x)):
        y = GF32_mult(g,y)

    # Bob's public key is [P,G,Y]
    encoded_message = encode(message)
    m = bin(int(encoded_message)) # Message converted to binary

    # Alice selects k, and calulcates a & b (c1, c2)
    k = random.randint(1, (int(p) - 1)) # Random value between 1 and p-1
    # a = (g ** k) mod p
    a = '10'
    for i in range(k):
        a = GF32_mult(g,a)

    # Bob decrypts the message
    b = y
    # b = ((y ** k) * m) mod p
    for i in range(k):
        b = GF32_mult(y,b)
    b = GF32_mult(b,m)
    print('c1: ',a,'c2: ',b)

    # clear_text = b / (a**x) mod p
    temp_a = a
    for i in range(x):
        a = GF32_mult(temp_a,a)
    inv = gf_invert(int(int(a,2)))
    clear_text = GF32_mult(bin(inv),b)
    print('Plain Text Letter in binary: ',clear_text)
    decode(clear_text)

# Start of main

print('Original Message: ',message)
print('************************************')

for i in range(len(message)):
    elgamal(message[i])

print('************************************')
print('Decrypted Message: ')
print(''.join(decoded_string))
