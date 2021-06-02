import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import warnings
import pickle
from sklearn.ensemble import RandomForestClassifier


warnings.filterwarnings("ignore")

data = pd.read_csv("weather_app/utils/Forest_fire.csv")
data = np.array(data)

X = data[1:, 1:-1]
y = data[1:, -1]
y = y.astype('int')
X = X.astype('int')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
log_reg = RandomForestClassifier()


log_reg.fit(X_train, y_train)

inputt=[int(x) for x in "45 32 60".split(' ')]

final=[np.array(inputt)]

b = log_reg.predict_proba(final)


pickle.dump(log_reg, open('weather_app/routes/model.pkl', 'wb'))
model=pickle.load(open('weather_app/routes/model.pkl', 'rb'))
