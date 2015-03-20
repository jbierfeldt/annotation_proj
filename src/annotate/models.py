from django.db import models
from django.db.models import signals

import nltk

def create_tokens_from_snippit(sender, instance, created, **kwargs):
    if created:
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_detector.tokenize(instance.text)
        for s in sentences:
            current_sentence = Sentence.objects.create(string=s, text_snippit=instance)
            current_sentence.save()
            sentence_tokens = nltk.word_tokenize(s)
            for token in sentence_tokens:
                token_entry = Token.objects.get_or_create(string=token)
                token_entry[0].sentence.add(current_sentence)

class TimeStampBaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Token(TimeStampBaseModel):
    string = models.CharField(max_length=200)
    sentence = models.ManyToManyField('Sentence')

    is_punctuation = models.NullBooleanField(null=True, blank=True)
    is_sentence_delimiter = models.NullBooleanField(null=True, blank=True)
    always_capitalized = models.NullBooleanField(null=True, blank=True)

    @property
    def count(self):
        return len(self.sentence.all())
    

    def __unicode__(self):
        return self.string

class Sentence(TimeStampBaseModel):
    string = models.TextField()
    text_snippit = models.ForeignKey('TextSnippit')

    def tokens(self):
        return self.token_set.all()

    def __unicode__(self):
        list_of_tokens = self.tokens()
        string = u''
        for i in range(len(list_of_tokens)):
            string += unicode(list_of_tokens[i]) + ' '
        return string

class TextSnippit(TimeStampBaseModel):
    text = models.TextField()

    def sentences(self):
        return self.sentence_set.all()

    def tokens(self):
        list_of_tokens = []
        for s in self.sentences():
            for t in s.tokens():
                list_of_tokens.append(t)
        return list_of_tokens
    
    def __unicode__(self):
        return self.text

signals.post_save.connect(create_tokens_from_snippit, sender=TextSnippit)
