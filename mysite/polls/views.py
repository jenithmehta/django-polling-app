# pylint: disable=[missing-function-docstring,no-member,missing-class-docstring ]
from typing import Any
from django.utils import timezone
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from polls.models import Question, Choice
from django.views import generic
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "latest_question_list"
    def get_queryset(self) -> QuerySet[Any]:
        "Returns last five questions"
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    template_name = "polls/detail.html"
    model = Question
    context_object_name = "question"
    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lte=timezone.now(),id=self.kwargs["pk"])

class ResultsView(generic.DetailView):
    template_name = "polls/results.html"
    model = Question
    context_object_name = "question"


def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    