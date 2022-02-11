import numpy as np

from config import config as default_config
from generate_word_dict import load_words

class WordleMaster(object):
    """Main class for wordle master"""

    def __init__(self, config=None):
        """Initialize the wordle master"""
        if not config:
            config = default_config
        self.config = config
        self.words = None
        self.freq = None
        self.word_length = None
        self.round = 0
        self.guess_results = None   # {'a': [0, 1, 2, 3, 4], 'b': [0, 1, 2, 3, 4]}
                                    # [0, 1, 2, 3, 4] means unknown
                                    # [0] means the location is correct
                                    # [0, 1, 3, 4] means the location is wrong
        self.current_guess = None
        self.contained_letters = []
        self.excluded_letters = []
        self.possible_words = []

    def start(self, word_length=5):
        self.word_length = word_length
        self.words, self.freq = load_words(self.config['word_file'], word_length)
        self.guess_results = {
            w: list(range(word_length)) for w in 'abcdefghijklmnopqrstuvwxyz'
        }
        self.current_guess = self.init_guess()

        return self.current_guess

    def answer(self, feedback):
        """
        Tell me the result of current guess.
        :param feedback: result of the current guess:
                e.g. [0, 1, 1, 0, 2]
                0 == not in the word
                1 == in the word but wrong location
                2 == correct letter
        :return:
        """

        # update the guess results
        if isinstance(feedback, str):
            feedback = [int(f) for f in feedback]
        if all(f == 2 for f in feedback):
            print('Found the word!')
            return True
        for i, f in enumerate(feedback):
            current_letter = self.current_guess[i]
            if f == 0:
                if current_letter not in self.contained_letters:
                    self.guess_results[current_letter] = []
                if current_letter not in self.contained_letters:
                    self.excluded_letters.append(current_letter)
                    self.excluded_letters = list(set(self.excluded_letters))
            elif f == 1:
                if i in self.guess_results[current_letter]:
                    self.guess_results[current_letter].remove(i)
                self.contained_letters.append(current_letter)
                self.contained_letters = list(set(self.contained_letters))
            elif f == 2:
                self.guess_results[current_letter] = [i]
                self.contained_letters.append(current_letter)
                self.contained_letters = list(set(self.contained_letters))
            else:
                raise ValueError('Invalid feedback value: {}'.format(f))

        # next guess
        next = self.next_guess()
        if next:
            return next
        else:
            print('No more words...')
            raise ValueError('No more words...')

    def init_guess(self):
        """Make initial guess"""
        guess_index = np.random.randint(self.config['initial_guess_range']) if self.config['random_guess'] else 0
        guess = self.words[guess_index]

        return guess

    def next_guess(self):
        """Make next guess"""
        if len(self.possible_words) == 0:
            possible_words = [w for w in self.words if self.is_valid(w)]
        else:
            possible_words = [w for w in self.possible_words if self.is_valid(w)]

        self.possible_words = possible_words

        if len(possible_words) > 0:
            guess_index = np.random.randint(min(len(possible_words), self.config['second_guess_range'])) if self.config['random_guess'] else 0
            self.current_guess = possible_words[guess_index]
            return self.current_guess
        else:
            return None


    def is_valid(self, word):
        """Check if the word is valid"""
        satisfy_known_letters = False
        satisfy_position = False

        if len(self.contained_letters) == 0 & len(self.excluded_letters) == 0:
            satisfy_known_letters = True
            satisfy_position = True
        else:
            for l in self.contained_letters:
                satisfy_known_letters = False
                satisfy_position = False
                satisfy_known_letters = all(l in word for l in self.contained_letters) and \
                                        all(l not in word for l in self.excluded_letters)
                if satisfy_known_letters:
                    allowed_letter_loc = self.guess_results[l]
                    satisfy_position = any(word[i] == l for i in allowed_letter_loc)
                if not satisfy_known_letters or not satisfy_position:
                    return False
        return satisfy_known_letters and satisfy_position


    def hint(self, guess, feedback):
        """
        Guess the next word given the history
        guess: ['planet', 'world']
        feedback: ['00000', '00001']
        """
        # start
        word_length = len(guess[0])
        self.word_length = word_length
        self.words, self.freq = load_words(self.config['word_file'], word_length)
        self.guess_results = {
            w: list(range(word_length)) for w in 'abcdefghijklmnopqrstuvwxyz'
        }

        for g, f in zip(guess, feedback):
            self.current_guess = g
            self.answer(f)
        possible_words_freq = [self.freq[self.words.index(w)] * 100 for w in self.possible_words]
        total_freq = sum(possible_words_freq)
        print(f'Possible Words: {self.possible_words}')
        print(f'Relative Possibility: {[f/total_freq * 100 for f in possible_words_freq]}')
