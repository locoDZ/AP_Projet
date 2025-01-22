import json
from datetime import datetime
import os
import random

class MCQApplication:
    def __init__(self):
        self.usersf = "users.json"
        self.questionsf = "questions.json"
        self.admins = ["riad", "fouad","youcef","admin"]  # list of admins
        self.load_users()
        self.load_questions()

    #function for admin to add questions to a specific category.
    def addQuestions(self):
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

    def save_questions(self):
        with open(self.questionsf, 'w') as f:
            json.dump(self.questions, f, indent=4)


    def is_admin(self, username):
        return username in self.admins

    def load_questions(self):
        with open(self.questionsf, 'r') as f:  # Changed from self.questions
            self.questions = json.load(f)

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
    def userExist(self, username):
            with open(self.usersf, 'r') as file:
                users = json.load(file)
            return username in users

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

    #Run an MCQ test for the user

    def run_test(self, username, category=None):
        # Initialize questions based on category
        if category:
            if category not in self.questions:
                print(f"Error: Category '{category}' not found in questions database!")
                return 0, 0
            questions = self.questions[category]
        else:
            questions = [q for cats in self.questions.values() for q in cats]

        # Calculate total available questions
        total_available = len(questions)

        # Let user choose number of questions
        while True:
            try:
                desired_count = input(f"\nHow many questions would you like to answer? (1-{total_available}): ").strip()
                desired_count = int(desired_count)
                if 1 <= desired_count <= total_available:
                    break
                print(f"Please enter a number between 1 and {total_available}.")
            except ValueError:
                print("Please enter a valid number.")

        selected_questions = random.sample(questions, desired_count)

        score = 0
        total_questions = len(selected_questions)

        print(f"\nStarting quiz for category: {category or 'All Categories'}")
        print(f"Answering {desired_count} out of {total_available} available questions")

        for i, question in enumerate(selected_questions, 1):
            print(f"\nQuestion {i}: {question['question']}")
            for j, option in enumerate(question['options'], 97):  # 97 is ASCII for 'a'
                print(f"{chr(j)}) {option}")
            while True:
                answer = input("Answer: ").lower()
                if answer in ['a', 'b', 'c']:
                    break
                print("Please enter a, b, or c.")

            # Test correct
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

        # Checking if user has history to update it
        if username not in self.users:
            self.users[username] = {"history": []}
        self.users[username]["history"].append(test_record)
        self.saveUsers()

        print(f"\nYour final score is: {score}/{total_questions}")
        input("\nPress Enter to continue..")
    def displayHistory(self, username):

        if username in self.users and self.users[username]["history"]:
            print(f"\n{username}'s History:")
            for record in self.users[username]["history"]:
                print(f"- Date: {record['date']}, Category: {record['category']}, "
                      f"Score: {record['score']}/{record['total']}")
        else:
            print("\nNo previous history found.")
        print()

    def exportResults(self, username):
        """Export user's results to a CSV file."""
        if username not in self.users:
            print("User not found.")
            return
        filename = f"{username}_results.csv"
        with open(filename, 'w') as f:
            f.write("Date,Score,Total Questions,Catigory\n")
            for record in self.users[username]["history"]:
                f.write(f"{record['date']},{record['score']},{record['total']},{record['category']}\n")
        print(f"\nResults exported to {filename}")
        input("\nPress Enter to continue...")

