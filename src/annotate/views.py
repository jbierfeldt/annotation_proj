from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from annotate.models import Token, Sentence, TextSnippit


class TextSnippitCreateView(CreateView):
    
    model = TextSnippit
    template_name_suffix = '_create'
    success_url = '/'

class TokenDetailView(DetailView):
    
    model = Token
    
    def get_object(self, queryset=None):
        obj = Token.objects.get(pk=self.kwargs['token_id'])
        return obj
          
    def get_context_data(self, **kwargs):
        # # Call the base implementation first to get a context
        context = super(TokenDetailView, self).get_context_data(**kwargs)
        context['chosen_token'] = self.get_object()
        return context

class SentenceDetailView(DetailView):
    
    model = Token
    
    def get_object(self, queryset=None):
        obj = Sentence.objects.get(pk=self.kwargs['sentence_id'])
        return obj
          
    def get_context_data(self, **kwargs):
        # # Call the base implementation first to get a context
        context = super(SentenceDetailView, self).get_context_data(**kwargs)
        context['chosen_sentence'] = self.get_object()
        return context

class RandomTokenDetailView(DetailView):
    
    model = Token
    
    def get_object(self, queryset=None):
        obj = Token.objects.all().order_by('?')[0]
        return obj
          
    def get_context_data(self, **kwargs):
        # # Call the base implementation first to get a context
        context = super(RandomTokenDetailView, self).get_context_data(**kwargs)
        context['chosen_token'] = self.get_object()
        return context

# Create your views here.
