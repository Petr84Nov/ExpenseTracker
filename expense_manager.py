import os

from expense import Expense
import json

class ExpenseManager:
    def __init__(self, filepath: str = 'expenses.json'):
        self.filepath = filepath

    def save_expenses(self, expenses: list[Expense])-> None:
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump([e.to_dict() for e in expenses], file, indent=2, ensure_ascii=False)

    def load_expenses(self) -> list[Expense]:
        if not os.path.exists(self.filepath) or os.path.getsize(self.filepath) == 0:
            return []

        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return [Expense.from_dict(item) for item in data]
        except FileNotFoundError:
            return []