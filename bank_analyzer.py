import pdfplumber
import pandas as pd
import re
import matplotlib.pyplot as plt

def display_banner():
    print("\n==================================================")
    print("  E N J L E E Z  Bank Analyzer v1.0")
    print("==================================================")
    print("   Developed by: E N J L E E Z (@enjleez) ")
    print("   Facebook | Twitter | Instagram: @enjleez")
    print("==================================================\n")

def extract_transactions(pdf_path):
    print("[+] Reading PDF:", pdf_path)
    transactions = []

    # Regex قابل للتعديل حسب شكل كشف البنك
    pattern = re.compile(
        r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(-?\d+\.\d{2})\s+(-?\d+\.\d{2})"
    )

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for match in pattern.findall(text):
                date, desc, amount, balance = match
                transactions.append({
                    "Date": date,
                    "Description": desc.strip(),
                    "Amount": float(amount),
                    "Balance": float(balance)
                })

    return pd.DataFrame(transactions)


def analyze_data(df):
    print("\n=== Bank Statement Summary ===\n")

    total_income = df[df["Amount"] > 0]["Amount"].sum()
    total_expense = df[df["Amount"] < 0]["Amount"].sum()
    largest_expense = df[df["Amount"] < 0]["Amount"].min()

    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expenses: {total_expense:.2f}")
    print(f"Largest Single Expense: {largest_expense:.2f}")

    df["Type"] = df["Amount"].apply(lambda x: "Income" if x > 0 else "Expense")

    # رسم بياني
    df.groupby("Type")["Amount"].sum().plot(kind="bar")
    plt.title("Income vs Expenses")
    plt.ylabel("Amount")
    plt.show()


def main():
    display_banner()
    pdf_path = input("Enter the full path of your bank statement PDF: ")

    df = extract_transactions(pdf_path)

    if df.empty:
        print("[!] No transactions detected. Try adjusting your regex for your bank format.")
        return

    print("\n[+] Extracted Transactions Preview:")
    print(df.head())

    analyze_data(df)

    output = "bank_analysis.xlsx"
    df.to_excel(output, index=False)
    print(f"\n[+] Exported full analysis to {output}")


if __name__ == "__main__":
    main()
