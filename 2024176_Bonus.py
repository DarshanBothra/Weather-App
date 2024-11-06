'''
Progress:
collected data for different cities and their respective temperature upto dec 31
made the header, city and date select options
implemented required data collection for selecte date and city
implemented date and selected city obtaining method
'''

import json
import tkinter as Tk
import matplotlib as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 
from tkcalendar import Calendar

city_file_mapping = {
    'New Delhi': 'dataset/New_Delhi.json',
    'Hyderabad': 'dataset/Hyderabad.json',
    'Indore': 'dataset/Indore.json',
    'Kolkata': 'dataset/Kolkata.json',
    'Mumbai': 'dataset/Mumbai.json',
    'Bangaluru': 'dataset/Bangaluru.json'
}

selected_city = "New Delhi"
def callback(selection):
    global selected_city
    selected_city = selection
    

def go(date_box, cal):
    date = cal.get_date()
    date_list = date.split('/')
    date_list = [int(d) for d in date_list]
    final_date = ""

    # Check if the obtained date is valid
    if date_list[2] == 24:
        if date_list[0] in (10, 11, 12):
            date_list[2] = 2024
            temp = date_list[1]
            date_list[1] = date_list[0]
            date_list[0] = temp
            date_list = reversed(date_list)
            date_list = [str(d) for d in date_list]
            if date_list[2] in list('123456789'):
                date_list[2] = f'0{date_list[2]}'
            final_date = "-".join(date_list)
            date_box.destroy()
        else:
            invalid_date_label.config(text = 'Invalid Date')
    else:
        invalid_date_label.config(text = 'Invalid Date')
    
    # if a valid date is obtained, we can proceed with displaying statistics
    if final_date:
        showStatistics(selected_city, final_date)
        
def openDateBox():
    date_box = Tk.Toplevel()
    date_box.title('Pick a Date')
    date_box.geometry('800x400')

    head_label = Tk.Label(date_box, text = 'Select a Date between October 1, 2024 to December 31, 2024', font = ('Halvetica', 18))
    head_label.place(relx = 0.5, y = 20, anchor = Tk.CENTER, height = 30)

    cal = Calendar(date_box, select_mode = 'day', year =  2024, month = 10, day = 1, font = ('Halvetica', 15), foreground = 'black', background = 'white')
    cal.place(relx = 0.5, y = 165, anchor = Tk.CENTER)

    get_date_button = Tk.Button(date_box, text = 'Go', command = lambda: go(date_box, cal), font = ('Halvetica', 18))
    get_date_button.place(relx = 0.5, anchor = Tk.CENTER, y = 320, width = 150, height = 30)
    
    global invalid_date_label
    invalid_date_label = Tk.Label(date_box, text = "", font = ('Halvetica', 20, 'bold'))
    invalid_date_label.place(relx = 0.5, anchor = Tk.CENTER, y = 360)
    date_box.mainloop()

def showStatistics(city, date):
    # Show today's forecast
    filename = city_file_mapping[city]
    week_stats = dict()
    with open(filename, 'r') as f:
        content = json.load(f)
    
    for day in content['days']:
        if day['datetime'] == date:
            week_stats['Date'] = [date]
            max_temp =  day['tempmax'] # seven day
            week_stats['Max Temp'] = [max_temp]
            min_temp = day['tempmin'] # seven day
            week_stats['Min Temp'] = [min_temp]
            sunrise = day['sunrise']
            sunset =  day['sunset']
            precip = day['precip']
            humidity = day['humidity']
            windspeed =  day['windspeed']
            winddir = day['winddir']
            condition = day['conditions']
            desc = day['description']
            ind = content['days'].index(day)
            # print(max_temp, min_temp, feel_temp, sunrise, sunset, precip, humidity, windspeed, winddir, condition, desc)
            break
    # for seven day forecast
    i = ind +1
    while i< ind +7:
        date = content['days'][i]['datetime']
        max_temp = content['days'][i]['tempmax']
        min_temp = content['days'][i]['tempmin']   
  

        week_stats['Date'].append(date)
        week_stats['Max Temp'].append(max_temp)
        week_stats['Min Temp'].append(min_temp)
        i+=1  
    # for stat in week_stats:
    #     print(stat, week_stats[stat])
    # print(week_stats)
    
    # Header Stats
    today_forecast_label_head.config(text = f'{city}\t{date}\t{condition}', bg = '#D3D3D3')
    today_forecast_label_maxtemp.config(text = f'HI: {week_stats["Max Temp"][0]}')
    today_forecast_label_mintemp.config(text = f'LO: {week_stats["Min Temp"][0]}')

    # Week Forecast
    week_forecast_header = Tk.Label(root, text = 'Seven Day Forecast', font = ('Halvetica', 25,))
    week_forecast_header.grid(row = 5, column = 0, columnspan = 3)

    week_forecast_frame = Tk.Frame(root)
    week_forecast_frame.grid(row = 6, column = 0, rowspan = 7)

    for day_counter in range(7):
        date = week_stats['Date'][day_counter]
        max_temp = week_stats['Max Temp'][day_counter]
        min_temp = week_stats['Min Temp'][day_counter]

        date_label = Tk.Label(week_forecast_frame, text = "", font = ('Halvetica', 20))
        date_forecast_label = Tk.Label(week_forecast_frame, text = "", font = ('Halvetica', 20, 'bold'))

        date_label.config(text = f"{date}")
        date_forecast_label.config(text = f"HI: {max_temp}\tLO: {min_temp}")
        
        # print(date, max_temp, min_temp)
        if day_counter%2 == 0:
            date_label.config(bg = '#d3d3d3')
            date_forecast_label.config(bg = '#d3d3d3')

        date_label.grid(row = day_counter, column = 0, pady = 15)
        date_forecast_label.grid(row = day_counter, column = 1, pady = 15)

    # Week Graph

    graph_frame = Tk.Frame(root)
    graph_frame.grid(row = 6, column=1, columnspan = 2, rowspan = 7)
    
    fig = Figure(figsize = (5.5, 5.5), dpi = 100)
    a = fig.add_subplot(111)

    y1 = week_stats['Max Temp']
    y2 = week_stats['Min Temp']
    x = [r[5:] for r in week_stats['Date']]

    a.plot(x, y1, color = 'orange', label = "Maximum Daily Temperature")
    a.plot(x, y2, color = 'blue', label = "Minimum Daily Temperature")
    a.legend()

    canvas = FigureCanvasTkAgg(fig, master = graph_frame)
    canvas.get_tk_widget().pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=True)
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=True)

    # Sunrise and Sunset

    sunrise_label = Tk.Label(root, text = "", font = ('Halvetica', 22))
    sunset_label = Tk.Label(root, text = "", font = ('Halvetica', 22))

    sunrise_label.grid(row = 13, column = 0)
    sunset_label.grid(row = 14, column = 0, pady = 5)

    sunrise_label.config(text = f'Sunrise: {sunrise} AM')
    sunset_label.config(text = f'Sunset: {sunset} PM')
     
    # Precipitation and Humidity

    precip_label = Tk.Label(root, text = "", font = ('Halvetica', 22))
    humid_label = Tk.Label(root, text = "", font = ('Halvetica', 22))

    precip_label.grid(row = 13, column = 1)
    humid_label.grid(row = 14, column = 1, pady = 5)

    precip_label.config(text = f'Precipitation: {precip} mm')
    humid_label.config(text = f'Humidity: {humidity}%')

    # Windspeed and Wind Direction

    wind_speed_label = Tk.Label(root, text = "", font = ('Halvetica', 22))
    wind_dir = Tk.Label(root, text = "", font = ('Halvetica', 22))

    wind_speed_label.grid(row = 13, column = 2)
    wind_dir.grid(row = 14, column = 2, pady = 5)

    wind_speed_label.config(text = f'Wind Speed: {windspeed}')
    wind_dir.config(text = f'Wind Direction: {winddir}')

    # Day Conditions and Description

    cond.grid(row = 3, column = 0, pady = 15, sticky = 'e')
    description.grid(row = 3, column = 1, pady = 15, sticky = 'e')
    cond.config(text = f'{condition}:')
    description.config(text = f'\t{desc}')

root = Tk.Tk()

root.title('Weather Forecast')
root.iconbitmap('appicon.avif')
# Header Label
main_label = Tk.Label(root, text = 'Weather Forecast', font = ('Halvetica', 30, 'bold'), width = 60)
main_label.grid(row = 0, column = 0, columnspan = 3)

# City selection
cities = [
    'New Delhi',
    'Mumbai',
    'Kolkata',
    'Bangaluru',
    'Hyderabad',
    'Indore'
]

city_select = Tk.StringVar()
city_select.set('New Delhi')
city_drop_down = Tk.OptionMenu(root, city_select, *cities, command = callback)
city_drop_down.config(width = 20)
city_drop_down.config(font = ('Havetica', 18,))
city_drop_down.grid(row = 1, column = 0, )

# Date Selection
date_button = Tk.Button(root, text = 'Select Date', command = openDateBox, font = ('Halvetica', 18), width = 20)
date_button.grid(row = 1, column = 2, sticky = 'w')


# Forecast 
today_forecast_label_head = Tk.Label(root, text = "", font = ('Halvetica', 28))
today_forecast_label_head.grid(row = 2, column=0, columnspan = 3)

today_forecast_label_maxtemp = Tk.Label(root, text = "", font = ('Halvetica', 22))
today_forecast_label_maxtemp.grid(row = 4, column = 0, sticky = 'e')

today_forecast_label_mintemp = Tk.Label(root, text = "", font = ('Halvetica', 22))
today_forecast_label_mintemp.grid(row = 4, column = 1, sticky = 'e')

cond = Tk.Label(root, text = "", font = ('Halvetica', 25, 'bold'))
description = Tk.Label(root, text = "", font = ('Halvetica', 25))

root.mainloop()