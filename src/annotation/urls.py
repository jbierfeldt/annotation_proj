from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic.base import TemplateView

from annotate.views import TokenDetailView, RandomTokenDetailView, SentenceDetailView, TextSnippitCreateView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RandomTokenDetailView.as_view(), name='random_token_detail'),
    url(r'^token/(?P<token_id>\d+)/$', TokenDetailView.as_view(), name='token_detail'),
    url(r'^sentence/(?P<sentence_id>\d+)/$', SentenceDetailView.as_view(), name='sentence_detail'),
    url(r'^snippit/create/$', TextSnippitCreateView.as_view(), name='textsnippit_create'),   
)