import os.path

import pandas as pd

from plotly.subplots import make_subplots
#from src.utils import Settings
import plotly.graph_objects as go
CSV_TO_PLOT = Settings.init()["path_sorter"]


def plot_metrics (dataframe, title):
    fig = make_subplots( rows=2, cols=3, start_cell="top-left",
                         subplot_titles=(
                         "CBO evolution over time", "LCOM evolution over time", "LOC", "FANIN evolution over time",
                         "FANOUT evolution over time", "WMC") )

    fig.add_trace( go.Scatter( y=dataframe["cbo"] ), row=1, col=1 )
    fig.add_trace( go.Scatter(  y=dataframe["lcom"] ), row=1, col=2 )
    fig.add_trace( go.Scatter(  y=dataframe["loc"] ), row=1, col=3 )
    fig.add_trace( go.Scatter(y=dataframe["fanin"] ), row=2, col=1 )
    fig.add_trace( go.Scatter( y=dataframe["fanout"] ), row=2, col=2 )
    fig.add_trace( go.Scatter(  y=dataframe["wmc"] ), row=2, col=3 )
    # Update xaxis properties
    fig.update_xaxes( title_text="commit", row=1, col=1 )
    fig.update_xaxes( title_text="commit", row=1, col=2 )
    fig.update_xaxes( title_text="commit", row=1, col=3 )
    fig.update_xaxes( title_text="commit", row=2, col=1 )
    fig.update_xaxes( title_text="commit", row=2, col=2 )
    fig.update_xaxes( title_text="commit", row=2, col=3 )

    # Update yaxis properties
    fig.update_yaxes( title_text="cbo", row=1, col=1 )
    fig.update_yaxes( title_text="lcom", row=1, col=2 )
    fig.update_yaxes( title_text="cbo", row=1, col=3 )
    fig.update_yaxes( title_text="fanin", row=2, col=1 )
    fig.update_yaxes( title_text="fanout", row=2, col=2 )
    fig.update_yaxes( title_text="cbo", row=2, col=3 )

    fig.update_layout( title_text=title , showlegend=False )
    fig.show()

if __name__ == "__main__":

    for file in os.scandir(CSV_TO_PLOT):
        filename_string = os.path.basename( file ).replace(".csv", "")

        dataframe = pd.read_csv( CSV_TO_PLOT + "\\" +os.path.basename(file) )
        if filename_string=="full_project_weighted":
            title= "Metriche del sistema Gerrit "
        elif filename_string=="full_project_not_weighted":
            title=None
        else:
            title = "Metriche della classe " + filename_string
        if not title==None:
            plot_metrics(dataframe, title )
