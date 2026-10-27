import os
import customtkinter as ctk
from datetime import date

from components import DateFilteredWidgert
from config import CATEGORIES, DEFAULT_FONT, MONTHS
from pc_details_layout import ExpenseDetailLayout
from expense_manager import ExpenseManager
from expense_analyzer import ExpenseAnalyzer

from tkinter import messagebox

class ExpenseLayout(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.expenses = None
        self.title('Expense')
        self.geometry('350x600')
        self.resizable(False, False)
        #self.today_date = date.today().strftime('%d.%m.%Y')

        self.load_total_amount()




        def save_expense():
            from expense import Expense
            try:
                amount = float(self.amount_entry.get())
            except ValueError:
                print('Hodnota není číslo.')
                messagebox.showerror('Chyba', 'Hodnota není číslo.')
                return


            category = self.category_box.get()
            date_str = date.today()
            note_str = self.note.get('1.0', 'end-1c')
            new_expense = Expense(amount=amount, category=category, date=date_str, note=note_str)
            self.expenses.append(new_expense)
            expense_manager = ExpenseManager()
            expense_manager.save_expenses(self.expenses)
            self.fill_expenses()

        def reset():
            try:
                os.remove('expenses.json')
            except FileNotFoundError:
                pass
            self.load_total_amount()
            self.fill_expenses()

        def on_year_changed(selected_year):
            if selected_year == 'All':
                self.month_box.set('All')
                self.month_box.configure(state='disabled')
            else:
                self.month_box.configure(state='normal')
            self.fill_expenses()

        # output frame
        view_frame = ctk.CTkFrame(self, fg_color='transparent')
        view_frame.pack(side='top', fill='both', padx=(10, 10), pady=(10, 30),)
        view_frame.grid_rowconfigure(0, weight=0)
        view_frame.grid_columnconfigure(1, weight=1)


        # self.month_box = ctk.CTkComboBox(view_frame, values=MONTHS, font=DEFAULT_FONT, command=lambda _: fill_expenses())
        # current_month_name = date.today().strftime('%B')
        # default_month = current_month_name if current_month_name in MONTHS else 'All'
        # self.month_box.set(default_month)
        # self.month_box.grid(row=0, column=0, padx=(10, 10), pady=10 , sticky='w')
        #
        # self.year_box = ctk.CTkComboBox(view_frame, values=self.available_years, font=DEFAULT_FONT, command=on_year_changed)
        # current_year = str(date.today().year)
        # default_year = current_year if current_year in self.available_years else 'All'
        # self.year_box.set(default_year)
        # self.year_box.grid(row=0, column=1, padx=(10, 10), pady=10, sticky='w')

        self.date_filter = DateFilteredWidgert(view_frame, self.expense_analyzer, on_change_callback=self.fill_expenses)
        self.date_filter.grid(row=0, column=0, columnspan=2 , padx=5, pady=5)

        ctk.CTkLabel(view_frame, text=f'Total expenses: ', font=DEFAULT_FONT).grid(row=1, column=0, padx=(10, 10), sticky='w')
        self.total_label = ctk.CTkLabel(view_frame, text=f'{self.load_total_amount()} Kč', font=DEFAULT_FONT)
        self.total_label.grid(row=1, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Food: ', font=DEFAULT_FONT).grid(row=2, column=0, padx=(10, 30), sticky='w')
        self.food_label = ctk.CTkLabel(view_frame, text=f'{self.category_amount.get('food', 0)} Kč', font=DEFAULT_FONT)
        self.food_label.grid(row=2, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Transport: ', font=DEFAULT_FONT).grid(row=3, column=0, padx=(10, 30), sticky='w')
        self.transport_label = ctk.CTkLabel(view_frame, text=f'{self.category_amount.get('transport', 0)} Kč', font=DEFAULT_FONT)
        self.transport_label.grid(row=3, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Housing: ', font=DEFAULT_FONT).grid(row=4, column=0, padx=(10, 30), sticky='w')
        self.housing_label = ctk.CTkLabel(view_frame, text=f'{self.category_amount.get('housing', 0)} Kč', font=DEFAULT_FONT)
        self.housing_label.grid(row=4, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Fun: ', font=DEFAULT_FONT).grid(row=5, column=0, padx=(10, 30), sticky='w')
        self.fun_label = ctk.CTkLabel(view_frame, text=f'{self.category_amount.get('fun', 0)} Kč', font=DEFAULT_FONT)
        self.fun_label.grid(row=5, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Other: ', font=DEFAULT_FONT).grid(row=6, column=0, padx=(10, 30), sticky='w')
        self.other_label = ctk.CTkLabel(view_frame, text=f'{self.category_amount.get('other', 0)} Kč', font=DEFAULT_FONT)
        self.other_label.grid(row=6, column=1, padx=(10, 30), sticky='e')

        ctk.CTkButton(view_frame, text='Details', font=DEFAULT_FONT, command=self.open_details_window).grid(row=7, column=0, columnspan=2, padx=(10, 30), sticky='ew')
        ctk.CTkButton(view_frame, text='Reset', font=DEFAULT_FONT, command=lambda: reset()).grid(row=8, column=0, columnspan=2, padx=(10, 30), sticky='ew')


        # input frame
        input_frame = ctk.CTkFrame(self, fg_color='transparent')
        input_frame.pack(side='bottom', fill='both', expand=True)

        # category label a roletka
        ctk.CTkLabel(input_frame, text='Category: ', font=DEFAULT_FONT).grid(row=0, column=0, padx=(10, 30))
        self.category_box = ctk.CTkComboBox(
            input_frame,
            values=CATEGORIES,
            font=DEFAULT_FONT
        )
        self.category_box.set('food')
        self.category_box.grid(row=0, column=1, padx=(10, 30))

        # amount label a entry
        ctk.CTkLabel(input_frame, text='Amount: ', font=DEFAULT_FONT).grid(row=1, column=0, padx=(10, 30))

        amount_frame = ctk.CTkFrame(input_frame, fg_color='transparent')
        amount_frame.grid(row=1, column=1, padx=(10, 30), pady=(10, 10))

        self.amount_entry = ctk.CTkEntry(
            amount_frame,
            font=DEFAULT_FONT,
            corner_radius=20,
        )
        self.amount_entry.pack(side='left', padx=(10, 2))
        ctk.CTkLabel(amount_frame, text='Kč', font=DEFAULT_FONT).pack(side='left')

        # aktuální datum
        ctk.CTkLabel(input_frame, text='Date: ', font=DEFAULT_FONT).grid(row=2, column=0, padx=(10, 30))

        actual_date = date.today().strftime('%d.%m.%Y')
        ctk.CTkLabel(input_frame, text=actual_date, font=DEFAULT_FONT).grid(row=2, column=1, padx=(10, 30))

        self.note = ctk.CTkTextbox(master=input_frame, wrap='word', height=100, font=DEFAULT_FONT)
        self.note.grid(row=3, column=0, columnspan=2 , sticky='ew' , padx=(10, 10), pady=(10, 10))

        # save button
        save_button = ctk.CTkButton(
            input_frame,
            text='Add',
            font=DEFAULT_FONT,
            corner_radius=25,
            command=save_expense,
        )
        save_button.grid(row=4, column=0, columnspan=2, sticky='ew', padx=(10, 10))

    # otevře okno s detaily
    def open_details_window(self):
        details_win = ExpenseDetailLayout(self, on_expense_changed=self.fill_expenses)
        # zjistí aktuální pozici a šířku hlavního okna na obrazovce
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()

        # spočítáme novou pozici: šířka hlavního okna + 10 pixelů mezera
        new_x = main_x + main_width + 100
        new_y = main_y
        details_win.geometry(f'+{new_x}+{new_y}')

        # přenesení okna do popředí a aktivace
        details_win.after(250, lambda: (details_win.lift(), details_win.focus_force()) )

    def load_total_amount(self):
        from expense_analyzer import ExpenseAnalyzer
        self.expenses = ExpenseManager('expenses.json').load_expenses()
        self.expense_analyzer = ExpenseAnalyzer(self.expenses)

        current_month_name = date.today().strftime('%B')  # zjistí aktuální měsíc
        current_year = date.today().year
        # selected_month = self.month_box.get() if hasattr(self, 'month_box') else current_month_name
        # selected_year = self.year_box.get() if hasattr(self, 'year_box') else str(date.today().year)
        if hasattr(self, 'date_filter'):
            selected_month, selected_year = self.date_filter.get_selected_values()
        else:
            selected_month = current_month_name
            selected_year = current_year

        # filtrace údajů
        filtered_expenses = self.expense_analyzer.filter_by_month_and_year(selected_month, selected_year)

        filtered_analyzer = ExpenseAnalyzer(filtered_expenses)
        total_amount = filtered_analyzer.total_amount()
        self.category_amount = filtered_analyzer.total_by_category()
        self.available_years = self.expense_analyzer.get_available_year()
        return total_amount


    def fill_expenses(self):
        self.total_label.configure(text=f'{self.load_total_amount()} Kč')
        self.food_label.configure(text=f'{self.category_amount.get("food", 0)} Kč')
        self.transport_label.configure(text=f'{self.category_amount.get("transport", 0)} Kč')
        self.housing_label.configure(text=f'{self.category_amount.get("housing", 0)} Kč')
        self.fun_label.configure(text=f'{self.category_amount.get("fun", 0)} Kč')
        self.other_label.configure(text=f'{self.category_amount.get("other", 0)} Kč')






app = ExpenseLayout()
app.mainloop()