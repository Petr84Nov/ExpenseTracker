import customtkinter as ctk
from datetime import date

from config import categories, default_font, default_by_category
from expense_analyzer import ExpenseAnalyzer
from expense_manager import ExpenseManager


class ExpenseLayout(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Expense')
        self.geometry('350x500')
        self.resizable(False, False)
        #self.today_date = date.today().strftime('%d.%m.%Y')

        self.expenses = ExpenseManager('expenses.json').load_expenses()
        self.category_amount = default_by_category


        def load_total_amount():
            from expense_analyzer import ExpenseAnalyzer
            expense_analyzer = ExpenseAnalyzer(self.expenses)
            total_amount = expense_analyzer.total_amount()
            self.category_amount = expense_analyzer.total_by_category()
            return total_amount

        load_total_amount()


        def save_expense():
            from expense import Expense
            amount = float(self.amount_entry.get())
            category = self.category_box.get()
            date_str = date.today()
            note_str = self.note.get('1.0', 'end-1c')
            new_expense = Expense(amount=amount, category=category, date=date_str, note=note_str)
            self.expenses.append(new_expense)
            expense_manager = ExpenseManager()
            expense_manager.save_expenses(self.expenses)
            self.total_label.configure(text=load_total_amount())
            self.food_label.configure(text=self.category_amount.get('food', 0))
            self.transport_label.configure(text=self.category_amount.get('transport', 0))
            self.housing_label.configure(text=self.category_amount.get("housing", 0))
            self.fun_label.configure(text=self.category_amount.get("fun", 0))
            self.other_label.configure(text=self.category_amount.get("other", 0))

        # output frame
        view_frame = ctk.CTkFrame(self, fg_color='transparent')
        view_frame.pack(side='top', fill='both', padx=(10, 10), pady=(10, 30))

        ctk.CTkLabel(view_frame, text=f'Total expenses: ', font=default_font).grid(row=0, column=0, padx=(10, 10), sticky='w')
        self.total_label = ctk.CTkLabel(view_frame, text=str(load_total_amount()), font=default_font)
        self.total_label.grid(row=0, column=1, padx=(10, 30))

        ctk.CTkLabel(view_frame, text='Food: ', font=default_font).grid(row=1, column=0, padx=(10, 30), sticky='w')
        self.food_label = ctk.CTkLabel(view_frame, text=str(self.category_amount.get('food', 0)), font=default_font)
        self.food_label.grid(row=1, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Transport: ', font=default_font).grid(row=2, column=0, padx=(10, 30), sticky='w')
        self.transport_label = ctk.CTkLabel(view_frame, text=str(self.category_amount.get('transport', 0)), font=default_font)
        self.transport_label.grid(row=2, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Housing: ', font=default_font).grid(row=3, column=0, padx=(10, 30), sticky='w')
        self.housing_label = ctk.CTkLabel(view_frame, text=str(self.category_amount.get('housing', 0)), font=default_font)
        self.housing_label.grid(row=3, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Fun: ', font=default_font).grid(row=4, column=0, padx=(10, 30), sticky='w')
        self.fun_label = ctk.CTkLabel(view_frame, text=str(self.category_amount.get('fun', 0)), font=default_font)
        self.fun_label.grid(row=4, column=1, padx=(10, 30), sticky='e')

        ctk.CTkLabel(view_frame, text='Other: ', font=default_font).grid(row=5, column=0, padx=(10, 30), sticky='w')
        self.other_label = ctk.CTkLabel(view_frame, text=str(self.category_amount.get('other', 0)), font=default_font)
        self.other_label.grid(row=5, column=1, padx=(10, 30), sticky='e')





        # input frame
        input_frame = ctk.CTkFrame(self, fg_color='transparent')
        input_frame.pack(side='bottom', fill='both', expand=True)

        # category label a roletka
        ctk.CTkLabel(input_frame, text='Category: ', font=default_font).grid(row=0, column=0, padx=(10, 30))
        self.category_box = ctk.CTkComboBox(
            input_frame,
            values=categories,
            font=default_font
        )
        self.category_box.set('food')
        self.category_box.grid(row=0, column=1, padx=(10, 30))

        # amount label a entry
        ctk.CTkLabel(input_frame, text='Amount: ', font=default_font).grid(row=1, column=0, padx=(10, 30))

        amount_frame = ctk.CTkFrame(input_frame, fg_color='transparent')
        amount_frame.grid(row=1, column=1, padx=(10, 30), pady=(10, 10))

        self.amount_entry = ctk.CTkEntry(
            amount_frame,
            font=default_font,
            corner_radius=20,
        )
        self.amount_entry.pack(side='left', padx=(10, 2))
        ctk.CTkLabel(amount_frame, text='Kč', font=default_font).pack(side='left')

        # aktuální datum
        ctk.CTkLabel(input_frame, text='Date: ', font=default_font).grid(row=2, column=0, padx=(10, 30))

        actual_date = date.today().strftime('%d.%m.%Y')
        ctk.CTkLabel(input_frame, text=actual_date, font=default_font).grid(row=2, column=1, padx=(10, 30))

        save_button = ctk.CTkButton(
            input_frame,
            text='Add',
            font=default_font,
            corner_radius=25,
            command=save_expense,
        )

        self.note = ctk.CTkTextbox(master=input_frame, wrap='word', height=100, font=default_font)
        self.note.grid(row=3, column=0, columnspan=2 , sticky='ew' , padx=(10, 10), pady=(10, 10))

        # save button
        save_button.grid(row=4, column=0, columnspan=2, sticky='ew', padx=(10, 10))









app = ExpenseLayout()
app.mainloop()