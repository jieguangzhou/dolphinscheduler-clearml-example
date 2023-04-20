try:
    import joblib
except ImportError:
    from sklearn.externals import joblib
import os

from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt

from clearml import Task
import pickle
import random

training_task_project = "training"  # $PARAM:
training_task_name = "test"  # $PARAM:

# from here on everything is logged automatically
# Connecting ClearML with the current process,
task = Task.init(project_name=training_task_project,
                 task_name=training_task_name)

train_data_path = "/tmp/clearml_test/training/iris_dataset.pkl"

model_dir = f"/tmp/clearml_test/{training_task_project}/{training_task_name}/{task.id}"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "model.pkl")

datas = pickle.load(open(train_data_path, 'rb'))

iris = datas['source']
X = iris.data
y = iris.target

X_train = datas["X_train"]
X_test = datas["X_test"]
y_train = datas["y_train"]
y_test = datas["y_test"]

# sklearn LogisticRegression class
model = LogisticRegression(solver='liblinear', multi_class='auto')
model.fit(X_train, y_train)

joblib.dump(model, model_path, compress=True)

loaded_model = joblib.load(model_path)
result = loaded_model.score(X_test, y_test)
x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
h = .02  # step size in the mesh
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
plt.figure(1, figsize=(4, 3))

plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=plt.cm.Paired)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')

plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())

plt.show()
