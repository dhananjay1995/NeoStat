from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import datetime
from statistics import mean

def Index(request):
	return render(request,'index.html')

## AJAX CALL TO GET DATA
@csrf_exempt		
def searchAPI(request):
	if request.method == "POST":
		start_date = request.POST.get("start_d")	
		end_date = request.POST.get("end_d")
		start_date = datetime.datetime.strptime(start_date,'%d-%m-%Y').strftime("%Y-%m-%d")
		end_date = datetime.datetime.strptime(end_date,'%d-%m-%Y').strftime("%Y-%m-%d")
		url = "https://api.nasa.gov/neo/rest/v1/feed?start_date="+str(start_date)+"&end_date="+str(end_date)+"&api_key=tYrMfAjtrLk6L2hgfC1lrKKpVZ33q2PjakiE1Lln"
		response = requests.get(url).json()["near_earth_objects"]
		dates, dates_values, fastest_list, closest_list, avg_list = ([] for i in range(5))

		for key in response:
			dates_values.append(len(response[key]))
			dates.append(key)
			key_data = response.get(key)
			fas = max(key_data, key=lambda fast: fast["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
			clo = min(key_data, key=lambda close: close["close_approach_data"][0]["miss_distance"]["kilometers"])
			avg_ast = [mean([size["estimated_diameter"]["kilometers"]["estimated_diameter_min"],size["estimated_diameter"]["kilometers"]["estimated_diameter_max"]]) for size in key_data]
			fastest_list.append(fas)
			closest_list.append(clo)
			avg_list.extend(avg_ast) 

		fastest_asteroid = max(fastest_list, key=lambda d: d["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])	
		closest_asteroid = min(closest_list, key=lambda d: d["close_approach_data"][0]["miss_distance"]["kilometers"])
		average_size = mean(avg_list)	
		print (fastest_asteroid)
		print (closest_asteroid)
		print (average_size)
		return JsonResponse({"dates":dates,"values":dates_values,
			"fastest_asteroid":fastest_asteroid,"closest_asteroid":closest_asteroid,
			"average_size":average_size
			})
	else:
		return JsonResponse({"error":"Method not supported"})	