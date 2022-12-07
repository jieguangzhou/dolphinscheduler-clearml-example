from pydolphinscheduler.tasks import Python, Shell
from pydolphinscheduler.core.process_definition import ProcessDefinition

CONVERT_TAG = "# $PARAM:"


# load script to dolphinscheduler, and convert special param with CONVERT_TAG
def load_script(path):
    with open(path, 'r') as f:
        script_lines = []
        for line in f:
            if CONVERT_TAG not in line:
                script_lines.append(line)
                continue

            base_line, annotation = line.rstrip().split(CONVERT_TAG)
            param_name, param_value = base_line.split("=")
            param_value = param_value.strip()

            annotation = annotation or param_name.strip()
            annotation = "${%s}" % annotation.strip()

            if param_value.startswith('"') and param_value.endswith('"'):
                annotation = "\"" + annotation + "\""

            new_line = param_name + "= " + annotation + "\n"
            script_lines.append("# original: " + line)
            script_lines.append(new_line)

        script = "".join(script_lines)
        return script


# The default startup parameter for the workflow
dataset_name = "dolphinscheduler-demo"  # $PARAM:
dataset_project = "iris"  # $PARAM:
dataset_version = "1.0.0"  # $PARAM:

with ProcessDefinition(
    name="prepare_data",
    param={
        "dataset_name": dataset_name,
        "dataset_project": dataset_project,
    }
) as pd:

    # prepare training data and teams message data
    task_data_preprocessing = Python(name="prepare_data",
                                     definition=load_script("prepare_data.py"))

    task_upload_data = Shell(
        name="upload_data", command=load_script("upload_data.sh"))

    task_data_preprocessing >> task_upload_data

    pd.submit()

# The default startup parameter for the workflow
training_task_project = "dolphinscheduler-demo"
training_task_name = "LogisticRegression"

with ProcessDefinition(
    name="training",
    param={
        "dataset_name": dataset_name,
        "dataset_project": dataset_project,
        "dataset_version": dataset_version,
        "training_task_project": training_task_project,
        "training_task_name": training_task_name,
    }
) as pd:

    task_pull_data = Python(name="pull_data",
                            definition=load_script("pull_data.py"))

    task_training = Python(name="training",
                           definition=load_script("train_model.py"))

    task_pull_data >> task_training

    pd.submit()
