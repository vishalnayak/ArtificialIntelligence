__author__ = 'vishal'

"""
Dictionary of all the spam words in the samples and the value is the respective frequency count.
"""
spam_words = {}
"""
Dictionary of all the not-spam words in the samples and the value is the respective frequency count.
"""
ham_words = {}
"""
Distinct words in the samples, size of which represents the vocab size
"""
words = {}

spam_mail_count = 0.0
ham_mail_count = 0.0
total_mail_count = 0.0

"""
Dictionary containing conditional probabilities of each word with respect to its class value.
"""
conditional_prob = {}


def main():
    """
    Builds the Naive Bayes model using the training data and predicts the data for test data.
    Compares the predicted and actual result and prints the statistics.
    """
    global spam_mail_count
    global ham_mail_count
    global total_mail_count
    import timeit

    """
    Timer to calculate running time
    """
    start_time = timeit.default_timer()
    f = open('train', 'r')
    for line in f:
        line_split = line.split(" ")
        line_length = len(line_split)
        """
        Counting the number of spam and not-spam emails
        """
        if line_split[1] == 'spam':
            spam_mail_count += 1
        else:
            ham_mail_count += 1

        """
        Each (word,frequency) pair is processed.
        If they belog to spam email, spam_words is updated.
        If they belog to spam email, ham_words is updated.
        Eventually, the count of all the words belonging to respective class is populated.
        """
        for word in range((line_length - 2) / 2):
            if line_split[1] == 'spam':
                if not line_split[word * 2 + 2] in spam_words:
                    spam_words[line_split[word * 2 + 2]] = 0
                spam_words[line_split[word * 2 + 2]] += int(line_split[word * 2 + 3])
            else:
                if not line_split[word * 2 + 2] in ham_words:
                    ham_words[line_split[word * 2 + 2]] = 0
                ham_words[line_split[word * 2 + 2]] += int(line_split[word * 2 + 3])
            """
            Filling words to calculate vocab size
            """
            if not line_split[word * 2 + 2] in words:
                words[line_split[word * 2 + 2]] = 0
        total_mail_count += 1
    f.close()
    print 'total lines:' + str(total_mail_count)
    print 'vocab size:' + str(len(words))

    spam_word_count = 0.0
    ham_word_count = 0.0
    for key in spam_words.keys():
        spam_word_count += spam_words[key]
    for key in ham_words.keys():
        ham_word_count += ham_words[key]

    print 'spam_word_count:' + str(spam_word_count)
    print 'ham_word_count:' + str(ham_word_count)
    print 'spam_mail_count:' + str(spam_mail_count)
    print 'ham_mail_count:' + str(ham_mail_count)
    print 'P(spam)=' + str(spam_mail_count / total_mail_count)
    print 'P(ham)=' + str(ham_mail_count / total_mail_count)

    """
    P(Spam)
    """
    p_spam = spam_mail_count / total_mail_count
    """
    P(Ham)
    """
    p_ham = ham_mail_count / total_mail_count

    """
    Laplace or Lidstone smoothing. 1 is Laplace. Less than 1 is Lidstone.
    """
    smoothing = 1

    """
    Conditional probabilities of spam words
    """
    for spam_word in spam_words:
        conditional_prob[(spam_word, 'spam')] = (spam_words[spam_word] + smoothing) / (spam_word_count + (len(words)))

    """
    Conditional probabilities of ham words
    """
    for ham_word in ham_words:
        conditional_prob[(ham_word, 'ham')] = (ham_words[ham_word] + smoothing) / (ham_word_count + (len(words)))

    import math

    """
    Processing test data
    """
    f = open('test', 'r')
    mismatch = 0
    for line in f:
        line_split = line.split(" ")
        line_length = len(line_split)
        """
        Both spam score and ham score is calculated for each email test sample
        """
        spam_score = math.log10(p_spam)
        ham_score = math.log10(p_ham)
        for word in range((line_length - 2) / 2):
            if not (line_split[word * 2 + 2], 'spam') in conditional_prob:
                spam_prob = 1
            else:
                spam_prob = conditional_prob[(line_split[word * 2 + 2], 'spam')]
            if not (line_split[word * 2 + 2], 'ham') in conditional_prob:
                ham_prob = 1
            else:
                ham_prob = conditional_prob[(line_split[word * 2 + 2], 'ham')]
            """
            Converting the spam and ham probabilities into log scale to make the computation additive instead of multiplicative
            """
            spam_score += math.log10(spam_prob)
            ham_score += math.log10(ham_prob)

        if spam_score > ham_score:
            print 'Classified as SPAM. Actual is ' + line_split[1]
            if 'spam' != line_split[1]:
                mismatch += 1
        else:
            print 'Classified as HAM. Actual is ' + line_split[1]
            if 'ham' != line_split[1]:
                mismatch += 1
    time_taken = timeit.default_timer() - start_time
    print 'Mismatches:',
    print mismatch
    print 'Accuracy:',
    print 100.0 - ((mismatch / 1000.0) * 100.0)
    print 'Running Time:',
    print time_taken
    f.close()


if __name__ == '__main__':
    main()
