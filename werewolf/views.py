from django.forms import formset_factory
from django.views.generic import FormView, ListView, CreateView
from django.views.generic.edit import CreateView, ModelFormMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django import forms
from .models import Choice, Question, Village, Remark, Resident
from .forms import VillageForm, RemarkForm, ResidentForm
from random import randint

class VillageIndex(CreateView):
    model = Village, Resident
    form_class = VillageForm
    template_name = 'werewolf/index.html'
    success_url = reverse_lazy('werewolf:index')

    def form_valid(self, form):
        form.instance.auther = self.request.user.username
        form.instance.character = '霧雨降る街'
        return super(VillageIndex, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Village.objects.filter(endflag=0).filter(delflag=0).order_by('-created_date')
        return context

def VillageRemarks(request):
    ArticleFormSet = formset_factory(ArticleForm)
    BookFormSet = formset_factory(BookForm)
    if request.method == 'POST':
        article_formset = ArticleFormSet(request.POST, request.FILES, prefix='articles')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if article_formset.is_valid() and book_formset.is_valid():
            # do something with the cleaned_data on the formsets.
            pass
    else:
        article_formset = ArticleFormSet(prefix='articles')
        book_formset = BookFormSet(prefix='books')
    return render(request, 'manage_articles.html', {
        'article_formset': article_formset,
        'book_formset': book_formset,
    })

class VillageResidentForm(CreateView):
    model = Resident
    form_class = ResidentForm
    template_name = 'werewolf/village.html'

    def get_success_url(self):
        return reverse_lazy('werewolf:village', args=(self.kwargs['village_id'],))

    def form_valid(self, form):
        form.instance.resident = self.request.user
        form.instance.village_id = self.kwargs['village_id']
        form.instance.character = randint(1,80)
        return super(VillageRemarks, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['remark_list'] = Remark.objects.filter(village=self.kwargs['village_id']).order_by('-date')
        return context

class VillageRemarkForm(CreateView):
    model = Remark
    form_class = RemarkForm
    template_name = 'werewolf/village.html'

    def get_success_url(self):
        return reverse_lazy('werewolf:village', args=(self.kwargs['village_id'],))

    def form_valid(self, form):
        form.instance.user = self.request.user.username
        form.instance.user_id = self.request.user
        form.instance.village_id = self.kwargs['village_id']
        form.instance.character = randint(1,80)
        form.instance.character_img_url = "rain/" + str(form.instance.character).zfill(2) + ".png"
        return super(VillageRemarks, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['remark_list'] = Remark.objects.filter(village=self.kwargs['village_id']).order_by('-date')
        return context

class VillageLog(ListView):
    model = Village
    template_name = 'werewolf/log.html'
    queryset = Village.objects.filter(endflag=1).filter(delflag=0).order_by('-created_date')

def VillageView(request, village_id):
    if request.method == 'POST':
        if 'remark' in request.POST:
            remark_form = RemarkForm(request.POST)
            if remark_form.is_valid():
                post = remark_form.save(commit=False)
                post.user_id = request.user
                post.user = request.user.username
                post.village_id = village_id
                post.character = Resident.objects.get(village=village_id, resident=request.user).character
                post.character_img_url = "rain/" + str(post.character).zfill(2) + ".png"
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
        elif 'resident' in request.POST:
            resident_form = ResidentForm(request.POST)
            if resident_form.is_valid():
                post = resident_form.save(commit=False)
                post.resident = request.user
                post.village_id = village_id
                post.character_img_url = "rain/" + str(post.character).zfill(2) + ".png"
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))           
    else:
        context = {
            'remark_form': RemarkForm(),
            'resident_form': ResidentForm(),
            'remark_list': Remark.objects.filter(village=village_id).order_by('-date')[:100],
            'resident_list': Resident.objects.filter(village=village_id),
        }
        try:
            context['myselfinfo'] = context['resident_list'].get(resident=request.user)
            context['isResident'] = True
            context['icon_url'] = context['myselfinfo'].character_img_url
        except:
            context['isResident'] = False
            context['icon_url'] =  'rain/01.png'
    return render(request, 'werewolf/village.html', context)

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
