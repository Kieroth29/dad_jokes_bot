import time
import praw
import re
import sqlite3
from random import choice
from apscheduler.schedulers.background import BackgroundScheduler

reddit = praw.Reddit('bot1')

def reply():
    print('Starting reply')
    conn = sqlite3.connect('replies.db')
    cursor = conn.cursor()
    
    jokes = cursor.execute("SELECT * FROM jokes").fetchall()

    opt_out = [item[1] for item in cursor.execute("SELECT username FROM opt_out").fetchall()]

    with open("subreddits.txt", "r") as subreddits_file:
        subreddits = subreddits_file.read().split(";\n")

    for subreddit in subreddits:
        sub = reddit.subreddit(subreddit)
        print("Searching subreddit:", subreddit)
        
        for submission in [item for item in sub.new(limit=50) if item.author is not None]:
            submission.comments.replace_more(limit=None)
            
            print("Reading post: ", submission.title, "\nby", submission.author)
            
            for comment in submission.comments.list():
                cursor.execute(f"SELECT comment_id FROM replies WHERE comment_id = '{comment.id}' ")
                
                print("Reading comment by", comment.author,":\n", comment.body)
                
                if len(cursor.fetchall()) == 0 and comment.author != "dad_jokes_bot" and comment.author not in opt_out:
                    if re.search("dad jokes", comment.body, re.IGNORECASE) or re.search("dad joke", comment.body, re.IGNORECASE) or re.search("u/dad_jokes_bot", comment.body, re.IGNORECASE):
                        joke = choice(jokes)
                        
                        print("Joke reply: ", joke)
                        
                        cursor.execute("""
                            INSERT INTO replies (submission_id, submission_title, comment_id, comment,      joke_id,    subreddit) VALUES (?,?,?,?,?,?)
                        """,                    (submission.id, submission.title, comment.id, comment.body, joke[0],    subreddit))
                        conn.commit()
                        
                        comment.reply(f"{joke[1]}\n\nI'm a bot! To summon me, comment 'dad joke', 'dad jokes' or just @me (u/dad_jokes_bot). If you wish to add or remove me to/from a subreddit, or check the list of supported ones, contact [my creator](https://reddit.com/u/AntaresSlayer), or issue a pull request to the subreddits.txt file in [my public repo!](https://github.com/Kieroth29/dad_jokes_bot)\n\nTo opt-out, reply to this message with 'opt-out'. ")
                    if re.search("opt-out", comment.body, re.IGNORECASE):
                        print("Opt-out")
                        if comment.parent().author == "dad_jokes_bot":
                            print("Opt-out to self")
                            cursor.execute("INSERT INTO opt_out (username) VALUES (?)", comment.author)
                            conn.commit()
                            
                            comment.reply("Successfully opted out. You will not receive any more replies from this bot! :)")
                        else:
                            print("Opt-out to other")
                            
    print("Finished search")
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(reply, 'interval', minutes=15, max_instances=3)
scheduler.start()

while True:
    time.sleep(0)