# Build custom Locust Docker and deploy to OpenShift
How to run on Windows Subsystem for Linux (WSL) and how to create a custom Docker image.

# Run the official Docker image with a custom locustfile

Ref https://docs.locust.io/en/stable/running-locust-docker.html

```
$ docker run -p 8089:8089 -v $PWD:/mnt/locust locustio/locust:1.3.1 -f /mnt/locust/locusttest1.py
```

Be sure to specify the tag.  Suprisingly, the default tag "latest" is an older version 1.1 (4 month old)!

**Additional steps for users of WSL on Windows 10:**

The normal folders in Ubuntu WSL cannot be properly mounted to a Docker container. Files in WSL will not be visible to the container after mounting.
To fix this, copy the required file(s) to a new folder in the Windows path in WSL and mount the volume from there to the container:

```
$ mkdir /c/Users/[Windows_user]/Documents/JHU/Locust
$ cp ~/locust_test_tool/locusttest1.py  /c/Users/[Windows_user]/Documents/JHU/Locust
$ docker run -p 8089:8089 -v /c/Users/[Windows_user]/Documents/JHU/Locust:/mnt/locust locustio/locust:1.3.1  -f /mnt/locust/locusttest1.py
```

**Troubleshooting tips:**

You can add `-it --entrypoint bash` in front of the image in the docker run command to override the entrypoint command and log onto the container to inspect it.

```
docker run -p 8089:8089 -v /c/Users/[Windows_user]/Documents/JHU/Locust:/mnt/locust -it --entrypoint bash locustio/locust:1.3.1
```

**Test:**
Browse to http://localhost:8089/ to confirm that you can see the Locust UI.


# Create a custom Docker image with a custom locustfile and the official base image

Create a Dockerfile to copy a custom locustfile into the base image locustio/locust:1.3.1:

```
FROM locustio/locust:1.3.1
ADD locustfile.py /home/locust/
# RUN pip3 install ...
# USER locust
# WORKDIR /home/locust
ENTRYPOINT ["locust", "-f ", "./locustfile.py"]
# Tip: each argument must be separately quoted!!  Combing them would result in "Unknown User(s)" or cannot find .py file error.
```

Build a local Docker image and run it locally:

```
docker build -t jackhu008/locust:1.3.1 .
...
docker run -p 8089:8089  jackhu008/locust:1.3.1
```

**Troubleshooting:**

Override ENTRYPOINT command to log onto the container to inspect it:

```
docker run -p 8089:8089 -it  --entrypoint bash jackhu008/locust:1.3.1
```

**Test:**
Browse to http://localhost:8089/ to confirm that you can see the Locust UI.


# Deploy the Locust to OpenShift

Push the custom image to Docker Hub

```
$ docker images
$ docker push jackhu008/locust
```
This pushes the custom image to https://hub.docker.com/r/jackhu008/locust .

Deploy to OpenShift:

```
$ oc new-app jackhu008/locust:1.3.1
...

$ oc get svc
NAME     TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)             AGE
locust   ClusterIP   172.21.9.234   <none>        5557/TCP,8089/TCP   18m

$ oc expose svc/locust --port 8089

$ oc get routes
NAME     HOST/PORT                                                   PATH   SERVICES   PORT  ...
locust   locust-locust-test.your.openshift.cluster.appdomain.cloud          locust     8089  ...
```
**Test:**
Browse to http://locust-locust-test.your.openshift.cluster.appdomain.cloud to confirm that you can see the Locust UI. 
