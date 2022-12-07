# dolphinscheduler-clearml-example


## Create ClearML CREDENTIALS

[Connect ClearML SDK to the Server](https://clear.ml/docs/latest/docs/getting_started/ds/ds_first_steps#connect-clearml-sdk-to-the-server)

New configuration stored in /home/<username>/clearml.conf


## Start DolphinScheduler 

### Build Docker image

```
docker build -f Dockerfile -t dolphinscheduler-standalone-server:3.1.1-clearml .
```

### Start DolphinScheduler 

```
# please set the actual value "/home/<username>/clearml.conf" in the following command
docker run --name dolphinscheduler-standalone-server -v /home/<username>/clearml.conf:/root/clearml.conf -p 12345:12345 -p 25333:25333 -d dolphinscheduler-standalone-server:3.1.1-clearml
```

And then, you can log in to the DolphinScheduler at http://localhost:12345/dolphinscheduler/ui

user: admin
password: dolphinscheduler123


## Submit workflow

```shell
# install the pydolphinscheduler to submit workflow using python script
python3 -m pip install apache-dolphinscheduler==3.1.1
```

```shell
# pydolphinscheduler will search the gatway config in PYDS_HOME
export PYDS_HOME=./
python3 pyds.py
```

