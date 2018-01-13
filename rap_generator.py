import re,random
import time
# freqDict is a dict of dict containing frequencies
def addToDict(fileName, freqDict):
	f = open(fileName, 'r')
	words = re.sub("\n", " \n", f.read()).lower().split(' ')

	# count frequencies curr -> succ
	for curr, succ in zip(words[1:], words[:-1]):
		# check if curr is already in the dict of dicts
		if curr not in freqDict:
			freqDict[curr] = {succ: 1}
		else:
			# check if the dict associated with curr already has succ
			if succ not in freqDict[curr]:
				freqDict[curr][succ] = 1;
			else:
				freqDict[curr][succ] += 1;

	# compute percentages
	probDict = {}
	for curr, currDict in freqDict.items():
		probDict[curr] = {}
		currTotal = sum(currDict.values())
		for succ in currDict:
			probDict[curr][succ] = currDict[succ] / currTotal
	return probDict

def markov_next(curr, probDict):
	if curr not in probDict:
		return random.choice(list(probDict.keys()))
	else:
		succProbs = probDict[curr]
		randProb = random.random()
		currProb = 0.0
		for succ in succProbs:
			currProb += succProbs[succ]
			if randProb <= currProb:
				return succ
		return random.choice(list(probDict.keys()))

def makeRap(curr, probDict, T = 500):
	rap = [curr]
	for t in range(T):
		rap.append(markov_next(rap[-1], probDict))
	return " ".join(rap)


rapFreqDict = {}
rapProbDict = addToDict('lyrics.txt', rapFreqDict)

startWord = raw_input("What do you want to start your rap with?\n")
print("Alright, your rap is being generated...")
time.sleep(5)
rap=makeRap(startWord, rapProbDict)
rap_file=open('generated_rap.txt','w')
rap_file.write(rap)
print 'Rap is Dope. Saved in a local file.'
