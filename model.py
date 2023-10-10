import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
df=pd.read_csv("C:\\Users\\HI\\Desktop\\loan1.csv")
df=df.drop(['Loan_ID', 'Gender',"Married"], axis=1)
df2=df.dropna()
categorical=["Education","Self_Employed","Property_Area"]
from sklearn.preprocessing import OrdinalEncoder
oe=OrdinalEncoder(categories=[["Graduate","Not Graduate"],["Yes","No"],["Urban","Semiurban","Rural"]])
array=oe.fit_transform(df2[categorical])
categorical1=["Education1","Self_Employed1","Property_Area1"]
df3=pd.DataFrame(array,columns=categorical1)
df4=pd.DataFrame(np.hstack((df3[categorical1].values,df2)),columns=["Education1","Self_Employed1","Property_Area1","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area","Loan_Status"])
df4=df4.drop(categorical,axis=1)
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
array1=le.fit_transform(df4["Loan_Status"])
y=pd.DataFrame(array1)
X=df4.drop("Loan_Status",axis=1)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
from sklearn.preprocessing import PolynomialFeatures
polynomial_features=PolynomialFeatures(degree=3)
poly_converter=polynomial_features.fit_transform(X_train)
poly_converter1=polynomial_features.fit_transform(X_test)
from sklearn.ensemble import RandomForestClassifier
rfc=RandomForestClassifier(bootstrap=True,max_features= 'sqrt',n_estimators=50,oob_score=True,max_samples=0.75,random_state=42)
rfc.fit(poly_converter,y_train)
pickle.dump(rfc,open("model.pkl","wb"))
pickle.dump(df4,open("ordinal.pkl","wb"))