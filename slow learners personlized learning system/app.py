from flask import Flask, render_template, request
from aiml_engine import build_kernel, CONCERN_CHOICES, GENERAL_QUESTIONS, recommend_resources

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

kernel = build_kernel()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = [request.form.get(f"question_{i}", "no") for i in range(len(GENERAL_QUESTIONS))]
        yes_count = sum(1 for answer in answers if answer.lower() in {"yes", "y"})

        if yes_count >= 2:
            return render_template(
                "concern.html",
                title="Personalized Support",
                concern_choices=CONCERN_CHOICES,
            )

        resources = recommend_resources("general")
        return render_template(
            "result.html",
            title="Improvement Tips",
            heading="General Learning Tips",
            message=kernel.respond("I AM NOT A SLOW LEARNER") + "\n\n" + kernel.respond("GENERAL TIPS"),
            resources=resources,
            show_restart=True,
        )

    return render_template(
        "index.html",
        title="Slow Learners Personalized Learning System",
        questions=GENERAL_QUESTIONS,
    )


@app.route("/concern", methods=["POST"])
def concern():
    choice = request.form.get("concern", "other").strip().lower()
    if choice not in CONCERN_CHOICES:
        choice = "other"

    response = kernel.respond(choice.upper())
    resources = recommend_resources(choice)
    topic_name = choice.capitalize()
    return render_template(
        "result.html",
        title="Remedial Advice",
        heading=f"Remedial Learning Support for {topic_name}",
        message=response,
        resources=resources,
        topic_name=topic_name,
        show_restart=True,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
