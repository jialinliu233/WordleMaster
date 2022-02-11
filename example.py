from wordle_master import WordleMaster
from compare_word import compare_word

truth = 'jerry'
wm = WordleMaster()
guess1 = wm.start(len(truth))
print(f'Initial guess: {guess1} is {compare_word(truth, guess1)}')
guess2 = wm.answer(compare_word(truth, guess1))
while not guess2 == True:
    compare_result = compare_word(truth, guess2)
    print(f'{guess2} is {compare_result}')
    guess2 = wm.answer(compare_result)
