import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


def file_uri(filename):
  return pathlib.Path(os.path.abspath(filename)).as_uri()

driver = webdriver.Chrome()

class WebpageTests(unittest.TestCase):
  def test_title(self):
    driver.get(file_uri("counter.html"))
    self.assertEqual(driver.title, "Counter")

  def test_increase(self):
    driver.get(file_uri("counter.html"))
    counterDisplay = driver.find_element(By.CSS_SELECTOR, "h1")
    counterSnapshot = int( counterDisplay.text )
    driver.find_element(value="increase").click()
    self.assertEqual(int(counterDisplay.text), counterSnapshot + 1)

  def test_decrease(self):
    driver.get(file_uri("counter.html"))
    counterDisplay = driver.find_element(By.CSS_SELECTOR, "h1")
    counterSnapshot = int( counterDisplay.text )
    driver.find_element(value="decrease").click()
    self.assertEqual(int(counterDisplay.text), counterSnapshot - 1)

  def test_multiple_increase(self):
    driver.get(file_uri("counter.html"))
    counterDisplay = driver.find_element(By.CSS_SELECTOR, "h1")
    counterSnapshot = int( counterDisplay.text )
    increase_button = driver.find_element(value="increase")
    clickAmount = 5
    for _ in range(clickAmount):
      increase_button.click()
    self.assertEqual(int(counterDisplay.text), counterSnapshot + clickAmount)

if __name__ == "__main__":
  unittest.main()