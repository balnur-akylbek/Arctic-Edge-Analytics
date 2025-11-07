from prometheus_client import start_http_server, Gauge
import requests, time

# --- CONFIG ---
API_KEY = "f019f59ec192480a62b74ad9df20b53f"
CITY = "Astana"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# --- DEFINE METRICS ---
temperature = Gauge('weather_temperature_celsius', 'Current temperature in Celsius')
humidity = Gauge('weather_humidity_percent', 'Humidity percentage')
pressure = Gauge('weather_pressure_hpa', 'Atmospheric pressure in hPa')
wind_speed = Gauge('weather_wind_speed_mps', 'Wind speed in meters per second')
clouds = Gauge('weather_clouds_percent', 'Cloudiness percentage')
visibility = Gauge('weather_visibility_meters', 'Visibility distance in meters')
feels_like = Gauge('weather_feels_like_celsius', 'Feels-like temperature in Celsius')
sunrise = Gauge('weather_sunrise_timestamp', 'Sunrise time (UTC timestamp)')
sunset = Gauge('weather_sunset_timestamp', 'Sunset time (UTC timestamp)')
day_length = Gauge('weather_day_length_seconds', 'Day length in seconds')

# --- MAIN LOOP ---
def collect_data():
    while True:
        try:
            r = requests.get(URL)
            data = r.json()

            temperature.set(data['main']['temp'])
            humidity.set(data['main']['humidity'])
            pressure.set(data['main']['pressure'])
            wind_speed.set(data['wind']['speed'])
            clouds.set(data['clouds']['all'])
            visibility.set(data.get('visibility', 0))
            feels_like.set(data['main']['feels_like'])
            sunrise.set(data['sys']['sunrise'])
            sunset.set(data['sys']['sunset'])
            day_length.set(data['sys']['sunset'] - data['sys']['sunrise'])

            print(f"✅ Data updated: {CITY}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

        time.sleep(20)  # update every 20s

if __name__ == "__main__":
    start_http_server(8000)
    collect_data()
