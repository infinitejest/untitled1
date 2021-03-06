from kivy.app import App

from kivy.network.urlrequest import UrlRequest
import json

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.uix.listview import ListItemButton



class CurrentWeather(BoxLayout):
    location = ListProperty(['New York', 'US'])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()

    def update_weather(self):
        weather_template = "http://api.openweathermap.org/data/2.5/" + \
                           "weather?q={},{}&unit=metric&APPID=" + "a3ce4c4c978cae4ace6c3e404899ac32"

        weather_url = weather_template.format(*self.location)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved (self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions =  data ['weather'][0]['description']
        self.temp = data ['main']['temp']
        self.temp_min = data ['main']['temp_min']
        self.temp_max = data['main']['temp_max']





class LocationButton(ListItemButton):
    location = ListProperty()


class AddLocationForm(BoxLayout):
    search_results = ObjectProperty()
    search_input = ObjectProperty()

    def args_converter(self, index, data_item):

        city, country = data_item

        return {'location':(city, country)}



    def search_location(self):
        search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=" + "a3ce4c4c978cae4ace6c3e404899ac32"

        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

        #TODO : Error Checking if location is not found

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data

        cities = [(d['name'], d['sys']['country']) for d in data['list']]



        self.search_results.item_strings = cities
        del self.search_results.adapter.data[:]
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()




        #TODO: Error checking if network failure

class WeatherRoot(BoxLayout):
    current_weather = ObjectProperty()

    def show_current_weather(self, location=None):

        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather = CurrentWeather()

        if location is not None:
            self.current_weather.location = location

        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())

class WeatherApp(App):
    pass


if __name__ == '__main__':
    WeatherApp().run()



        #api.openweathermap.org/data/2.5/forecast/city?id=524901&APPID=1111111111
# APIID: a3ce4c4c978cae4ace6c3e404899ac32