from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.
def report(message_list):
    import csv
    import datetime
    def append_messages_to_csv(file_path, messages):
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            date=datetime.datetime.now()
            message_list.append(str(date))
            writer.writerow(messages)

    # messages_list = ["arun", "btl", "summa+"]
    file_path = "message.csv"
    append_messages_to_csv(file_path, message_list)
def fetch():
    import serial
    ser = serial.Serial('COM6', 9600)  
    cood = ser.readline().decode().strip()
    methane=ser.readline().decode().strip()
    height=ser.readline().decode().strip()
    return [cood,int(methane),int(height)]
def get():
    import requests
    import polyline
    import folium

    # Sample coordinates
    data = fetch()
    place_coords = [(10.828717639888575,77.05522150909225),(10.829032521118684,77.06515825260522)] # --> Default Coordinates for corporation 
    curr_cood=data[0].split()
    c_cood=(float(curr_cood[0]),float(curr_cood[1]))
    if data[1] <50 or data[2]>50000:
        if c_cood not in place_coords:
            place_coords.append(c_cood)
    else:
        if c_cood in place_coords:
            place_coords.remove(c_cood)
        


    print(data)
    # Initialize the map with the first coordinate as the starting location
    m = folium.Map(location= place_coords[0], zoom_start=12)
    # Connect the coordinates using OpenStreetMap OSRM API
    route_points = []
    for i in range(len(place_coords) - 1):
        origin = f"{place_coords[i][1]},{place_coords[i][0]}"
        destination = f"{place_coords[i + 1][1]},{place_coords[i + 1][0]}"
        url = f"http://router.project-osrm.org/route/v1/driving/{origin};{destination}?overview=full"

        # Send a request to the OSRM API
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 'Ok':
                # Extract the route geometry from the response
                route_geometry = data['routes'][0]['geometry']
                decoded_polyline = polyline.decode(route_geometry)

                # Add the decoded polyline points to the route
                route_points.extend(decoded_polyline)

    # Convert the route points to latitude and longitude coordinates
    route_lat = [point[0] for point in route_points]
    route_lon = [point[1] for point in route_points]

    # Add markers for the coordinates
    for index, point in enumerate(place_coords):
        folium.Marker(point,
                    popup=f"Location {index+1}",
                    icon=folium.Icon(color='red', icon_color='white', prefix='fa', icon='map-marker')
                    ).add_to(m)

    # Connect the points with a polyline
    folium.PolyLine(list(zip(route_lat, route_lon)), color='red', weight=2.5, opacity=1).add_to(m)

    # Save the map as an HTML file
    m.save(r'C:\Users\HARESH Admin\Desktop\Trash track\trashtrack\temp\kinathukadavu.html')
def signup(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        pword=request.POST.get('password')
        email=request.POST.get('email')
        user=User.objects.create_user(uname,email,pword)
        user.save()
        return redirect('main')
    return render(request,'signup.html')
def loggin(request):
    if request.method=='POST':
        username=request.POST.get('uname')
        password=request.POST.get('pword')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('main')
        else:
            return HttpResponse("Login failed")
    return render(request,'login.html')
def pollachi(request):
    if request.method=='POST':
        click=request.POST.get('click')
        print(click)
        get()
    return render(request,'pollachi.html')
def null(request):
    return render(request,'NULL.html')
def main(request):
    if request.method=='POST':
        name=request.POST.get('name')
        address=request.POST.get('add')
        msg=request.POST.get('message')
        report([name,address,msg])
    return render(request,'main.html')
def Coimbature(request):
    return render(request,'coimbatore.html')
def kinathukadavu(request):
    return render(request,'kinathukadavu.html')
