def load_words(file, length=5):
    with open(file) as word_file:
        all_data = word_file.read().splitlines()

    all_words_count = [w.split('\t') for w in all_data]
    all_words = [w[0].lower() for w in all_words_count]
    all_counts = [int(w[1]) for w in all_words_count]
    all_freqs = [float(w) / 580071238022 for w in all_counts]
    target_word_index = [i for i, w in enumerate(all_words) if len(w) == length]
    target_words = [all_words[i] for i in target_word_index]
    target_freqs = [all_freqs[i] for i in target_word_index]


    return target_words, target_freqs


if __name__ == '__main__':
    words, freqs = load_words('data/all_words.txt', 5)
    print(len(words))
    with open('data/words5.txt', 'w') as f:
        for i in range(len(words)):
            f.write(words[i] + '\t' + str(freqs[i]) + '\n')


