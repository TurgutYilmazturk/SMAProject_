from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from . import models
from django.shortcuts import get_object_or_404
from django.contrib import messages
import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from praw.models import MoreComments
from django.contrib.auth import get_user_model
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect

reddit = praw.Reddit(
     client_id="J5ECOUqkljDYvQ",
     client_secret="HWN03vk8ykTOEm3zTCTfJShlLsnHrw",
     user_agent="www.turgutcemyilmazturk.com /tubikcan",
     username="tubikcan",
     password="redditicinpass",
 )

sia = SentimentIntensityAnalyzer()

# Create your views here.

class AnalysisView(generic.CreateView):

    fields=('topic',)
    model=models.Analysis

    def form_valid(self,form):
        # if(AnalysisCheck()):
            self.object = form.save(commit=False)
            self.object.analysis_positive=1
            self.object.analysis_neutral=1
            self.object.analysis_negative=1
            self.object.user=self.request.user
            self.object.save()
            return HttpResponseRedirect("results")



class ResultsView(generic.TemplateView):
    template_name="analysis/results.html"


class HistoryView(generic.ListView):
    context_object_name='h_analysis'
    model=models.Analysis

    def get_queryset(self):
        return models.Analysis.objects.filter(user=self.request.user)

def AnalysisCheck():
    pass
