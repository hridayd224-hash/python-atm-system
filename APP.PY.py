import json
from datetime import date


class BankAccount:

    def __init__(self, name, balance, pin):
        self.name = name
        self.balance = balance
        self.pin = pin
        self.daily_limit = 50000
        self.daily_withdrawn = 0
        self.last_date = str(date.today())
        self.history = []

    # Reset daily limit automatically
    def reset_daily_limit(self):
        today = str(date.today())

        if today != self.last_date:
            self.daily_withdrawn = 0
            self.last_date = today
            self.history.append("Daily withdrawal limit reset")

    
    def deposit(self, amount):

        if amount <= 0:
            print("Amount must be positive.\n")
            return

        self.balance += amount
        self.history.append(f"Deposited ₹{amount}")

        print(f"\n₹{amount} deposited successfully.")
        self.check_balance()

    
    def withdraw(self, amount):

        self.reset_daily_limit()

        if amount <= 0:
            print("Amount must be positive.\n")

        elif self.daily_withdrawn + amount > self.daily_limit:

            remaining = self.daily_limit - self.daily_withdrawn

            print(f"Daily limit exceeded.")
            print(f"You can withdraw only ₹{remaining} more today.\n")

        elif amount > self.balance:
            print("Insufficient Balance.\n")

        else:

            self.balance -= amount
            self.daily_withdrawn += amount

            self.history.append(f"Withdrawn ₹{amount}")

            print(f"\n₹{amount} withdrawn successfully.")
            self.check_balance()

            print(
                f"Today's withdrawal: ₹{self.daily_withdrawn}/{self.daily_limit}\n"
            )

    
    def check_balance(self):
        print(f"Current Balance: ₹{self.balance}\n")

   
    def show_history(self):

        print("\n------ Last 5 Transactions ------")

        if len(self.history) == 0:
            print("No transactions yet.")

        else:

            for transaction in self.history[-5:]:
                print(transaction)

        print()




def save_accounts(accounts):

    data = {}

    for name, account in accounts.items():

        data[name] = {
            "balance": account.balance,
            "pin": account.pin,
            "daily_limit": account.daily_limit,
            "daily_withdrawn": account.daily_withdrawn,
            "last_date": account.last_date,
            "history": account.history
        }

    with open("accounts.json", "w") as file:
        json.dump(data, file, indent=4)




def load_accounts():

    accounts = {}

    try:

        with open("accounts.json", "r") as file:
            data = json.load(file)

        for name, info in data.items():

            account = BankAccount(
                name,
                info["balance"],
                info["pin"]
            )

            account.daily_limit = info["daily_limit"]
            account.daily_withdrawn = info["daily_withdrawn"]
            account.last_date = info["last_date"]
            account.history = info["history"]

            accounts[name] = account

    except FileNotFoundError:
        pass

    return accounts




accounts = load_accounts()

while True:

    print("\n========== BANK SYSTEM ==========")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    option = input("Enter choice: ")

   

    if option == "1":

        name = input("Enter Name: ")

        if name in accounts:
            print("Account already exists.\n")
            continue

        balance = float(input("Enter Initial Balance: "))

        while True:

            pin = input("Create 4-digit PIN: ")

            if len(pin) == 4 and pin.isdigit():
                break

            print("PIN must contain exactly 4 digits.")

        accounts[name] = BankAccount(name, balance, pin)

        save_accounts(accounts)

        print("Account created successfully.\n")

    

    elif option == "2":

        name = input("Enter Name: ")

        if name not in accounts:
            print("Account not found.\n")
            continue

        account = accounts[name]

        attempts = 3

        while attempts > 0:

            entered_pin = input("Enter PIN: ")

            if entered_pin == account.pin:
                print(f"\nWelcome {account.name}!\n")
                break

            attempts -= 1

            if attempts > 0:
                print(f"Wrong PIN! Attempts left: {attempts}")

            else:
                print("Account locked for this session.\n")

        if attempts == 0:
            continue

    

        while True:

            print("========== ATM MENU ==========")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Last 5 Transactions")
            print("5. Logout")

            choice = input("Enter choice: ")

            if choice == "1":
                account.check_balance()

            elif choice == "2":

                amount = float(input("Enter Deposit Amount: "))
                account.deposit(amount)
                save_accounts(accounts)

            elif choice == "3":

                amount = float(input("Enter Withdrawal Amount: "))
                account.withdraw(amount)
                save_accounts(accounts)

            elif choice == "4":
                account.show_history()

            elif choice == "5":
                save_accounts(accounts)
                print("Logged out successfully.\n")
                break

            else:
                print("Invalid choice.\n")

   

    elif option == "3":
        save_accounts(accounts)
        print("Thank you for using our ATM!")
        break

    else:
        print("Invalid choice.\n")