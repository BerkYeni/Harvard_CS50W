def main() -> None:
  people = [
    {"name": "Harry", "house": "Gryffindor",},
    {"name": "Cho", "house": "Ravenclaw",},
    {"name": "Drako", "house": "Slytherin",},
  ]

  people.sort(key= lambda person: person["name"])
  print(people)


if __name__ == '__main__':
  main()