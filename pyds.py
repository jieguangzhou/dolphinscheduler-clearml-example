from pydolphinscheduler.tasks import Python, Shell
from pydolphinscheduler.core.process_definition import ProcessDefinition
from pydolphinscheduler.core.resource import Resource

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

environment_name='ml_pipeline'

with ProcessDefinition(
    name="prepare_data",
    param={
        "dataset_name": dataset_name,
        "dataset_project": dataset_project,
    }
) as pd:

    # prepare training data and teams message data
    task_data_preprocessing = Python(name="prepare_data",
                                     definition=load_script("prepare_data.py"),
                                     environment_name=environment_name)

    task_upload_data = Shell(
        name="upload_data", command=load_script("upload_data.sh"), environment_name=environment_name)

    task_data_preprocessing >> task_upload_data

    pd.submit()

# The default startup parameter for the workflow
training_task_project = "ds-demo"
training_task_name = "ds-lr"

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
                            definition=load_script("pull_data.py"), environment_name=environment_name)

    task_training = Python(name="training",
                           definition=load_script("train_model.py"), environment_name=environment_name)

    task_pull_data >> task_training

    pd.submit()

# output=$(clearml-serving create --name "${service_name}" --project "${service_project}")
# service_id=$(echo "$output" | grep -oP 'id=\K[a-z0-9]+')
service_name = "iris"
service_project = "ds-demo"
port = 16888
endpoint="iris_lr"
model_name=f"{training_task_name} - model"
project_name=training_task_project

# file_name = "preprocess.py"
#
# with open(file_name, "r") as f:
#       content = f.read()

with ProcessDefinition(
    name="deploy",
    param={
        "model_name": model_name,
        "project_name": project_name,
        "service_name": service_name,
        "service_project": service_project,
        "port": port,
        "endpoint": endpoint,
    },
   #  resource_list=[
   #    Resource(name=file_name, content=content),
   # ]
) as pd:
    create_service = Shell(name="create_service", 
                           command=load_script("create_service.sh"), 
                           environment_name=environment_name)
    create_service.add_out("service_id")
    add_endpoint = Shell(
            name="add_endpoint", 
            command=load_script("add_endpoint.sh"), 
            environment_name=environment_name, 
            # resource_list=[file_name],
            ) 
    start_service = Shell(name="start_service", 
                          command=load_script("start_service.sh"), 
                          environment_name=environment_name)

    curl_command = """curl -X POST "http://127.0.0.1:16888/serve/iris_lr" -H "accept: application/json" -H "Content-Type: application/json" -d '{"x0": 1, "x1": 2, "x2":5.9, "x3": 2.1}'"""
    test_server = Shell(name="test_server",
                        command = curl_command,
                        fail_retry_times=5,
                        fail_retry_interval=1)

    create_service >> add_endpoint >> start_service >> test_server
    pd.submit()



