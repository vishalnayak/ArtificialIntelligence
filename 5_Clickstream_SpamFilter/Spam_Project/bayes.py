###  File from parsing the train and test data ...
### Author : Ashish and Vishal
###   Usage :  python bayes.py train test


import sys
import os
import re
import time


### Creating dictionaries for keeping the ount of all the spam words along with their frequency and ham words along with their frequency.

spam = {}
ham = {}
cond_prob_word_seeing_ham = {}
cond_prob_word_seeing_spam ={}
cond_prob_spam_seeing_word = {}
cond_prob_ham_seeing_word = {}


####   This is the main parsing function which will first parse through the training data and build the has table.

def parsing_func():
	spam_count = 0
	ham_count = 0
	i = 2

####    Take the train file for training data from the command line as the second argument.
        f = open(sys.argv[1],"r")
 	for line in f:
		i = 2
		### Splitting the email on whitespaces and storing in a list called word
		word = line.split(" ")
		length = len(word)

		###   Checking for ham and then parsing through the email and storing the words occuring along with their frequency in the ham dictionary.
		if (word[1] == "ham"):
			ham_count += 1
			for k in range((length -2) /2):
				if word[i] not in ham:
					ham[word[i]] = int(word[i+1])
				else:
					ham[word[i]] = int(ham[word[i]]) +  int(word[i+1])
				i = i + 2
				k += 1
		###   Checking for spam and then parsing through the email and storing the words occuring along with their frequency in the spam dictionary.
		elif (word[1] == "spam"):
			spam_count += 1
			for k in range((length -2) /2):
                                if word[i] not in spam:
                                        spam[word[i]] = int(word[i+1])
                                else:
                                        spam[word[i]] = int(spam[word[i]]) +  int(word[i+1])
                                i = i + 2
                                k += 1
		else:
			print "Something wrong\n"
	#### calculating the probability of the spam and ham emails out of the total emails in the training set.
	total_count = spam_count + ham_count
	spam_prob = float(spam_count)/float(total_count)
	ham_prob = float(ham_count)/float(total_count)
	#####  Calculating the conditional probablity of word seeing that the mail is ham 
	for key,values in ham.items():
		cond_prob_word_seeing_ham[key] = float(values)/float(ham_count)
	#for keys,val in cond_prob_word_seeing_ham.items():
	#	print (keys,val)
	#####  Calculating the conditional probablity of word seeing that the mail is spam 
	for key,values in spam.items():
		cond_prob_word_seeing_spam[key] = float(values)/float(spam_count)
	#for keys,val in cond_prob_word_seeing_spam.items():
	#	print (keys,val)
	#for kkk,vvv in spam.items():
	#	print (kkk,vvv)


############    Precalculating the conditional probability of the mail being spam or ham given word i.e P(Spam/word) or P(ham/word)

	for key,values in spam.items():
		cond_prob_spam_seeing_word[key] = (float(cond_prob_word_seeing_spam[key])*float(spam_prob) )/( ( float(cond_prob_word_seeing_spam[key])*float(spam_prob) )  + ( float(cond_prob_word_seeing_ham[key])*float(ham_prob)  ) )
		cond_prob_ham_seeing_word[key] = 1 - float(cond_prob_spam_seeing_word[key])
		#print cond_prob_ham_seeing_word[key]		
	
####    Take the test file for testing data from the command line as the second argument.
#### Now we will parse through the test data and calculate the probability using bayes rule using Laplace smoothing.


	import math
	f = open(sys.argv[2],"r")
	counter = 0
	non_counter = 0
	hhh = 0
	sss = 0
 	for line in f:
		prob_of_spam = 0
		prob_of_ham = 0
		spam_score = 0
		ham_score = 0
		i = 2
		 ### Splitting the email on whitespaces and storing in a list called word

		word = line.split(" ")
		length = len(word)
		mail = word[1]
		if mail == "spam":
			sss += 1
		elif mail == "ham":
			hhh += 1
	#	print mail
		for k in range((length -2) /2):
			#print(word[i] + " " + word[i+1])
			#i = i + 2
			#k += 1
			

			#### Calculating the conditional probability for all the emails being spam or ham knowing that the word has already occured.

			if word[i] not in spam:
				prob_of_spam = 0
			else:
				if word[i] not in cond_prob_spam_seeing_word:
				#### Here we are doing laplace smoothing 

					cond_prob_spam_seeing_word[word[i]] = 1
				else:
					prob_of_spam = float(word[i+1])*float( math.log10(cond_prob_spam_seeing_word[word[i]]))
			if word[i] not in ham:
				prob_of_ham = 0
			else:
				if word[i] not in cond_prob_ham_seeing_word:
					cond_prob_ham_seeing_word[word[i]] =1
				else:
					prob_of_ham =float(word[i+1])* float( math.log10(cond_prob_ham_seeing_word[word[i]]))

			spam_score += prob_of_spam
			ham_score += prob_of_ham
			
			i = i +2
			k += 1

		#### Now we are just comparing the ham probability to spam probabilty score whichever is higher we are assigning that to the email and then checking for accuracy .

		#print(str(spam_score) + " " + str(ham_score))
		if spam_score > ham_score:
	#		print "It should be a SPAM"
			if mail == "spam":
	#			print "Bang ON ==================" 
				counter += 1
			#print spam_score, ham_score
		elif spam_score < ham_score:
	#		print "It should be a HAM"
			if mail == "ham":
				counter += 1
	print "Accruracy = ",
	print float(counter)*100/float(sss+hhh),
	print "%"
	############ the count of spam in test is sss and count of ham is hhh
	print "Spam count in test data = ",sss
	print "ham count in test data = ",hhh
	
####     These are for extracting the values of key and values from the dictionaries.....
	#for key in ham.keys():
	#	print key
	#for value in ham.values():
	#	print value
	
#	print ham
#	print "OOOOOOOOOOOOOOOOOOOOOOOOO\n"
#	print spam
	print "-----------------------------------\n"
	print "Spam count in train data = ",spam_count
	print "Ham count in train data = ",ham_count
parsing_func()

