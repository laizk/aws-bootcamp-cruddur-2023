# Week 1 — App Containerization

## Required Homework

### I watched all of the videos for the week:
- My key takeaway from Chirag's spending considerations is that for GitPod, need to ensure that there are no concurrent workspaces running as the consumption aggregates, hence the cost aggregates as well. One needs to explicitly stop the workspace when not anymore in use even if the workspace will be deleted after 30 minutes of idle time.
- My key takeaway from Ashish's Container security considerations is that it is recommended to utilize existing tools like Snyk to ensure containers are secure and have no vulnerabilities.
- Alongside with the instructions that Andrew has demonstrated in GitPod, I was also doing it in my local machine as part of the stretch homework below.

<br>

After following through the videos about "live stream", "OpenAI document", "Write Flask Backend Enpoint for Notifications" and "Write a React Page for Notifications" and referring to [Andrew Brown's week 1 instructions](https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-1/journal/week1.md), I was able to set up run front-end and back-end containers simultaneously and linked them together through docker-compose file.  I was also able to add in the Notifications feature. The final working results are shown below screenshot:

<br>

### Frontend

![Alt text](assets/week1/docker-frontend-deploy.png)


### Backend

![Alt text](assets/week1/docker-backend-deploy.png)

<br>

Below is a summary of steps I took to achieve the above final results:
1. For frontend, I ensured to run `npm install` within the frontend-react-js so the frontend container needs to copy the contents of node_module folder. To automatically achieve this when gitpod is launched, I modified [gitpod.yml](../.gitpod.yml) to include below:
   
   ![Alt text](assets/week1/gitpod-frontend-npm-install.png)

2. Created [Dockerfile](../frontend-react-js/Dockerfile) at frontend
3. Created [Dockerfile](../backend-flask/Dockerfile) at backend
4. For the above, ensure that the Dockerfiles are in the correct directories
5. Create [docker-compose.yml](../docker-compose.yml) to orchestrate running the frontend and backend containers.
6. Performed `compose up` over the docker-compose.yml file to start running the containers.
   
    ![Alt text](assets/week1/compose-up.png)

    or run the code:

    ```sh
    docker-compose up
    ```

    or 

    ```sh
    docker compose up
    ```

7. When the run was done, I ensured to make the ports are running successfully and make them public
   
   ![Alt text](assets/week1/ports-public.png)

8. Verified that both backend and frontend components are working.
9. At backend, I appended `/api/activies/home` to the url and esure that a message in JSON format is returned.
10. At frontend, I ensured to see all elements of the Cruddur app. User will need to sign up and sign in to see the full features.
11. To add notifications, I added/modified the following scripts as per instructions:
    1.  Frontend:  
        1.  [NotificationsFeedPage.css](../frontend-react-js/src/pages/NotificationsFeedPage.css) - to cover any CSS styles similar to Home page.
        2.  [NotificationsFeedPage.js](../frontend-react-js/src/pages/NotificationsFeedPage.js) - to provide the actual React component for notifications.
        3.  [App.js](../frontend-react-js/src/App.js) - to include the Notifications component into the App
    
    2.  Backend:
        1.  [notifications_activities.py](../backend-flask/services/notifications_activities.py) - to facilitate the logic for notifications activities at the backend including the data
        2.  [app.py](../backend-flask/app.py) - to add the notifications_activities service into the application
        3.  [openapi-3.0.yml](../backend-flask/openapi-3.0.yml) - to add the notifications_activities service into the API service. At this point, I learned more about [OpenAPI](https://swagger.io/specification/#oas-components).

12. Changes were reflected in the applications.

<br>

### For the above, there are important docker commands I noted:

Build Container

```
docker build -t  backend-flask ./backend-flask
```

Run Container

```
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```

Get Container Images or Running Container Ids
```
docker ps
docker images
```

Gain Access to a Container
```
docker exec CONTAINER_ID -it /bin/bash
```

Delete an Image
```
docker image rm backend-flask --force
```

<br>

### Ran DynamoDB Local Container and ensured it worked

I first incorporated the follow code into the [gitpod.yml](../.gitpod.yml) file:

```yml
services:
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
```

Then, I followed the steps indicated in the [100 Days of Cloud](https://github.com/100DaysOfCloud/challenge-dynamodb-local) challenge by Andrew Brown:

### Result screenshot:

![Alt text](assets/week1/gitpod-dynamodb-success.png)


<br>

### Ran Postgres Container and ensured it worked
I first incorporated the follow code into the [gitpod.yml](../.gitpod.yml) file:

```yml
services:
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
volumes:
  db:
    driver: local
```

and

```yml
  - name: postgres
    init: |
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
      sudo apt update
      sudo apt install -y postgresql-client-13 libpq-dev
```

I was able to verify successful connection through:

### Database Explorer extension
![Alt text](assets/week1/gitpod-postgres-success.png)

### CLI

Using command:

```
psql -U postgres -h localhost
```

Screenshots:

![Alt text](assets/week1/gitpod-postgres-cli.png)
![Alt text](assets/week1/gitpod-postgres-psql.png)

<br>

## Homework Challenges

### Learned how to install Docker on my localmachine and get the same containers running outside of Gitpod / Codespaces
I installed Docker Desktop for Mac
![Alt text](assets/week1/docker-local-install.png)

I ran the same Dockerfile as was with the live stream
![Alt text](assets/week1/docker-local-image.png)

c. However, I noticed a difference. In local, only 5 layers were processed until "COPY . ." command. The rest did not show up.
![Alt text](assets/week1/docker-build-local.png)

d. I was able to successfully deploy backend-flask app locally, using the command:

```
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask 
```

Screenshot:

![Alt text](assets/week1/docker-deploy-local.png)


In the attempt to deploy the app locally, I created a :[docker-compose-local.yml](../docker-compose-local.yml)

I experienced an issue with using https for both FRONTEND_URL and BACKEND_URL. I search workaround in the internet and the one that worked for me is to change https to http. Not secure but anyway, this is local.

![Alt text](assets/week1/docker-run-frontend-local-error.png)


After the https -> http fix, I was able to successfully deploy frontend app using docker-compose.yml file from localhost and implemented the notifications changes locally:

![Alt text](assets/week1/frontend-notifications-local.png)

I also was able to successfully setup dynamodb and postgres:

DynamoDB:

![Alt text](assets/week1/dynamodb-local.png)


Postgres:

![Alt text](assets/week1/postgres-local.png)


*** However, there were pre-requisites I needed to do:
1. For Dynamodb tests, I installed AWS cli to my local machine by following the instructions in this [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
2. For Postgres, I installed postgres to my local machine by following the instructions in this [link](https://www.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/)


<br>

### Pushed and tagged a image to DockerHub (they have a free tier)

I used the following commands to push image to DockerHub:

```
docker tag backend-flask t0pz/aws-bootcamp-cruddur-2023-backend_flask:v1.0.0
docker push t0pz/aws-bootcamp-cruddur-2023-backend_flask:v1.0.0
```

CLI terminal screenshot:

![Alt text](assets/week1/dockerhub-push-cli.png)

Dockerhub screenshot:

![Alt text](assets/week1/dockerhub-push-ui.png)


### Implement a healthcheck in the V3 Docker compose file

I inserted the following command in [docker-compose.yml](../docker-compose.yml) to check the health for frontend:

```
    healthcheck:
      test: curl --fail http://localhost:3000 || exit 1
      interval: 60s
      retries: 5
      start_period: 20s
      timeout: 10s
```

Screenshot:

![Alt text](assets/week1/docker-compose-healthcheck.png)


To check health after `compose up` is run and all services up, I inspected the frontend container:

![Alt text](assets/week1/docker-compose-inspect-health.png)

<br>

### Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes. 

I tried to use just CLI for this challenge. The steps I did are:
1. Create the EC2 instance using CLI with user data to install
   1. Pre-requisites
      1. Security group ID (as shown below image)
         1. VPC ID [vpc-08f8bfea0b9921e41] - for the security group. 
         2. One Subnet ID [subnet-0880d493944aadd77] - to launch ec2 instance

            ![Alt text](assets/week1/challenge-ec2-vpc-subnet.png)
    
      2. AMI Id [ami-0dfcb1ef8550277af]
   
            ![Alt text](assets/week1/challenge-ec2-ami.png)


      3. Security Group ID [sg-02212de69fc7a47fd] to attach to ec2 instance. I created a security group using the VPC ID above:

        ```
            aws ec2 create-security-group \
                --group-name ec2-docker-sg \
                --description "AWS ec2 CLI SG for docker demo" \
                --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=ec2-docker-sg}]' \
                --vpc-id "vpc-08f8bfea0b9921e41"
        ```

      4. Add inbound firewall rules to the security group. I added 2 for SSH and for HTTP access.
   
        ```
            aws ec2 authorize-security-group-ingress \
                --group-id "sg-02212de69fc7a47fd" \
                --protocol tcp \
                --port 22 \
                --cidr "0.0.0.0/0" 
        ```

        ```
            aws ec2 authorize-security-group-ingress \
                --group-id "sg-02212de69fc7a47fd" \
                --protocol tcp \
                --port 80 \
                --cidr "0.0.0.0/0" 
        ```

      5. Create SSH Key Pair [demo-key]
        
        ```
            aws ec2 create-key-pair --key-name  wp-key-ec2-docker \
            --query 'KeyMaterial' --output text > ~/.ssh/wp-key-ec2-docker.pem
        ```

      6. Finally, create the EC2 instance. I created a [user data scripts](scripts/user_data.sh) to automatically install docker into the EC2 instance when launched.
   
    ```
        aws ec2 run-instances \
            --image-id ami-0dfcb1ef8550277af\
            --count 1 \
            --instance-type t2.micro \
            --key-name wp-key-ec2-docker \
            --security-group-ids sg-02212de69fc7a47fd \
            --subnet-id subnet-0880d493944aadd77 \
            --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=server}]' \
    --user-data file://<path to user_data.sh>
    ```

<br>

2. Access the EC2 instance and pull image, and perform some docker commands

    1. TO connect to the EC2 instance via SSH client, I followed steps #2, #3 and the example command in the screenshot below:

        ![Alt text](assets/week1/challenge-connect-to-instance.png)


        For #2, the location of the PEM file is the one indicated when creating SSH Key Pair.

        To ensure key is not publicly viewable
        ```
            chmod 400 wp-key-ec2-docker.pem
        ```

        Connect via SSH 
        ```
            ssh -i "wp-key-ec2-docker.pem" ec2-user@ec2-44-204-82-218.compute-1.amazonaws.com
        ```

        Screenshot of successful access and successful installation of docker:

        ![Alt text](assets/week1/challenge-ec2-connect.png)

    2. I pulled a sample public docker image

    ```
       docker pull bbachin1/node-api
    ```

    3. I ran the container
   
    ```
        docker run -d -p 80:3000 --name nodeapi bbachin1/node-api
    ```

    4. I verified it is running

    ```
        docker ps
    ```

    5. I executed into docker container

    ```
        docker exec -it nodeapi /bin/sh
    ```

    Screenshot of steps #2 to #5:

    ![Alt text](assets/week1/challenge-ec2-docker-commands.png)


    6. From AWS management console > EC2 instance, I navigated to the running instance and grabbed the Public IPv4 address:

    ![Alt text](assets/week1/challenge-console-public-ip.png)

    To check whether the app is working through the EC2 instance, I appended '/name/[any texts]' to the Public IPv4 address. In my case:

    ```
        http://44.204.82.218/name/Kristoffer%20Laiz
    ```

    Screenshot of result:

    ![Alt text](assets/week1/challenge-ec2-docker-output.png)

