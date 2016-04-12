from math import sqrt


critics = {
	'Lisa Rose':{'Lady in the Water':2.5 , 'Snakes on a Plane':3.5 , 'Just My Luck':3.0 , 
	'Superman returns':3.5 , 'You, Me and Dupree':2.5, 'The Night Listener':3.0},

	'Gene Seymour':{'Lady in the Water':3.0 , 'Snakes on a Plane':3.5 , 'Just My Luck':1.5 , 
	'Superman returns':5.0 , 'You, Me and Dupree':3.5, 'The Night Listener':3.0},

	'Michael Phillips':{'Lady in the Water':2.5 , 'Snakes on a Plane':3.0 , 
	'Superman returns':3.5 , 'The Night Listener':4.0},

	'Claudia Puig':{'Snakes on a Plane':3.5 , 'Just My Luck':3.0 , 
	'Superman returns':4.0 , 'You, Me and Dupree':2.5, 'The Night Listener':4.5},

	'Mick LaSalle':{'Lady in the Water':3.0 , 'Snakes on a Plane':4.0 , 'Just My Luck':2.0 , 
	'Superman returns':3.0 , 'You, Me and Dupree':2.0, 'The Night Listener':3.0},

	'Jack Matthews':{'Lady in the Water':3.0 , 'Snakes on a Plane':4.0 , 
	'Superman returns':5.0 , 'You, Me and Dupree':3.5, 'The Night Listener':3.0},

	'Toby':{'Snakes on a Plane':4.5 , 'Superman returns':4.0 , 'You, Me and Dupree':1.0}
}

def sim_distance(prefers,person1,person2): 
	si = {}
	for item in prefers[person1]:
		if item in prefers[person2]:
			si[item] = 1
	if len(si)==0:
		return 0
	sum_of_squares = sum([pow(prefers[person1][item]-prefers[person2][item],2) for item in prefers[person1] if item in prefers[person2]])

	return 1/(1+sqrt(sum_of_squares))


def sim_pearson(prefers,p1,p2):
	si = {}
	for item in prefers[p1]:
		if item in prefers[p2]:
			si[item]=1
	n = len(si)
	if n==0:
		return 1
	
	sum1 = sum([prefers[p1][it] for it in si])
	sum2 = sum([prefers[p2][it] for it in si])

	sum1Sq = sum([pow(prefers[p1][it],2) for it in si])
	sum2Sq = sum([pow(prefers[p2][it],2) for it in si])

	pSum = sum([prefers[p1][it]*prefers[p2][it] for it in si])

	num = pSum - (sum1*sum2/n)
	den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den == 0:
		return 0

	r = num/den
	return r


def topMatches(prefers,person,n=5,similarity=sim_pearson):
	scores = [(similarity(prefers,person,other),other) 
		for other in prefers if other != person]
	scores.sort()
	scores.reverse()
	return scores[0:n]


def getRecommendations(prefers,person,similarity=sim_pearson):
	totals = {}
	simSums= {}
	for other in prefers:
		if other == person: continue
		sim = similarity(prefers,person,other)

		if sim <= 0 :
			continue
		for item in prefers[other]:
			if item not in prefers[person] or prefers[person][item]==0 :
				totals.setdefault(item,0)
				totals[item]+=prefers[other][item]*sim
				simSums.setdefault(item,0)
				simSums[item]+=sim

	rankings = [(total/simSums[item],item) for item,total in totals.items()]

	rankings.sort()
	rankings.reverse()
	return rankings


def transformPrefers(prefers):
	result = {}
	for person in prefers:
		for item in prefers[person]:
			result.setdefault(item,{})
			result[item][person] = prefers[person][item]
	return result


def calculateSimilarItems(prefers,n=10):
	result={}
	itemPrefers = transformPrefers(prefers)
	c=0
	for item in itemPrefers:
		c+=1
		if c%100 == 0 : print "%d / %d" % (c,len(itemPrefers))

		scores = topMatches(itemPrefers,item,n=n,similarity=sim_distance)
		result[item] = scores
	return result


def getRecommendationItems(prefers,itemMatch,user):
	userRating = prefers[user]
	scores = {}
	totalSim = {}

	for (item,rating) in userRating.items():
		for (similarity,item2) in itemMatch[item]:
			if item2 in userRating: continue
			scores.setdefault(item2,0)
			scores[item2]+=similarity*rating

			totalSim.setdefault(item2,0)
			totalSim[item2]+=similarity

	rankings = [(score/totalSim[item],item) for item,score in scores.items()]

	rankings.sort()
	rankings.reverse()
	return rankings



#print sim_distance(critics,'Lisa Rose','Gene Seymour')

#print sim_pearson(critics,'Lisa Rose','Gene Seymour')

#print topMatches(critics,'Toby',3,sim_distance)

#print getRecommendations(critics,'Toby')

#movies = transformPrefers(critics)
#print topMatches(movies,'Superman returns')
#print getRecommendations(movies,'Just My Luck')


itemSim = calculateSimilarItems(critics)
print getRecommendationItems(critics,itemSim,'Toby')
