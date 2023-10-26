import unittest as u

from prime import is_prime

class Test(u.TestCase):
  def test_1(self):
    """Test that 1 is not prime."""
    self.assertFalse(is_prime(1))

  def test_2(self):
    """Test that 2 is prime."""
    self.assertTrue(is_prime(2))

  def test_3(self):
    """Test that 3 is prime."""
    self.assertTrue(is_prime(3))

  def test_8(self):
    """Test that 8 is not prime."""
    self.assertFalse(is_prime(8))

  def test_10(self):
    """Test that 10 is not prime."""
    self.assertFalse(is_prime(10))

  def test_11(self):
    """Test that 11 is prime."""
    self.assertTrue(is_prime(11))

if __name__ == "__main__":
  u.main()