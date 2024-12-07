from tkinter import *
from tkinter import ttk
import requests

# List of cities for selection (example dataset for demonstration)
cities_list = [
    "Anantapur", "Chittoor", "East Godavari", "Ahmedabad", "Bharuch", 
    "Chennai", "Bangalore", "Hyderabad", "Kolkata", "Mumbai", 
    "Pune", "Lucknow", "Kanpur", "Delhi"
]

def fetch_weather():
    #Fetches weather information for the selected city using the OpenWeatherMap API.
    
    selected_city = city_combobox.get()
    api_key = "APIKEY"  #Replace with your API key
    weather_url = f"Weather_website_URL"
    
    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        weather_data = response.json()
        
        # Extract and process weather data
        temp_kelvin = weather_data['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        humidity = weather_data['main']['humidity']
        condition = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        pressure = weather_data['main']['pressure']
        country_code = weather_data['sys']['country']
        full_city_name = f"{selected_city}, {country_code}"
        
        # Update the result label with formatted weather information
        result_label.config(
            text=(
                f"City: {full_city_name}\n"
                f"Temperature: {temp_celsius:.2f} °C / {temp_fahrenheit:.2f} °F\n"
                f"Humidity: {humidity}%\n"
                f"Weather: {condition}\n"
                f"Wind Speed: {wind_speed} m/s\n"
                f"Pressure: {pressure} hPa"
            )
        )
    except requests.exceptions.RequestException as req_error:
        result_label.config(text=f"Error: Unable to connect to the weather service.\nDetails: {req_error}")
    except KeyError:
        result_label.config(text="Error: Unable to retrieve weather data. Please check the city name.")

def update_suggestions(event):

    typed_value = event.widget.get()
    if typed_value:
        matching_cities = [city for city in cities_list if typed_value.lower() in city.lower()]
        update_listbox(matching_cities)
    else:
        update_listbox([])

def update_listbox(matches):
    """
    Updates the listbox with a list of matching city names.
    """
    suggestion_listbox.delete(0, END)
    for match in matches:
        suggestion_listbox.insert(END, match)

def select_city(event):
    """
    Sets the selected city from the listbox into the combobox and clears the suggestions.
    """
    selected_city = suggestion_listbox.get(ACTIVE)
    city_combobox.set(selected_city)
    update_listbox([])

# GUI setup
app_window = Tk()
app_window.title("Weather Application")
app_window.config(bg="#f5f5f5")
app_window.geometry("600x400")

# App Title
app_title = Label(app_window, text="Weather App", font=("Helvetica", 24, "bold"), fg="#333", bg="#f5f5f5")
app_title.place(x=200, y=20)

# City Selection Combobox
city_combobox = ttk.Combobox(app_window, values=cities_list, font=("Helvetica", 12))
city_combobox.place(x=200, y=80, width=200)
city_combobox.bind('<KeyRelease>', update_suggestions)

# Suggestion Listbox
suggestion_listbox = Listbox(app_window, font=("Helvetica", 12))
suggestion_listbox.place(x=200, y=110, width=200, height=100)
suggestion_listbox.bind('<<ListboxSelect>>', select_city)

# Fetch Weather Button
fetch_button = Button(
    app_window, text="Get Weather", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=fetch_weather
)
fetch_button.place(x=250, y=220)

# Result Label
result_label = Label(app_window, text="", font=("Helvetica", 12), wraplength=500, justify="left", bg="#f5f5f5")
result_label.place(x=50, y=270)

# Run the application
app_window.mainloop()
