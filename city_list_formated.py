## listing city formates
city_list=[]
country=",us"
with open('Documents/hobbie_projects/weatherForecasting/city_list') as fp:
	for line in fp:
#		place=str(line)+str(country)
		city_list.append(line)

city_list[:]=[n.rstrip('\n') for n in city_list]
print(city_list)