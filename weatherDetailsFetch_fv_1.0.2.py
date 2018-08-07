import requests
import time
import json
import pymysql
now=time.strftime("%Y%m%d%H%M%S")

#constants
appid=str("0c42f7f6b53b244c78a418f4f181282a")
rawURL=str("http://api.openweathermap.org/data/2.5/weather?")
cities_list=['Ajo', 'Avondale', 'Bisbee', 'Casa Grande', 'Chandler', 'Clifton', 'Douglas', 'Flagstaff', 'Florence', 'Gila Bend', 'Glendale', 'Globe', 'Kingman',\
 'Bakersfield', 'Barstow', 'Belmont', 'Berkeley', 'Beverly Hills', 'Brea', 'Buena Park', 'Burbank', 'Calexico', 'Calistoga', 'Carlsbad', 'Carmel', 'Chico', 'Chula Vista',\
  'Claremont', 'Compton', 'Concord', 'Corona', 'Coronado', 'Costa Mesa', 'Culver City', 'Daly City', 'Davis', 'Downey', 'El Centro', 'El Cerrito', 'El Monte', 'Escondido', \
  'Eureka', 'Fairfield', 'Fontana', 'Fremont', 'Fresno', 'Fullerton', 'Garden Grove', 'Hayward', 'Hollywood', 'Huntington Beach', 'Indio', 'Inglewood', 'Irvine', 'La Habra',\
  'Laguna Beach', 'Lancaster', 'Livermore', 'Lodi', 'Lompoc', 'Long Beach', 'Los Angeles', 'Malibu', 'Martinez', 'Marysville', 'Menlo Park', 'Merced', 'Modesto', 'Monterey', 'Mountain View', 'Napa', 'Needles', 'Newport Beach', 'Norwalk', 'Novato', 'Oakland', 'Oceanside', 'Ojai', 'Ontario', 'Orange',\
  'Oroville', 'Oxnard', 'Pacific Grove', 'Palm Springs', 'Palmdale', 'Palo Alto', 'Pasadena', 'Petaluma', 'Pomona', 'Port Hueneme', 'Rancho Cucamonga', 'Red Bluff', 'Redding',\
  'Redlands', 'Redondo Beach', 'Redwood City', 'Richmond', 'Riverside', 'Roseville', 'Sacramento', 'Salinas', 'San Bernardino', 'San Clemente', 'San Diego', 'San Fernando',\
  'San Francisco', 'San Gabriel', 'San Jose', 'San Juan Capistrano', 'San Leandro', 'San Luis Obispo', 'San Marino', 'San Mateo', 'San Pedro', 'San Rafael', 'San Simeon',\
  'Santa Ana', 'Santa Barbara', 'Santa Clara', 'Santa Clarita', 'Santa Cruz', 'Santa Monica', 'Santa Rosa', 'Sausalito', 'Simi Valley', 'Sonoma', 'South San Francisco',\
  'Stockton', 'Sunnyvale', 'Susanville', 'Thousand Oaks', 'Torrance', 'Turlock', 'Ukiah', 'Vallejo', 'Ventura', 'Victorville', 'Visalia', 'Walnut Creek', 'West Covina',\
  'Whittier', 'Woodland', 'Yorba Linda', 'Yuba City']
numberOfCities=len(cities_list)

#function for city table update
def insert_wdf_city(cid,\
	cname,\
	clon,\
	clat,\
	ccod):
	db=pymysql.connect("172.17.0.2","root","Happy123","wdf")

#	SQL insert command to insert parsed data
	count_query=("select count(*) from wdf.city where city_id is not null;")
	sql_insert="insert into wdf.city VALUES('%d', '%s', '%d', %d, %d)" % \
	 (cid, cname, clon, clat, ccod)
	
#	sql_truncate1="SET FOREIGN_KEY_CHECKS = 0; TRUNCATE table wdf.city; SET FOREIGN_KEY_CHECKS = 1;"
	cursor=db.cursor()
	execusion1=cursor.execute(count_query)
	dbCityCount=eval("%s" % cursor.fetchone())
	
	if numberOfCities == dbCityCount:
		pass
#	print("cities list in DB are upto date")
	else:
#		execusion2=cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
#		execusion3=cursor.execute("TRUNCATE table wdf.city")
#		execusion4=cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
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
	sql_insert="insert into wdf.weather(runner_time,\
	weather_temp_min,\
	weather_temp_max,\
	weather_description,\
	weather_pressure,\
	weather_humidity,\
	weather_wind_speed,\
	city_city_id) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
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


#	Loop for Cities weather details check
for city in cities_list:
	URL=rawURL+"appid="+appid+"&q="+city
	weatherResponseStatus=requests.get(URL)

	# writing status o/p to log file
	wdf1=open("logs/wdfapi.log",mode='a')
	wdf1.write('{}, "city {} weather response status is : ",{}\n'.format(now,city,weatherResponseStatus))
	wdf1.close()

#	printing dictonary into JSON format
	data=weatherResponseStatus.json()

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
	   	w_pr=data['weather'][0]['description'],\
	   	w_humi=data['main']['humidity'],\
	   	w_win_spd=data['wind']['speed'])

