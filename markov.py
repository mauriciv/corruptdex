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
        pokemon_tweet = text_model.make_sentence_with_start(pokemon)
        if len(pokemon_tweet) < 140:
            print(pokemon_tweet)
            tweeted = True
            it_tweet = text_model.make_sentence_with_start('It')
            if len(it_tweet) < 140:
                print(' ' + it_tweet)

            its_tweet = text_model.make_sentence_with_start('Its')
            if len(its_tweet) < 140:
                print('  ' + its_tweet)

            last_tweet = text_model.make_sentence_with_start('This')
            if len(last_tweet) < 140:
                print('   ' + last_tweet)

            print('    ' + text_model.make_short_sentence(140))
        else:
            failure += 1
            print("Failure number: " + str(failure))


if __name__ == "__main__":
    main()
