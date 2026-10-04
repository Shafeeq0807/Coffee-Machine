import unittest
from decimal import Decimal
from main import CoffeeMachine, OrderError

class MachineTests(unittest.TestCase):
    def test_exact_change_and_inventory(self):
        machine = CoffeeMachine()
        self.assertEqual(machine.order("espresso", Decimal("2.00")), Decimal("0.50"))
        self.assertEqual(machine.resources, {"water":250,"milk":200,"coffee":82})
        self.assertEqual(machine.profit, Decimal("1.50"))

    def test_rejected_orders_do_not_mutate_state(self):
        for name,payment in [("tea", "2"), ("latte", "0.10"), ("espresso", "NaN"), ("espresso", "Infinity"), ("espresso", "1.501"), ("espresso", "-1"), ("espresso", "1e100")]:
            machine = CoffeeMachine()
            before = machine.resources.copy()
            with self.assertRaises(OrderError): machine.order(name, Decimal(payment))
            self.assertEqual(machine.resources, before)
            self.assertEqual(machine.profit, 0)

    def test_insufficient_inventory_refund(self):
        machine = CoffeeMachine(resources={"water":0,"milk":0,"coffee":0})
        with self.assertRaises(OrderError): machine.order("latte", Decimal("5"))
        self.assertEqual(machine.profit, 0)

    def test_instances_have_independent_inventory(self):
        first, second = CoffeeMachine(), CoffeeMachine()
        first.order("espresso", Decimal("1.50"))
        self.assertEqual(second.resources["water"], 300)

    def test_refill_validation(self):
        machine = CoffeeMachine()
        machine.refill("water",100)
        self.assertEqual(machine.resources["water"],400)
        for ingredient,quantity in [("sugar",10),("water",-1),("water",1.5),("water",True)]:
            with self.assertRaises(OrderError): machine.refill(ingredient,quantity)

if __name__ == "__main__": unittest.main()
