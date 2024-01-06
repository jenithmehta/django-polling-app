# pylint: disable=[missing-function-docstring,no-member]
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from polls.models import Question
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # output = ",".join([q.question_text for q in latest_question_list])
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request,"polls/index.html",context)

def detail(request,question_id):
    question_detail = get_object_or_404(Question,pk=question_id)
    return render(request,"polls/detail.html",{'question_detail':question_detail})

def results(request,question_id):
    return HttpResponse(f"You are looking at the results of question {question_id}")

def vote(request,question_id):
    return HttpResponse(f"You are voting on question {question_id}")