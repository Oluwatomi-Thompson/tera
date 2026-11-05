// Intentionally unused: quizzes are submitted as a plain HTML form POST to
// /lessons/<slug>/quiz (see app/lessons/routes.py:submit_quiz), graded
// server-side, and the result page is server-rendered. That keeps "did my
// quiz submission actually save?" simple and reliable, with no JS required
// to complete a lesson. If quiz-taking ever needs a JS-driven experience
// (instant per-question feedback, no page reload), build it against the
// existing route — it already returns a normal HTML page, so adding a
// fetch()-based flow here would mean adding a JSON variant of that route
// too, which isn't worth it for the MVP.
