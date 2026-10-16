import customtkinter as ctk
from config import CATEGORIES, DEFAULT_FONT
from expense_manager import ExpenseManager
from expense_analyzer import ExpenseAnalyzer

class ExpenseDetailLayout(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Expense Details')
        self.geometry('350x500')
        self.resizable(False, False)

        # načtení výdajů
        self.expenses = ExpenseManager('expenses.json').load_expenses()
        self.analyzer = ExpenseAnalyzer(self.expenses)

        # roletka pro výběr kategorie
        self.category_box = ctk.CTkComboBox(
            self,
            values=CATEGORIES,
            font = DEFAULT_FONT,
            #command=self.on_category_selected
            command=self.display_expenses
        )
        self.category_box.pack(padx=20, pady=20)
        self.category_box.set(CATEGORIES[0]) # nastaví výchozí kategorii

        # scrollovací rám pro výpis položek (podle tvého nákresu)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=30, height=300)
        self.scroll_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # zobrazíme položky pro výchozí kategorii
        self.display_expenses(CATEGORIES[0])

    # když uživatel změní kategorii v roletce znovu se vypíší hodnoty v dané kategorii
    def on_category_selected(self, choice):
        self.display_expenses(choice)

    def display_expenses(self, category:str):
        # vyčistí staré widgety v scrolovacím rámu
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # výpis výdajů pro danou kategorii
        filtered_expenses = self.analyzer.filter_by_category(category)
        if not filtered_expenses:
            warning_label = ctk.CTkLabel(self.scroll_frame, text='Nenalezeny žádné výdaje', fg='red', font=DEFAULT_FONT)
            warning_label.pack(pady=20)
            return

        # řádek s názvem nebo poznámkou, částkou a tlačítkem delete
        for index, expense in enumerate(filtered_expenses):
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
            row_frame.pack(fill='left', padx=5)

            # název, částka
            text_decription = expense.note if expense.note else category
            decription_label = ctk.CTkLabel(row_frame, text=text_decription, fg='blue', font=DEFAULT_FONT)
            decription_label.pack(side='left', padx=20)

            # delete button
            delete_button = ctk.CTkButton(
                row_frame,
                text='Delete',
                width=70,
                font=DEFAULT_FONT,
                command=lambda e=expense: self.delete_expense(e)
            )
            delete_button.pack(side='right', padx=5)

    def delete_expense(self, expense_to_delete):
        print(f'Mazání: {expense_to_delete}')




