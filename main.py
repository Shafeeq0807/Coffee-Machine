"""Coffee machine CLI. Importing this module never prompts for input."""
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

MENU = {
    "espresso": {"ingredients": {"water": 50, "coffee": 18}, "cost": Decimal("1.50")},
    "latte": {"ingredients": {"water": 200, "milk": 150, "coffee": 24}, "cost": Decimal("2.50")},
    "cappuccino": {"ingredients": {"water": 250, "milk": 100, "coffee": 24}, "cost": Decimal("3.00")},
}
COINS = {"quarters": 25, "dimes": 10, "nickels": 5, "pennies": 1}

class OrderError(ValueError):
    """An order rejected without changing the machine state."""

@dataclass
class CoffeeMachine:
    resources: dict[str, int] = field(default_factory=lambda: {"water": 300, "milk": 200, "coffee": 100})
    profit: Decimal = Decimal("0.00")

    def order(self, name: str, payment: Decimal) -> Decimal:
        """Validate, charge, and dispense atomically. Return exact change."""
        if name not in MENU:
            raise OrderError("Choose espresso, latte, or cappuccino.")
        try:
            payment = Decimal(str(payment))
        except (InvalidOperation, ValueError) as exc:
            raise OrderError("Payment must be a valid currency amount.") from exc
        try:
            valid_payment = payment.is_finite() and payment >= 0 and payment == payment.quantize(Decimal("0.01"))
        except InvalidOperation:
            valid_payment = False
        if not valid_payment:
            raise OrderError("Payment must be a non-negative amount with at most two decimal places.")
        drink = MENU[name]
        for ingredient, quantity in drink["ingredients"].items():
            if self.resources.get(ingredient, 0) < quantity:
                raise OrderError(f"Not enough {ingredient}. Payment refunded.")
        if payment < drink["cost"]:
            raise OrderError("Not enough money. Payment refunded.")
        for ingredient, quantity in drink["ingredients"].items():
            self.resources[ingredient] -= quantity
        self.profit += drink["cost"]
        return payment - drink["cost"]

    def refill(self, ingredient: str, quantity: int) -> None:
        if ingredient not in self.resources or type(quantity) is not int or quantity <= 0:
            raise OrderError("Use refill <water|milk|coffee> <positive whole number>.")
        self.resources[ingredient] += quantity

    def report(self) -> str:
        return "\n".join([f"Water: {self.resources['water']} ml", f"Milk: {self.resources['milk']} ml",
                          f"Coffee: {self.resources['coffee']} g", f"Revenue: ${self.profit:.2f}"])

def collect_payment() -> Decimal:
    cents = 0
    for coin, value in COINS.items():
        while True:
            raw = input(f"Number of {coin}: ").strip()
            if raw.isascii() and raw.isdigit() and len(raw) <= 6:
                cents += int(raw) * value
                break
            print("Enter a non-negative whole number of coins (up to six digits).")
    return Decimal(cents) / 100

def main() -> None:
    machine = CoffeeMachine()
    print("COFFEE MACHINE / Fresh coffee, exact change")
    print("Commands: menu, report, refill <ingredient> <quantity>, off")
    try:
        while True:
            choice = input("\nYour order: ").strip().lower()
            if choice in {"off", "quit", "exit"}:
                print("Machine switched off. See you next time!")
                return
            if choice in {"menu", "help"}:
                for name, drink in MENU.items():
                    print(f"{name.title():12} ${drink['cost']:.2f}")
            elif choice == "report":
                print(machine.report())
            elif choice.startswith("refill"):
                try:
                    _, ingredient, quantity = choice.split()
                    machine.refill(ingredient, int(quantity))
                    print(f"Refilled {ingredient}.")
                except (ValueError, OrderError) as exc:
                    print(str(exc) if isinstance(exc, OrderError) else "Use refill <ingredient> <quantity>.")
            elif choice in MENU:
                try:
                    # Reject unavailable orders before asking for coins.
                    for ingredient, amount in MENU[choice]["ingredients"].items():
                        if machine.resources[ingredient] < amount:
                            raise OrderError(f"Not enough {ingredient}. Refill first.")
                    change = machine.order(choice, collect_payment())
                    print(f"Enjoy your {choice}! Change: ${change:.2f}")
                except OrderError as exc:
                    print(exc)
            else:
                print("Unknown command. Type menu, report, refill, or off.")
    except (EOFError, KeyboardInterrupt):
        print("\nOrder cancelled. Machine switched off.")

if __name__ == "__main__":
    main()
