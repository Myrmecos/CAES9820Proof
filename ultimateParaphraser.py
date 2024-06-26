
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn

def tag(sentence):
 words = word_tokenize(sentence)
 words = pos_tag(words)
 return words

def paraphraseable(tag):
 return tag.startswith('NN') or tag == 'VB' or tag.startswith('JJ')

def pos(tag):
 if tag.startswith('NN'):
  return wn.NOUN
 elif tag.startswith('V'):
  return wn.VERB

def synonyms(word, tag):
    lemma_lists = [ss.lemmas() for ss in wn.synsets(word, pos(tag))]
    lemmas = [lemma.name() for lemma in sum(lemma_lists, [])]
    return set(lemmas)

def synonymIfExists(sentence):
 for (word, t) in tag(sentence):
   if paraphraseable(t):
    syns = synonyms(word, t)
    if syns:
     if len(syns) > 1:
      yield [word, list(syns)]
      continue
   yield [word, []]

def paraphrase(sentence):
 return [x for x in synonymIfExists(sentence)]

def select(i):

    for j in i[1]:
        if not ("_" in j):
            return j
    return i[0]


def processParaphrase(lst):
    retStr = ""
    for i in lst:
        retStr += select(i)
        retStr += " "
    return retStr

def ultimate_paraphrase(sentence):
    pfl = paraphrase(sentence)
    return processParaphrase(pfl)

if __name__ == "__main__":
    para = (paraphrase("The quick brown fox jumps over the lazy dog"))
    para1 = processParaphrase(para)
    print(para1)