import customtkinter as ctk
from datetime import date
from config import  DEFAULT_FONT, MONTHS

class DateFilteredWidgert(ctk.CTkFrame):
    def __init__(self, master, analyzer, on_change_callback=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)

        self.analyzer = analyzer
        self.on_change_callback = on_change_callback

        # načtení dat
        available_years = self.analyzer.get_available_year()
        curr_year = str(date.today().year)
        default_year = curr_year if curr_year in available_years else 'All'

        current_month = date.today().strftime('%B')
        default_month = current_month if current_month in MONTHS else 'All'

        # změna roku i se zamykáním
        def on_year_changed(selected_year):
            if selected_year == 'All':
                self.month_box.set('All')
                self.month_box.configure(state='disabled')
            else:
                self.month_box.configure(state='normal')

            if self.on_change_callback:
                self.on_change_callback()

        self.month_box = ctk.CTkComboBox(self, values=MONTHS, font=DEFAULT_FONT, command=lambda _: self.on_change_callback() if self.on_change_callback else None)
        self.month_box.set(default_month)
        self.month_box.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.year_box = ctk.CTkComboBox(self, values=available_years, font=DEFAULT_FONT, command=on_year_changed)
        self.year_box.set(default_year)
        self.year_box.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # výchozí stav zámku
        if default_year == 'All':
            self.month_box.set('All')
            self.month_box.configure(state='normal')

    def get_selected_values(self):
        return self.month_box.get(), self.year_box.get()
