endpoint="${endpoint}"
model_name="${model_name}"
project_name="${project_name}"
clearml-serving --id ${service_id} model add --engine sklearn --endpoint "${endpoint}" --preprocess "preprocess.py" --name "${model_name}" --project "${project_name}"
