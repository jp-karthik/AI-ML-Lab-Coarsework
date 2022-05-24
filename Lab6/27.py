import pandas
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = pandas.read_csv("spambase.data",header=None)

X = data.iloc[:,:-1]
Y = data.iloc[:,-1]
scale = StandardScaler()
X=scale.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3)

# #for linear kernel
model = svm.SVC(kernel="linear",C=1)
model.fit(X_train,Y_train)
print("____________________________________________________________\n")
print("=>> Linear Kernel")
print(f"*Training Set accuracy: {model.score(X_train,Y_train)}")
print(f"*Test Set accuracy: {model.score(X_test,Y_test)}")
print("____________________________________________________________\n")

#for quadratic kernel
model = svm.SVC(kernel="poly",C=20,degree=2)
model.fit(X_train,Y_train)
print("____________________________________________________________\n")
print("=>> Quadratic Kernel")
print(f"*Training set accuracy: {model.score(X_train,Y_train)}")
print(f"*Test Set accuracy: {model.score(X_test,Y_test)}")
print("____________________________________________________________\n")

#for gaussian kernel
model = svm.SVC(kernel="rbf",C=1)
model.fit(X_train,Y_train)
print("____________________________________________________________\n")
print("=>> Guassian Kernel")
print(f"*Training Set accuracy: {model.score(X_train,Y_train)}")
print(f"*Test Set accuracy: {model.score(X_test,Y_test)}")
print("____________________________________________________________\n")