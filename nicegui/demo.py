from nicegui import ui
from random import randint, random

COL_TRANSP = "#505050"
COL_DISP = "#EE9010"
COL_SCREW = "#20E040"


def update_gantt():
    gantt.options["series"][0]["data"][0] = randint(100, 500)
    gantt.options["series"][0]["data"][1] = randint(100, 500)
    gantt.options["series"][1]["data"][0] = randint(100, 500)
    gantt.options["series"][1]["data"][1] = randint(100, 500)


def update_graph():
    graph.options["series"]["nodes"][0]["x"] = random() - 1
    graph.options["series"]["nodes"][0]["y"] = random()
    graph.options["series"]["nodes"][1]["x"] = random() + 1
    graph.options["series"]["nodes"][1]["y"] = random()


with ui.grid(columns=2).classes("w-full"):
    gantt = ui.echart(
        {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {},
            "xAxis": {"type": "value"},
            "yAxis": {
                "type": "category",
                "data": ["Product A", "Product A"],
            },
            "series": [
                {
                    "name": "Screwing",
                    "type": "bar",
                    "stack": "total",
                    "label": {"show": True},
                    "emphasis": {"focus": "series"},
                    "data": [320, 200],
                    "itemStyle": {"color": COL_SCREW},
                },
                {
                    "name": "Transport",
                    "type": "bar",
                    "stack": "total",
                    "label": {"show": True},
                    "emphasis": {"focus": "series"},
                    "data": [110, 33],
                    "itemStyle": {"color": COL_TRANSP},
                },
                {
                    "name": "Dispensing",
                    "type": "bar",
                    "stack": "total",
                    "label": {"show": True},
                    "emphasis": {"focus": "series"},
                    "data": [120, 399],
                    "itemStyle": {"color": COL_DISP},
                },
            ],
        },
    )
    graph = ui.echart(
        {
            "series": {
                "type": "graph",
                # "layout": "force",
                "label": {"show": True},
                "symbolSize": 100,
                "edgeSymbol": ["none", "arrow"],
                "nodes": [
                    {
                        "name": "Screwing",
                        "x": -1,
                        "y": 0,
                        "itemStyle": {"color": COL_SCREW},
                    },
                    {
                        "name": "Dispensing",
                        "x": 1,
                        "y": 0,
                        "itemStyle": {"color": COL_DISP},
                    },
                ],
                "links": [
                    {
                        "source": "Screwing",
                        "target": "Dispensing",
                        "lineStyle": {"width": 2},
                    }
                ],
            }
        }
    )
    ui.button("Update", on_click=update_gantt)
    ui.button("Update", on_click=update_graph)

ui.run()
