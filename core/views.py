import os
from django.shortcuts import render
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser


# Create your views here.
def homepage(request):
    return render(request, 'core/index.html')

# Load environment variables
load_dotenv()

def ai_lesson_planner(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        topic = request.POST.get("topic")
        grade = request.POST.get("grade")
        duration = request.POST.get("duration")
        learning_objectives = request.POST.get("learning_objectives")
        customization = request.POST.get("customization")

        if not all([subject, topic, grade, duration, learning_objectives]):
            return render(request, "core/ai_lesson_planner.html", {"error": "Please fill all required fields."})

        # Construct AI prompt
        prompt = (
            f"Generate a detailed lesson plan for the subject of {subject} on the topic of {topic}. "
            f"This lesson is intended for {grade} students and will last for {duration}. "
            f"The following are the learning objectives: {learning_objectives}. "
            f"Return the results as Markdown and don't return class size. "
            f"This is how the user wants the plan to be customized: {customization}. "
        )

        try:
            model = ChatGroq(model="llama3-70b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))
            parser = StrOutputParser()
            output = model | parser
            lesson_plan = output.invoke(prompt)
        except Exception as e:
            lesson_plan = f"⚠️ Error: {str(e)}"

        return render(request, "core/ai_lesson_planner.html", {"lesson_plan": lesson_plan})

    return render(request, "core/ai_lesson_planner.html")