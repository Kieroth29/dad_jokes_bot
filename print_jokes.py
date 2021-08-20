with open("jokes.txt", "r") as jokes_file:
    jokes = jokes_file.read()
    jokes = jokes.split(";\n\n")
    jokes = list(jokes)
    print("Jokes added to array successfully.")
    
for joke in jokes:
    print(joke)