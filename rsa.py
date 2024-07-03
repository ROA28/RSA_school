import numpy
import random
import sympy

message = input("Input message: ")
o_bytes = message.encode('utf-8')
o_int = int.from_bytes(o_bytes, 'little')

roll = random.SystemRandom()

def prime_test(n, a):
  exp = n - 1
  while not exp & 1:
    exp >>= 1
  if pow(a, exp, n) == 1:
    return True
  while exp < n - 1:
    if pow(a, exp, n) == n - 1:
      return True
    else:
      exp <<= 1
  return False

def miller_rabin(n, k = 40):
  for _ in range(k):
    a = roll.randrange(2,n-1)
    if not prime_test(n, a):
      return False
  return True

def prime_candidate(bit_length):
  p = random.getrandbits(bit_length)
  p |= 1
  return p

def prime_generator(bit_length):
  p = 6
  while not miller_rabin(p):
    p = prime_candidate(bit_length)
  return p

p = prime_generator(1024)
q = prime_generator(1024)
n = p * q
phi_n = (p-1)*(q-1)
e = 65537
d = sympy.mod_inverse(e, phi_n)

encoded_int = pow(o_int, e, n)
decoded_int = pow(encoded_int, d, n)

decoded_bytes = decoded_int.to_bytes((decoded_int.bit_length() + 7) // 8, 'little')
decoded_message = decoded_bytes.decode('utf-8')
