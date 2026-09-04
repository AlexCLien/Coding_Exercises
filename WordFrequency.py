'''
Given a string of text, count how many times each word appears.

My idea is using a first we have a string of text. Then we seperate the string using regex and a for loop to concatenate and seperate the string into a list of words. Then for each word in the list if the word exist in the count list, +=, if not add word to count list with a value of 1.

'''
import re

text = "Language models learn from language data, but language data does not contain every part of language."

def parser(text):
    word_list = re.split(r'\s+', text)
    return word_list

parsed_text = parser(text) 

counted_words = {} 
def count_word(list_of_words):
    for word in list_of_words:
        if word in counted_words:
            counted_words[word] += 1
        else:
            counted_words[word] = 1
    return counted_words
print(count_word(parsed_text))