import json
from datetime import datetime
import os


class MCQApplication:
    def __init__(self):
        self.users_file = "users.json"
        self.questions_file = "questions.json"
        self.load_users()
        self.load_questions()

    def load_questions(self):
        """Load questions from JSON file."""
        try:
            with open(self.questions_file, 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.questions_file} not found!")
            print("Please ensure the questions file exists in the same directory.")
            exit(1)
        except json.JSONDecodeError:
            print(f"Error: {self.questions_file} is not properly formatted!")
            exit(1)

    def load_users(self):
        """Load users from JSON file or create new file if it doesn't exist."""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()

    def save_users(self):
        """Save users to JSON file."""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def display_history(self, username):
        """Display user's MCQ history."""
        if username in self.users and self.users[username]["history"]:
            print(f"\n{username}'s History:")
            for record in self.users[username]["history"]:
                print(f"- Date: {record['date']}, Category: {record['category']}, "
                      f"Score: {record['score']}/{record['total']}")
        else:
            print("\nNo previous history found.")
        print()

    def get_categories(self):
        """Return available question categories."""
        return list(self.questions.keys())

    def display_menu(self, categories):
        """Display the category selection menu."""
        print("\nAvailable options:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        print(f"{len(categories) + 1}. All Categories")
        print(f"{len(categories) + 2}. View History")
        print(f"{len(categories) + 3}. Export Results")
        print(f"{len(categories) + 4}. Exit")
        print("\nYou can select an option by entering either:")
        print("- The number (e.g., '1')")
        print("- The category name (e.g., 'Python')")
        print("- Commands: 'all', 'history', 'export', 'exit'")

    def get_menu_choice(self, categories):
        """Get user menu choice with support for both numbers and text."""
        valid_commands = {
            'all': len(categories) + 1,
            'history': len(categories) + 2,
            'export': len(categories) + 3,
            'exit': len(categories) + 4
        }

        while True:
            choice = input("\nEnter your choice: ").strip().lower()

            # Try to convert to number if input is numeric
            if choice.isdigit():
                num_choice = int(choice)
                if 1 <= num_choice <= len(categories) + 4:
                    return num_choice

            # Check for text commands
            if choice in valid_commands:
                return valid_commands[choice]

            # Check for category names
            for i, category in enumerate(categories, 1):
                if choice == category.lower():
                    return i

            print("\nInvalid choice. Please enter:")
            print("- A number between 1 and", len(categories) + 4)
            print("- A category name:", ", ".join(categories))
            print("- Or one of:", ", ".join(valid_commands.keys()))

    def run_test(self, username, category=None):
        """Run an MCQ test for the user."""
        if category:
            if category not in self.questions:
                print(f"Error: Category '{category}' not found in questions database!")
                return 0, 0
            questions = self.questions[category]
        else:
            questions = [q for cats in self.questions.values() for q in cats]

        score = 0
        total_questions = len(questions)

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

            is_correct = answer == question['correct_answer']
            if is_correct:
                score += 1
                print("Correct!")
            else:
                correct_option = question['options'][ord(question['correct_answer']) - 97]
                print(f"Incorrect. The correct answer was {question['correct_answer']}) {correct_option}")

        # Save results
        test_record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "score": score,
            "total": total_questions,
            "category": category or "All"
        }

        if username not in self.users:
            self.users[username] = {"history": []}
        self.users[username]["history"].append(test_record)
        self.save_users()

        print(f"\nYour final score: {score}/{total_questions}")
        input("\nPress Enter to continue...")
        return score, total_questions

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


def main():
    app = MCQApplication()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the Computer Science MCQ!")
    username = input("\nEnter your username: ")

    categories = app.get_categories()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nWelcome back, {username}!")
        app.display_menu(categories)

        choice = app.get_menu_choice(categories)

        if choice == len(categories) + 4:  # Exit
            print("\nThank you for using the MCQ application!")
            break
        elif choice == len(categories) + 2:  # View History
            app.display_history(username)
            input("Press Enter to continue...")
        elif choice == len(categories) + 3:  # Export Results
            app.export_results(username)
        else:
            selected_category = None if choice == len(categories) + 1 else categories[choice - 1]
            app.run_test(username, selected_category)


if __name__ == "__main__":
    main()