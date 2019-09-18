import random
from os import listdir
from os.path import isfile, join

import markovify


# import pprint

def main():
    files = [f for f in listdir('./pokemon') if isfile(join('./pokemon', f))]
    with open('./corruptdex.txt', 'w') as outfile:
        for fname in files:
            with open('./pokemon/' + fname) as infile:
                outfile.write(infile.read())

    with open('./corruptdex.txt') as f:
        text = f.read()

    text_model = markovify.Text(text)
    # text_model.get_value = get_value

    pokemon_names = map(lambda p: p.split('.')[0].split('-')[1].capitalize(), files)
    pokemon = random.choice(list(pokemon_names))
    tweeted = False
    failure = 0
    while tweeted is False:
        full_tweet = ""
        pokemon_tweet = text_model.make_sentence_with_start(pokemon)
        if len(pokemon_tweet) < 280:
            full_tweet = full_tweet + pokemon_tweet
            tweeted = True
            more_text = text_model.make_sentence()
            # more_text = text_model.make_sentence_with_start(random.choice(['If', 'It', 'Its', 'It's', 'By', 'When', 'On', 'Once', 'There', 'The', 'They', 'This', 'A', 'An', 'As', 'At', 'For', 'Despite', 'Due']))
            if len(full_tweet + more_text) <= 280:
                full_tweet = full_tweet + ' ' + more_text
            even_more_text = text_model.make_sentence()
            if len(full_tweet + even_more_text) <= 280:
                full_tweet = full_tweet + ' ' + even_more_text
            print(full_tweet)

        else:
            failure += 1
            print("Failure number: " + str(failure))



if __name__ == "__main__":
    main()
