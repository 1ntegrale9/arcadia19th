from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Village, Remark
from .forms import VillageForm, RemarkForm
from random import randint

def index(request):
    if request.method == "POST":
        form = VillageForm(request.POST)
        if form.is_valid():
            village = form.save(commit=False)
            village.character = "霧雨降る街"
            village.save()
            return redirect('werewolf:index')
    else:
        form = VillageForm()
    latest_village_list = Village.objects.order_by('created_date')
    return render(request, 'werewolf/index.html', {'latest_village_list':latest_village_list, 'form':form})

def village(request, village_id):
    if request.method == "POST":
        form = RemarkForm(request.POST)
        if form.is_valid():
            remark = form.save(commit=False)
            remark.village_id = village_id
            remark.character = randint(1,80)
            remark.character_img_url = "rain/" + str(remark.character).zfill(2) + ".png"
            remark.save()
            return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
    else:
        form = RemarkForm()
    remark_list = Remark.objects.filter(village=village_id).order_by('date')
    return render(request, 'werewolf/village.html', {'remark_list':remark_list, 'form':form})

class DetailView(generic.DetailView):
    model = Question
    template_name = 'werewolf/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'werewolf/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'werewolf/detail.html', {
            'question': question,
            'error_message': "投票先を選択してください",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('werewolf:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'werewolf/results.html', {'question': question})
