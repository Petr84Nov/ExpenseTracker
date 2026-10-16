
from dataclasses import dataclass, asdict
from datetime import date


@dataclass
class Expense:
    amount: float
    category: str
    date: date
    note: str = ''

    # uložení do JSON
    def to_dict(self) -> dict:
        data = asdict(self) #převede vstupní atributy na slovník
        data['date'] = self.date.isoformat() # přepíše date na string
        return data

    # načtení z JSON
    # @classmethod
    def from_dict(data: dict) -> 'Expense':
        data['date'] = date.fromisoformat(data['date'])
        return Expense(**data)