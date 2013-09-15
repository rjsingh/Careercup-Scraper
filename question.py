#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup
import random
import cPickle as pickle

def pick_link():
    links = {"Amazon":'amazon-interview-questions', "Microsoft":'microsoft-interview-questions', "Google":'google-interview-questions'}
    
    choice = random.choice(links.keys())
    
    return (choice, "http://www.careercup.com/page?pid=" + links[choice])


def get_num_pages(link):

    c = 1
    while True:
        soup = BeautifulSoup(urllib2.urlopen(link+'&n='+str(c)).read())
        
        if(soup.get_text().find('Sorry - no more questions!') > -1):
            return c-1

        c += 1

def get_all_questions(link):
    questions = []

    c = 1
    while True:
        soup = BeautifulSoup(urllib2.urlopen(link+'&n='+str(c)).read())

        if soup.get_text().find('Sorry - no more questions!') > -1:
            break
        else:
            for q in soup.findAll('li', attrs={'class':'question'}):
                href = q.findAll('span', attrs={'class':'entry'})[0].a.get('href')
                quest = q.p.getText()
                questions.append((href, quest))

            break
    return questions


(company, link) = pick_link()
questions = get_all_questions(link)

with open(company, 'wb') as fp:
    pickle.dump(questions, fp)
