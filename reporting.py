import psycopg2

DB_NAME = 'news'
DB_USER = 'vagrant'

def get_most_popular_articles():
	"""gets the most popular three articles of all time, as a sorted list with the most popular article at the top."""
	# Connect to an existing database
	conn = psycopg2.connect("dbname=%s user=%s" % (DB_NAME, DB_USER))
	# Open a cursor to perform database operations
	cursor = conn.cursor()
	# Query the database and obtain data as Python objects
	cursor.execute("select articles.title, count(*) as views from articles left join log"
	              " on concat('/article/',articles.slug)=log.path where path like '/article/%'"
	              " group by log.path, articles.title order by views desc limit 3;")
	popular_articles = cursor.fetchall()
	# Close communication with the database
	cursor.close()
	conn.close()
	return popular_articles


def get_most_popular_authors():
	"""gets the authors with the most page views, when you sum up all of the articles each author has written. 
	givess a sorted list with the most popular author at the top."""
	# Connect to an existing database
	conn = psycopg2.connect("dbname=%s user=%s" % (DB_NAME, DB_USER))
	# Open a cursor to perform database operations
	cursor = conn.cursor()
	# Query the database and obtain data as Python objects
	cursor.execute("select authors.name, authors_score.views from authors left join authors_score"
		           " on authors.id=authors_score.author_id order by views desc;")
	popular_authors = cursor.fetchall()
	# Close communication with the database
	cursor.close()
	conn.close()
	return popular_authors


def get_most_popular_authors():
	"""gets the authors with the most page views, when you sum up all of the articles each author has written. 
	givess a sorted list with the most popular author at the top."""
	# Connect to an existing database
	conn = psycopg2.connect("dbname=%s user=%s" % (DB_NAME, DB_USER))
	# Open a cursor to perform database operations
	cursor = conn.cursor()
	# Query the database and obtain data as Python objects
	cursor.execute("select authors.name, authors_score.views from authors left join authors_score"
		           " on authors.id=authors_score.author_id order by views desc;")
	popular_authors = cursor.fetchall()
	# Close communication with the database
	cursor.close()
	conn.close()
	return popular_authors


def get_down_times():
	"""gets the days when more than 1% of requests lead to errors"""
	# Connect to an existing database
	conn = psycopg2.connect("dbname=%s user=%s" % (DB_NAME, DB_USER))
	# Open a cursor to perform database operations
	cursor = conn.cursor()
	# Query the database and obtain data as Python objects
	cursor.execute("select * from error_rates where error_rate>1.0")
	down_times = cursor.fetchall()
	# Close communication with the database
	cursor.close()
	conn.close()
	return down_times


def write_article_info(articles):
	"""writes article-related information in report-file.txt"""
	report_file = open("report-file.txt", "a")
	report_file.write("MOST POPULAR ARTICLES:\n")
	
	for article in articles:
		report_file.write("\"")
		report_file.write(article[0])
		report_file.write("\" : ")
		report_file.write(str(article[1]))
		report_file.write(" views\n")

	report_file.write("\n\n\n")
	report_file.close()


def write_author_info(authors):
	"""writes author-related information in report-file.txt"""
	report_file = open("report-file.txt", "a")
	report_file.write("MOST POPULAR AUTHORS:\n")
	
	for author in authors:		
		report_file.write(author[0])
		report_file.write(" : ")
		report_file.write(str(author[1]))
		report_file.write(" views\n")

	report_file.write("\n\n\n")
	report_file.close()

def write_down_time_info(down_times):
	"""writes error-rate information in report-file.txt"""
	report_file = open("report-file.txt", "a")
	report_file.write("DOWN TIME INFO:\n")
	
	for down_time in down_times:		
		report_file.write(down_time[0])
		report_file.write(" : ")
		report_file.write(str(down_time[1]))
		report_file.write("% errors\n")

	report_file.write("\n\n\n")
	report_file.close()


popular_articles = get_most_popular_articles()
write_article_info(popular_articles)

popular_authors = get_most_popular_authors()
write_author_info(popular_authors)

down_times = get_down_times()
write_down_time_info(down_times)


# create view authors_score as select articles.author as author_id, count(*) as views from articles left join log on concat('/article/', articles.slug)=log.path group by articles.author;
# create view request_counts as select date_trunc('day', time) as date, count(*) as request_count from log group by date;
# create view error_counts as select date_trunc('day', time) as date, count(*) as error_count from log where status not like '200%' group by date;
# create view error_rates as select to_char(request_counts.date, 'FMMonth FMDDth, YYYY') as date, round((error_counts.error_count * 100.0)/request_counts.request_count, 2) as error_rate from request_counts left join error_counts on request_counts.date=error_counts.date;