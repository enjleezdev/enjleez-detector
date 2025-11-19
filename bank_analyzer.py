#!/usr/bin/env python3
import pdfplumber
import pandas as pd
import re
import os

def display_banner():
    print("\n==================================================")
    print("  E N J L E E Z  Bank Analyzer v1.0")
    print("==================================================")
    print("   Developed by: E N J L E E Z (@enjleez) ")
    print("   Facebook | Twitter | Instagram: @enjleez")
    print("==================================================\n")

def extract_transactions(pdf_path):
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            i = 0
            while i < len(lines):
                line = lines[i]
                # تحقق من وجود تاريخ في بداية السطر
                match = re.match(r'(\d{4}/\d{2}/\d{2})', line)
                if match:
                    date = match.group(1)
                    description_lines = [line[len(date):].strip()]
                    # جمع أسطر الوصف حتى السطر الذي يحتوي على الأرقام
                    j = i + 1
                    while j < len(lines) and not re.search(r'(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})', lines[j]):
                        description_lines.append(lines[j])
                        j += 1
                    # السطر j يحتوي على Debit/Credit/Balance
                    if j < len(lines):
                        amounts_line = lines[j]
                        amounts_match = re.search(r'(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})', amounts_line)
                        if amounts_match:
                            debit, credit, balance = amounts_match.groups()
                            description = ' '.join(description_lines).replace('**', ' ').replace('\n',' ').strip()
                            transactions.append([date, description, debit, credit, balance])
                    i = j
                i += 1

    df = pd.DataFrame(transactions, columns=['Date', 'Description', 'Debit', 'Credit', 'Balance'])
    return df

def main():
    display_banner()
    pdf_path = input("Enter the full path of your bank statement PDF: ").strip()
    
    if not os.path.isfile(pdf_path):
        print(f"[!] File not found: {pdf_path}")
        return
    
    print(f"[+] Reading PDF: {pdf_path}")
    df = extract_transactions(pdf_path)

    if df.empty:
        print("[!] No transactions detected. Check your PDF format.")
        return
    
    output_file = "bank_statement_output.xlsx"
    df.to_excel(output_file, index=False)
    print(f"[+] Transactions exported successfully to: {output_file}")

if __name__ == "__main__":
    main()
