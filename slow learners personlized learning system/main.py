import aiml
from pathlib import Path

GENERAL_QUESTIONS = [
    "Do you often feel confused during lessons?",
    "Do you need more time than others to understand new topics?",
    "Do you struggle to remember what you learned in class?",
    "Do you feel like your classmates finish exercises faster than you?",
]

CONCERN_CHOICES = ["math", "reading", "writing", "attention", "memory", "other"]


def build_kernel() -> aiml.Kernel:
    kernel = aiml.Kernel()
    aiml_file = Path(__file__).resolve().parent / "aiml" / "slow_learners.aiml"
    if not aiml_file.exists():
        raise FileNotFoundError(f"AIML file not found: {aiml_file}")
    kernel.learn(str(aiml_file))
    return kernel


def ask_yes_no(question: str) -> bool:
    while True:
        answer = input(question + " (yes/no): ").strip().lower()
        if answer in {"yes", "y"}:
            return True
        if answer in {"no", "n"}:
            return False
        print("Please answer yes or no.")


def ask_concern() -> str:
    print("\nWhich area is your biggest concern?")
    for choice in CONCERN_CHOICES:
        print(f" - {choice}")
    answer = input("Enter your area of concern: ").strip().lower()
    if answer not in CONCERN_CHOICES:
        print("I will use general remedial advice for your request.")
        return "other"
    return answer


def main() -> None:
    print("Welcome to the Slow Learners Personalized Learning System.")
    print("Answer a few questions and I will help you with study tips.\n")

    kernel = build_kernel()
    print(kernel.respond("HELLO"))

    yes_count = 0
    for question in GENERAL_QUESTIONS:
        if ask_yes_no(question):
            yes_count += 1

    print()
    if yes_count >= 2:
        print(kernel.respond("I AM A SLOW LEARNER"))
        concern = ask_concern()
        response = kernel.respond(concern.upper())
        print("\n" + response)
    else:
        print(kernel.respond("I AM NOT A SLOW LEARNER"))
        print("\n" + kernel.respond("GENERAL TIPS"))

    print("\nKeep practicing and remember that steady effort leads to improvement.")


if __name__ == "__main__":
    main()
