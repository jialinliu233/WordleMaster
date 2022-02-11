from wordle_master import WordleMaster
wm = WordleMaster()
guess = ['power', 'indie', 'crimp', 'image']
feedback = ['00000', '10000', '00110', '11010']
wm.hint(guess, feedback)