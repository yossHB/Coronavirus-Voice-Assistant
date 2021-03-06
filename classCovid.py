import requests
import json
import threading
import time
class CovidData:
    def __init__(self, api_key,project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.get_data()

    # get updated data from the web site
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        self.data = json.loads(response.text)

    #use it to minimize the redondance
    def get(self,key,item):
        data = self.data[key]
        for content in data:
            if content['name'].lower() == item.lower():
                try:
                    return content['value']
                except :
                    return content
        return " --"

    def get_total_cases(self):
        return self.get("Total","Coronavirus Cases:")

    def get_total_deaths(self):
        return self.get("Total","Deaths:")

    def get_country_data(self,country):
        return self.get("country",country)

    def get_list_of_countries(self):
        countries = []
        for country in self.data["country"]:
            countries.append(country["name"])
        return countries

    def update_data(self):
        response  = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)
        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)
        thread= threading.Thread(target=poll)
        thread.start()
