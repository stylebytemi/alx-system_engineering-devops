#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""
import re
import requests
import sys

def add_title(dictionary, hot_posts):
    """ Adds item into a list """
    if len(hot_posts) == 0:
        return

    title = hot_posts[0]['data']['title'].split()
    for word in title:
        word_lower = word.lower()
        for key in dictionary.keys():
            key_lower = key.lower()
            c = re.compile(r"\b{}\b".format(re.escape(key_lower)), re.I)
            if c.findall(word_lower):
                dictionary[key] += 1
    hot_posts.pop(0)
    add_title(dictionary, hot_posts)

def recurse(subreddit, dictionary, after=None):
    """ Queries to Reddit API """
    u_agent = 'Mozilla/5.0'
    headers = {
        'User-Agent': u_agent
    }

    params = {
        'after': after
    }

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    res = requests.get(url,
                       headers=headers,
                       params=params,
                       allow_redirects=False)

    if res.status_code != 200:
        return None

    dic = res.json()
    hot_posts = dic['data']['children']
    add_title(dictionary, hot_posts)
    after = dic['data']['after']
    if not after:
        return
    recurse(subreddit, dictionary, after=after)

def count_words(subreddit, word_list):
    """ Init function """
    dictionary = {}

    for word in word_list:
        dictionary[word] = 0

    recurse(subreddit, dictionary)

    l = sorted(dictionary.items(), key=lambda kv: (-kv[1], kv[0]))

    if len(l) != 0:
        for item in l:
            if item[1] != 0:
                print("{}: {}".format(item[0], item[1]))
    else:
        print("")

# Example usage
subreddit = 'python'
word_list = ['python', 'javascript', 'java']
count_words(subreddit, word_list)
