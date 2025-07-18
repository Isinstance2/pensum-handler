from pensum_handler import PensumHandler
from pensum_handler import logging

if __name__ == "__main__":
    print("Welcome to your uni logs!!:")
    uni = PensumHandler()
    uni.completed_summary()

    while True:
        user_input = input("Would you like to update a completed class? (y/n): ").strip().lower()

        if user_input == 'y':
            course_input = input("Type course name: ").strip()
            results = uni.get_code(course_input)

            if not results:
                print("❌ Course not found. Try again.")
                continue

            # If multiple results, show options to the user
            if len(results) > 1:
                print("⚠️ Multiple courses found:")
                for idx, (code, name) in enumerate(results, 1):
                    print(f"{idx}. {name} ({code})")

                try:
                    choice = int(input("Select a course by number: "))
                    code = results[choice - 1][0]
                except (ValueError, IndexError):
                    print("❌ Invalid choice.")
                    continue
            else:
                code = results[0][0]

            month = input(f"Enter month (YYYY-MM) for {code}: ").strip()
            
            try:
                score = int(input("Enter score: ").strip())
            except ValueError:
                print("❌ Score must be a number.")
                continue

            uni.mark_completed(code, month, score)
            logging.info(f"✅ Course {code} has been marked as completed!")

        elif user_input == 'n':
            print("👋 Exiting update loop.")
            break

        else:
            print("❗Please enter 'y' or 'n'.")

    





