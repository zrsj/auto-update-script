Prerequisites:
* Set up Git on your machine
* Create a GitHub account and set up a repo for the project
* Install PostgreSQL on your machine
* Populate the Northwind database as per https://github.com/pthom/northwind_psql
* Create a directory structure as follows:
```cd $HOME
mkdir -p workforce/{app1,app2,app3}/{sql,data,code}
tree -L 3 workforce
```
* Within each sql subdirectory, create a file query.sql that collects some data from the database
Tasks:

* Write a Python script that executes the queries and saves the output as data.csv within the respective data subdirectory
* Schedule the job to be done every morning at 7am
* Connect to the database directly from the app within the code subdirectory (to be provided)

Other deliverables:
* Prepare a presentation of no more than 10 slides by 18 February 2019, detailing what you’ve learned at the ATO
* Present to the team on 20 February 2019
