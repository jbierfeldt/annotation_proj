import random
from copy import deepcopy


def weighted_pick(freq_dict):
    '''Picks next word from bigram frequency dictionary based on frequency weight'''
    r = random.uniform(0, sum(freq_dict.itervalues()))
    s = 0.0
    for k, v in freq_dict.iteritems():
        s += v
        if r < s: return k
    return k

def pick(nGram_dict, word):
        ''' parse through a nGram count dictionary until the level of counts is reached
        where the frequency conversion can be made'''
        try:
            selected_word = weighted_pick(nGram_dict[word])
        except:
            for (k,v) in nGram_dict.items():
                pick(v, word)
        return selected_word

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

def tokenize(word):
    punctuation = '?.!:;,'
    setence_delimiter = '.?!'
    non_delimiter_tokens = ['mr.', 'dr.', 'mrs.']
    if word in punctuation and word not in non_delimiter_tokens:
        if word in setence_delimiter:
            return Token(word, is_punct=True, is_delim=True)
        else:
            return Token(word, is_punct=True)
    else:
        return Token(word)

def build_token_count_dict(list_of_tokens):
    token_count_dict = {}
    for token in list_of_tokens:
        token_count_dict[token] = token.count
    return token_count_dict

def build_token_freq_dict(list_of_tokens):
    token_freq_dict = deepcopy(build_token_count_dict(list_of_tokens))
    add_freqs(token_freq_dict)
    return token_freq_dict

def build_context_target_pairs(N, list_of_sentences):
    context_target_pairs = []
    contextLength = N - 1
    if N > 1: # Need separate logic for unigrams, where N = 1
        for sentence in list_of_sentences:
            for index in range(len(list_of_tokens)):
                contextBegin = index - contextLength
                context = self.list_of_tokens[contextBegin:index]
                target = self.list_of_tokens[index]
                if context != []: # context slices with negative index will be blank, we'll ignore these
                    context = tuple(context)
                    context_target_pairs += [(context, target)]
    else: # allows for empty contexts in unigrams
        pass
    return context_target_pairs
def build_NGram_count_dict(self, N):
    results = nGramDict(N)
    context_target_pairs = self.build_context_target_pairs(N)
    for (context,target) in context_target_pairs:
        level = results #pointer, not a copy
        if context not in level:
            level[context] = {}
        level = level[context]
        if target not in level:
            level[target] = 0
        level[target] += 1
    return results
def build_NGram_freq_dict(self, N):
    results = nGramDict(N)
    context_target_pairs = self.build_context_target_pairs(N)
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
def get_random_token(self, **kwargs):
    weighted = kwargs.get('weighted', False)
    disallow_punct = kwargs.get('disallow_punct', False)
    if weighted == True:
        selected_token = weighted_pick(self.token_freq_dict)
    else:
        selected_token = random.choice(self.token_count_dict.keys())
    if disallow_punct == True:
        if selected_token.is_punct == True:
            selected_token = self.get_random_token(**kwargs)
    return selected_token
def get_random_sentence(self, **kwargs):
    weighted = kwargs.get('weighted', False)
    selected_sentence = random.choice(self.list_of_sentences)
    return selected_sentence
def generate_segment(self, context_length):
    bigram_dict = self.build_NGram_freq_dict(2) #for building initial segment
    seed_word = Token('.')
    initial_seg_constructor = [seed_word]
    while len(initial_seg_constructor) < context_length:
        new_seg = weighted_pick(bigram_dict[tuple([initial_seg_constructor[-1]])])
        initial_seg_constructor.append(new_seg)
    initial_seg = tuple(initial_seg_constructor)
    return initial_seg
def generate_sentence(self, **kwargs):
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