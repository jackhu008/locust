FROM locustio/locust:1.3.1
ADD locustfile.py /home/locust/
#RUN pip3 install ...

USER locust

ENTRYPOINT ["locust", "./locustfile.py"] 
