from collections import defaultdict
from datetime import date

from expense import Expense


class ExpenseAnalyzer:
    def __init__(self, expenses: list[Expense]):
        self.expenses = expenses

    def total_amount(self) -> float:
        return  sum(e.amount for e in self.expenses)

    def total_by_category(self) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)
        for e in self.expenses:
            totals[e.category] += e.amount
        return dict(totals)

    def total_by_month(self) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)
        for e in self.expenses:
            totals[e.date.strftime('%Y-%m')] += e.amount
        return dict(totals)

    def filter_by_category(self, category: str) -> list[Expense]:
        return [e for e in self.expenses if e.category == category]

    def filter_by_date_range(self, start_date: date, end_date: date) -> list[Expense]:
        return [e for e in self.expenses if start_date <= e.date <= end_date]