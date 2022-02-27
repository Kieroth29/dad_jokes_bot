# dad_jokes_bot

dad_jokes_bot is a Reddit Python bot, which replies to mentions or certain comments with dad jokes, in predefined subreddits. This bot is powered by [Praw](https://praw.readthedocs.io/en/latest/index.html) and [Reddit API](https://www.reddit.com/dev/api).

## Usage

dad_jokes_bot is triggered by mentions (u/dad_jokes_bot)
Supported subreddits are in the **subreddits.txt** file. Feel free to open pull requests to add this bot to your favorite subs, including its name to the top of the file. The format is:

```
subreddit1;
subreddit2;
subreddit3
```

## Modules

### reply.py

This is the main module, loading jokes, subreddits and replied comments to Python objects. If a comment with the keywords is found, and its ID does not belong to the replied comments list, the bot will randomly choose a joke and reply to it.

### print_jokes

Simple testing module, printing each joke from a list, populated by the **jokes.txt** file.

## License

[MIT](https://choosealicense.com/licenses/mit/)
