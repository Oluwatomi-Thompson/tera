"""
No WTForm here on purpose: a quiz's question count is dynamic (driven by
whatever's in the lesson's .md file), so the quiz form is rendered directly
from `lesson.questions` in templates/lessons/quiz.html and parsed from raw
`request.form` in routes.py (`submit_quiz`) instead of a fixed WTForms class.
"""
