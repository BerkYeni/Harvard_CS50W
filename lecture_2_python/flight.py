def main() -> None:
  a_flight = Flight(3)
  a_flight.add_passenger("harry")
  a_flight.add_passenger("ron")
  a_flight.add_passenger("hermoine")
  a_flight.add_passenger("drako")

  print(a_flight.passengers)

class Flight():
  def __init__(self, passenger_limit: int) -> None:
    self.passenger_limit = passenger_limit
    self.passengers = []
  
  def add_passenger(self, passenger_name: str) -> None:
    if not self.can_add_passenger():
      return
    self.passengers.append(passenger_name)
  
  def remaining_capacity(self) -> int:
    return self.passenger_limit - len(self.passengers)

  def can_add_passenger(self) -> bool:
    return self.remaining_capacity() > 0


if __name__ == '__main__':
  main()