import pandas as pd
import csv

from data_entry import *
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_donnees.csv"
    COLUMNS = [
        "Date",
        "Amount",
        "Category",
        "Description"
    ]

    @classmethod
    def initialise_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=date_format)
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y")

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found in the given range')
        else:
            print(f"Transactions from {start_date.strftime(date_format)} to {end_date.strftime(date_format)}: ")
            print(filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime("%d/%m/%Y")}))

        total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
        total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
        print("\nSummary:")
        print(f"Total Income: €{total_income:.2f}")
        print(f"Total Expense: €{total_expense:.2f}")
        print(f"Net Savings: €{(total_income - total_expense):.2f}")
        return filtered_df

def add():
    CSV.initialise_csv()
    date = get_date("Enter the date of transaction in DD/MM/YYYY format or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df, start_date, end_date):
    df["Date"] = pd.to_datetime(df["Date"], format=date_format)
    df.set_index("Date", inplace=True)

    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    daily_index = pd.date_range(start=start_date, end=end_date, freq="D")
    income_df = df[df["Category"] == "Income"].resample("D")["Amount"].sum().reindex(daily_index, fill_value=0)   #gom dữ liệu lại theo ngày
    expense_df = df[df["Category"] == "Expense"].resample("D")["Amount"].sum().reindex(daily_index, fill_value=0)

    plt.figure(figsize=(12, 8))
    plt.plot(income_df.index, income_df.values, label="Income", color="green")
    plt.plot(expense_df.index, expense_df.values, label="Expense", color="red")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1.Add a new transaction")
        print("2.View transactions and summary within a date range")
        print("3.Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date of transaction in DD/MM/YYYY format: ")
            end_date = get_date("Enter the end date of transaction in DD/MM/YYYY format: ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to view a plot over the date range? (y/n): ").lower() == "y":
                plot_transactions(df, start_date, end_date)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()