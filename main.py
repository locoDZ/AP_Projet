from functionFile import *

#this is the main function

def main():
    app = MCQApplication()
    #using clear command of os to clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the Computer Science MCQ!")
    username = input("\nEnter your username: ")

    categories = app.get_categories()
    is_admin = app.is_admin(username)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if app.userExist(username):
            print(f"\nWelcome back, {username}!")
        else:
            print(f"Welcome , {username}!")
        app.display_menu(categories, is_admin)
        choice = app.getMenuChoice(categories, is_admin)
        if choice == len(categories) + 4:  # Exit
            print("\nThank you for using ourS MCQ!")
            break
        elif choice == len(categories) + 2:  # View History
            app.displayHistory(username)
            input("Press Enter to continue...")
        elif choice == len(categories) + 3:  # Export Results
            app.exportResults(username)
        elif is_admin and choice == len(categories) + 5:  # Add Questions
            app.addQuestions()
        else:
            selected_category = None if choice == len(categories) + 1 else categories[choice - 1]
            app.run_test(username, selected_category)


if __name__ == "__main__":
    main()
