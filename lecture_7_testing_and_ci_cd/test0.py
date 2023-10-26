from prime import is_prime

def test_is_prime(x, expected):
  if is_prime(x) != expected:
    print(f"ERROR: is_prime({x}) was not equal to {expected}")