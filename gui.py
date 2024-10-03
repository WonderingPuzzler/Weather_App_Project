from tkinter import *
import requests
import json
from datetime import date



class GUI:
    def __init__(self, window: Tk) -> None:
        """
        Creates first GUI section and asks user what type of forecast they want

        :param window: Connects GUI elements to the main Tkinter window
        """

        self.api_key = 'a756d79cb586aea74ab654ea947af540' #API Key gotten from OpenWeatherMap.org using free account

        self.new_canvas(window)
        self.canvas.create_text(570, 50, text="    GET WEATHER!\n         ANYTIME!", fill="BLACK", font=("Arial", 25), anchor="center")
        self.canvas.create_oval(370, 110, 770, 450, fill="#FFDF57", outline="#FFDF57")

        self.button_5_day = Button(window, text='5-Day Weather', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_weather_cord(window))
        self.button_5_day.place(x=40, y=460, width=300, height=100)

        self.button_current = Button(window, text='Current Weather', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.current_weather_cord(window))
        self.button_current.place(x=810, y=460, width=300, height=100)

    def five_day_weather_cord(self, window: Tk) -> None:
        """
        Gets the coordinates needed for a 5-day weather forecast and creates the GUI necessary to get the information

        :param window: Connects GUI elements to main Tkinter window
        """

        self.next_screen(window)
        self.new_canvas(window)

        self.label_top = Label(window, text="TYPE IN THE LATITUDE AND LONGITUDE\n     FOR THE AREA THAT YOU NEED\n          5-DAY WEATHER FOR (include - sign if exists):", font=("Arial Bold", 20), anchor="center", bg='#2998D8')
        self.label_top.place(x=225, y=10)

        self.label_latitude = Label(window, text='LATITUDE', font=('Arial Bold', 20), bg='#2998D8')
        self.label_latitude.place(x=485, y=125)
        self.five_input_latitude = Entry(window)
        self.five_input_latitude.configure(font=('Arial Bold', 20))
        self.five_input_latitude.place(x=0, y=175, width=1150, height = 50)

        self.label_longitude = Label(window, text='LONGITUDE', font=('Arial Bold', 20), bg='#2998D8')
        self.label_longitude.place(x=470, y=240)
        self.five_input_longitude = Entry(window)
        self.five_input_longitude.configure(font=('Arial Bold', 20))
        self.five_input_longitude.place(x=0, y=290, width=1150, height=50)

        self.measurement = StringVar(value='FAHRENHEIT')
        self.radio_button = Radiobutton(window, text='TEMPERATURE IN FAHRENHEIT', font=('Arial Bold', 25), variable=self.measurement, value='FAHRENHEIT', bg='#2998D8')
        self.radio_button.place(x=10, y=350)
        self.radio_button = Radiobutton(window, text='TEMPERATURE IN CELSIUS', font=('Arial Bold', 25), variable=self.measurement, value='CELSIUS', bg='#2998D8')
        self.radio_button.place(x=625, y=350)


        self.button_back = Button(window, text='Back', font=('Arial Bold', 12), bg='#FFDF57',command=lambda: self.create_intro_again(window))
        self.button_back.place(x=20, y=490, width=300, height=100)

        self.button_continue = Button(window, text='Continue', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_date(window))
        self.button_continue.place(x=830, y=490, width=300, height=100)




    def current_weather_cord(self, window: Tk) -> None:
        """
        Gets the weather coordinates for a current weather forecast and makes the GUI that gets this information

        :param window: Connects GUI elements to main Tkinter window
        """
        self.next_screen(window)
        self.new_canvas(window)

        self.label_top = Label(window, text="TYPE IN THE LATITUDE AND LONGITUDE\n     FOR THE AREA THAT YOU NEED\n          CURRENT WEATHER FOR (include - sign if exists):", font=("Arial Bold", 20), anchor="center", bg = '#2998D8')
        self.label_top.place(x=225, y= 10)

        self.label_latitude = Label(window, text='LATITUDE', font=('Arial Bold', 20), bg='#2998D8')
        self.label_latitude.place(x=485, y=125)
        self.input_latitude = Entry(window)
        self.input_latitude.configure(font=('Arial Bold', 20))
        self.input_latitude.place(x=0, y=175, width=1150, height = 50)

        self.label_longitude = Label(window, text='LONGITUDE', font=('Arial Bold', 20), bg='#2998D8')
        self.label_longitude.place(x=470, y=240)
        self.input_longitude = Entry(window)
        self.input_longitude.configure(font=('Arial Bold', 20))
        self.input_longitude.place(x=0, y=290, width=1150, height=50)

        self.measurement = StringVar(value='FAHRENHEIT')
        self.radio_button = Radiobutton(window, text='TEMPERATURE IN FAHRENHEIT', font=('Arial Bold', 25), variable=self.measurement, value='FAHRENHEIT', bg='#2998D8')
        self.radio_button.place(x=10, y=350)
        self.radio_button = Radiobutton(window, text='TEMPERATURE IN CELSIUS', font=('Arial Bold', 25), variable=self.measurement, value='CELSIUS', bg='#2998D8')
        self.radio_button.place(x=625, y=350)


        self.button_back = Button(window, text='Back', font=('Arial Bold', 12), bg='#FFDF57',command=lambda: self.create_intro_again(window))
        self.button_back.place(x=20, y=490, width=300, height=100)

        self.button_continue = Button(window, text='Continue', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.current_date(window))
        self.button_continue.place(x=830, y=490, width=300, height=100)






    def five_day_date(self, window: Tk) -> None:
        """
        Has the GUI get the current date and time for 5-day forecast, so as to allow for the necessary .json() information to be taken. Also checks to make sure longitude and latitude is usable for forecast

        :param window: Connects GUI elements to main Tkinter window
        """

        if self.five_input_latitude.get().replace('.','').replace('-','').isnumeric() == False or self.five_input_longitude.get().replace('.','').replace('-','').isnumeric() == False:
            self.five_input_latitude.delete(0, END)
            self.five_input_longitude.delete(0, END)
            self.label_top = Label(window, text="BAD LONGITUDE OR LATITUDE ENTERED!", font=("Arial", 20), anchor="center")

        else:
            self.longitude = self.five_input_longitude.get().strip()
            self.latitude = self.five_input_latitude.get().strip()

            self.weather_data = requests.get(      #Request code, knowledge of status, and API use gotten from https://openweathermap.org/current & https://www.youtube.com/watch?v=baWzHKfrvqw
                f"https://api.openweathermap.org/data/2.5/forecast?lat={float(self.latitude)}&lon={float(self.longitude)}&units=imperial&appid={self.api_key}")
            self.status = self.weather_data.status_code

            if self.status == 400: #Code made with help by https://www.youtube.com/watch?v=baWzHKfrvqw
                self.five_input_latitude.delete(0, END)
                self.five_input_longitude.delete(0, END)
                self.label_top = Label(window, text="BAD LONGITUDE OR LATITUDE ENTERED!", font=("Arial", 20), anchor="center")
            else:
                self.longitude = self.five_input_longitude.get()
                self.latitude = self.five_input_latitude.get()

                self.next_screen(window)
                self.new_canvas(window)

                self.canvas.create_text(590, 50, text="TYPE TODAY'S DATE (DD/MM/YYYY)", fill="BLACK", font=("Arial", 20), anchor="center")
                self.canvas.create_text(590, 85, text="(ONLY SHOWS DAYS WITHIN CURRENT MONTH)", fill="BLACK", font=("Arial", 20), anchor="center")

                self.label_day = Label(window, text='DAY', font=('Arial Bold', 20), bg='#2998D8')
                self.label_day.place(x=535, y=125)
                self.input_day = Entry(window)
                self.input_day.configure(font=('Arial Bold', 18))
                self.input_day.place(x=0, y=175, width=1150, height=50)

                self.label_month = Label(window, text='MONTH', font=('Arial Bold', 20), bg='#2998D8')
                self.label_month.place(x=510, y=240)
                self.input_month = Entry(window)
                self.input_month.configure(font=('Arial Bold', 18))
                self.input_month.place(x=0, y=290, width=1150, height=50)

                self.label_year = Label(window, text='YEAR', font=('Arial Bold', 20), bg='#2998D8')
                self.label_year.place(x=520, y=355)
                self.input_year = Entry(window)
                self.input_year.configure(font=('Arial Bold', 18))
                self.input_year.place(x=0, y=405, width=1150, height=50)

                self.button_back = Button(window, text='Back', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_weather_cord(window))
                self.button_back.place(x=20, y=490, width=300, height=100)

                self.button_continue = Button(window, text='Continue', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_weather(window))
                self.button_continue.place(x=830, y=490, width=300, height=100)


    def current_date(self, window: Tk) -> None:
        """
        Makes the GUI to get the current date and time for current weather forecast, so as to allow for the necessary .json() information to be taken also checks to make sure longitude and latitude is usable for forecast

        :param window: Connects GUI elements to main Tkinter window
        """

        if self.input_latitude.get().replace('.','').replace('-','').isnumeric() == False or self.input_longitude.get().replace('.','').replace('-','').isnumeric() == False:
            self.input_latitude.delete(0, END)
            self.input_longitude.delete(0, END)
            self.label_top = Label(window, text="BAD LONGITUDE OR LATITUDE ENTERED!", font=("Arial", 20), anchor="center")
        else:
            self.longitude = self.input_longitude.get().strip()
            self.latitude = self.input_latitude.get().strip()

            self.weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={float(self.latitude)}&lon={float(self.longitude)}&units=imperial&appid={self.api_key}") #weather call gotten from https://openweathermap.org/current
            self.status = self.weather_data.status_code #knowledge of status code gotten from https://www.youtube.com/watch?v=baWzHKfrvqw and https://openweathermap.org/faq

            if self.status == 400: #Code made with help by https://www.youtube.com/watch?v=baWzHKfrvqw
                self.input_latitude.delete(0, END)
                self.input_longitude.delete(0, END)
                self.label_top = Label(window, text="BAD LONGITUDE OR LATITUDE ENTERED!", font=("Arial", 20), anchor="center")
            else:

                self.next_screen(window)
                self.new_canvas(window)

                self.canvas.create_text(590, 50, text="          CURRENT WEATHER GENERATING, \nPRESS CONTINUE BUTTON TO GAIN WEATHER INFO", fill="BLACK", font=("Arial", 20), anchor="center")

                self.canvas.create_oval(370, 110, 770, 450, fill="#FFDF57", outline="#FFDF57")

                self.button_back = Button(window, text='Back', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.current_weather_cord(window))
                self.button_back.place(x=20, y=490, width=300, height=100)

                self.button_continue = Button(window, text='Continue', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.current_weather(window))
                self.button_continue.place(x=830, y=490, width=300, height=100)



    def five_day_weather(self, window: Tk) -> None:
        """
        Creates the GUI and runs actions to create the five-day weather forecast, as well as allowing the user to go back or go find the current weather, changing measurement based on Fahrenheit or Celsius

        :param window: Connects GUI elements to main Tkinter window
        """

        self.weather_days = 0

        self.today_date = date.today()
        self.input_date = f'{self.input_year.get()}-{self.input_month.get()}-{self.input_day.get()}'

        try:
            self.input_date = date.fromisoformat(self.input_date)
        except :
            self.input_year.delete(0, END)
            self.input_month.delete(0, END)
            self.input_day.delete(0, END)

        if len(self.input_day.get()) != 2 or self.input_day.get().isnumeric() == False or len(self.input_month.get()) != 2 or self.input_month.get().isnumeric() == False or len(self.input_year.get()) != 4 or self.input_year.get().isnumeric() == False:
            self.input_year.delete(0, END)
            self.input_month.delete(0, END)
            self.input_day.delete(0, END)

        elif self.today_date != self.input_date:
            self.input_year.delete(0, END)
            self.input_month.delete(0, END)
            self.input_day.delete(0, END)

        elif self.input_month.get() == '02' and self.input_day.get() == '29':
            self.input_year.delete(0, END)
            self.input_month.delete(0, END)
            self.input_day.delete(0, END)

        else:
            if self.input_month.get() in ['01', '03', '05', '07', '08', '10','12'] and self.input_day.get() == '31' or self.input_month.get() in ['04', '06', '09', '11'] and self.input_day.get() == '30' or self.input_month.get() == '02' and self.input_day.get() == '28':
                self.weather_days = 1

            elif self.input_month.get() in ['01', '03', '05', '07', '08', '10','12'] and self.input_day.get() == '30' or self.input_month.get() in ['04', '06', '09', '11'] and self.input_day.get() == '29' or self.input_month.get() == '02' and self.input_day.get() == '27':
                self.weather_days = 2

            elif self.input_month.get() in ['01', '03', '05', '07', '08', '10','12'] and self.input_day.get() == '29' or self.input_month.get() in ['04', '06', '09', '11'] and self.input_day.get() == '28' or self.input_month.get() == '02' and self.input_day.get() == '26':
                self.weather_days = 3

            elif self.input_month.get() in ['01', '03', '05', '07', '08', '10','12'] and self.input_day.get() == '28' or self.input_month.get() in ['04', '06', '09', '11'] and self.input_day.get() == '27' or self.input_month.get() == '02' and self.input_day.get() == '25':
                self.weather_days = 4


            self.year = self.input_year.get()
            self.year = int(self.year)
            self.month = self.input_month.get()
            self.month = int(self.month)
            self.day = self.input_day.get()
            self.day = int(self.day)

            self.hour = '06:00:00'

            self.next_screen(window)
            self.new_canvas(window)


            self.temp_list = []
            self.temp_min_list = []
            self.weather_list = []

            if self.measurement.get() == 'FAHRENHEIT':
                self.weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={float(self.latitude)}&lon={float(self.longitude)}&units=imperial&appid={self.api_key}") #5-day weather request gotten from https://openweathermap.org/forecast5
                self.data = self.weather_data.json() #Knowledge of .json() and interaction with openweathermap.org gotten from https://www.youtube.com/watch?v=baWzHKfrvqw

                for i in range(6):
                    self.day_2 = int(self.day) + i
                    if self.month < 10:
                        self.month_2 = str(0) + str(self.month)
                    if self.day < 10:
                        self.day_2 = str(0) + str(int(self.day) + i)
                    if self.month >= 10 or self.day >= 10:
                        self.month_2 = self.month



                    self.time = f"{self.year}-{self.month_2}-{self.day_2} {self.hour}" #Help in knowledge of how to extract parts of .json gained from https://www.youtube.com/watch?v=baWzHKfrvqw
                    for forecast in self.data['list']:

                        if forecast['dt_txt'] == self.time:

                            self.temp_list.append(forecast['main']['temp']) #Similar code can be found in https://www.youtube.com/watch?v=baWzHKfrvqw
                            self.temp_min_list.append(forecast['main']['temp_min']) #Similar code can be found in https://www.youtube.com/watch?v=baWzHKfrvqw
                            self.weather_list.append(forecast['weather'][0]['main']) #Similar code can be found in https://www.youtube.com/watch?v=baWzHKfrvqw
                            break

                if self.weather_days == 1:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°F\n\n{self.temp_min_list[0]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")

                elif self.weather_days == 2:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°F\n\n{self.temp_min_list[0]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°F\n\n{self.temp_min_list[1]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")

                elif self.weather_days == 3:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°F\n\n{self.temp_min_list[0]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°F\n\n{self.temp_min_list[1]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(560, 300, text=f"{self.weather_list[2]}\n\n\nDay 3\n\n{self.temp_list[2]}°F\n\n{self.temp_min_list[2]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")

                elif self.weather_days == 4:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°F\n\n{self.temp_min_list[0]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°F\n\n{self.temp_min_list[1]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(560, 300, text=f"{self.weather_list[2]}\n\n\nDay 3\n\n{self.temp_list[2]}°F\n\n{self.temp_min_list[2]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(785, 300, text=f"{self.weather_list[3]}\n\n\nDay 4\n\n{self.temp_list[3]}°F\n\n{self.temp_min_list[3]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                else:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°F\n\n{self.temp_min_list[0]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°F\n\n{self.temp_min_list[1]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(560, 300, text=f"{self.weather_list[2]}\n\n\nDay 3\n\n{self.temp_list[2]}°F\n\n{self.temp_min_list[2]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(785, 300, text=f"{self.weather_list[3]}\n\n\nDay 4\n\n{self.temp_list[3]}°F\n\n{self.temp_min_list[3]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(1010, 300, text=f"{self.weather_list[4]}\n\n\nDay 5\n\n{self.temp_list[4]}°F\n\n{self.temp_min_list[4]}°F", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")

            else:
                self.weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={float(self.latitude)}&lon={float(self.longitude)}&units=metric&appid={self.api_key}") #API code once again gotten from https://openweathermap.org/forecast5
                self.data = self.weather_data.json() #Knowledge of .json() and interaction with openweathermap.org gotten from https://www.youtube.com/watch?v=baWzHKfrvqw

                for i in range(6):
                    self.day_2 = int(self.day) + i
                    if self.month < 10:
                        self.month_2 = str(0) + str(self.month)
                    if self.day < 10:
                        self.day_2 = str(0) + str(int(self.day) + i)
                    if self.month >= 10 or self.day >= 10:
                        self.month_2 = self.month

                    self.time = f"{self.year}-{self.month_2}-{self.day_2} {self.hour}" # Again, https://www.youtube.com/watch?v=baWzHKfrvqw helped with how to disect .json() giving code examples
                    for forecast in self.data['list']:

                        if forecast['dt_txt'] == self.time:
                            self.temp_list.append(forecast['main']['temp']) #Similar code can be found in https://www.youtube.com/watch?v=baWzHKfrvqw
                            self.temp_min_list.append(forecast['main']['temp_min'])
                            self.weather_list.append(forecast['weather'][0]['main'])
                            break

                if self.weather_days == 1:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°C\n\n{self.temp_min_list[0]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")

                elif self.weather_days == 2:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°C\n\n{self.temp_min_list[0]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°C\n\n{self.temp_min_list[1]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")

                elif self.weather_days == 3:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°C\n\n{self.temp_min_list[0]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°C\n\n{self.temp_min_list[1]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")
                    self.canvas.create_text(560, 300, text=f"{self.weather_list[2]}\n\n\nDay 3\n\n{self.temp_list[2]}°C\n\n{self.temp_min_list[2]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")

                elif self.weather_days == 4:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°C\n\n{self.temp_min_list[0]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°C\n\n{self.temp_min_list[1]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")
                    self.canvas.create_text(560, 300, text=f"{self.weather_list[2]}\n\n\nDay 3\n\n{self.temp_list[2]}°C\n\n{self.temp_min_list[2]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")
                    self.canvas.create_text(785, 300, text=f"{self.weather_list[3]}\n\n\nDay 4\n\n{self.temp_list[3]}°C\n\n{self.temp_min_list[3]}°C", fill="#FFDF57", font=("Arial Bold", 30), anchor="center")

                else:
                    self.canvas.create_text(110, 300, text=f"{self.weather_list[0]}\n\n\nDay 1\n\n{self.temp_list[0]}°C\n\n{self.temp_min_list[0]}°C", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(335, 300, text=f"{self.weather_list[1]}\n\n\nDay 2\n\n{self.temp_list[1]}°C\n\n{self.temp_min_list[1]}°C", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(560, 300, text=f"{self.weather_list[2]}\n\n\nDay 3\n\n{self.temp_list[2]}°C\n\n{self.temp_min_list[2]}°C", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(785, 300, text=f"{self.weather_list[3]}\n\n\nDay 4\n\n{self.temp_list[3]}°C\n\n{self.temp_min_list[3]}°C", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")
                    self.canvas.create_text(1010, 300, text=f"{self.weather_list[4]}\n\n\nDay 5\n\n{self.temp_list[4]}°C\n\n{self.temp_min_list[4]}°C", fill="#FFDF57", font=("Arial Bold", 30),anchor="center")

            self.button_five_day = Button(window, text='More 5-Day Weather', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_weather_cord(window))
            self.button_five_day.place(x=20, y=550, width=300, height=50)

            self.button_more_city = Button(window, text='Current Weather', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.current_weather_cord(window))
            self.button_more_city.place(x=880, y=550, width=300, height=50)



    def current_weather(self, window: Tk) -> None:
        """
        Creates the GUI and runs actions to create the current weather forecast, as well as allowing the user to go back or go find the 5-day weather, changing measurement based on Fahrenheit or Celsius

        :param window: Connects GUI elements to main Tkinter window
        """

        self.next_screen(window)
        self.new_canvas(window)


        if self.measurement.get() == 'FAHRENHEIT':
            self.weather_data = requests.get( # API code can be found at https://openweathermap.org/current
                f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&units=imperial&appid={self.api_key}")
            self.data = self.weather_data.json() #Knowledge of .json() and interaction with openweathermap.org gotten from https://www.youtube.com/watch?v=baWzHKfrvqw


            self.temp = self.data['main']['temp'] #Similar code found in https://www.youtube.com/watch?v=baWzHKfrvqw; help with navigating .json() file
            self.feels_like = self.data['main']['feels_like']
            self.humidity = self.data['main']['humidity']
            self.air_pressure = self.data['main']['pressure']
            self.weather = self.data['weather'][0]['main']
            self.wind_speed = self.data['wind']['speed']
            self.cloud_percentage = self.data['clouds']['all']
            self.city = self.data['name']
            self.country = self.data['sys']['country']

            self.canvas.create_text(500, 50, text=f'CURRENT WEATHER IN {self.city}, {self.country}', font=("Arial Bold", 30), anchor="center" )
            self.canvas.create_text(200, 150, text=f"Feels Like: {self.feels_like}°F", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(175, 500, text=f"Air Pressure: {self.air_pressure}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(620, 500, text=f"Cloud Percentage: {self.cloud_percentage}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(1025, 500, text=f"Humidity: {self.humidity}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(950, 150, text=f"Wind Speed: {self.wind_speed}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(550, 300, text=f"{self.temp}°F", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(550, 225, text=f"{self.weather}", fill="BLACK", font=("Arial Bold", 28), anchor="center")

            self.button_five_day = Button(window, text='5-Day Weather', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_weather_cord(window))
            self.button_five_day.place(x=20, y=550, width=300, height=50)

            self.button_more_city = Button(window, text='Another City', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.current_weather_cord(window))
            self.button_more_city.place(x=880, y=550, width=300, height=50)

        else:
            self.weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&units=metric&appid={self.api_key}") # API code can be found at https://openweathermap.org/current
            self.data = self.weather_data.json() #Knowledge of .json() and interaction with openweathermap.org gotten from https://www.youtube.com/watch?v=baWzHKfrvqw


            self.temp = self.data['main']['temp'] #Similar code found in https://www.youtube.com/watch?v=baWzHKfrvqw; help with navigating .json() file
            self.feels_like = self.data['main']['feels_like']
            self.humidity = self.data['main']['humidity']
            self.air_pressure = self.data['main']['pressure']
            self.weather = self.data['weather'][0]['main']
            self.wind_speed = self.data['wind']['speed']
            self.cloud_percentage = self.data['clouds']['all']
            self.city = self.data['name']
            self.country = self.data['sys']['country']

            self.canvas.create_text(550, 50, text=f'CURRENT WEATHER IN {self.city}, {self.country}', font=("Arial Bold", 30), anchor="center")
            self.canvas.create_text(200, 150, text=f"Feels Like: {self.feels_like}°C", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(175, 500, text=f"Air Pressure: {self.air_pressure}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(620, 500, text=f"Cloud Percentage: {self.cloud_percentage}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(1025, 500, text=f"Humidity: {self.humidity}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(950, 150, text=f"Wind Speed: {self.wind_speed}", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(550, 300, text=f"{self.temp}°C", fill="BLACK", font=("Arial Bold", 28), anchor="center")
            self.canvas.create_text(550, 225, text=f"{self.weather}", fill="BLACK", font=("Arial Bold", 28),anchor="center")

            self.button_five_day = Button(window, text='5-Day Weather', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_weather_cord(window))
            self.button_five_day.place(x=20, y=550, width=300, height=50)

            self.button_more_city = Button(window, text='Another City', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.current_weather_cord(window))
            self.button_more_city.place(x=880, y=550, width=300, height=50)

    def next_screen(self, window: Tk) -> None:
        """
        Destroys the canvas and widgets so a new screen can be made
        :param window: connects GUI actions to main Tk window
        """
        self.canvas.destroy()
        [widget.destroy() for widget in window.winfo_children()]


    def new_canvas(self, window: Tk) -> None:
        """
        Creates a new canvas so new widgets and screen GUI can be made
        :param window: connects GUI actions to main Tk window
        """
        self.canvas = Canvas(window, width=1150, height=600, bg='#2998D8')
        self.canvas.pack()

    def create_intro_again(self, window: Tk) -> None:
        """
        Creates intro again since __init__ cannot be called multiple times, and so user can go back to start screen again
        :param window: connects GUI actions to main Tk window
        """

        self.next_screen(window)
        self.new_canvas(window)
        self.canvas.create_text(570, 50, text="    GET WEATHER!\n         ANYTIME!", fill="BLACK", font=("Arial", 25), anchor="center")

        self.canvas.create_oval(370, 110, 770, 450, fill="#FFDF57", outline="#FFDF57")

        self.button_5_day = Button(window, text='5-Day Weather', font=('Arial Bold', 12), bg='#FFDF57', command=lambda: self.five_day_weather_cord(window))
        self.button_5_day.place(x=40, y=460, width=300, height=100)

        self.button_current = Button(window, text='Current Weather', font=('Arial Bold', 12), bg='#FFDF57',command=lambda: self.current_weather_cord(window))
        self.button_current.place(x=810, y=460, width=300, height=100)

        self.button_current = Button(window, text='Current Weather', font=('Arial Bold', 12), bg='#FFDF57',command=lambda: self.current_weather_cord(window))
        self.button_current.place(x=810, y=460, width=300, height=100)
