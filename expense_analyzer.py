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

    def filter_by_month_and_year(self, month: str, year: str) -> list[Expense]:
        filtered = self.expenses

        # 1. Filtrování podle roku
        if year != 'All':
            filtered = [e for e in filtered if str(e.date.year) == str(year)]

        # 2. Filtrování podle měsíce
        if month != 'All':
            months_dict = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            month_num = months_dict.get(month)
            if month_num:
                filtered = [e for e in filtered if e.date.month == month_num]

        return filtered

    def get_available_year(self) -> list[str]:
        # měsíce v json
        years = {str(e.date.year) for e in self.expenses}
        current_year = str(date.today().year)
        years.add(current_year)
        sorted_years = sorted(years)
        # přidání možnost All
        if 'All' not in sorted_years:
            sorted_years.insert(0, 'All')
        return sorted_years

