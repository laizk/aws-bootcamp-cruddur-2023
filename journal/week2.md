# Week 2 — Distributed Tracing

## Required Homework

For all required homework, I followed along exactly (except that I did it in my local machine first, to save credits, then tested using GitPod) what Andrew has demonstration in the instructional videos and referring to the branch:
https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-2/journal/week2.md. 

The only difference is that I was also maintaining [docker-compose-local.yml](../docker-compose-local.yml) to run specifically in my local. Other than these, all steps are identical. Hence, I will not be repeating the same steps here but will show screenshots of my results.

### Telemetry

I setup honeycomb instrumentation in my local. Honeycomb received my data:

![Alt text](assets/week2/week2-local-backend-honeycomb-data.png)

I also received email from Honeycomb.io Support that a new dataset is created with the details.

![Alt text](assets/week2/week2-local-backend-honeycomb-email.png)

After setting a 'mock-data' span, I was able to see it in honeycomb:

![Alt text](assets/week2/week2-local-backend-honeycomb-2spans.png)

I was able to add app.now and app.result_length and see this in honeycomb

![Alt text](assets/week2/week2-local-backend-honeycomb-span-app.png)


### X-RAY

I was able to create the xray group

![Alt text](assets/week2/week2-local-backend-xray-group.png)

I was also able to create the sampling rule

![Alt text](assets/week2/week2-local-backend-xray-sampling.png)

I was able to make X-ray work

![Alt text](assets/week2/week2-local-backend-xray-working.png)

I was able to create custom subsegment. This one is a bit different as I did this in the [notifications_activities.py](../backend-flask/services/notifications_activities.py).

![Alt text](assets/week2/week2-local-xray-subsegment.png)


### CLOUDWATCH

I was able to configure cloudwatch at backend, and successfully sent logs in AWS Console

![Alt text](assets/week2/week2-local-cloudwatch.png)

### ROLLBAR

I was able to configure rollbar with test Hello World and with an error

Hello world!

![Alt text](assets/week2/week2-local-rollbar-helloworld.png)

With error (this is due to me still working on the x-ray segment/subsegment which caused error in notification page)

![Alt text](assets/week2/week2-local-rollbar.png)



