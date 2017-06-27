# Logs Analysis

> Vishesh Mittal

## About

This is the third project for the Udacity Full Stack Nanodegree. In this project, a large database with over a million rows is explored by building complex SQL queries to draw business conclusions for the data. The project mimics building an internal reporting tool for a newpaper site to discover what kind of articles the site's readers like. The database contains newspaper articles, as well as the web server log for the site.

## To Run

### You will need:
- Python3
- Vagrant
- VirtualBox

### Setup
1. Install Vagrant And VirtualBox
2. Clone this repository

### To Run

Launch Vagrant VM by running `vagrant up`, you can then log in with `vagrant ssh`

To load the data, use the command `psql -d news -f newsdata.sql` to connect a database and run the necessary SQL statements.

The database includes three tables:
- Authors table
- Articles table
- Log table

In order to execute the program, you would need to create the following views:
- authors_score:

`create view authors_score as select articles.author as author_id, count(*) as views from articles left join log on concat('/article/', articles.slug)=log.path group by articles.author;`
- request_counts:

`create view request_counts as select date_trunc('day', time) as date, count(*) as request_count from log group by date;`
- error_counts:

`create view error_counts as select date_trunc('day', time) as date, count(*) as error_count from log where status not like '200%' group by date;`
- error_rates:

`create view error_rates as select to_char(request_counts.date, 'FMMonth FMDDth, YYYY') as date, round((error_counts.error_count * 100.0)/request_counts.request_count, 2) as error_rate from request_counts left join error_counts on request_counts.date=error_counts.date;`


To execute the program, run `python3 reporting.py` from the command line.
