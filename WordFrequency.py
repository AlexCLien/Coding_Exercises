'''
Given a string of text, count how many times each word appears.

My idea is using a first we have a string of text. Then we seperate the string using regex and a for loop to concatenate and seperate the string into a list of words. Then for each word in the list if the word exist in the count list, +=, if not add word to count list with a value of 1.

'''
import re

text = "Language models learn from language data, but language data does not contain every part of language."

def parser(text):
    '''
    Uses regex to split the string into a list of words. It then returns word_list.
    '''
    word_list = re.split(r'\s+', text) #regex expression splits the string by detecting one or more whitespace character. When it detects it makes the split.
    return word_list

parsed_text = parser(text) 


def count_word(list_of_words):
    '''
    This function takes in a list. For each item in the list it adds to the dictionary as a key and a value of 1. If the key already exist in the dictionary then it adds to the value 1. The function returns the dictionary.
    '''
    counted_words = {} # initializes the dictionary
    for word in list_of_words: # checks if word is in the dictionary
        if word in counted_words: # if it is a key in the dictionary then add 1 to the value
            counted_words[word] += 1
        else: # if it is not in the dictionary, add the key with a value of 1
            counted_words[word] = 1
    return counted_words
print(count_word(parsed_text))
