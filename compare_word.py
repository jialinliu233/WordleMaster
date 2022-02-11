def compare_word(truth, guess):
    results = [0 for i in range(len(truth))]
    for i, w in enumerate(truth):
        if w == guess[i]:
            results[i] = 2
        else:
            if w in guess:
                results[guess.index(w)] = 1

    return results
