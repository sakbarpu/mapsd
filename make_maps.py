import plotly.graph_objects as go
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1], sep="\t")
if sys.argv[2] == "commits": to_plot = " #Commits "
elif sys.argv[2] == "developers": to_plot = " #Developers "
print (df.columns)

fig = go.Figure(data=go.Choropleth(
    locations = df[' Code2 '],
    z = df[to_plot],
    text = df[' Name '],
    colorscale = 'Reds',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='black',
    marker_line_width=0.75,
    colorbar_tickprefix = '',
    colorbar_title = 'Number of ' + sys.argv[2].capitalize(),
))

fig.update_layout(
    title_text='2018 Number of Software ' + sys.argv[2].capitalize(),
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
#    annotations = [dict(
#        x=0.05,
#        y=0.15,
#        xref='paper',
#        yref='paper',
#        text='Source: MapSD software development map',
#        showarrow = False
#    )]
)

fig.show()

