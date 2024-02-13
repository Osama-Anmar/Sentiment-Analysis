import pyarabic.arabrepr
import re
import os
from pyarabic.araby import strip_tashkeel, strip_tatweel, tokenize
import arabicstopwords.arabicstopwords as stp
import qalsadi.lemmatizer 
from ruqiya import ruqiya
from tashaphyne.stemming import ArabicLightStemmer

class TextNormalization:
     def __init__(self,
                 remove_emojis,
                 remove_hashtags,
                 remove_emails,
                 remove_URLs,
                 remove_new_line_char,
                 remove_mentions,
                 remove_single_char,
                 remove_duplicate_char,
                 remove_duplicate_word,
                 remove_stop_words,
                 remove_special_character,
                 remove_puncuations,
                 remove_html_tags,
                 remove_numbers,
                 remove_non_arabic,
                 remove_arabic_diacritics,
                 normalize_alef_maqsura,
                 normalize_alef,
                 normalize_teh_marbuta,
                 normalize_arabic_tashkeel,
                 normalize_arabic_tatweel,
                 remove_longest_than,
                 remove_whitespace,
                 lemmatize,
                 stemmer,
                 ):

          self.remove_emojis = remove_emojis
          self.remove_hashtags = remove_hashtags
          self.remove_emails = remove_emails
          self.remove_URLs = remove_URLs
          self.remove_new_line_char = remove_new_line_char
          self.remove_mentions = remove_mentions
          self.remove_single_char = remove_single_char
          self.remove_duplicate_char = remove_duplicate_char
          self.remove_duplicate_word = remove_duplicate_word
          self.remove_stop_words = remove_stop_words
          self.remove_special_character = remove_special_character
          self.remove_puncuations = remove_puncuations
          self.remove_html_tags = remove_html_tags
          self.remove_numbers = remove_numbers
          self.remove_non_arabic = remove_non_arabic
          self.remove_arabic_diacritics = remove_arabic_diacritics
          self.normalize_alef_maqsura = normalize_alef_maqsura
          self.normalize_alef = normalize_alef
          self.normalize_teh_marbuta = normalize_teh_marbuta
          self.normalize_arabic_tashkeel = normalize_arabic_tashkeel
          self.normalize_arabic_tatweel = normalize_arabic_tatweel
          self.remove_longest_than = remove_longest_than
          self.remove_whitespace = remove_whitespace
          self.lemmatize = lemmatize
          self.stemmer = stemmer

     def delete_emojis(self,text):
          "Delete All Emojis From Text"
          text = ruqiya.remove_emojis(text)
          return text

     def delete_hashtags(self,text):
          "Delete All Hashtags From Text"
          text =  ruqiya.remove_hashtags(text)
          return text

     def delete_emails(self,text):
          "Delete All Emails From Text"
          text = ruqiya.remove_emails(text)
          return text

     def delete_url(self,text):
          "Delete All URL From Text"
          text = ruqiya.remove_URLs(text)
          return text

     def delete_new_line_char(self,text):
          "Delete New Line Symbols From Text"
          text = text.replace('\n', ' ')
          return text 
     
     def delete_mention(self,text):
          "Delete All Mention From Text"
          text = ruqiya.remove_mentions(text)
          return text

     def delete_single_char(self,text):
          "Delete Alone Chars From Text"
          text = ' '.join( [w for w in text.split() if len(w)>1] )
          return text

     def delete_duplicate_char(self,text):
          "Delete Chars Word Has More Than 2 Same Following Char"
          text = re.sub(r'(.)\1+', r'\1\1', text)
          return text

     def delete_duplicate_word(self,text):
          "Delete Followed Occurrences Of Duplicate Words"
          text = re.sub(r'\b(\w+)( \1)+', r'\1', text)
          return text

     def delete_stop_words(self,text):
          "Delete StopWords From Text"
          StopWords1 = set(stp.stopwords_list())
          stop = open('ArabicStopWord.txt','r', encoding='Utf-8')
          StopWords2 = set(stop.read().split('\n'))
          stop.close()
          StopWords = StopWords1.union(StopWords2)
          text = tokenize(text)
          text = [word for word in text if word not in StopWords]
          return ' '.join(text)


     def delete_special_character(self,text):
          "Delete Special Character From Text"
          Pattern = re.compile('[^a-zA-Z0-9\s' + "{}_!-?.:;""''()،؟.." + '\u0600-\u06FF]')
          text = re.sub(Pattern, ' ', text)
          return text

     def delete_punctuations(self,text):
          "Delete Punctuations Words"
          Punctuations = "{}_!-?.:;""''()،؟,..[]"
          for punctuation in Punctuations:
            text = text.replace(punctuation, ' ')
          return text  

     def delete_html_tags(self,text):
          "Delete All HTL Tags From Text"
          text = re.sub("<.*?>", ' ', text)
          return text

     def delete_number(self,text):
          "Delete All Number From Text"
          text = re.sub(r'\d+', '', text)
          return text

     def delete_non_arabic(self,text):
          "Delete Non Arabic Word And Char"
          pattern = re.compile('[^0-9\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD.0-9\s.{}_!-?.:;()،؟..""'']+')
          text = re.sub(pattern, ' ', text)
          return text

     def delete_arabic_diacritics(self,text):
          "Delete Arabic Dediacritization"
          text = ruqiya.remove_diacritics(text)
          return text

     
     def convert_alef_maqsura(self,text):
          "Normalize alef maksura 'ى' to yeh 'ي'"
          text = text = re.sub("ى", "ي", text)
          return text

     def convert_alef(self,text):
          "Normalize alef variants to 'ا'"
          text = re.sub("[ٱأإٲٳٵآ]", "ا", text)
          return text

     def convert_teh_marbuta(self,text):
          "Normalize teh marbuta 'ة' to heh 'ه'"
          text = re.sub("ة", "ه", text)
          return text

     def delete_arabic_tashkeel(self,text):
          "Delete Arabic Tashkeel"
          text = strip_tashkeel(text)
          return text

     def delete_arabic_tatweel(self,text):
          "Delete Arabic Tashkeel"
          text = strip_tatweel(text)
          return text

     def delete_longest_than(self,text):
          "Delete All Words That Longest Than The Longest Word In Arabic"
          for word in text.split():
               if len(word) >=16:
                    text = text.replace(word, '')
          return text

     def delete_whitespace(self,text):
          "Delete Extra WhiteSpace"
          text = text.strip()
          return text 

     def lemmatizer_(self,text):
          lem = qalsadi.lemmatizer.Lemmatizer()
          text = " ".join([lem.lemmatize(word) for word in text.split()])
          return text

     def stemmer_(self, text):
          stemmer = ArabicLightStemmer()
          text = " ".join([stemmer.light_stem(word) for word in text.split()])
          return text


     def normalization(self, text):
          if self.remove_emojis == True:
               text = self.delete_emojis(text)
          if self.remove_hashtags == True:
               text = self.delete_hashtags(text)
          if self.remove_emails == True:
               text = self.delete_emails(text)
          if self.remove_URLs == True:
               text = self.delete_url(text)
          if self.remove_new_line_char == True:
               text = self.delete_new_line_char(text)
          if self.remove_mentions == True:
               text = self.delete_mention(text)
          if self.remove_single_char == True:
               text = self.delete_single_char(text)
          if self.remove_duplicate_char == True:
               text = self.delete_duplicate_char(text)
          if self.remove_duplicate_word == True:
               text = self.delete_duplicate_word(text)
          if self.remove_stop_words == True:
               text = self.delete_stop_words(text)
          if self.remove_special_character == True:
               text = self.delete_special_character(text)
          if self.remove_puncuations == True:
               text = self.delete_punctuations(text)
          if self.remove_html_tags == True:
               text = self.delete_html_tags(text)
          if self.remove_numbers == True:
               text = self.delete_number(text)
          if self.remove_non_arabic == True:
               text = self.delete_non_arabic(text)
          if self.remove_arabic_diacritics == True:
               text = self.delete_arabic_diacritics(text)
          if self.normalize_alef_maqsura == True:
               text = self.convert_alef_maqsura(text)
          if self.normalize_alef == True:
               text = self.convert_alef(text)
          if self.normalize_teh_marbuta == True:
               text = self.convert_teh_marbuta(text)
          if self.normalize_arabic_tashkeel == True:
               text = self.delete_arabic_tashkeel(text)
          if self.normalize_arabic_tatweel == True:
               text = self.delete_arabic_tatweel(text)
          if self.remove_longest_than == True:
               text = self.delete_longest_than(text)
          if self.remove_whitespace == True:
               text = self.delete_whitespace(text)
          if self.lemmatizer_ == True:
               text = self.lemmatizer_(text)
          if self.stemmer == True:
               text = self.stemmer_(text)
          return text
          