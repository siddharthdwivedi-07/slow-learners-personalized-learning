import aiml
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

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


class LearningApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Slow Learners Personalized Learning System")
        self.geometry("560x360")
        self.resizable(False, False)

        self.kernel = build_kernel()
        self.current_question = 0
        self.yes_count = 0

        self.header = tk.Label(self, text="Slow Learners Personalized Learning System", font=("Arial", 14, "bold"))
        self.header.pack(pady=(20, 10))

        self.message = tk.Label(self, text="Welcome! Click Start to begin the learning assessment.", wraplength=520, justify="left", font=("Arial", 11))
        self.message.pack(pady=(0, 20))

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", width=14, command=self.start_assessment)
        self.start_button.grid(row=0, column=0, padx=8)

        self.yes_button = tk.Button(self.button_frame, text="Yes", width=14, command=lambda: self.answer_question(True))
        self.no_button = tk.Button(self.button_frame, text="No", width=14, command=lambda: self.answer_question(False))

        self.choice_var = tk.StringVar(value=CONCERN_CHOICES[0])
        self.choice_menu = tk.OptionMenu(self, self.choice_var, *CONCERN_CHOICES)
        self.submit_choice = tk.Button(self, text="Submit", width=14, command=self.submit_concern)

        self.restart_button = tk.Button(self, text="Restart", width=14, command=self.reset)

    def start_assessment(self) -> None:
        self.start_button.pack_forget()
        self.message.configure(text=self.kernel.respond("HELLO"))
        self.show_question()

    def show_question(self) -> None:
        if self.current_question < len(GENERAL_QUESTIONS):
            self.message.configure(text=GENERAL_QUESTIONS[self.current_question])
            self.yes_button.grid(row=0, column=0, padx=8)
            self.no_button.grid(row=0, column=1, padx=8)
        else:
            self.finish_assessment()

    def answer_question(self, yes: bool) -> None:
        if yes:
            self.yes_count += 1
        self.current_question += 1
        self.show_question()

    def finish_assessment(self) -> None:
        self.yes_button.grid_forget()
        self.no_button.grid_forget()
        if self.yes_count >= 2:
            self.message.configure(text=self.kernel.respond("I AM A SLOW LEARNER"))
            self.choice_menu.pack(pady=16)
            self.submit_choice.pack()
        else:
            self.message.configure(text=self.kernel.respond("I AM NOT A SLOW LEARNER") + "\n\n" + self.kernel.respond("GENERAL TIPS"))
            self.restart_button.pack(pady=16)

    def submit_concern(self) -> None:
        choice = self.choice_var.get().strip().lower()
        if choice not in CONCERN_CHOICES:
            messagebox.showinfo("Notice", "No valid concern selected, showing general advice.")
            choice = "other"
        self.choice_menu.pack_forget()
        self.submit_choice.pack_forget()
        response = self.kernel.respond(choice.upper())
        self.message.configure(text=response)
        self.restart_button.pack(pady=16)

    def reset(self) -> None:
        self.current_question = 0
        self.yes_count = 0
        self.message.configure(text="Welcome! Click Start to begin the learning assessment.")
        self.restart_button.pack_forget()
        self.start_button.pack()


if __name__ == "__main__":
    app = LearningApp()
    app.mainloop()
