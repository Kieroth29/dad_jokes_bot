import praw
import re
import json
from random import choice

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
    replies.append(item)

for subreddit in subreddits:
    sub = reddit.subreddit(subreddit)
    for submission in [item for item in sub.new(limit=1000) if item.author is not None]:
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if comment.id not in replied:
                if re.search("dad jokes", comment.body, re.IGNORECASE) or re.search("dad joke", comment.body, re.IGNORECASE) or re.search("u/dad_jokes_bot", comment.body, re.IGNORECASE):
                    joke = choice(jokes)
                    comment.reply(f"{joke}\n\nI'm a bot! To summon me, comment 'dad joke', 'dad jokes' or just @me (u/dad_jokes_bot). If you wish to add or remove me to/from a subreddit, or check the list of supported ones, contact [my creator](https://reddit.com/u/AntaresSlayer), or issue a pull request to the subreddits.txt file in [my public repo!](https://github.com/Kieroth29/dad_jokes_bot)")

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
