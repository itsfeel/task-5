import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Currency Converter")
        self.root.geometry("450x400")
        self.root.configure(bg="#ffffff")

        self.countries = self.load_country_data()
        self.rates = self.fetch_exchange_rates()
        self.create_widgets()
        self.update_currency_menu()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="USD to Foreign Currency Converter", font=("Arial", 18, "bold"), bg="#ffffff", fg="#333333")
        title_label.pack(pady=15)

        tk.Label(self.root, text="Enter Amount in USD:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 12), width=30, borderwidth=2, relief="sunken")
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Choose Target Country:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
        self.country_var = tk.StringVar(value="Select Country")
        self.country_menu = ttk.Combobox(self.root, textvariable=self.country_var, font=("Arial", 12), state="readonly", width=30)
        self.country_menu.pack(pady=5, padx=20)

        convert_button = tk.Button(self.root, text="Convert Now", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.convert_currency, relief="raised")
        convert_button.pack(pady=10)

        refresh_button = tk.Button(self.root, text="Refresh Rates", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=self.refresh_rates, relief="raised")
        refresh_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#ffffff")
        self.result_label.pack(pady=10)

    def fetch_exchange_rates(self):
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()['rates']
        except requests.RequestException as e:
            messagebox.showerror("API Error", f"Unable to fetch exchange rates: {e}")
            return {}

    def load_country_data(self):
        return {
            'USD': 'United States Dollar',
            'EUR': 'Euro',
            'JPY': 'Japanese Yen',
            'GBP': 'British Pound Sterling',
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'SEK': 'Swedish Krona',
            'NZD': 'New Zealand Dollar'
        }

    def update_currency_menu(self):
        self.rates = self.fetch_exchange_rates()
        if self.rates:
            sorted_countries = sorted(self.countries.items(), key=lambda item: item[1])
            self.country_menu['values'] = [f"{name} ({code})" for code, name in sorted_countries]
        else:
            self.country_menu['values'] = []

    def refresh_rates(self):
        self.update_currency_menu()
        messagebox.showinfo("Refresh", "Exchange rates updated successfully.")

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            selected_country = self.country_var.get()

            if selected_country == "Select Country":
                raise ValueError("Please select a country.")

            currency_code = selected_country.split('(')[-1].strip(' )')
            if currency_code not in self.rates:
                raise ValueError("Selected currency is not available.")
            
            converted_amount = amount * self.rates[currency_code]
            self.result_label.config(text=f"{amount:.2f} USD = {converted_amount:.2f} {currency_code}")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Conversion Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
