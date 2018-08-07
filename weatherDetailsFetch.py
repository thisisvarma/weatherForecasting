import requests
import time
import json
import pymysql
now=time.strftime("%Y%m%d%H%M%S")
print(now)
appid=str("0c42f7f6b53b244c78a418f4f181282a")
rawURL=str("http://api.openweathermap.org/data/2.5/weather?")
cities_list=["London,uk","phoenix,us"]	
numberOfCities=len(cities_list)

#function for city table update
def insert_wdf_city(cid,\
	cname,\
	clon,\
	clat,\
	ccod):
	db=pymysql.connect("172.17.0.2","root","Happy123","wdf")
	#SQL insert command to insert parsed data
	count_query=("select count(*) from wdf.city where city_id is not null;")
	sql_insert="insert into wdf.city VALUES('%d', '%s', '%d', %d, %d)" % \
	 (cid, cname, clon, clat, ccod)
	
#	sql_truncate1="SET FOREIGN_KEY_CHECKS = 0; TRUNCATE table wdf.city; SET FOREIGN_KEY_CHECKS = 1;"
	cursor=db.cursor()
	execusion1=cursor.execute(count_query)
	dbCityCount=eval("%s" % cursor.fetchone())
	
	if numberOfCities == dbCityCount:
		print("cities list in DB are upto date")
	else:
		execusion2=cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
		execusion3=cursor.execute("TRUNCATE table wdf.city")
		execusion4=cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
		execusion5=cursor.execute(sql_insert)
	db.commit()
	db.close()

# function to update weather table
def insert_wdf_weather(r_t,\
	c_c_id,\
	w_temp_mn,\
	w_temp_mx,\
	w_desc,\
	w_pr,\
	w_humi,\
	w_win_spd):
	db=pymysql.connect("172.17.0.2","root","Happy123","wdf")
	#SQL insert command to insert weather data
#	sql_insert="insert into wdf.weather(runner_time,\
#	weather_temp_min,\
#	weather_temp_max,\
#	weather_description,\
#	weather_pressure,\
#	weather_humidity,\
#	weather_wind_speed) VALUES('%d', '%d', '%d', '%s', '%d', '%d', '%d', '%d')" % \
	
	sql_insert="insert into wdf.weather(runner_time,\
	weather_temp_min,\
	weather_temp_max,\
	weather_description,\
	weather_pressure,\
	weather_humidity,\
	weather_wind_speed,\
	city_city_id) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
	(r_t,\
	w_temp_mn,\
	w_temp_mx,\
	w_desc,\
	w_pr,\
	w_humi,\
	w_win_spd,\
	c_c_id)

	cursor=db.cursor()
	execusion1=cursor.execute(sql_insert)
	db.commit()
	db.close()

for city in cities_list:
	URL=rawURL+"appid="+appid+"&q="+city
	print(URL)
	weatherResponseStatus=requests.get(URL)

	# writing status o/p to log file
	wdf1=open("wdfapi.log",mode='a')
	wdf1.write('{}, "current weather response status is : ",{}\n'.format(now,weatherResponseStatus))
	wdf1.close()

	#printing dictonary into JSON format
	data=weatherResponseStatus.json()
	
	#writing weather report to log file
	# wdf2=open("weatherreport.log",mode='a')
	# wdf2.write("{} - {} id={} temp={} humidity={} temp_max={} temp_min= {}\n".format\
	# 	(now,data['name'],data['id'],data['main']['temp'],data['main']['humidity'],data['main']['temp_max'],data['main']['temp_min']))
	# wdf2.close()

#	writing city parsing data to mySQL server
	insert_wdf_city(cid=data['id'],\
		cname=data['name'],\
		clon=data['coord']['lon'],\
		clat=data['coord']['lat'],\
		ccod=data['cod'])
	
#	writing weather parsing data to mySQL server
	insert_wdf_weather(r_t=now,\
		c_c_id=data['id'],\
	   	w_temp_mn=data['main']['temp_min'],\
	   	w_temp_mx=data['main']['temp_max'],\
	   	w_desc=data['weather'][0]['main'],\
	   	w_pr="pending",\
	   	w_humi=data['main']['humidity'],\
	   	w_win_spd=data['wind']['speed'])