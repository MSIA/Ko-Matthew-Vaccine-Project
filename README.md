# MSiA423 Project: Mid-Pandemic Water Cooler Conversations
### Author: Matthew Ko
### QA: Christina Chang

<!-- toc -->

- [Project Charter](#project-charter)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Set up environment variables](#1-set-up-environment-variables)
    + [How to set up environment variables required](#how-to-set-up-environment-variables-required)
  * [2. Create database and acquire data from source](#2-create-database-and-acquire-data-from-source)
    + [Build the image](#build-the-image)
    + [Run acquire and create database](#run-acquire-and-create-database)
  * [3. Run the model training pipeline](#3-run-the-model-training-pipeline)
  * [4. Run the app](#4-run-the-app)

<!-- tocstop -->

## Project Charter
### 1. Vision
Now that we are on the verge of tackling the pandemic with the best of science and technology, namely vaccines produced by companies such as Moderna and Pfizer. To reach herd immunity, vaccines are the best way to avoid consequences such as overloading of hospitals and preventable deaths that would result from unchecked spreading of the virus. Additionally, it would allow society to function more normally at a much quicker rate. However, there are many individuals and groups within the United States that have decided not to receive any of the vaccines for a variety of reasons. But if you do not know one of these individuals very closely, but still need to share a space with them and risk your own or your family's health, an upfront confrontation may not change their mind about receiving the vaccine. In a satirical manner, this app's goal is to help users quickly gauge why an acquaintance at work or school might not want to get the vaccine so they can accommodate conversation topics naturally that may address these concerns. Water cooler conversations can now be productive in helping end this pandemic by naturally persuading people to get the vaccine and save lives.
### 2. Mission
Using the Household Pulse Survey public use files, [link](https://www.census.gov/programs-surveys/household-pulse-survey/datasets.html), this project will identify the most useful features of the survey in determining the reasons people will not get the COVID-19 vaccine, identified by multiple questions within the survey. Then, using these identified features, the app will ask for the user's input and predict how likely a user is to not get the vaccine for a given reason. Lastly, the app will provide possible conversation starters and links to sources with facts and figures that debunk certain myths.
### 3. Success Criteria
#### 1. Machine Learning Performance Metric
The model will be assessed using metrics suitable for classification, such as accuracy, F1-score, and recall. In this case, precision will likely be optimized so that we can be as sure as possible this person meets the criteria of someone that does not want the vaccine for a given reason. A precision of 70% required to go live with model.
#### 2. Business Metric
The business metric will be tracked by the number of users. If the number of users (overall site traffic) increases by 10% each month and the overall audience becomes more diverse, the app will be considered successful. Metrics tracked would be states people are viewing the site from, as well as volume of individuals from each state. Additionally, interactivity metrics such as number of times users used the app or whether they shared the app with others are effective at determining the app is useful. Ideally 50% of users use the app more than one time and 33% share it with others through social media or copying the link with a given button on the site.

## Directory structure

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API
│   ├── test.yaml                     <- Configurations for general source data information
│   
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git.
│   ├── additional/                   <- Created data sources for app
│   ├── clean/                        <- Clean data
│   ├── raw/                          <- Raw data
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── src/                              <- Source data for the project
│
├── tests/                             <- Files necessary for running model tests (see documentation below)
│
├── app.py                            <- Flask wrapper for running the model
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies
├── Makefile                          <- Wrapper for docker commands
```

## Running the app

### 1. Set up environment variables

Configuration files for running web app are located in the `config/` folder.
`config.py` includes variables to configure local data storage, as well as S3 bucket information\
flaskconfig.py includes configurations for flask app, including local and RDS MYSQL databases.

#### 1.1: How to set up environment variables required

The following environment variables are needed for the application to run in relation to AWS S3 and and RDS services.

For S3 services:
```bash
export AWS_ACCESS_KEY_ID="MY_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="MY_SECRET_ACCESS_KEY"
```

For RDS services:
```bash
export SQLALCHEMY_DATABASE_URI="{dialect}://{user}:{pw}@{host}:{port}/{db}"
```

The form of SQLALCHEMY_DATABASE_URI is above, where `dialect` is the type of sql database connecting to, the `user` is the database user, `pw` is the password, `host` is the host of the connection, along with the `port` and name of database `db`. If local, the SQLALCHEMY_DATABASE_URI is set by default to `sqlite:///data/vSentiment.db`.
If the SQLALCHEMY_DATABASE_URI is not set when running the app, it will use a locally created database. Instructions to create this database is in step 2.

### 2. Create database and acquire data from source

This step is required if you would like to run the app locally without connections to AWS S3 or RDS. This step will download the data from the source site as well as create a local database that are both required for the app. Optionally this step will allow the user to push the raw data into their own s3 bucket.

### 2.1 Build the image

The Dockerfile used for running the ingestion and setting up the database is located in the `app/` folder.

To build the image for ingesting the data and setting up the database, run this command from the root of the repository:

```bash
make image
```

Or building it directly with docker, run:

```bash
docker build -f app/Dockerfile -t vaccine_project_mjk3551 .
```

This command builds the Docker image, with the tag `vaccine_project_mjk3551`, based on the instructions in `app/Dockerfile` and the files existing in this directory.

### 2.2 Run acquire and create database

To acquire raw data, create the database and upload the raw data to S3, run from this directory:

```bash
make acquire
```

Or you can use run docker commands to run these steps individually:

Create database:

```bash
docker run --mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project_mjk3551 run.py create_db
```

Acquire raw data and upload it to S3:

```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project_mjk3551 run.py acquire --s3_raw s3://2021-msia423-ko-matthew/raw/pulse2021.csv
```

The raw data will be uploaded to the S3 path: `s3://2021-msia423-ko-matthew/raw/pulse2021.csv`. If you do not have the environment variables `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID` set, this step will result in an error.

### 3. Run the model training pipeline

This step follows the creation of the database and acquisition of the raw data. If environment variables `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID` indicated above are set correctly, run the following step and it will upload the training artifacts to S3. In addition, the directory is mounted so you should see the artifacts in the data and models folder.

```bash
make pipeline
```

Or you can use docker commands to run each step individually. However, it is recommended to run the make command above.

Clean the raw data:

```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project_mjk3551 run.py clean --s3_raw s3://2021-msia423-ko-matthew/raw/pulse2021.csv --s3_clean s3://2021-msia423-ko-matthew/clean/clean.csv
```

Train and evaluate model:

```bash
docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(shell pwd)",target=/app/ -p 5000:5000 vaccine_project_mjk3551 app.py
```

### 4. Run the app

This step follows the model training pipeline and requires the artifacts created in step 3. If the environment variable `SQLALCHEMY_DATABASE_URI` is set, it will attempt to use the specified database, otherwise it will use the default database created in step 2.2.

Note: If you are attempting to connect to the RDS database as part of Northwestern MSiA program with credentials set in the SQLALCHEMY_DATABASE_URI, please remember to connect to the Northwestern VPN.

Run from the root directory:

```bash
make app
```

Alternatively, you can run the functionality above, with a docker command.

```bash
docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(shell pwd)",target=/app/ -p 5000:5000 vaccine_project_mjk3551 app.py
```

After the command finishes, you should be able to access the app at: http://0.0.0.0:5000/
