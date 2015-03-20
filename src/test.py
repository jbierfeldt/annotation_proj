import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "annotation.settings")

# your imports, e.g. Django models
from annotate.models import *

django.setup()

def add_freqs(count_dict):
    ''' converts a count dictionary to a frequency dictionary'''
    allcounts = count_dict.values()
    total = float(sum(allcounts))
    for (k,v) in count_dict.items():
        count_dict[k] = v/total
    return count_dict

def decorate_freqs(nGram_dict):
        ''' parse through a nGram count dictionary until the level of counts is reached
        where the frequency conversion can be made'''
        try:
            add_freqs(nGram_dict)
        except TypeError:
            for (k,v) in nGram_dict.items():
                decorate_freqs(v)


def build_context_target_pairs(N, list_of_sentences):
    context_target_pairs = []
    contextLength = N - 1
    if N > 1: # Need separate logic for unigrams, where N = 1
        for sentence in list_of_sentences:
            tokens_in_sent = sentence.token_set.all()
            for index in range(len(tokens_in_sent)):
                contextBegin = index - contextLength
                if contextBegin < 0:
                    print "skipping!"
                    continue
                context = tokens_in_sent[contextBegin:index]
                target = tokens_in_sent[index]
                if context != []: # context slices with negative index will be blank, we'll ignore these
                    context = tuple(context)
                    context_target_pairs += [(context, target)]
    else: # allows for empty contexts in unigrams
        pass
    return context_target_pairs

def build_NGram_count_dict(N, list_of_sentences):
    results = {}
    context_target_pairs = build_context_target_pairs(N, list_of_sentences)
    for (context,target) in context_target_pairs:
        level = results #pointer, not a copy
        if context not in level:
            level[context] = {}
        level = level[context]
        if target not in level:
            level[target] = 0
        level[target] += 1
    return results

def build_NGram_freq_dict(N, list_of_sentences):
    results = {}
    context_target_pairs = build_context_target_pairs(N, list_of_sentences)
    for (context,target) in context_target_pairs:
        level = results #pointer, not a copy
        if context not in level:
            level[context] = {}
        level = level[context]
        if target not in level:
            level[target] = 0
        level[target] += 1
    decorate_freqs(results) # convert counts to frequency in the
    return results

def generate_segment(context_length, list_of_sentences):
    bigram_dict = build_NGram_freq_dict(2, list_of_sentences) #for building initial segment
    seed_word = token
    initial_seg_constructor = [seed_word]
    while len(initial_seg_constructor) < context_length:
        new_seg = weighted_pick(bigram_dict[tuple([initial_seg_constructor[-1]])])
        initial_seg_constructor.append(new_seg)
    initial_seg = tuple(initial_seg_constructor)
    return initial_seg
    
def generate_sentence(list_of_sentences, **kwargs):
    generated_sentence = []
    N = kwargs.get('gram_length', 2)
    ngram_dict = self.build_NGram_freq_dict(N)
    context_length = N - 1
    initial_seg = self.generate_segment(context_length)
    for token in initial_seg: #ignore first, which should be sentence delimiter.
        generated_sentence.append(token)
    last_seg = initial_seg
    while last_seg[-1].is_delim == False:
        try:
            new_seg = weighted_pick(ngram_dict[last_seg])
            generated_sentence.append(new_seg)
            last_seg = tuple(generated_sentence[-context_length:])
        except KeyError:
            initial_seg = self.generate_segment(context_length)
            generated_sentence = []
            for token in initial_seg:
                generated_sentence.append(token)
            last_seg = initial_seg
    return Sentence(generated_sentence[1:])

sentences = Sentence.objects.all()
period = sentences[0].token_set.all().last
print period

# print build_NGram_freq_dict(2, sentences)
