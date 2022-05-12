"""Eliza homework. Relationship advisor"""
__author__ = "Benjamin Caulfield"

import re

from random import choice

# this idea of keyword rankings was lifted from the Eliza paper. 
# Dividing into categories, and separating emotions into superlative and perjorative was my own.
keyword_dict = {
            "father": [4, "fam"],
            "myself": [2, "self"],
            "good": [5, "emo", "s"],
            "bad": [5, "emo", "p"],
            "ok": [5, "emo", "s"],
            "evil": [5, "emo", "p"],
            "lust": [6, "sex", "p"],
            "flesh": [6, "sex", "p"],
            "devil": [6, "rel", "p"],
            "hurt": [6, "emo", "p"],
            "father": [5, "fam"],
            "dad": [5, "fam"],
            "mother": [5, "fam"],
            "mom": [5, "fam"],
            "brother": [5, "fam"],
            "sister": [5, "fam"],
            "friend": [5, "fam"],
            "sex": [6, "sex"],
            "fantasy": [6, "sex"],
            "lie": [6, "emo", "p"],
            "believe": [5, "rel"],
            "love": [6, "emo", "s"],
            "joy": [6, "emo", "s"],
            "kill": [6, "emo", "p"],
            "sad": [6, "emo", "p"],
            "happy": [6, "emo", "s"],
            "hate": [6, "emo", "p"],
            "trust": [6, "emo", "s"],
            "always": [4, "conj"],
            "afraid": [3, "emo", "p"],
            "guilt": [6, "emo", "p"],
            "doctor": [5, "fam"],
            "sick": [6, "emo", "p"],
            "helps": [5, "emo", "s"],
            "doomed": [6, "emo", "p"],
            "cry": [6, "emo", "p"],
            "husband": [5, "fam"],
            "wife": [5, "fam"],
            "God": [5, "rel"],
            "bad": [5, "emo", "p"],
            "glad": [4, "emo", "p"],
            "sexual": [6, "sex"], 
            "blame": [6, "emo", "p"],
            "awful": [5, "emo", "p"],
            "fun": [5, "emo", "s"],
            "anger": [6, "emo", "p"],
            "frightening": [6, "emo", "p"],
            "children": [5, "fam"],
            "difficult": [6, "emo", "p"],
            "hard": [6, "emo", "p"],
            "easy": [6, "emo", "s"],
            "risky": [6, "emo", "s"],
            "respect": [4, "emo", "s"],
            "end": [7, "time"],
            "start": [7, "time"]
            }

# This idea was also taken from Eliza paper, but I saw a version of this dictionary on datacamp.com
pronoun_transformation = {
            "I": "you",
            "you": "I",
            "my": "your",
            "your": "my",
            "mine": "yours",
            "yours": "mine",            
            "me": "you",
            "am": "are",
            "are": "am",
            "I'm": "you are",
            "You're": "I am"
}

no_keyword_or_verb_found = [
                    "I'm not sure what you mean. Perhaps you can elaborate ",
                    "That's fascinating. Can you go into a little more depth? ",
                    "That's a wonderful insight. What would your father say about that? ",
                    "I think we're making a lot of progress here. What does that make you think about? ",
                    "To pretend, I actually do the thing: I have therefore only pretended to pretend. How does that make you feel? ",
                    "I think it was Dylan who said 'He not busy being born is busy dying', I think that applies here. "
                    ]

#verb suffixes
eds = re.compile(r'\b\w+ed\b')
ings = re.compile(r'\b\w+ing\b')

def main():
    response = greeting()
    while not detect_goodbye(response):
        pronoun = transform_pronoun(response)
        keyword = ranking_keyword(response)
        if keyword is None:
            print(choice(no_keyword_or_verb_found))
        elif keyword and pronoun:
            print(transform_with_pronoun(pronoun, keyword))
        else:
            print(transform_with_no_pronoun(keyword))
        response = input(">>>") 
    goodbye()

def greeting():
    patient = input("Hello there. Whom do I have the pleasure of speaking with? ")
    print(f"Hello, {patient}, let's get to the bottom of this. ")
    return input("What seems to be troubling you today? ")

def detect_goodbye(response):
    goodbyes = re.compile('(B|bye)|(F|farewell)|(G|gotta go)|(T|thanks for nothing)')
    if goodbyes.search(response):
        return True
    return False

def goodbye():
    print("Good luck!")


def transform_pronoun(response):
    words = [word.lower() for word in response.split(" ")]
    pronouns = [pronoun_transformation[word] for word in words if word in pronoun_transformation]
    if pronouns:
        return pronouns[0]
    return None  

def ranking_keyword(response):
    matches = {}
    words = [word.lower() for word in response.split(" ")]
    
    tensed_words = [tensing(word) for word in words]
    
    for word in tensed_words:
        if word in keyword_dict:
            matches[word] = keyword_dict[word]
            
    if matches:
        return max(matches.keys())
    else:
        return no_keyword(response)

def no_keyword(response):
    words = response.split(" ")
    for word in words:
        if re.findall(eds, word) or re.findall(ings, word):
            return tensing(word)
    return None

def tensing(word):
    if re.findall(eds, word):
        return re.findall(eds, word)[0][:-2]
    elif re.findall(ings, word):
        return re.findall(ings, word)[0][:-3] 
    else:
        return word

def transform_with_pronoun(pronoun, keyword):
    if keyword not in keyword_dict:
        return f"Interesting! What more can {pronoun} tell me about how it feels to {keyword}? "
    elif keyword_dict[keyword][1] == "emo":
        if keyword_dict[keyword][2] == "p":
            return f"What does {pronoun} feeling {keyword} make you think of? " 
        else:
            return f"{pronoun} feeling {keyword}. What do you think about that? "
    elif keyword_dict[keyword][1] == "fam":
        return f"What do {pronoun} think that says about your {keyword}? "
    elif keyword_dict[keyword][1] == "sex":
        return f"Well, it certainly seems {pronoun} think about {keyword} a lot. Tell me more. "
    else:
        return f"Why do {pronoun} think that had to {keyword} like that? " 
                    

def transform_with_no_pronoun(keyword):
    if keyword not in keyword_dict:
        return f"Interesting! What more can you tell me about how it feels to {keyword}? "
    elif keyword_dict[keyword][1] == "emo":
        if keyword_dict[keyword][2] == "p":
            return f"What a terrible ordeal you are going through. What does feeling {keyword} make you think of? . " 
        else:
            return f"That's a really positive development. Tell me more about feeling {keyword}. "
    elif keyword_dict[keyword][1] == "fam":
        return f"What do you think that says about your {keyword}? "
    elif keyword_dict[keyword][1] == "sex":
        return f"Well, thinking about {keyword} is perfectly normal. Tell me more. "
    else:
        return f"Why do you think that had to {keyword} like that? "
      

main()

