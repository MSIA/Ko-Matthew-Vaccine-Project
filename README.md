# MSiA423 Project: Mid-Pandemic Water Cooler Conversations
### Author: Matthew Ko
### QA: Christina Chang

<!-- toc -->

- [Project Charter](#project-charter)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database)
    + [Adding additional songs](#adding-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
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

#### 1.1: how to set up environment variables required\

The following environment variables are needed for the application to run in relation to AWS S3 and and RDS services.

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
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
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY vaccine_project run.py --ingest --s3path='s3://your-bucket/location-of-file-in-s3'
```

This command runs the `run.py` command in the `project` image to download the data from the source website, unzip it, and push the data into S3.


### 1. Initialize the database

#### Create the database
To create the database in the location configured in `config.py` run:

`python run.py create_db --engine_string=<engine_string>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db`.

#### Adding songs
To add songs to the database:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on
##### Local SQLite database

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file:

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database
```

### 3. Run the Flask app

To run the Flask app, run:

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker

### 1. Build the image

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo):

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.

### 2. Run the container

To run the app, run from this directory:

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port.

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container

Once finished with the app, you will need to kill the container. To do so:

```bash
docker kill test
```

where `test` is the name given in the `docker run` command.

### Example using `python3` as an entry point

We have included another example of a Dockerfile, `app/Dockerfile_python` that has `python3` as the entry point such that when you run the image as a container, the command `python3` is run, followed by the arguments given in the `docker run` command after the image name.

To build this image:

```bash
 docker build -f app/Dockerfile_python -t pennylane .
```

then run the `docker run` command:

```bash
docker run -p 5000:5000 --name test pennylane app.py
```

The new image defines the entry point command as `python3`. Building the sample PennyLane image this way will require initializing the database prior to building the image so that it is copied over, rather than created when the container is run. Therefore, please **do the step [Create the database with a single song](#create-the-database-with-a-single-song) above before building the image**.

# Testing

From within the Docker container, the following command should work to run unit tests when run from the root of the repository:

```bash
python -m pytest
```

Using Docker, run the following, if the image has not been built yet:

```bash
 docker build -f app/Dockerfile_python -t pennylane .
```

To run the tests, run:

```bash
 docker run penny -m pytest
```
