from sklearn import datasets
from sklearn.model_selection import train_test_split
import pickle
import os

# Connecting ClearML with the current process,
# from here on everything is logged automatically

data_path = "/tmp/clearml_test/iris_dataset.pkl"

iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


datas = {
    "source": iris,
    "X_train": X_train,
    "X_test": X_test,
    "y_train": y_train,
    "y_test": y_test,
}


os.makedirs(os.path.dirname(data_path), exist_ok=True)

pickle.dump(datas, open(data_path, "wb"))

print("Saved dataset to {}".format(data_path))
