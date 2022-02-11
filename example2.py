from wordle_master import WordleMaster


truth = 'lover'
wm = WordleMaster()
guess1 = wm.start(5)
print(guess1)
while True:
    print(wm.answer(str(input('Enter the result: '))))
