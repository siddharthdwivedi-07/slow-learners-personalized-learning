import aiml
from pathlib import Path
from typing import Final, List

GENERAL_QUESTIONS: Final[List[str]] = [
    "Do you often feel confused during lessons?",
    "Do you need more time than others to understand new topics?",
    "Do you struggle to remember what you learned in class?",
    "Do you feel like your classmates finish exercises faster than you?",
]

CONCERN_CHOICES: Final[List[str]] = ["math", "reading", "writing", "attention", "memory", "other"]

RESOURCE_MAP = {
    "math": [
        {
            "title": "Khan Academy Math",
            "url": "https://www.khanacademy.org/math",
            "description": "Free guided lessons and practice to build stronger math foundations.",
        },
        {
            "title": "Math Is Fun",
            "url": "https://www.mathsisfun.com",
            "description": "Clear explanations and practice problems for important math topics.",
        },
        {
            "title": "IXL Math Practice",
            "url": "https://www.ixl.com/math",
            "description": "Adaptive exercises that help learners review skills step by step.",
        },
    ],
    "reading": [
        {
            "title": "ReadWorks",
            "url": "https://www.readworks.org",
            "description": "AI-curated reading passages with question sets to improve comprehension.",
        },
        {
            "title": "Storyline Online",
            "url": "https://www.storylineonline.net",
            "description": "Engaging audiobook videos that make reading practice enjoyable.",
        },
        {
            "title": "Newsela",
            "url": "https://www.newsela.com",
            "description": "Grade-appropriate articles with built-in supports for stronger reading habits.",
        },
    ],
    "writing": [
        {
            "title": "Purdue OWL Writing Lab",
            "url": "https://owl.purdue.edu",
            "description": "Practical writing advice and examples for essays, sentences, and structure.",
        },
        {
            "title": "Grammarly Blog",
            "url": "https://www.grammarly.com/blog",
            "description": "Writing tips and clear examples for improving clarity and grammar.",
        },
        {
            "title": "Write & Improve",
            "url": "https://writeandimprove.com",
            "description": "Practice writing and get instant feedback to improve over time.",
        },
    ],
    "attention": [
        {
            "title": "Pomofocus Timer",
            "url": "https://pomofocus.io",
            "description": "Use the Pomodoro method to build focus and short study sessions.",
        },
        {
            "title": "Mindful.org",
            "url": "https://www.mindful.org",
            "description": "Simple attention exercises and tips for staying calm and focused.",
        },
        {
            "title": "Simple Study Skills",
            "url": "https://www.understood.org/articles/en/school-learning/partnering-with-child/learning-tools-technology/study-skills",
            "description": "Strategies to reduce distraction and make study time more effective.",
        },
    ],
    "memory": [
        {
            "title": "Quizlet",
            "url": "https://quizlet.com",
            "description": "Use flashcards and spaced repetition exercises to strengthen memory.",
        },
        {
            "title": "Memrise",
            "url": "https://www.memrise.com",
            "description": "Memory-friendly learning techniques with short, repeated drills.",
        },
        {
            "title": "Learning Scientists",
            "url": "https://www.learningscientists.org",
            "description": "Evidence-based memory strategies for learners of all ages.",
        },
    ],
    "other": [
        {
            "title": "Study Skills Guide",
            "url": "https://www.educationcorner.com/study-skills.html",
            "description": "General study strategies that can help any learner build confidence.",
        },
        {
            "title": "Edutopia Learning Tips",
            "url": "https://www.edutopia.org/topic/study-skills",
            "description": "Practical advice and classroom-tested approaches for better habits.",
        },
    ],
    "general": [
        {
            "title": "Khan Academy Study Skills",
            "url": "https://www.khanacademy.org/college-careers-more/learnstorm-growth-mindset",
            "description": "Guidance on building a growth mindset and better study routines.",
        },
        {
            "title": "Coursera Learning How to Learn",
            "url": "https://www.coursera.org/learn/learning-how-to-learn",
            "description": "A popular course about memory, focus, and effective study techniques.",
        },
    ],
}


def recommend_resources(topic: str):
    topic = topic.strip().lower()
    return RESOURCE_MAP.get(topic, RESOURCE_MAP["general"])


def build_kernel() -> aiml.Kernel:
    kernel = aiml.Kernel()
    aiml_file = Path(__file__).resolve().parent / "aiml" / "slow_learners.aiml"
    if not aiml_file.exists():
        raise FileNotFoundError(f"AIML file not found: {aiml_file}")
    kernel.learn(str(aiml_file))
    return kernel
