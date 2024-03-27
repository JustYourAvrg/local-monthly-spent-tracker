import customtkinter as ctk
import datetime

from utils import Utility
from data_management import dataManagement
from tkinter import messagebox


# CTK APPEARANCE SETUP
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class UI:
    def __init__(self):
        # Get the number of the current month
        self.cur_month_int = datetime.datetime.now().month

        # Check if the current month is January to set the previous month to December
        if self.cur_month_int - 1 == 0:
            self.cur_month_check = 12
        else:
            self.cur_month_check = self.cur_month_int - 1

        # Show data from the previous month
        if dataManagement.execute_query("SELECT * FROM total_spent WHERE month = ?", (Utility.get_month_str(self.cur_month_check),)):
            messagebox.showinfo('Spent last month', f"You spent ${dataManagement.execute_query('SELECT spent FROM total_spent WHERE month = ?', (Utility.get_month_str(self.cur_month_check),))[0][0]} last month.")

        # Get the current month and check if it exists in the database
        self.cur_month = Utility.get_month_str(self.cur_month_int)
        if not dataManagement.execute_query("SELECT * FROM total_spent WHERE month = ?", (self.cur_month,)):
            # If it doesn't exist, create a new row with the current month
            dataManagement.execute_query("INSERT INTO total_spent (spent, month) VALUES (?, ?)", (0, self.cur_month))

        # Get the total spent for the current month
        self.monthly_spent = dataManagement.execute_query("SELECT spent FROM total_spent WHERE month = ?", (self.cur_month,))


    def add_to_spent(self, amount):
        # Get the current spent and add the new amount to it
        cur_spent = float(dataManagement.execute_query("SELECT spent FROM total_spent WHERE month = ?", (self.cur_month,))[0][0])
        total_to_add = cur_spent + round(float(amount), 2)

        dataManagement.execute_query("UPDATE total_spent SET spent = spent + ? WHERE month = ?", (round(float(amount), 2), self.cur_month))
        self.update_ui(total_to_add)
    

    def update_ui(self, total_to_add):
        # Update the total spent label and clear the input
        self.total_spent_label.configure(text=f"${total_to_add}")
        self.spent_input.delete(0, 'end')


    def client_ui(self):
        # Setup window
        self.ui = ctk.CTk()
        self.ui.geometry('400x400')
        self.ui.resizable(False, False)
        self.ui.title(f"Total Spent Monthly - {self.cur_month}")

        self.month_label = ctk.CTkLabel(master=self.ui, text=self.cur_month, font=ctk.CTkFont(size=44))
        self.month_label.pack(pady=10)

        self.total_spent_label = ctk.CTkLabel(master=self.ui, text=f'${self.monthly_spent[0][0]}', font=ctk.CTkFont(size=60))
        self.total_spent_label.pack(pady=(100, 0))

        self.input_frame = ctk.CTkFrame(master=self.ui)
        self.input_frame.pack(fill='x', pady=(90, 0))

        self.input_label = ctk.CTkLabel(master=self.input_frame, text='Add to total spent')
        self.input_label.grid(row=0, column=0)

        self.spent_input = ctk.CTkEntry(master=self.input_frame, width=280)
        self.spent_input.grid(row=1, column=0, padx=(5, 0))
        
        self.spent_input_btn = ctk.CTkButton(master=self.input_frame, text='Confirm', width=100, command=lambda: self.add_to_spent(self.spent_input.get()))
        self.spent_input_btn.grid(row=1, column=1, padx=(10, 0))

        # Start the mainloop
        self.ui.mainloop()


if __name__ == '__main__':
    # Setup the data management
    dataManagement = dataManagement()
    dataManagement.setup()

    # Start the UI
    ui = UI()
    ui.client_ui()
