# MSiA423 Project: Mid-Pandemic Water Cooler Conversations
### Author: Matthew Ko
### QA: Christina Chang

<!-- toc -->

- [Project Charter](#project-charter)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Set up environment variables](#1-set-up-environment-variables)
    + [How to set up environment variables required](#how-to-set-up-environment-variables-required)
  * [2. Build the image](#2-build-the-image)
  * [3. Push data to S3](#3-push-data-to-s3)
  * [4. Initialize the database](#4-initialize-the-database)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

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
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git.
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project.
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup.
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project
│
├── test/                             <- Files necessary for running model tests (see documentation below)
│
├── app.py                            <- Flask wrapper for running the model
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies
```

## Running the app

### 1. Set up environment variables

Configuration files for running web app are located in the `config/` folder.
CHANGEME.env needs to be renamed to config.env and it includes a place to store S3 Access Keys and RDS Host,User,Password,Port,and db information.\
config.py includes variables to configure local data storage, as well as S3 bucket information\
flaskconfig.py includes configurations for flask app, including local and RDS MYSQL databases.

#### 1.1: How to set up environment variables required\

The following environment variables are needed for the application to run in relation to AWS S3 and and RDS services.

For S3 services:
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY

For RDS services:
* MYSQL_HOST
* MYSQL_PORT
* MYSQL_USER
* MYSQL_PASSWORD
* MYSQL_DB

The provided CHANGEME.env file is provided for the user to edit and use for setting up the required environment variables. The user will then pass the required environment variables through subsequent docker run commands using -e or --env-file arguments. The CHANGEME.env file is not required if the user already has these environment variables currently defined. If the MYSQL_* variables are not set, the user can set the database to be built locally rather than through AWS RDS.

### 2. Build the image

The Dockerfile used for running the ingestion and setting up the database is located in the `app/` folder.

To build the image for ingesting the data and setting up the database, run this command from the root of the repository:

```bash
 docker build -f app/Dockerfile -t vaccine_project .
```

This command builds the Docker image for ingesting and setting up the databse, with the tag `project`, based on the instructions in `app/Dockerfile` and the files existing in this directory.

### 3. Push data to S3

To push data to S3, run from this directory:

```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY vaccine_project run.py ingest --s3path='s3://your-bucket/location-of-file-in-s3'
```

This command runs the `run.py` command in the `project` image to download the data from the source website, unzip it, and push the data into S3.


### 4. Initialize the database

#### Create the database
To create the database either in RDS or locally run from this directory:

```bash
docker run \
    -e MYSQL_HOST \
    -e MYSQL_USER \
    -e MYSQL_DB \
    -e MYSQL_PASSWORD \
    -e MYSQL_PORT \
    -e SQLALCHEMY_DATABASE_URI \
    --mount type=bind,source="$(pwd)/data/",target=/app/data/ \
     vaccine_project run.py create_db
```

If the MYSQL_HOST environment variable is set, the above command will attempt to connect to AWS RDS services and create the database there at the specified RDS instance.

Without a MYSQL_HOST environment variable set, the above command creates a local database located at `sqlite:///data/vSentiment.db`. If you would like to set the location of the database, please set the SQLALCHEMY_DATABASE_URI environment variable to the appropriate connection string before running the above command. Otherwise, it will be automatically generated and set to `sqlite:///data/vSentiment.db` and pass it into the docker run command above instead of / in addition to the environment variables listed above.

For midpoint PR: The table name created is called "vaccine_model" in both RDS and the local database. For chloe and fausto's convenience, will be removed later. I was able to see the table in RDS and use the local vSentiment.db using pandas.read_sql and sqlalchemy. 
