from django.shortcuts import render
import requests
from api.views import get_question, check_answer
from rest_framework.test import APIRequestFactory
# Create your views here.
def Index(request):
   try:
      response = get_question(request)
      data = response.data
      question = data.get("question")
      if question:
         context = {
         "question":question,
         "options": data.get("options"),
         "question_id": data.get("question_id"),
         }
      else:
         context = {
            "erorr":"idk what the error is gng.."
         }
      
      return render(request, "shot/main.html", context)

   except requests.exceptions.RequestException as e:
      return render(request, "shot/main.html", {"error": str(e)})


def SubmitAnswer(request):
    if request.method == "POST":
      chose_answer = request.POST.get("choice")
      question_id = request.POST.get("question_id")

      
      factory = APIRequestFactory()
      drf_request = factory.post(
         "/api/submit_answer",
         {"question_id": question_id, "chosen_answer": chose_answer},
         format='json'
      )

      response = check_answer(drf_request)
      result = response.data  

      if result.get("correct") == True:
         return render(request, "shot/result.html", {"content": True})
      else:
         return render(request, "shot/result.html", {"content": False})
    else:
        return render(request, "shot/main.html", {"error": "Unknown error"})