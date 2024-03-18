import random
import math

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(n, k=5):
    """Miller-Rabin primality test"""
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Write n as (2^r)*d + 1
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bit_length):
    """Generate a large prime number"""
    while True:
        prime_candidate = random.randint(2**(bit_length-1), 2**bit_length - 1)
        if is_prime(prime_candidate):
            return prime_candidate

def powmod(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def key_gen(bit_length):
    """Generate RSA key pair"""
    # Choose two large prime numbers (p and q)
    p = generate_large_prime(bit_length)
    q = generate_large_prime(bit_length)

    # Calculate n and m
    n = p * q
    m = (p - 1) * (q - 1)

    # Choose a specific value for e
    e = 65537

    # Determine d such that (e * d) mod m = 1
    d = powmod(e, -1, m)

    # Return the public and private keys
    return (e, n), (d, n)

def encrypt(message, public_key):
    """Encrypt a message using RSA"""
    e, n = public_key
    return powmod(message, e, n)

def decrypt(ciphertext, private_key):
    """Decrypt a ciphertext using RSA"""
    d, n = private_key
    return powmod(ciphertext, d, n)

# Example usage
bit_length = 1024  # Adjust this based on desired key size
public_key, private_key = key_gen(bit_length)
message = 42
ciphertext = encrypt(message, public_key)
decrypted_message = decrypt(ciphertext, private_key)

print("Decrypted Message:", decrypted_message)
