balance = int(input("Enter your pocket money: "))

total_spent = 0

spending_history = []

while True:

    print("\n===== Pocket Money Tracker =====")
    print("1. Spend Money")
    print("2. Check Balance")
    print("3. View Spending History")
    print("4. Exit")

    choice = input("Choose an option: ")

    # OPTION 1 — Spend Money
    if choice == "1":

        spent = int(input("Enter amount spent: "))

        if spent <= 0:

            print("Please enter a valid amount.")

        elif spent > balance:

            print("Insufficient balance!")

        else:

            balance -= spent

            total_spent += spent

            spending_history.append(spent)

            print("Money spent successfully.")

            print("Remaining Balance:", balance)

            if balance < 1000:
                print("Warning: Your balance is low!")

    # OPTION 2 — Check Balance
    elif choice == "2":

        print("Current Balance:", balance)

        print("Total Spent:", total_spent)

    # OPTION 3 — Spending History
    elif choice == "3":

        if len(spending_history) == 0:

            print("No spending history yet.")

        else:

            print("Spending History:")

            for amount in spending_history:
                print(amount)

    # OPTION 4 — Exit
    elif choice == "4":

        print("Exiting program...")
        break

    # INVALID OPTION
    else:

        print("Invalid option. Try again.")
