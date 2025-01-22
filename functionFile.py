import json
from datetime import datetime
import os


class MCQApplication:
    def __init__(self):
        self.usersf = "users.json"
        self.questions = "questions.json"
        self.admins = ["riad", "fouad","youcef","admin"]  # list of admins
        self.load_users()
        self.load_questions()

    #function for admin to add questions to a specific category.
    def add_questions(self):
        print("\nAdding Questions:")
        categories = self.get_categories()

        # Display available categories
        print("\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        # Select a category
        while True:
            choice = input("\nSelect a category by number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(categories):
                category = categories[int(choice) - 1]
                break
            print("Invalid choice. Please select a valid category number.")
        # Add questions to the selected category
        while True:
            print(f"\nAdding a new question to the category: {category}")
            question = input("Enter the question: ").strip()
            options = []
            for opt in ["a", "b", "c"]:
                options.append(input(f"Enter option {opt}: ").strip())
            correct_answer = input("Enter the correct answer (a, b, or c): ").strip().lower()


            if correct_answer not in ['a', 'b', 'c']:
                print("Invalid correct answer. It must be 'a', 'b', or 'c'.")
                continue
            # Add the new question to the selected category
            new_question = {
                "question": question,
                "options": options,
                "correct_answer": correct_answer
            }
            self.questions[category].append(new_question)
            self.save_questions()
            print("\nQuestion added successfully!")
            choice = input("Do you want to add another question? (yes/no): ").strip().lower()
            if choice != "yes":
                break
    #Save questions to JSON file.
    def save_questions(self):
        with open(self.questions, 'w') as f:
            json.dump(self.questions, f, indent=4)
    #Check if the user is an admin.
    def is_admin(self, username):
        return username in self.admins

    def load_questions(self): #Load questions from JSON file.
        try:
            with open(self.questions, 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.questions} not found!")
            print("Please ensure the questions file exists in the same directory.")
            exit(1)
        except json.JSONDecodeError:
            print(f"Error: {self.questions} is not properly formatted!")
            exit(1)
    #Load users from JSON file or create new file if it doesn't exist.
    def load_users(self):
        if os.path.exists(self.usersf):
            with open(self.usersf, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.saveusers()
    #Save users to JSON file.
    def saveUsers(self):
        with open(self.usersf, 'w') as f:
            json.dump(self.users, f, indent=4)
    def displayHistory(self, username):
        """Display user's MCQ history."""
        if username in self.users and self.users[username]["history"]:
            print(f"\n{username}'s History:")
            for record in self.users[username]["history"]:
                print(f"- Date: {record['date']}, Category: {record['category']}, "
                      f"Score: {record['score']}/{record['total']}")
        else:
            print("\nNo previous history found.")
        print()
    #Return available question categories."""
    def get_categories(self):
        return list(self.questions.keys())

    def display_menu(self, categories, is_admin=False):
        """Display the category selection menu."""
        print("\nAvailable options:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        print(f"{len(categories) + 1}. All Categories")
        print(f"{len(categories) + 2}. View History")
        print(f"{len(categories) + 3}. Export Results")
        print(f"{len(categories) + 4}. Exit")
        if is_admin:
            print(f"{len(categories) + 5}. Add Questions")
        print("\nYou can select an option by entering either:")
        print("- The number (e.g., '1')")
        print("- The category name (e.g., 'Python')")
        print("- Commands: 'all', 'history', 'export', 'exit'")

    def getMenuChoice(self, categories, is_admin=False):
        """Get user menu choice with support for both numbers and text."""
        valid_commands = {
            'all': len(categories) + 1,
            'history': len(categories) + 2,
            'export': len(categories) + 3,
            'exit': len(categories) + 4
        }
        if is_admin:
            valid_commands['add'] = len(categories) + 5
        while True:
            choice = input("\nEnter your choice: ").strip().lower()
            if choice.isdigit():
                num_choice = int(choice)
                if 1 <= num_choice <= len(categories) + (5 if is_admin else 4):
                    return num_choice
            if choice in valid_commands:
                return valid_commands[choice]
            for i, category in enumerate(categories, 1):
                if choice == category.lower():
                    return i

            print("\nInvalid choice. Please enter:")
            print("- A number between 1 and", len(categories) + (5 if is_admin else 4))
            print("- A category name:", ", ".join(categories))
            print("- Or one of:", ", ".join(valid_commands.keys()))
    #Run an MCQ test for the user.
    def run_test(self, username, category=None):
      #checking if categorie exist and doing test on categorie
        if category:
            if category not in self.questions:
                print(f"Error: Category '{category}' not found in questions database!")
                return 0, 0
            questions = self.questions[category]
        else:
            questions = [q for cats in self.questions.values() for q in cats]

        score = 0
        total_questions = len(questions)
        #doing all categories
        print(f"\nStarting quiz for category: {category or 'All Categories'}")
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}: {question['question']}")
            for j, option in enumerate(question['options'], 97):  # 97 is ASCII for 'a'
                print(f"{chr(j)}) {option}")
            while True:
                answer = input("Answer: ").lower()
                if answer in ['a', 'b', 'c']:
                    break
                print("Please enter a, b, or c.")
            #test correct
            is_correct = answer == question['correct_answer']
            if is_correct:
                score += 1
                print("Correct!")
            else:
                correct_option = question['options'][ord(question['correct_answer']) - 97]
                print(f"Incorrect. The correct answer was {question['correct_answer']}) {correct_option}")
        test_record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "score": score,
            "total": total_questions,
            "category": category or "All"
        }
      #cheking if user have history to update it
        if username not in self.users:
            self.users[username] = {"history": []}
        self.users[username]["history"].append(test_record)
        self.save_users()

        print(f"\nYour final score: {score}/{total_questions}")
        input("\nPress Enter to continue...")
        return score, total_questions
    #cvs handling file
    def export_results(self, username):
        """Export user's results to a CSV file."""
        if username not in self.users:
            print("User not found.")
            return
        filename = f"{username}_results.csv"
        with open(filename, 'w') as f:
            f.write("Date,Score,Total Questions,Category\n")
            for record in self.users[username]["history"]:
                f.write(f"{record['date']},{record['score']},{record['total']},{record['category']}\n")
        print(f"\nResults exported to {filename}")
        input("\nPress Enter to continue...")
 # check user existance
    def user_exist(self, username):
        try:
            with open(self.usersf, 'r') as file:
                users = json.load(file)
            return username in users
        except FileNotFound:
            print("The file users.json does not exist.")
            return False

