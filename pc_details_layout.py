import customtkinter as ctk

from components import DateFilteredWidgert
from config import CATEGORIES, DEFAULT_FONT, MONTHS
from expense_manager import ExpenseManager
from expense_analyzer import ExpenseAnalyzer

class ExpenseDetailLayout(ctk.CTkToplevel):
    def __init__(self, *args, on_expense_changed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Expense Details')
        self.geometry('500x450')
        self.resizable(False, False)

        # načtení výdajů
        self.expenses = ExpenseManager('expenses.json').load_expenses()
        self.analyzer = ExpenseAnalyzer(self.expenses)
        self.on_expense_changed = on_expense_changed

        self.date_filter = DateFilteredWidgert(self, self.analyzer, on_change_callback=self.refresh_expenses)
        self.date_filter.pack(fill='both', padx=5, pady=5, expand=True)

        # roletka pro výběr kategorie
        self.category_box = ctk.CTkComboBox(
            self,
            values=CATEGORIES,
            font = DEFAULT_FONT,
            #command=self.on_category_selected
            command=lambda _: self.refresh_expenses()
        )
        self.category_box.pack(padx=10, pady=5)
        self.category_box.set(CATEGORIES[0]) # nastaví výchozí kategorii

        # scrollovací rám pro výpis položek (podle tvého nákresu)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=30, height=300)
        self.scroll_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # zobrazíme položky pro výchozí kategorii
        # self.display_expenses(CATEGORIES[0])
        self.refresh_expenses()

    # když uživatel změní kategorii v roletce znovu se vypíší hodnoty v dané kategorii
    def on_category_selected(self, choice):
        self.display_expenses(choice)

    def display_expenses(self, filtered_expenses , category:str):
        # vyčistí staré widgety v scrolovacím rámu
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # výpis výdajů pro danou kategorii
        # filtered_expenses = self.analyzer.filter_by_category(category)
        if not filtered_expenses:
            warning_label = ctk.CTkLabel(self.scroll_frame, text='Nenalezeny žádné výdaje', text_color='red', font=DEFAULT_FONT)
            warning_label.pack(pady=20)
            return

        # řádek s názvem nebo poznámkou, částkou a tlačítkem delete
        for index, expense in enumerate(filtered_expenses):
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
            row_frame.pack(fill='x', padx=5)
            row_frame.grid_columnconfigure(0, weight=1)

            # název, částka
            text_decription = expense.note if expense.note else category
            decription_label = ctk.CTkLabel(row_frame, text=text_decription, text_color='blue', font=DEFAULT_FONT,
                                            wraplength=200, # zalamovač řádků
                                            justify='left', # zarovná řádka doleva
                                            anchor='w')
            decription_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

            amount_label = ctk.CTkLabel(row_frame, text=f'{expense.amount} Kč', text_color='blue', font=DEFAULT_FONT)
            amount_label.grid(row=0, column=1, padx=5,)

            # delete button
            delete_button = ctk.CTkButton(
                row_frame,
                text='Delete',
                width=70,
                height=24,
                font=DEFAULT_FONT,
                corner_radius=25,
                command=lambda e=expense: self.delete_expense(e)
            )
            delete_button.grid(row=0, column=2, padx=5, pady=5)


    def refresh_expenses(self):
        selected_category = self.category_box.get()
        selected_month, selected_year = self.date_filter.get_selected_values()

        month_year_filtered = self.analyzer.filter_by_month_and_year(selected_month, selected_year)
        temp_analyzer = ExpenseAnalyzer(month_year_filtered)
        final_filtered = temp_analyzer.filter_by_category(selected_category)
        self.display_expenses(final_filtered, selected_category)

    def delete_expense(self, expense_to_delete):
        # print(f'Mazání: {expense_to_delete}')
        self.expenses.remove(expense_to_delete) # odstranění položky z lokálního slovníku
        ExpenseManager('expenses.json').save_expenses(self.expenses) # přepsání expese.json novými daty
        # překreslí aktuálně vybranou kategorii
        self.analyzer = ExpenseAnalyzer(self.expenses)
        self.refresh_expenses()

        # změní hodnoty v hlavním okně
        if self.on_expense_changed:
            self.on_expense_changed() # zavolá se self.fill_expenses v hlavním okně




