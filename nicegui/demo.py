from nicegui import ui
from random import randint, random


COLORS = {
    "TRANSP": {"default": "#A0A0A0", "highlight": "#505050"},
    "DISP": {"default": "#F5C080", "highlight": "#EE9010"},
    "SCREW": {"default": "#90F0A0", "highlight": "#20E040"},
    "IDLE": {"default": "#D5D5D5", "highlight": "#AAAAAA"},
}

SERIES = {
    "Screwing": {
        "color": COLORS["SCREW"],
        "gantt_idx": 1,
        "graph_idx": 0,
        "edge_idx": None,
    },
    "Transport": {
        "color": COLORS["TRANSP"],
        "gantt_idx": 2,
        "graph_idx": None,
        "edge_idx": 0,
    },
    "Dispensing": {
        "color": COLORS["DISP"],
        "gantt_idx": 3,
        "graph_idx": 1,
        "edge_idx": None,
    },
}


class ChartLinker:
    def __init__(self, gantt, graph):
        self.gantt = gantt
        self.graph = graph

    def setup_events(self):
        ui.run_javascript(
            f"""
        setTimeout(() => {{
            const gantt = getElement({self.gantt.id}).chart;
            const graph = getElement({self.graph.id}).chart;
            
            if (gantt && graph) {{
                gantt.on('mouseover', p => emitEvent('gantt_hover', {{name: p.seriesName}}));
                gantt.on('mouseout', () => emitEvent('gantt_leave', {{}}));
                graph.on('mouseover', p => emitEvent('graph_hover', {{name: p.name}}));
                graph.on('mouseout', () => emitEvent('graph_leave', {{}}));
            }}
        }}, 1000);
        """
        )

    def highlight(self, name):
        if name == "Screwing > Dispensing":
            name = "Transport"

        if name not in SERIES:
            return

        series = SERIES[name]
        highlight_color = series["color"]["highlight"]

        # graph
        edge_idx = series["edge_idx"]
        graph_idx = series["graph_idx"]
        if edge_idx is not None:
            self.graph.options["series"]["links"][edge_idx]["lineStyle"][
                "color"
            ] = highlight_color
            self.graph.options["series"]["links"][edge_idx]["lineStyle"][
                "width"
            ] = 4
        if graph_idx is not None:
            self.graph.options["series"]["nodes"][graph_idx]["itemStyle"][
                "color"
            ] = highlight_color
        self.graph.update()
        # gantt
        self.gantt.options["series"][series["gantt_idx"]]["itemStyle"][
            "color"
        ] = highlight_color
        self.gantt.update()

    def reset_colors(self):
        for name, series in SERIES.items():
            default_color = series["color"]["default"]
            edge_idx = series["edge_idx"]
            graph_idx = series["graph_idx"]
            if graph_idx is not None:
                self.graph.options["series"]["nodes"][graph_idx]["itemStyle"][
                    "color"
                ] = default_color
            self.gantt.options["series"][series["gantt_idx"]]["itemStyle"][
                "color"
            ] = default_color

        # Reset edge
        self.graph.options["series"]["links"][0]["lineStyle"]["color"] = "#999"
        self.graph.options["series"]["links"][0]["lineStyle"]["width"] = 2

        self.gantt.update()
        self.graph.update()


def create_gantt():
    return ui.echart(
        {
            "tooltip": {"trigger": "item"},
            "xAxis": {"type": "value"},
            "yAxis": {"type": "category", "data": ["Product A", "Product B"]},
            "series": [
                {
                    "name": "Idle",
                    "type": "bar",
                    "stack": "total",
                    "data": [200, 0],
                    "itemStyle": {"color": COLORS["IDLE"]["default"]},
                    "emphasis": {"disabled": True},
                },
                {
                    "name": "Screwing",
                    "type": "bar",
                    "stack": "total",
                    "data": [320, 200],
                    "itemStyle": {"color": COLORS["SCREW"]["default"]},
                    "emphasis": {"disabled": True},
                },
                {
                    "name": "Transport",
                    "type": "bar",
                    "stack": "total",
                    "data": [110, 320],
                    "itemStyle": {"color": COLORS["TRANSP"]["default"]},
                    "emphasis": {"disabled": True},
                },
                {
                    "name": "Dispensing",
                    "type": "bar",
                    "stack": "total",
                    "data": [150, 110],
                    "itemStyle": {"color": COLORS["DISP"]["default"]},
                    "emphasis": {"disabled": True},
                },
            ],
        }
    )


def create_graph():
    return ui.echart(
        {
            "tooltip": {"trigger": "item"},
            "series": {
                "type": "graph",
                "label": {"show": True},
                "symbolSize": 100,
                "edgeSymbol": ["none", "arrow"],
                "nodes": [
                    {
                        "name": "Screwing",
                        "x": -1,
                        "y": 0,
                        "itemStyle": {"color": COLORS["SCREW"]["default"]},
                    },
                    {
                        "name": "Dispensing",
                        "x": 1,
                        "y": 0,
                        "itemStyle": {"color": COLORS["DISP"]["default"]},
                    },
                ],
                "links": [
                    {
                        "source": "Screwing",
                        "target": "Dispensing",
                        "lineStyle": {"width": 2, "color": "#999"},
                    }
                ],
            },
        }
    )


def update_gantt(gantt):
    for i in range(len(gantt.options["series"]) - 1):
        val = randint(50, 400)
        gantt.options["series"][i]["data"][0] = val
        gantt.options["series"][i + 1]["data"][1] = val
    gantt.update()


def update_graph(graph):
    for i, node in enumerate(graph.options["series"]["nodes"]):
        node["x"] = random() + (-1 if i == 0 else 1)
        node["y"] = random()
    graph.update()


def main():
    with ui.grid(columns=2).classes("w-full"):
        gantt = create_gantt()
        graph = create_graph()
        ui.button("Update Gantt", on_click=lambda: update_gantt(gantt))
        ui.button("Update Graph", on_click=lambda: update_graph(graph))

    linker = ChartLinker(gantt, graph)

    ui.on(
        "gantt_hover",
        lambda e: linker.highlight(e.args.get("name")),
    )
    ui.on("gantt_leave", lambda e: linker.reset_colors())
    ui.on("graph_hover", lambda e: linker.highlight(e.args.get("name")))
    ui.on("graph_leave", lambda e: linker.reset_colors())

    ui.timer(2.0, linker.setup_events, once=True)


if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run()
