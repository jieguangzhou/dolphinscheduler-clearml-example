port=${port}
docker rm -f $(docker ps -a | grep "${port}->8080" | awk '{print $1}')
docker run -d -v ~/clearml.conf:/root/clearml.conf -v /tmp/clearml_test/:/tmp/clearml_test -p ${port}:8080 -e CLEARML_SERVING_TASK_ID=${service_id} clearml-serving-inference:latest
