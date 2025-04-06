import os
from django.shortcuts import render
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

def homepage(request):
    return render(request, 'core/index.html')

def ai_lesson_planner(request):
    context = {}
    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        topic = request.POST.get("topic", "").strip()
        grade = request.POST.get("grade", "").strip()
        duration = request.POST.get("duration", "").strip()
        learning_objectives = request.POST.get("learning_objectives", "").strip()
        customization = request.POST.get("customization", "").strip()

        if not all([subject, topic, grade, duration, learning_objectives]):
            context["error"] = "Please fill all required fields."
        else:
            prompt = (
                f"Generate a detailed lesson plan for {subject} on {topic} for {grade} students "
                f"lasting {duration}. Learning objectives: {learning_objectives}. "
                f"Customization: {customization}. Return in Markdown format."
            )
            try:
                model = ChatGroq(model="llama3-70b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))
                lesson_plan = (model | StrOutputParser()).invoke(prompt)
                context["lesson_plan"] = lesson_plan
                context["form_data"] = request.POST  # To repopulate form
            except Exception as e:
                context["error"] = f"⚠️ Error generating plan: {str(e)}"

    return render(request, "core/ai_lesson_planner.html", context)

def ai_study_planner(request):
    context = {}
    if request.method == "POST":
        form_data = {
            "grade": request.POST.get("grade", "").strip(),
            "subjects": request.POST.get("subjects", "").strip(),
            "available_days": request.POST.get("available_days", "").strip(),
            "study_hours_per_day": request.POST.get("study_hours_per_day", "").strip(),
            "preferred_study_times": request.POST.get("preferred_study_times", "").strip(),
            "exam_dates": request.POST.get("exam_dates", "").strip(),
            "weak_areas": request.POST.get("weak_areas", "").strip(),
            "customization": request.POST.get("customization", "").strip(),
        }

        required_fields = ["grade", "subjects", "available_days", "study_hours_per_day", "preferred_study_times"]
        if not all(form_data[field] for field in required_fields):
            context["error"] = "Please fill all required fields."
        else:
            prompt = (
                f"Create a study timetable for {form_data['grade']} grade. "
                f"Subjects: {form_data['subjects']}. Available: {form_data['available_days']}. "
                f"Hours/day: {form_data['study_hours_per_day']}. Preferred times: {form_data['preferred_study_times']}. "
                f"{'Exams: ' + form_data['exam_dates'] + '. ' if form_data['exam_dates'] else ''}"
                f"{'Weak areas: ' + form_data['weak_areas'] + '. ' if form_data['weak_areas'] else ''}"
                f"Custom: {form_data['customization']}. Format: Markdown with days, time slots, techniques, and tips."
            )
            try:
                model = ChatGroq(model="llama3-70b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))
                study_plan = (model | StrOutputParser()).invoke(prompt)
                context["study_plan"] = study_plan
                context["form_data"] = form_data
            except Exception as e:
                context["error"] = f"⚠️ Error generating plan: {str(e)}"

    return render(request, "core/ai_study_planner.html", context)