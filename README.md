## CorruptDex

CorruptDex is a twitter bot that uses markov chains to generate nonsensical dex entries for Pokémon.

## Installation

You must have Python 3 installed.

The best way to install CorruptDex is to create a new virtual enviroment and clone the repository in there.

```bash
python3 -m venv corruptdex
cd corruptdex && git clone https://github.com/mauriciv/corruptdex.git src
source ./bin/activate
cd src && pip3 install -r requirements.txt
```

If you intend to make a bot you should copy the env.py.example file to a file named env.py and modify it so it has your Twitter tokens.

If you only want to play around with it, you can do `python3 markov.py` and it will print a few tweets.
