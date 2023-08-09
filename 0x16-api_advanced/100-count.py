#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""
import re
import requests
import sys

def add_title(dictionary, hot_posts):
    if not hot_posts:
        return

    title = hot_posts[0]['data']['title'].split()
    for word in title:
        for key in dictionary.keys():
            c = re.compile("^{}$".format(key), re.I)
            if c.findall(word):
                dictionary[key] += 1
    hot_posts.pop(0)
    add_title(dictionary, hot_posts)

def recurse(subreddit, dictionary, after=None):
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
        return

    dic = res.json()
    hot_posts = dic['data']['children']
    add_title(dictionary, hot_posts)
    after = dic['data']['after']
    if after:
        recurse(subreddit, dictionary, after=after)

def count_words(subreddit, word_list):
    dictionary = {word: 0 for word in word_list}

    recurse(subreddit, dictionary)

    sorted_words = sorted(dictionary.items(), key=lambda kv: (-kv[1], kv[0]))

    for word, count in sorted_words:
        if count != 0:
            print("{}: {}".format(word, count))

# Example usage
subreddit = 'python'
word_list = ['python', 'javascript', 'java']
count_words(subreddit, word_list)
