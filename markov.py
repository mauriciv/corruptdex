import random
from os import listdir
from os.path import isfile, join
import re
import spacy
import markovify
from markovify.chain import BEGIN
from pprint import pp

nlp = spacy.load("en_core_web_sm")

class ParamError(Exception):
    pass

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = ''
        for word in words:
            # if "'" in word and ('PUNCT' in word or 'PART' in word or 'AUX' in word):
            if 'PUNCT' in word \
                or 'AUX' in word and "'s" in word \
                or 'PART' in word and "'s" in word:
                # pp(word)
                sentence = sentence + word.split('::')[0]
            else:
                sentence = sentence + ' ' + word.split('::')[0]
        # sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

    def make_sentence_with_start(self, beginning, strict=True, **kwargs):
        """
        Tries making a sentence that begins with `beginning` string,
        which should be a string of one to `self.state` words known
        to exist in the corpus.

        If strict == True, then markovify will draw its initial inspiration
        only from sentences that start with the specified word/phrase.

        If strict == False, then markovify will draw its initial inspiration
        from any sentence containing the specified word/phrase.

        **kwargs are passed to `self.make_sentence`
        """
        split = tuple([beginning]) # Here is the only change from the base class method
        word_count = len(split)

        if word_count == self.state_size:
            init_states = [ split ]

        elif word_count > 0 and word_count < self.state_size:
            if strict:
                init_states = [ (BEGIN,) * (self.state_size - word_count) + split ]

            else:
                init_states = [ key for key in self.chain.model.keys()
                    # check for starting with begin as well ordered lists
                    if tuple(filter(lambda x: x != BEGIN, key))[:word_count] == split ]

                random.shuffle(init_states)
        else:
            err_msg = "`make_sentence_with_start` for this model requires a string containing 1 to {0} words. Yours has {1}: {2}".format(self.state_size, word_count, str(split))
            raise ParamError(err_msg)

        for init_state in init_states:
            output = self.make_sentence(init_state, **kwargs)
            if output is not None:
                return output

        return None


def main():
    files = [f for f in listdir('./pokemon') if isfile(join('./pokemon', f))]
    with open('./corruptdex.txt', 'w') as outfile:
        for fname in files:
            with open('./pokemon/' + fname) as infile:
                outfile.write(infile.read())

    with open('./corruptdex.txt') as f:
        text = f.read()
    text_model = get_text_model(text)

    pokemon_names = map(lambda p: p.split('.')[0].split('-')[1].capitalize(), files)
    pokemon = random.choice(list(pokemon_names))

    remaining_length = 280
    first_sentence = None
    first_sentence_lenght = 141
    while first_sentence_lenght > 140:
        try:
            first_sentence = text_model.make_sentence_with_start(pokemon + '::PROPN').strip()
            first_sentence_lenght = len(first_sentence)
        except KeyError:
            try:
                first_sentence = text_model.make_sentence_with_start(pokemon + '::NOUN').strip()
                first_sentence_lenght = len(first_sentence)
            except KeyError:
                continue

    remaining_length = remaining_length - len(first_sentence)
    failure = 0
    second_sentence = text_model.make_short_sentence(remaining_length).strip()
    while True:
        if failure > 4096:
            second_sentence = text_model.make_sentence_with_start(random.choice(['It::PRON', 'Its::DET'])).strip()
            break
        if pokemon in second_sentence and not second_sentence.strip().startswith(pokemon):
            break
        failure += 1
        print("Failure number: " + str(failure))
        second_sentence = text_model.make_short_sentence(remaining_length).strip()

    remaining_length = remaining_length - len(second_sentence)
    third_sentence = text_model.make_short_sentence(remaining_length).strip()

    pp('remaining_legth = ' + str(remaining_length))

    if len(first_sentence + '\n' + second_sentence + '\n' + third_sentence) < 280:
        print(first_sentence + '\n' + second_sentence + '\n' + third_sentence)
    else:
        print(first_sentence + '\n' + second_sentence)
    print('First sentence length: ' + str(len(first_sentence)))
    print('Second sentence length: ' + str(len(second_sentence)))
    print('Third sentence length: ' + str(len(third_sentence)))
    print('Total length with line breaks: ' + str(len(first_sentence + '\n' + second_sentence + '\n' + third_sentence)))

def get_text_model(text: str) -> markovify.Text:
    json_text = ''
    text_model = None
    if isfile('corruptdex.json'):
        with open('corruptdex.json', 'r') as json_file:
            json_text = json_file.read()
            text_model = POSifiedText.from_json(json_text)
    else:
        text_model = POSifiedText(text)
        json_text = text_model.to_json()
        with open('corruptdex.json', 'w') as json_file:
            json_file.write(json_text)

    return text_model


if __name__ == "__main__":
    main()
