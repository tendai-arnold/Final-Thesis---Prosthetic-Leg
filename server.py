import pandas as pd
import datetime

from jupyter_dash import JupyterDash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


path = "./Data/data/110001/"

cols = [
    "right_acc_x",
    "right_acc_y",
    "right_acc_z",
    "right_gyr_x",
    "right_gyr_y",
    "right_gyr_z",
    "left_acc_x",
    "left_acc_y",
    "left_acc_z",
    "left_gyr_x",
    "left_gyr_y",
    "left_gyr_z",
    "chest_acc_x",
    "chest_acc_y",
    "chest_acc_z",
    "chest_gyr_x",
    "chest_gyr_y",
    "chest_gyr_z",
]

# Patient questionnaire questions
mood = [
    "mood_well",
    "mood_down",
    "mood_fright",
    "mood_tense",
    "phy_sleepy",
    "phy_tired",
    "mood_cheerf",
    "mood_relax",
]
mood_nams = [
    "Well",
    "Down",
    "Frightened",
    "Tense",
    "Sleepy",
    "Tired",
    "Cheerful",
    "Relaxed",
]


# Figure 1 (symptom_cats)
symptom = ["tremor", "slowness", "stiffness", "muscle_tension", "dyskinesia"]


# Figure 2 (functionality_cats)
functionality_label = [
    "act_problemless",
    "mobility_well",
    "sit_still",
    "feels",
    "walk_well",
]

# Figure 2 (label)
functionality_names = [
    "Current Activity",
    "Mobility Comfort",
    "Sit & Stand",
    "Feels",
    "Walk",
]

# Loop through files and load csv's into dataframe.  Reset columns and index.  Add start and end times to a list
rec_times = []
df = {}


def load_data():
    for i in range(1, 8):
        url = path + f"data_{i}.csv"
        df[f"df{i}"] = pd.read_csv(url)
        df[f"df{i}"].set_index("time", inplace=True)
        df[f"df{i}"].columns = cols
        start = df[f"df{i}"].index[0].split(" ")[1][:-7]
        end = df[f"df{i}"].index[-1].split(" ")[1][:-7]
        rec_times.append([start, end])


# Make loop to make all time-series plots
def make_plots():
    for i in range(1, 8):
        df[f"fig{i}"] = make_subplots(
            rows=6,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            subplot_titles=[
                "Accelerometry Left",
                "Gyro Left",
                "Accelerometry Right",
                "Gyro Right",
                "Accelerometry Chest",
                "Gyro Chest",
            ],
        )
        data = df[f"df{i}"]
        sensor_axis_types = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z"]

        count, count_l = 1, 0
        for sens in ["left", "right", "chest"]:
            for d_type in ["acc", "gyr"]:
                for axis, color in zip(
                    ["x", "y", "z"], ["MediumSeaGreen", "SandyBrown", "DodgerBlue"]
                ):
                    count_l += 1
                    if count_l > 3:
                        legend_vis = False
                    else:
                        legend_vis = True

                    df[f"fig{i}"].add_trace(
                        go.Scatter(
                            x=data.index,
                            y=data[f"{sens}_{d_type}_{axis}"],
                            marker_color=color,
                            name=f"{axis}-axis",
                            showlegend=legend_vis,
                        ),
                        row=count,
                        col=1,
                    )
                count += 1

        df[f"fig{i}"].update_layout(height=1500, width=1300)


load_data()
make_plots()

# Store figures in a list
figures = [
    df["fig1"],
    df["fig2"],
    df["fig3"],
    df["fig4"],
    df["fig5"],
    df["fig6"],
    df["fig7"],
]

# Patient survey data
quest_url = "./Data/data/110001/110001_features900.csv"
df_quest = pd.read_csv(quest_url)

# Create data-frames
df_mood = df_quest[mood]
df_symptom = df_quest[symptom]
df_functionality = df_quest[functionality_label]

#########################################################################################################
# FRONT-END
#########################################################################################################

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
)


app = JupyterDash(__name__, external_stylesheets=[dbc.themes.COSMO, dbc_css])
app.layout = dbc.Container(
    [
        html.H3("Prosthetic Patient Dashboard"),
        html.Img(
            src="https://images.pexels.com/photos/8436907/pexels-photo-8436907.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            style={"margin": "1em", "height": "200px"},
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.DropdownMenu(
                    label="Choose Dataset",
                    menu_variant="dark",
                    children=[
                        dbc.DropdownMenuItem("Dataset 1", id="1"),
                        dbc.DropdownMenuItem("Dataset 2", id="2"),
                        dbc.DropdownMenuItem("Dataset 3", id="3"),
                        dbc.DropdownMenuItem("Dataset 4", id="4"),
                        dbc.DropdownMenuItem("Dataset 5", id="5"),
                        dbc.DropdownMenuItem("Dataset 6", id="6"),
                        dbc.DropdownMenuItem("Dataset 7", id="7"),
                    ],
                    id="dropdown_item",
                    className="mt-3",
                    style={"margin-bottom": "1rem"},
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5("Date", style={"font-weight": "bold"}),
                                        html.H5(id="date"),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.H5(
                                            "Recording Time",
                                            style={"font-weight": "bold"},
                                        ),
                                        html.H5(id="time_frame"),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.H5(
                                            "Survey Time", style={"font-weight": "bold"}
                                        ),
                                        html.H5(id="time_surv"),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    width=8,
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Symptoms", style={"font-weight": "bold"}),
                                dcc.Graph(id="pd_symptoms", className="w-100"),
                            ],
                            width=4,
                        ),
                        dbc.Col(
                            [
                                html.H5("Functionality", style={"font-weight": "bold"}),
                                dcc.Graph(id="functionality"),
                            ],
                            width=4,
                        ),
                    ]
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Time Series Graphs", style={"margin-top": "20px"}),
                        html.Div(id="data_set"),
                        dcc.Graph(id="time-series"),
                        html.Div(style={"margin-bottom": "20px"}),
                    ],
                    width=12,
                ),
            ]
        ),
    ],
    className="dbc",
    fluid=True,
)

# Data Segment Selector Callback
@app.callback(
    Output("data_set", "children"),
    Output("date", "children"),
    Output("time_frame", "children"),
    Output("time_surv", "children"),
    Output("pd_symptoms", "figure"),
    Output("functionality", "figure"),
    Output("time-series", "figure"),
    [
        Input("1", "n_clicks"),
        Input("2", "n_clicks"),
        Input("3", "n_clicks"),
        Input("4", "n_clicks"),
        Input("5", "n_clicks"),
        Input("6", "n_clicks"),
        Input("7", "n_clicks"),
    ],
)
def update_figs(*args):
    # Obtain data segment index
    ctx = dash.callback_context
    if not ctx.triggered:
        data_set_index = "1"
    else:
        data_set_index = ctx.triggered[0]["prop_id"].split(".")[0]

    data_set_index = int(data_set_index)
    i = data_set_index - 1

    out_label = f"Data Segment {data_set_index}"

    # Get date and time frames
    date = df_quest["beep_time_start"][i].split(" ")[0]
    date = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))
    date = date.strftime("%b %d %Y")

    # recording time
    time_frame = f"{rec_times[i][0]} - {rec_times[i][1]}"

    # survey time
    start = df_quest["beep_time_start"][i].split(" ")[1][:-3]
    end = df_quest["beep_time_end"][i].split(" ")[1][:-3]
    time_surv = f"{start} - {end}"

    # PD_symptoms plot
    # TODO: Figure 1
    fig_sp_pd = go.Figure()
    fig_sp_pd.add_trace(
        go.Scatterpolar(r=df_symptom.iloc[i], theta=symptom, fill="toself")
    )
    fig_sp_pd.update_polars(radialaxis_range=(1, 10))
    fig_sp_pd.update_layout(margin=dict(l=0, r=0, t=20, b=20))

    # functionality plot
    # TODO: Figure 2
    fig_f = go.Figure()
    fig_f.add_trace(
        go.Scatterpolar(
            r=df_functionality.iloc[i], theta=functionality_names, fill="toself"
        )
    )
    fig_f.update_layout(margin=dict(l=0, r=0, t=20, b=20))
    fig_f.update_polars(radialaxis_range=(1, 10))

    # time-series plot
    fig_ts = figures[i]

    # return figures
    return (
        out_label,
        date,
        time_frame,
        time_surv,
        fig_sp_pd,
        fig_f,
        fig_ts,
    )


app.run_server(debug=True)
