from nicegui import ui
from random import randint, random
from typing import Dict, Any

# Color constants
class Colors:
    TRANSP = "#505050"
    DISP = "#EE9010" 
    SCREW = "#20E040"
    HIGHLIGHT = "#0010EE"
    IDLE = "#AAAAAA"

# Data mappings
SERIES_CONFIG = {
    "Screwing": {"color": Colors.SCREW, "gantt_index": 1, "graph_index": 0},
    "Transport": {"color": Colors.TRANSP, "gantt_index": 2, "graph_index": None},
    "Dispensing": {"color": Colors.DISP, "gantt_index": 3, "graph_index": 1},
}


class ChartLinker:
    """Handles linking between gantt and graph charts"""
    
    def __init__(self, gantt_chart, graph_chart):
        self.gantt = gantt_chart
        self.graph = graph_chart
        
    def setup_event_listeners(self):
        """Set up event listeners after UI is initialized"""
        ui.run_javascript(f"""
        setTimeout(() => {{
            const ganttChart = getElement({self.gantt.id}).chart;
            const graphChart = getElement({self.graph.id}).chart;
            
            if (ganttChart && graphChart) {{
                console.log('Setting up chart event linking');
                
                ganttChart.on('mouseover', (params) => {{
                    const safeParams = extractSafeParams(params);
                    emitEvent('gantt_hover', safeParams);
                }});
                
                ganttChart.on('mouseout', (params) => {{
                    emitEvent('gantt_leave', extractSafeParams(params));
                }});
                
                graphChart.on('mouseover', (params) => {{
                    emitEvent('graph_hover', extractSafeParams(params));
                }});
                
                graphChart.on('mouseout', (params) => {{
                    emitEvent('graph_leave', extractSafeParams(params));
                }});
            }}
            
            function extractSafeParams(params) {{
                return {{
                    seriesName: params.seriesName,
                    seriesIndex: params.seriesIndex,
                    dataIndex: params.dataIndex,
                    name: params.name,
                    value: params.value,
                    componentType: params.componentType
                }};
            }}
        }}, 1000);
        """)
    
    def highlight_corresponding_element(self, element_name: str, target_chart: str):
        """Highlight corresponding element in the target chart"""
        if element_name not in SERIES_CONFIG:
            return
            
        config = SERIES_CONFIG[element_name]
        
        if target_chart == "graph" and config["graph_index"] is not None:
            self.graph.options["series"]["nodes"][config["graph_index"]]["itemStyle"]["color"] = Colors.HIGHLIGHT
            self.graph.update()
        elif target_chart == "gantt":
            self.gantt.options["series"][config["gantt_index"]]["itemStyle"]["color"] = Colors.HIGHLIGHT
            self.gantt.update()
    
    def reset_colors(self):
        """Reset all chart elements to their original colors"""
        # Reset graph nodes
        for name, config in SERIES_CONFIG.items():
            if config["graph_index"] is not None:
                self.graph.options["series"]["nodes"][config["graph_index"]]["itemStyle"]["color"] = config["color"]
        
        # Reset gantt series
        for name, config in SERIES_CONFIG.items():
            self.gantt.options["series"][config["gantt_index"]]["itemStyle"]["color"] = config["color"]
        
        self.gantt.update()
        self.graph.update()


def create_gantt_chart() -> ui.echart:
    """Create and configure the Gantt chart"""
    return ui.echart({
        "tooltip": {"trigger": "item"},
        "legend": {},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": ["Product A", "Product B"],
        },
        "series": [
            {
                "name": "Idle",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [200, 0],
                "itemStyle": {"color": Colors.IDLE},
            },
            {
                "name": "Screwing",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [320, 200],
                "itemStyle": {"color": Colors.SCREW},
            },
            {
                "name": "Transport", 
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [110, 320],
                "itemStyle": {"color": Colors.TRANSP},
            },
            {
                "name": "Dispensing",
                "type": "bar", 
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [150, 110],
                "itemStyle": {"color": Colors.DISP},
            },
        ],
    })


def create_graph_chart() -> ui.echart:
    """Create and configure the Graph chart"""
    return ui.echart({
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
                    "itemStyle": {"color": Colors.SCREW},
                },
                {
                    "name": "Dispensing",
                    "x": 1,
                    "y": 0,
                    "itemStyle": {"color": Colors.DISP},
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
    })


def update_gantt_data(gantt: ui.echart):
    """Update Gantt chart with random data"""
    t_idle = randint(100, 300)
    t_screw = randint(200, 400)
    t_transp = randint(100, 300)
    t_disp = randint(150, 350)
    gantt.options["series"][0]["data"] = [t_idle, 0]
    gantt.options["series"][1]["data"] = [t_screw, t_idle]
    gantt.options["series"][2]["data"] = [t_transp, t_screw]
    gantt.options["series"][3]["data"] = [t_disp, t_transp]
    gantt.update()


def update_graph_data(graph: ui.echart):
    """Update Graph chart with random positions"""
    graph.options["series"]["nodes"][0]["x"] = random() - 1
    graph.options["series"]["nodes"][0]["y"] = random()
    graph.options["series"]["nodes"][1]["x"] = random() + 1 
    graph.options["series"]["nodes"][1]["y"] = random()
    graph.update()


def main():
    """Main application logic"""
    with ui.grid(columns=2).classes("w-full"):
        gantt = create_gantt_chart()
        graph = create_graph_chart()
        
        ui.button("Update Gantt", on_click=lambda: update_gantt_data(gantt))
        ui.button("Update Graph", on_click=lambda: update_graph_data(graph))

    # Set up chart linking
    linker = ChartLinker(gantt, graph)
    
    # Event handlers using the linker
    def handle_gantt_hover(e):
        series_name = e.args.get('seriesName')
        if series_name:
            linker.highlight_corresponding_element(series_name, "graph")
    
    def handle_gantt_leave(e):
        linker.reset_colors()
    
    def handle_graph_hover(e):
        node_name = e.args.get('name')
        if node_name:
            linker.highlight_corresponding_element(node_name, "gantt")
    
    def handle_graph_leave(e):
        linker.reset_colors()
    
    # Register event handlers
    ui.on('gantt_hover', handle_gantt_hover)
    ui.on('gantt_leave', handle_gantt_leave) 
    ui.on('graph_hover', handle_graph_hover)
    ui.on('graph_leave', handle_graph_leave)
    
    # Set up event listeners after UI loads
    ui.timer(2.0, linker.setup_event_listeners, once=True)


# Use the multiprocessing-compatible guard
if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run()