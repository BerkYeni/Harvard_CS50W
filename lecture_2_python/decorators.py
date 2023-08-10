def main() -> None:
  some_function()

def announce(func, *args):
  def announcer():
    print(f"function '{func.__name__}' is starting to be executed")
    result = func(*args)
    print(f"function '{func.__name__}' has been executed")
    return result
  return announcer

@announce
def some_function():
  print("this is some function")

if __name__ == '__main__':
  main()