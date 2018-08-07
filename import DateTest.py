# import time
# import requests
# import json
# print(dir(time))
# print(time.localtime())
# print(time.clock())
# print(time.process_time())

# Currr= time.strftime("%Y%m%d")
# print(Currr)

# print(dir(requests))
# print(dir(json))


# cities_list=["London,uk","Pheonix,us"]


# for city in cities_list:
# 	cityname=city
# 	print(cityname)


# data=open("city_list",mode='r')
# for row in data:
# 	country=us
# 	city_list=("{},{}".format(row,country))
# 	wd

import pymysql
#print(dir(pymysql))

# def insert_wdf_city(cid,cname,clon,clat,ccod):
# #	sql="INSERT INTO wdf.city VALUES (cid,cname,clon,clat,ccod)"
# 	db=pymysql.connect("172.17.0.2","root","Happy123","wdf")

# 	sql = "insert into wdf.city VALUES('%d', '%s', '%d', %d, %d)" % \
# 	 (cid, cname, clon, clat, ccod)
# 	cursor=db.cursor()
# 	excusion=cursor.execute(sql)
# 	db.commit()
# 	db.close()
# insert_wdf_city(123,"phx",123,123,123)

# def insert_wdf_weather(c_c_id,r_t,we_t_m,w_t_mx,w_desc,w_pr,w_hu,wea_w_sp):
# #	query="INSERT into weather(runner_time,weather_temp_min,weather_temp_max,weather_description,weather_pressure,weather_humidity,weather_wind_speed) \
# #	VALUES ("r_t",we_t_m,w_t_mx,w_desc,w_pr,w_hu,wea_w_sp)"
# """
# tested mysql insert command is 

# INSERT into weather(city_city_id,runner_time,weather_temp_min,weather_temp_max,weather_description,weather_pressure,weather_humidity,weather_wind_speed) \
# VALUES (1234,20180101,200,2000,"inert Test Decription",200,45,20);
# """
# 	query="INSERT into wdf.weather (city_city_id,runner_time,weather_temp_min,weather_temp_max,weather_description,weather_pressure,weather_humidity,weather_wind_speed) VALUES (c_c_id,r_t,we_t_m,w_t_mx,w_desc,w_pr,w_hu,wea_w_sp);"
# 	try:
# 		db=pymysql.connect("172.17.0.2","root","Happy123","wdf")
# 		cursor=db.cursor()
# 		cursor.execute(query)
# #		mysqlVersion=cursor.fetchone()
# #		print("mysqlVersion is: ",mysqlVersion)
# 	except Error as error:
# 		print(error)
# 	finally:
# 		db.close()

#insert_wdf_weather(2018010101,200,2000,"inert Test Decription",200,45,20)

def insert_wdf_weather(r_t,\
	c_id,\
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
	sql_insert="insert into wdf.weather VALUES('%d', '%d', '%d', '%d', '%s', '%d', '%d', '%d')" % \
	(r_t,\
		c_id,\
		w_temp_mn,\
		w_temp_mx,\
		w_desc,\
		w_pr,\
		w_humi,\
		w_win_spd)

	cursor=db.cursor()
	execusion1=cursor.execute(sql_insert)
	db.commit()
	db.close()

insert_wdf_weather(123454545,\
	2643743,\
	21,\
	321,\
	"pending",\
	2323,\
	123454543,\
	12345)

