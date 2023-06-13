""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from phonemizer import phonemize


# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]

_sentence_stops= ',:,!.?;\n\r'

def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text):
  return normalize_numbers(text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)

def english_cleaner_and_mark_sentences(text):
  '''Pipeline for English text, including abbreviation expansion. + punctuation + stress'''

  def split_sentence(text):
    sentences = []
    is_stop = True
    index_start = 0
    index_end = 0

    for index, s in enumerate(text):
      if (s == ' '):
        index_end += 1
        continue

      if (s in _sentence_stops) == is_stop:
        index_end += 1
      else:
        if index_start != index_end:
          sentences.append((index_start, index_end, is_stop))
        index_start = index
        index_end = index + 1
        is_stop = not is_stop

    if index_start != index_end:
      sentences.append((index_start, index_end, is_stop))

    return sentences

  text = convert_to_ascii(text)
  cleaned_text = lowercase(text)
  cleaned_text = expand_abbreviations(cleaned_text)
  phonemes = phonemize(cleaned_text, language='en-us', backend='espeak', strip=True, preserve_empty_lines=True, preserve_punctuation=True, with_stress=True)
  cleaned_phonemes = collapse_whitespace(phonemes)
  
  splitted_text = split_sentence(text)
  splitted_phonemes = split_sentence(phonemes)
  
  if len(splitted_text) != len(splitted_phonemes):
    return cleaned_phonemes, [(0, len(text), False)]
  
  marked_sentences = []
  for index, sentence in enumerate(splitted_text):
    s, e, _ = sentence
    marked_sentences.append((text[s:e],  splitted_phonemes[index]))
  return cleaned_phonemes, marked_sentences
