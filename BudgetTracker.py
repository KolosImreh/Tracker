import sqlite3

class BudgetTracker:
    def __init__(self, db_name):
        try:
            # Establish connection to the database
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # Create necessary tables if they don't exist
            self.create_tables()
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def create_tables(self):
        try:
            # Create tables for expenses, income, budgets, and financial goals
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                    id INTEGER PRIMARY KEY,
                                    category TEXT,
                                    amount REAL
                                )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                                    id INTEGER PRIMARY KEY,
                                    category TEXT,
                                    amount REAL
                                )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                                    id INTEGER PRIMARY KEY,
                                    category TEXT,
                                    budget REAL
                                )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS financial_goals (
                                    id INTEGER PRIMARY KEY,
                                    goal TEXT,
                                    progress REAL
                                )''')
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating tables:", e)

    def add_expense(self, category, amount):
        try:
            # Insert a new expense record into the expenses table
            self.cursor.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, amount))
            self.conn.commit()
            print("Expense added successfully.")
        except sqlite3.Error as e:
            print("Error adding expense:", e)

    def update_expense(self, category, new_amount):
        try:
            # Update the amount of an expense for a specific category
            self.cursor.execute("UPDATE expenses SET amount=? WHERE category=?", (new_amount, category))
            self.conn.commit()
            print("Expense updated successfully.")
        except sqlite3.Error as e:
            print("Error updating expense:", e)

    def delete_expense_category(self, category):
        try:
            # Delete all expenses associated with a specific category
            self.cursor.execute("DELETE FROM expenses WHERE category=?", (category,))
            self.conn.commit()
            print("Expense category deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting expense category:", e)

    def view_categories(self, table):
        try:
            # View all unique categories from either expenses or income table
            if table == "expenses":
                self.cursor.execute("SELECT DISTINCT category FROM expenses")
            elif table == "income":
                self.cursor.execute("SELECT DISTINCT category FROM income")
            categories = self.cursor.fetchall()
            categories = [category[0] for category in categories]
            return categories
        except sqlite3.Error as e:
            print("Error viewing categories:", e)
            return []

    def track_spending(self):
        try:
            # Sum up expenses for each category
            self.cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
            spending = self.cursor.fetchall()
            return spending
        except sqlite3.Error as e:
            print("Error tracking spending:", e)
            return []

    def track_income(self):
        try:
            # Sum up income for each category
            self.cursor.execute("SELECT category, SUM(amount) FROM income GROUP BY category")
            income = self.cursor.fetchall()
            return income
        except sqlite3.Error as e:
            print("Error tracking income:", e)
            return []

    def calculate_budget(self):
        try:
            # Calculate total budget by subtracting total expenses from total income
            total_income = sum([item[1] for item in self.track_income()])
            total_expenses = sum([item[1] for item in self.track_spending()])
            budget = total_income - total_expenses
            return budget
        except sqlite3.Error as e:
            print("Error calculating budget:", e)
            return None

    def close_connection(self):
        try:
            # Close the database connection
            self.conn.close()
            print("Database connection closed.")
        except sqlite3.Error as e:
            print("Error closing database connection:", e)

    # Additional methods for managing income, budgets, and financial goals...
    def add_income(self, category, amount):
        try:
            # Insert a new income record into the income table
            self.cursor.execute("INSERT INTO income (category, amount) VALUES (?, ?)", (category, amount))
            self.conn.commit()
            print("Income added successfully.")
        except sqlite3.Error as e:
            print("Error adding income:", e)

    def add_income_category(self, category):
        try:
            # Insert a new income category
            self.cursor.execute("INSERT INTO income (category, amount) VALUES (?, ?)", (category, 0.0))
            self.conn.commit()
            print("Income category added successfully.")
        except sqlite3.Error as e:
            print("Error adding income category:", e)

    def view_expenses_by_category(self, category):
        try:
            # View expenses for a specific category
            self.cursor.execute("SELECT * FROM expenses WHERE category=?", (category,))
            expenses = self.cursor.fetchall()
            return expenses
        except sqlite3.Error as e:
            print("Error viewing expenses by category:", e)
            return []

    def delete_income_category(self, category):
        try:
            # Delete all income records associated with a specific category
            self.cursor.execute("DELETE FROM income WHERE category=?", (category,))
            self.conn.commit()
            print("Income category deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting income category:", e)

    def view_income_by_category(self, category):
        try:
            # View income for a specific category
            self.cursor.execute("SELECT * FROM income WHERE category=?", (category,))
            income = self.cursor.fetchall()
            return income
        except sqlite3.Error as e:
            print("Error viewing income by category:", e)
            return []

    def set_budget(self, category, budget):
        try:
            # Set budget for a specific category
            self.cursor.execute("INSERT INTO budgets (category, budget) VALUES (?, ?)", (category, budget))
            self.conn.commit()
            print("Budget for category '{}' set successfully.".format(category))
        except sqlite3.Error as e:
            print("Error setting budget:", e)

    def view_budget(self, category):
        try:
            # View budget for a specific category
            self.cursor.execute("SELECT budget FROM budgets WHERE category=?", (category,))
            budget = self.cursor.fetchone()
            if budget:
                return budget[0]
            else:
                return None
        except sqlite3.Error as e:
            print("Error viewing budget:", e)
            return None

    def set_financial_goal(self, goal):
        try:
            # Set a financial goal
            self.cursor.execute("INSERT INTO financial_goals (goal, progress) VALUES (?, ?)", (goal, 0.0))
            self.conn.commit()
            print("Financial goal '{}' set successfully.".format(goal))
        except sqlite3.Error as e:
            print("Error setting financial goal:", e)

    def view_financial_goals(self):
        try:
            # View all financial goals
            self.cursor.execute("SELECT * FROM financial_goals")
            goals = self.cursor.fetchall()
            return goals
        except sqlite3.Error as e:
            print("Error viewing financial goals:", e)
            return []

    def update_goal_progress(self, goal_id, progress):
        try:
            # Update progress towards a financial goal
            self.cursor.execute("UPDATE financial_goals SET progress=? WHERE id=?", (progress, goal_id))
            self.conn.commit()
            print("Progress towards goal updated successfully.")
        except sqlite3.Error as e:
            print("Error updating goal progress:", e)

def main():
    # Set up the BudgetTracker instance with the database name
    db_name = "budget_tracker.db"
    budget_tracker = BudgetTracker(db_name)

    # Display the menu and handle user inputs
    while True:
        print("\nBudget Tracker Menu:")
        print("1. Add expense")
        print("2. Update an expense amount")
        print("3. Delete an expense category")
        print("4. View expenses")
        print("5. View expenses by category")
        print("6. Add income")
        print("7. Add income categories")
        print("8. Delete an income category")
        print("9. View income")
        print("10. View income by category")
        print("11. View expense or income categories")
        print("12. Track spending")
        print("13. Track income")
        print("14. Calculate budget")
        print("15. Set budget for a category")
        print("16. View budget for a category")
        print("17. Set financial goals")
        print("18. View progress towards financial goals")
        print("19. Update goal progress")
        print("20. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            budget_tracker.add_expense(category, amount)
        elif choice == "2":
            category = input("Enter expense category to update: ")
            new_amount = float(input("Enter new expense amount: "))
            budget_tracker.update_expense(category, new_amount)
        elif choice == "3":
            category = input("Enter expense category to delete: ")
            budget_tracker.delete_expense_category(category)
        elif choice == "4":
            print("Expenses:")
            expenses = budget_tracker.track_spending()
            for expense in expenses:
                print(expense)
        elif choice == "5":
            category = input("Enter category to view expenses: ")
            expenses = budget_tracker.view_expenses_by_category(category)
            for expense in expenses:
                print(expense)
        elif choice == "6":
            category = input("Enter income category: ")
            amount = float(input("Enter income amount: "))
            budget_tracker.add_income(category, amount)
        elif choice == "7":
            category = input("Enter income category to add: ")
            budget_tracker.add_income_category(category)
        elif choice == "8":
            category = input("Enter income category to delete: ")
            budget_tracker.delete_income_category(category)
        elif choice == "9":
            print("Income:")
            income = budget_tracker.track_income()
            for item in income:
                print(item)
        elif choice == "10":
            category = input("Enter category to view income: ")
            income = budget_tracker.view_income_by_category(category)
            for item in income:
                print(item)
        elif choice == "11":
            table_choice = input("Enter 'expenses' or 'income' to view categories: ")
            categories = budget_tracker.view_categories(table_choice)
            print("Categories:", categories)
        elif choice == "12":
            spending = budget_tracker.track_spending()
            print("Spending:")
            for item in spending:
                print(item)
        elif choice == "13":
            income = budget_tracker.track_income()
            print("Income:")
            for item in income:
                print(item)
        elif choice == "14":
            budget = budget_tracker.calculate_budget()
            if budget is not None:
                print("Budget:", budget)
        elif choice == "15":
            category = input("Enter category to set budget: ")
            budget = float(input("Enter budget amount: "))
            budget_tracker.set_budget(category, budget)
        elif choice == "16":
            category = input("Enter category to view budget: ")
            budget = budget_tracker.view_budget(category)
            if budget:
                print("Budget for category {}: {}".format(category, budget))
            else:
                print("No budget set for category", category)
        elif choice == "17":
            goal = input("Enter financial goal: ")
            budget_tracker.set_financial_goal(goal)
        elif choice == "18":
            goals = budget_tracker.view_financial_goals()
            for goal in goals:
                print(goal)
        elif choice == "19":
            goal_id = int(input("Enter goal ID: "))
            progress = float(input("Enter progress towards goal: "))
            budget_tracker.update_goal_progress(goal_id, progress)
        elif choice == "20":
            budget_tracker.close_connection()
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 20.")

# Check if the script is being run directly
if __name__ == "__main__":
    main()