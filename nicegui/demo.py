from nicegui import ui
from random import randint, random

COL_TRANSP = "#505050"
COL_DISP = "#EE9010"
COL_SCREW = "#20E040"
COL_HIGHLIGHT = "#0010EE"


def update_gantt():
    gantt.options["series"][0]["data"][0] = randint(100, 500)
    gantt.options["series"][0]["data"][1] = randint(100, 500)
    gantt.options["series"][1]["data"][0] = randint(100, 500)
    gantt.options["series"][1]["data"][1] = randint(100, 500)
    gantt.update()


def update_graph():
    graph.options["series"]["nodes"][0]["x"] = random() - 1
    graph.options["series"]["nodes"][0]["y"] = random()
    graph.options["series"]["nodes"][1]["x"] = random() + 1
    graph.options["series"]["nodes"][1]["y"] = random()
    graph.update()


# Event handlers for individual elements
def handle_gantt_element_hover(e):
    print(f"Gantt element hover event: {e.args}")
    series_name = e.args.get('seriesName')
    print(f"Series name: {series_name}")
    # Highlight the hovered element in the graph
    if series_name == "Screwing":
        graph.options["series"]["nodes"][0]["itemStyle"]["color"] = COL_HIGHLIGHT
        graph.update()
    elif series_name == "Dispensing":
        graph.options["series"]["nodes"][1]["itemStyle"]["color"] = COL_HIGHLIGHT
        graph.update()


def handle_gantt_element_leave(e):
    print(f"Gantt element leave event")
    # Reset the graph node colors when leaving
    graph.options["series"]["nodes"][0]["itemStyle"]["color"] = COL_SCREW
    graph.options["series"]["nodes"][1]["itemStyle"]["color"] = COL_DISP
    graph.update()


def handle_graph_element_hover(e):
    print(f"Graph element hover event: {e.args}")
    node_name = e.args.get('name')
    print(f"Node name: {node_name}")
    # Highlight the corresponding series in the Gantt chart
    if node_name == "Screwing":
        gantt.options["series"][0]["itemStyle"]["color"] = COL_HIGHLIGHT
        gantt.update()
    elif node_name == "Dispensing":
        gantt.options["series"][2]["itemStyle"]["color"] = COL_HIGHLIGHT
        gantt.update()


def handle_graph_element_leave(e):
    print(f"Graph element leave event")
    # Reset the Gantt chart series colors when leaving
    gantt.options["series"][0]["itemStyle"]["color"] = COL_SCREW
    gantt.options["series"][2]["itemStyle"]["color"] = COL_DISP
    gantt.update()


def setup_event_listeners():
    """Set up event listeners after UI is initialized"""
    ui.run_javascript(f"""
    setTimeout(() => {{
        // Get the chart instances
        const ganttChart = getElement({gantt.id}).chart;
        const graphChart = getElement({graph.id}).chart;
        
        if (ganttChart) {{
            console.log('Setting up Gantt chart events');
            // Listen for mouseover events on chart elements
            ganttChart.on('mouseover', function(params) {{
                console.log('Gantt mouseover params:', params);
                // Extract only the properties we need to avoid circular references
                const safeParams = {{
                    seriesName: params.seriesName,
                    seriesIndex: params.seriesIndex,
                    dataIndex: params.dataIndex,
                    name: params.name,
                    value: params.value,
                    componentType: params.componentType
                }};
                emitEvent('gantt_element_hover', safeParams);
            }});
            
            ganttChart.on('mouseout', function(params) {{
                console.log('Gantt mouseout params:', params);
                const safeParams = {{
                    seriesName: params.seriesName,
                    seriesIndex: params.seriesIndex,
                    dataIndex: params.dataIndex,
                    name: params.name
                }};
                emitEvent('gantt_element_leave', safeParams);
            }});
        }} else {{
            console.log('Gantt chart not found');
        }}
        
        if (graphChart) {{
            console.log('Setting up Graph chart events');
            graphChart.on('mouseover', function(params) {{
                console.log('Graph mouseover params:', params);
                const safeParams = {{
                    seriesName: params.seriesName,
                    seriesIndex: params.seriesIndex,
                    dataIndex: params.dataIndex,
                    name: params.name,
                    value: params.value,
                    componentType: params.componentType
                }};
                emitEvent('graph_element_hover', safeParams);
            }});
            
            graphChart.on('mouseout', function(params) {{
                console.log('Graph mouseout params:', params);
                const safeParams = {{
                    seriesName: params.seriesName,
                    seriesIndex: params.seriesIndex,
                    dataIndex: params.dataIndex,
                    name: params.name
                }};
                emitEvent('graph_element_leave', safeParams);
            }});
        }} else {{
            console.log('Graph chart not found');
        }}
    }}, 1000);
    """)


with ui.grid(columns=2).classes("w-full"):
    gantt = ui.echart(
        {
            "tooltip": {"trigger": "item"},
            "legend": {},
            "xAxis": {"type": "value"},
            "yAxis": {
                "type": "category",
                "data": ["Product A", "Product B"],
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
    
    ui.button("Update Gantt", on_click=update_gantt)
    ui.button("Update Graph", on_click=update_graph)

# Handle the emitted events
ui.on('gantt_element_hover', handle_gantt_element_hover)
ui.on('gantt_element_leave', handle_gantt_element_leave)
ui.on('graph_element_hover', handle_graph_element_hover)
ui.on('graph_element_leave', handle_graph_element_leave)

# Set up events when the page loads
ui.timer(2.0, setup_event_listeners, once=True)

ui.run()  # Only call this once!
