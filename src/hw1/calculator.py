from backend.api import add


def sum() -> None:
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))
    result = add(num1, num2)
    print(f"The result of {num1} + {num2} is {result}")


if __name__ == "__main__":
    sum()
