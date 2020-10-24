# Run Locust as a Docker container with a custom locustfile.py
Tips for WSL (Windows Subsystem for Linux) users and creation of a custom Docker image.
Ref https://docs.locust.io/en/stable/running-locust-docker.html

# Run the official Docker image with a custom locustfile

```
$ docker run -p 8089:8089 -v $PWD:/mnt/locust locustio/locust:1.3.1 -f /mnt/locust/locusttest1.py
```

Be sure to specify the tag.  Suprisingly, the default tag "latest" is an older version 1.1 (4 month old)!

**== Additional steps for users of WSL on Windows 10: ====**

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
