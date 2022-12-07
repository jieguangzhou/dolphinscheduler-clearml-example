import pickle
from clearml import Dataset
import os
import shutil


dataset_name = "iris_data"  # $PARAM:
dataset_project = "test"  # $PARAM:
dataset_version = "1.0.1"  # $PARAM:

train_data_path = "/tmp/clearml_test/training/iris_dataset.pkl"

dataset_folder = Dataset.get(
    dataset_name=dataset_name,
    dataset_project=dataset_project,
    dataset_version=dataset_version).get_local_copy()


dataset_path = os.path.join(dataset_folder, "iris_dataset.pkl")

datas = pickle.load(open(dataset_path, "rb"))


os.makedirs(os.path.dirname(train_data_path), exist_ok=True)
shutil.copyfile(dataset_path, train_data_path)

print(datas.keys())

print(dataset_path)
