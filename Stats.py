import time
from datetime import date, timedelta
import datetime
from aqt import mw
from os.path import dirname, join, realpath
from aqt.utils import showInfo, tooltip
def Stats():
	###STREAK####
	config = mw.addonManager.getConfig(__name__)
	newday = int(config['newday'])
	reviews = mw.col.db.list("SELECT id FROM revlog")
	date_list = []
	Streak = 0
	for i in reviews:
		normal = time.strftime('%Y-%m-%d', time.gmtime(int(i)/1000.0))
		i = time.strftime('%Y-%m-%d-%H', time.gmtime(int(i)/1000.0))
		i = i.split("-")
		if int(i[3]) < newday:
			old_date = datetime.date(int(i[0]), int(i[1]), int(i[2]))
			one_day = datetime.timedelta(1)
			new_date = old_date - one_day
			date_list.append(str(new_date))
		else:
			date_list.append(normal)
	
	time_now = datetime.datetime.now().time()
	new_day = datetime.time(int(config['newday']),0,0)
	
	if time_now < new_day:
		start_date = date.today() - timedelta(days=1)
		start_date2 = date.today() - timedelta(days=1)
	else:
		start_date = date.today()
		start_date2 = date.today()

	end_date = date(2000, 1, 1)
	delta = timedelta(days=1)
	while start_date >= end_date:
		if start_date.strftime("%Y-%m-%d") in date_list:
			Streak = Streak + 1
		else:
			break
		start_date -= delta
	###REVIEWS TODAY####

	studied_today = mw.col.findCards('rated:1')
	total_cards = 0
	for i in studied_today:
		value = mw.col.db.execute("SELECT * FROM revlog WHERE cid = (?) ORDER BY id DESC",(i)).fetchall()
		for i in value:
			id_time = i[0]
			id_time = time.strftime('%Y-%m-%d', time.gmtime(int(id_time)/1000.0))
			if str(id_time) == str(start_date2):
				total_cards += 1

	###TIME SPEND TODAY###
	
	time_today = 0
	for i in studied_today:
		value = mw.col.db.execute("SELECT * FROM revlog WHERE cid = (?) ORDER BY id DESC",(i)).fetchall()
		for i in value:
			id_time = i[0]
			id_time = time.strftime('%Y-%m-%d', time.gmtime(int(id_time)/1000.0))
			# showInfo(str(id_time))
			# showInfo(str(date.today()))
			if str(id_time) == str(start_date2):
				time_today = time_today + int(i[7])
	time_today = round(time_today/60000, 1)

	return(Streak, total_cards, time_today)