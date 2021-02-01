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
from django import template
from prawcore import NotFound


register = template.Library()
reddit = praw.Reddit(
     client_id="bZHFNA6gZjvG_Q",
     client_secret="1l-pgLeHaR-D66hrm4m58DZHpiZBkQ",
     user_agent="www.turgutcemyilmazturk.com by /tubikcan",

 )

sia = SentimentIntensityAnalyzer()

# Create your views here.

class AnalysisView(generic.CreateView):

    fields=('topic','limit','time_filter')
    model=models.Analysis

    def form_valid(self,form):

            self.object = form.save(commit=False)
            global reddit
            top_posts = reddit.subreddit(self.object.topic).top(self.object.time_filter, limit=self.object.limit)
            try:
                result_dict=AnalysisDone(top_posts)
            except NotFound:
                return HttpResponse("<h1>Hatalı<h1>")

            if(result_dict['positive']==0 and result_dict['negative']==0 and result_dict['neutral'] <5):
                return HttpResponseRedirect("<h1>Hatalı<h1>")

            else:
                self.object.user=self.request.user
                self.object.analysis_neutral=result_dict['neutral']
                self.object.analysis_negative=result_dict['negative']
                self.object.analysis_positive=result_dict['positive']
                self.object.save()
                return HttpResponseRedirect("results")






class ResultsView(generic.TemplateView):
    template_name="analysis/results.html"


class HistoryView(generic.ListView):
    context_object_name='h_analysis'
    model=models.Analysis

    def get_queryset(self):
        return models.Analysis.objects.filter(user=self.request.user)


def AnalysisDone(top_posts):
    for submission in top_posts:
        sub_entries_nltk = {'negative': 0, 'positive' : 0, 'neutral' : 0}
        nltk_sentiment(submission.title, sub_entries_nltk)
        submission_comm = reddit.submission(id=submission.id)

        for count, top_level_comment in enumerate(submission_comm.comments):
            count_comm = 0
            try :
                nltk_sentiment(top_level_comment.body, sub_entries_nltk)
                replies_of(top_level_comment,
                           count_comm,
                           sub_entries_nltk)
            except:
                continue

        return sub_entries_nltk


def nltk_sentiment(review, sub_entries_nltk):
    vs = sia.polarity_scores(review)
    if not vs['neg'] > 0.05:
        if vs['pos'] - vs['neg'] > 0:
            sub_entries_nltk['positive'] = sub_entries_nltk['positive'] + 1
            return 'Positive'
        else:
            sub_entries_nltk['neutral'] = sub_entries_nltk['neutral'] + 1
            return 'Neutral'

    elif not vs['pos'] > 0.05:
        if vs['pos'] - vs['neg'] <= 0:
            sub_entries_nltk['negative'] = sub_entries_nltk['negative'] + 1
            return 'Negative'
        else:
            sub_entries_nltk['neutral'] = sub_entries_nltk['neutral'] + 1
            return 'Neutral'
    else:
        sub_entries_nltk['neutral'] = sub_entries_nltk['neutral'] + 1
        return 'Neutral'


def replies_of(top_level_comment, count_comment, sub_entries_textblob, sub_entries_nltk):
    if len(top_level_comment.replies) == 0:
        count_comment = 0
        return
    else:
        for num, comment in enumerate(top_level_comment.replies):
            try:
                count_comment += 1
                nltk_sentiment(comment.body, sub_entries_nltk)
            except:
                continue
            replies_of(comment, count_comment, sub_entries_textblob,sub_entries_nltk)
