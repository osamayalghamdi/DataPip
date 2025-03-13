from plotly import graph_objs as go
import altair as alt
import pandas as pd

def create_plotly_chart(data, x_column, y_column, chart_type='line', title='Chart'):
    if chart_type == 'line':
        fig = go.Figure(data=go.Scatter(x=data[x_column], y=data[y_column], mode='lines+markers'))
    elif chart_type == 'bar':
        fig = go.Figure(data=go.Bar(x=data[x_column], y=data[y_column]))
    elif chart_type == 'scatter':
        fig = go.Figure(data=go.Scatter(x=data[x_column], y=data[y_column], mode='markers'))
    else:
        raise ValueError("Unsupported chart type. Use 'line', 'bar', or 'scatter'.")
    
    fig.update_layout(title=title, xaxis_title=x_column, yaxis_title=y_column)
    return fig

def create_altair_chart(data, x_column, y_column, chart_type='line', title='Chart'):
    source = pd.DataFrame(data)
    
    if chart_type == 'line':
        chart = alt.Chart(source).mark_line().encode(x=x_column, y=y_column).properties(title=title)
    elif chart_type == 'bar':
        chart = alt.Chart(source).mark_bar().encode(x=x_column, y=y_column).properties(title=title)
    elif chart_type == 'scatter':
        chart = alt.Chart(source).mark_circle().encode(x=x_column, y=y_column).properties(title=title)
    else:
        raise ValueError("Unsupported chart type. Use 'line', 'bar', or 'scatter'.")
    
    return chart

def save_plotly_chart(fig, filename):
    fig.write_html(filename)

def save_altair_chart(chart, filename):
    chart.save(filename)