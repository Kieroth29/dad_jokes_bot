import praw
import pdb
import re
import os
import json
from dotenv import load_dotenv
from random import choice
load_dotenv()

reddit = praw.Reddit('bot1')

with open("replied_to.json", "r") as f:
    replied_to = f.read()
    replied_to = json.loads(replied_to)

with open("jokes.txt", "r") as jokes_file:
    jokes = jokes_file.read()
    jokes = jokes.split(";\n\n")
    jokes = list(jokes)

with open("subreddits.txt", "r") as subreddits_file:
    subreddits = subreddits_file.read()
    subreddits = subreddits.split(";\n")

reply = False
replies = []
replied = []
for item in replied_to:
    replied.append(item['comment_id'])

for subreddit in subreddits:
    sub = reddit.subreddit(subreddit)
    for submission in sub.new(limit=10):

        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if comment.id not in replied:
                if re.search("dad jokes", comment.body, re.IGNORECASE) or re.search("dad joke", comment.body, re.IGNORECASE) or re.search("u/dad_jokes_bot", comment.body, re.IGNORECASE):
                    joke = choice(jokes)
                    comment.reply(joke)

                    replies.append({
                        "submission_id": submission.id,
                        "submission_title": submission.title,
                        "comment_id": comment.id,
                        "comment": comment.body
                    })

                    reply = True

if reply == True:
    with open("replied_to.json", "w") as f:
        json.dump(replies, f)
