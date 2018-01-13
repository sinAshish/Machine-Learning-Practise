import numpy  as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

data=fetch_movielens(min_rating=3.0)


#print our dataset
print repr(data['train'])
print repr(data['test'])

#create diff models

model1=LightFM(loss='warp')
model2=LightFM(loss='logistic')
model3=LightFM(loss='bpr')
model4=LightFM(loss='warp-kos')

#train our models

model1.fit(data['train'],epochs=30,num_threads=2)
model2.fit(data['train'],epochs=30,num_threads=2)
model3.fit(data['train'],epochs=30,num_threads=2)
model4.fit(data['train'],epochs=30,num_threads=2)

#recommendation time


def sample_recommendation(model,data,user_ids):
	#number of users and movies in training data
    n_users, n_items = data['train'].shape
    print n_items, n_users
    #generate recommendations for each user we input
    for user_id in user_ids:

        #movies they already like
        known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]

        #movies our model predicts they will like
        scores = model.predict(user_id, np.arange(n_items))
        #rank them in order of most liked to least
        top_items = data['item_labels'][np.argsort(-scores)]

        #print out the results
        print("User %s" % user_id)
        print("     Known positives:")

        for x in known_positives[:10]:
            print("        %s" % x)

        print("     Recommended:")

        for x in top_items[:10]:
            print("        %s" % x)
            
sample_recommendation(model1, data, [3, 25, 450])
sample_recommendation(model2, data, [3, 25, 450])
sample_recommendation(model3, data, [3, 25, 450])
sample_recommendation(model4, data, [3, 25, 450])