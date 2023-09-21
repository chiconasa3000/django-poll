from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
from django.shortcuts import render, get_object_or_404

# Create your views here. oversight the questions
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    
    # template = loader.get_template("polls/index.html")
    # context = {
    #     "latest_question_list": latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

# details about the page
# it alway receive a request from the user
def detail(request, question_id):
    # high coupled
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Questino does not exist")
    # return render(request,"polls/detail.html", {"question": question})

    # low coupled
    question = get_object_or_404(Question,pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


# results from the page
def results(request, question_id):
    response = "You are looking as the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You are voting on question %s." % question_id)
