from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)


def course_chat(course_title, lesson_title, lesson_content, question):
    prompt = f"""
You are an AI assistant helping a student.

Course: {course_title}
Lesson: {lesson_title}

Lesson Content:
{lesson_content}

Student Question:
{question}

Explain clearly and simply.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


def generate_summary(lesson_content):
    prompt = f"""
Summarize this lesson in clear bullet points:

{lesson_content}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


def generate_quiz(lesson_content):
    prompt = f"""
Create 5 multiple choice questions from this lesson.
Provide:
- Question
- 4 options
- Correct answer clearly marked

Lesson:
{lesson_content}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text