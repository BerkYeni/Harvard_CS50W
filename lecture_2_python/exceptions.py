import sys

def main() -> None:
  try:
    x = int(input("x: "))
    y = int(input("y: "))
  except ValueError:
    # print("x and y must be integers")
    sys.exit(ValueError("x and y must be integers"))

  try:
    print(x / y)
  except ZeroDivisionError:
    # print("y must not be 0")
    sys.exit(ZeroDivisionError("y must not be 0"))


if __name__ == '__main__':
  main()