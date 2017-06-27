import psycopg2

DB_NAME = 'news'
DB_USER = 'vagrant'

def get_most_popular_articles():
	"""gets the most popular three articles of all time, as a sorted list with the most popular article at the top."""
	conn = psycopg2.connect("dbname=%s user=%s" % (DB_NAME, DB_USER))
	cursor = conn.cursor()
	cursor.execute("select articles.title, count(*) as views from articles left join log"
	              " on concat('/article/',articles.slug)=log.path where path like '/article/%'"
	              " group by log.path, articles.title order by views desc limit 3;")
	popular_articles = cursor.fetchall()
	cursor.close()
	conn.close()
	return popular_articles


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


popular_articles = get_most_popular_articles()
#write to report
write_article_info(popular_articles)
