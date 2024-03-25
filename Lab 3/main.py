import pandas as pd
from spyre import server

OPTIONS = [{"label": "Вінницька", "value": 1}, {"label": "Волинська", "value": 2},
           {"label": "Дніпропетровська", "value": 3}, {"label": "Донецька", "value": 4},
           {"label": "Житомирська", "value": 5}, {"label": "Закарпатська", "value": 6},
           {"label": "Запорізька", "value": 7}, {"label": "Івано-Франківська", "value": 8},
           {"label": "Київська", "value": 9},
           {"label": "Кіровоградська", "value": 10}, {"label": "Луганська", "value": 11},
           {"label": "Львівська", "value": 12}, {"label": "Львівська", "value": 12},
           {"label": "Миколаївська", "value": 13}, {"label": "Одеська", "value": 14},
           {"label": "Полтавська", "value": 15}, {"label": "Рівенська", "value": 16}, {"label": "Сумська", "value": 17},
           {"label": "Тернопільська", "value": 18}, {"label": "Харківська", "value": 19},
           {"label": "Херсонська", "value": 20}, {"label": "Хмельницька", "value": 21},
           {"label": "Черкаська", "value": 22}, {"label": "Чернівецька", "value": 23},
           {"label": "Чернігівська", "value": 24}, {"label": "Республіка Крим", "value": 25}]


def getDataFromCSV():
    data = pd.read_csv("./data.csv")
    return data


class StockExample(server.App):
    title = "NOAA data visualization"

    inputs = [
        {
            "type": "dropdown",
            "label": "NOAA data dropdown",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"},
            ],
            "key": "ticker",
            "action_id": "update_data",
        },
        {
            "type": "dropdown",
            "label": "Region",
            "options": OPTIONS,
            "key": "region",
            "action_id": "update_data",
        },
        dict(type='text', key='year', label='years', value='2000', action_id='update_data')
    ]

    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot",
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "output_type": "html",
            "get_html": "getHTML",
        }
    ]

    def getData(self, year, region):
        data = getDataFromCSV()
        filtered_data = data[(data['area'] == region) & (data['Year'] == year)]
        return filtered_data

    def getPlot(self, params):
        ticker = params['ticker']
        region = int(params['region'])
        year = int(params['year'])
        data = getDataFromCSV()
        filtered_data = data[(data['area'] == region) & (data['Year'] == year)]
        plt = filtered_data.plot(x='Week', y=ticker)
        plt.set_ylabel("Values")
        plt.set_xlabel("Weeks")
        plt.set_title(f"Graphic for {region} region in {year}")
        fig = plt.get_figure()
        return fig

    def getHTML(self, params):
        year = int(params['year'])
        region = int(params['region'])
        data = self.getData(year, region)
        return data.to_html()


app = StockExample()
app.launch()
