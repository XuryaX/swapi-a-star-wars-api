# SwapiEx: A Star Wars API Explorer

## Pre-requisites
- Python 3.x
- pip
- poetry

## Steps to Install Poetry
1. Open a terminal window
2. Run the following command to download and install Poetry:
```
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
``` 
3. Verify that Poetry is installed correctly by running the following command:
```
    poetry --version
   ``` 
If installed correctly, this should display the version of Poetry installed.

## Build
```
make build
```
## Run Tests
```
make test
```
## Run
```
make run
```

## Engineering Design Choices

### Functional Requirements
- Users can request to load data from an external source.
- Users can explore datasets and view details about each dataset.
- Users can view a grid of data with infinite scrolling.
- Users can view value counts for selected columns in the dataset.

### Non-Functional Requirements
- The application should be responsive and performant.
- The UI should be intuitive and easy to use.
- Optimize Memory Usage
- Fast Query Execution
- Low Latency

### High-Level Design
The Django application is divided into three main components:
1. The front-end, built with HTML, CSS, and JavaScript.
2. The back-end, built with Django and Django REST Framework.
3. The database, which stores the datasets' associated metadata.
4. The data-warehouse, which stores dataset splitted into different number of files.

### Low-Level Design

# Frontend
The front-end is responsible for rendering the UI and making API requests to the back-end. 
The front-end is fairly simple client decoupled from the Backend. It is easily possible to change to Angular fairly easily.

# Backend
The back-end provides the API endpoints for fetching datasets, data details, and value counts.
The database stores the datasets and their associated metadata.

*Loading & Storing Data*

The data is read from the source and split into individual CSV files, with each page of data saved into its own file. For larger datasets, only the small dataset that is requested is loaded into memory, rather than the entire file, to improve performance.

*Resolution of referenced resources.*

To resolve homeworld for characters, the result is cached in an in-memory cache to reduce the number of requests needed for resolution.

*Serving Data*

There are 2 functional requirements for exploration of data

There are two functional requirements for exploring data:

*Load data with pagination*

A page of data is loaded from memory and sent to the client. Only the page that is requested is loaded into memory and sent to the user.

*Value Count*

This function is similar to running the SQL query `select col_1,col_2,count(*) from table group by col_1,col_2`.
The `petl` library is used for aggregation after reading the entire dataset.


### API Signatures
The back-end provides the following API endpoints:
- GET /api/data/list - Returns a list of available datasets.
- GET /api/explore/{dataset_id}/{page} - Returns a page of data for the given dataset.
- GET /api/explore/value_count/{dataset_id}/{columns} - Returns value counts for the specified columns in the given dataset.
- POST /api/fetch_and_process/ - Triggers a background process to fetch and process new datasets.

### Potential Improvements

- To make a stable data service, we can setup a cronjob to fetch latest data from external server.
- In Production environment we would probably be using a file-storage service like S3
- We would probably want to use a cache that can be shared with multiple requests. We can fairly easily use Redis.
- async i/o can be used to improve performance with parallel I/O.
