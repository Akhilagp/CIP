
#In [ ]:
import sys
import pandas as pd
import numpy as np
from sklearn import feature_extraction

#In [ ]:

import dataset
import pandas as pd
import numpy as np
from feature import  get_feature
from sklearn.externals import joblib

#In [ ]:

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn import metrics

#pre-load data
#In [ ]:

import os
def load_simple_data():
	files = os.listdir('./dgadetec/AlgorithmPowereddomains')
	
	domain_list = []
	for f in files:
		path = './dgadetec/AlgorithmPowereddomains/'+f
		domains = pd.read_csv(path,names=['domain'])
		domains = domains['domain'].tolist()
		for item in domains:
			domain_list.append(item)
	return domain_list

	'''
	def load_data():
	if os.path.exists('./dgadetec/resource/train.npy'):
		train = np.load('./dgadetec/resource/train.npy')
		return train

	domains360 = pd.read_csv('./dgadetec/resource/360.txt',
							header=None)[[1]]
	domains360 = domains360.dropna()
	domains360['label'] = [0]*domains360.shape[0]

	#domains360 = domains360.drop_duplicates()

	domainsdga = pd.read_csv('./dgadetec/resource/dga-feed.txt', 
								names=['domain'], 
								header=None)
	domainsdga = domainsdga.dropna()
	domainsdga['label'] = [0]*domainsdga.shape[0]

	domain_normal = pd.read_csv('./dgadetec/resource/normal_domains.csv', 
							names=['domain'],
							header=None)
	domain_normal = domain_normal.dropna()
	domain_normal['label'] = [1]*domain_normal.shape[0]


	train = np.concatenate((domains360.values, domainsdga.values, domain_normal.values),axis=0)

	#train = train.drop_duplicates(subset=1)
	
	#train = np.array(train)
	np.random.shuffle(train)
	np.save('./dgadetec/resource/train.npy', train)

	return train
	'''

def load_data():
	print("HEY")
	if os.path.exists('../datas/train.npy'):
		train = np.load('../datas/train.npy')
		return train
	train = pd.read_csv("blah.csv",header=None,names=['domain','label'])
	#print(train.head(5))
	print("tr",train.dtypes)
	train1 = np.array(train.values)
	print(np.where(np.isnan(train1)))
	np.random.shuffle(train1)
	np.save('../datas/train.npy', train1)

	return train



#In [5]:

data = load_data()
data = pd.DataFrame(data, columns=['domain', 'label'])
data = data.drop_duplicates(subset='domain')
data = np.array(data)
print(np.any(np.isnan(data)))
#print(np.where(np.isnan(data)))
print("all samples= ",data.shape)
print("dataY contains:", np.unique(data[:,1]))

#all samples=  (2101904, 2)
#dataY contains: [0 1]

#In [20]:

trainX = data[:5000,0]
trainY = data[:5000,1].astype(int) 
testX = data[5000:6000, 0]
testY = data[5000:6000, 1].astype(int)

#In [ ]:


#In [21]:

trainX = get_feature(trainX)
testX = get_feature(testX)


#In [38]:

print(trainX.shape)
#print(trainX.dtypes)
#Out[38]:

#(50000, 10)

#various models
#In [22]:

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
#In [23]:

def metric_me(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    f1 =f1_score(y_true, y_pred)
    
    return accuracy, f1

#In [24]:

simpleLR = LogisticRegression()
simpleLR.fit(trainX, trainY)
pred_y = simpleLR.predict(testX)
acc, f1 = metric_me(testY, pred_y)
print("simpleLR acc={} f1={}".format(acc, f1))
######################################################################
simpleSVM = SVC()
simpleSVM.fit(trainX,trainY)
pred_y = simpleSVM.predict(testX)
acc, f1 = metric_me(testY, pred_y)
print("simpleSVM acc={} f1={}".format(acc, f1))
###########################################################################3
simpleGBM = GradientBoostingClassifier()
simpleGBM.fit(trainX, trainY)
pred_y = simpleGBM.predict(testX)
acc, f1= metric_me(testY, pred_y)
print("simpleGBM acc={} f1={}".format(acc, f1))

###########################################################################3
simpleRF = RandomForestClassifier(n_estimators = 1000, max_depth = 2, random_state = 42)
simpleRF.fit(trainX,trainY)
pred_y = simpleRF.predict(testX)
acc, f1 = metric_me(testY,pred_y.round())
print("simpleRF acc={} f1={}".format(acc, f1))
###########################################################################3
simpleJ48 = tree.DecisionTreeClassifier()
simpleJ48.fit(trainX, trainY)
pred_y = simpleJ48.predict(testX)
acc, f1= metric_me(testY, pred_y)
print("simpleJ48 acc={} f1={}".format(acc, f1))
'''
simpleLR acc=0.912 f1=0.9098360655737705
simpleSVM acc=0.937 f1=0.9347150259067358
simpleGBM acc=0.94 f1=0.937888198757764
'''

#In [39]:

from sklearn.externals import joblib
joblib.dump(simpleLR, 'model_cr/LR.pkl')
joblib.dump(simpleSVM, 'model_cr/SVM.pkl')
joblib.dump(simpleGBM, 'model_cr/GBM.pkl')
joblib.dump(simpleRF,'model_cr/RF.pkl')
joblib.dump(simpleJ48,'model_cr/J48.pkl')
#Out[39]:

#['./dgadetec/models/GBM.pkl']

#In [37]:

import time

start = time.clock()
X = get_feature([sys.argv[1]])
print(X)
pred_result_GBM = simpleGBM.predict(X)
pred_result_SVM = simpleSVM.predict(X)
pred_result_LR = simpleLR.predict(X)
pred_result_RF = simpleRF.predict(X)
pred_result_J48 = simpleJ48.predict(X)
end = time.clock()

print(end-start)
print(pred_result_GBM)
print(pred_result_SVM)
print(pred_result_LR)
print(pred_result_RF)
print(pred_result_J48)
'''
[0.41643357]
0.051492580530577925
[0]
[1]
[0]
'''

