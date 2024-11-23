from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from tkinter import messagebox
from datetime import datetime
from tkinter import *
import requests
import pytz

def is_connected():
    """Check if the user is connected to the internet."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def get_user_location():
    """Retrieve the user's location based on their IP address."""
    try:
        response = requests.get("http://ip-api.com/json/").json()
        if response['status'] == "success":
            return response['city']
        else:
            return None
    except Exception as e:
        return None

def convert_temp(temp, to_fahrenheit=False):
    """Convert temperature between Celsius and Fahrenheit."""
    if to_fahrenheit:
        return round((temp * 9/5) + 32, 1)
    else:
        return round((temp - 32) * 5/9, 1)

def get_weather(*args):
    """Fetch and display weather details."""
    if not is_connected():
        messagebox.showerror("Weather App", "Please check your internet connection.")
        return

    city = text_box.get() if text_box.get() else get_user_location()

    if not city:
        messagebox.showerror("Weather App", "Could not determine your location. Please enter a city name.")
        return

    try:
        # Geolocation and Timezone
        geo_locator = Nominatim(user_agent='WeatherApp')
        location = geo_locator.geocode(city)
        timezone = TimezoneFinder()
        result = timezone.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home).strftime('%I:%M %p')
        time_label.config(text=f"Local Time: {local_time}")
        timezone_label.config(text=f"Timezone: {result}")
        lon_label.config(text=f"Longitude: {location.longitude:.2f}")
        lat_label.config(text=f"Latitude: {location.latitude:.2f}")

        # Weather API
        api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=6ab9537c94001a93096b2c7e83aa9df0'
        json_data = requests.get(api).json()

        if json_data.get('cod') != 200:
            raise ValueError(json_data.get('message', 'Unknown Error'))

        # Extract Weather Data
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description'].capitalize()
        temp_celsius = round(json_data['main']['temp'] - 273.15, 1)
        temp_fahrenheit = convert_temp(temp_celsius, to_fahrenheit=True)
        wind = json_data['wind']['speed']
        humidity = json_data['main']['humidity']
        pressure = json_data['main']['pressure']
        visibility = round(json_data['visibility'] / 1000, 1)

        # Update Weather Details
        temp = f"{temp_celsius}°C" if not temp_in_fahrenheit.get() else f"{temp_fahrenheit}°F"
        temperature_label.config(text=f"Temperature: {temp}")
        feel_label.config(text=f"{condition} | Feels Like {temp}")
        wind_label.config(text=f"Wind Speed: {wind} m/s")
        humidity_label.config(text=f"Humidity: {humidity}%")
        weather_label.config(text=f"Condition: {description}")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        visibility_label.config(text=f"Visibility: {visibility} KM")
        location_label.config(text=f"Weather in {city.upper()}")
        text_box.delete(0, 'end')

    except Exception as e:
        messagebox.showerror("Weather App", f"Error: {e}")

def toggle_temp_unit():
    """Toggle between Celsius and Fahrenheit."""
    get_weather()

# Tkinter Window
window = Tk()
window.title("Minimal Weather App")
window.geometry('600x400')
window.config(bg='#f0f0f0')
window.resizable(height=False, width=False)

# Header
header_label = Label(window, text="Weather App", font=('Calibri', 20, 'bold'), bg='#f0f0f0', fg='blue')
header_label.pack(pady=10)

# Search Bar
text_box = Entry(window, justify='center', width=30, font=('Calibri', 14), bg='#ffffff', fg='black')
text_box.pack(pady=10)
text_box.focus()

search_button = Button(window, text="Get Weather", command=get_weather, font=('Calibri', 12), bg='blue', fg='white')
search_button.pack()

# Temperature Toggle
temp_in_fahrenheit = BooleanVar()
toggle_temp_button = Checkbutton(
    window,
    text="Display in Fahrenheit",
    variable=temp_in_fahrenheit,
    command=toggle_temp_unit,
    bg='#f0f0f0',
    font=('Calibri', 12)
)
toggle_temp_button.pack()

# Weather Details
location_label = Label(window, text="Enter a city or press Enter", font=('Calibri', 14), bg='#f0f0f0', fg='black')
location_label.pack(pady=10)

temperature_label = Label(window, text="", font=('Calibri', 16, 'bold'), bg='#f0f0f0', fg='red')
temperature_label.pack()

feel_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
feel_label.pack()

time_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
time_label.pack()

timezone_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
timezone_label.pack()

lon_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
lon_label.pack()

lat_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
lat_label.pack()

wind_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
wind_label.pack()

humidity_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
humidity_label.pack()

weather_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
weather_label.pack()

pressure_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
pressure_label.pack()

visibility_label = Label(window, text="", font=('Calibri', 12), bg='#f0f0f0', fg='black')
visibility_label.pack()

# Bind Enter Key to Search
window.bind('<Return>', get_weather)

# Run the App
window.mainloop()

