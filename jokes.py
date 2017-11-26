# jokes.txt jokes 1-8 taken from http://www.devtopics.com/best-programming-jokes/
# jokes.txt jokes 9-13 taken from https://www.hongkiat.com/blog/programming-jokes/

from random import randint

def get_joke():
    with open('jokes.txt') as f:
        jokes = f.readlines()
    jokes = [joke.strip() for joke in jokes]

    random_joke = jokes[randint(0, len(jokes)-1)]

    return random_joke
