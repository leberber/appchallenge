
from dash_iconify import DashIconify 
import pandas as pd
from dash import dcc, html
import dash_mantine_components as dmc
import dash_ag_grid as dag


def iconify(icon, color = 'dark', width=20, cN = '_'):
    return DashIconify(
        icon=icon,  
        color=color, 
        width = width, 
        className=cN
    )

def badge(children, color = 'dark'):
    return dmc.Badge(
        children=children,  
        color=color, 
    )

def CheckboxChip(label, value, **kwargs):
    return dmc.Checkbox(
        **kwargs,
        label=label, 
        value=value, 
        p = 0,
        iconColor = 'blue',
        # size = 'lg',
        
        styles = {
                "input": {
                    "display":'none', "height":'50px',   "padding":'5px 15px 5px 0px', 
                },
                "label": {
                    "cursor":'pointer',
                "padding":'0px 15px 0px 0px', "fontSize" :'14px',  'display': 'inline-block', 'color': 'gray',
                },
            }
    )
def expendable_box(id, rootClass, titleText, children):
    return dmc.Paper(
        id=id,
        shadow='md',
        className=rootClass,
        children=[
            dmc.Box(titleText, className="vertical-text"),
            dmc.Box(titleText, className="horizontal-text"),
            dmc.Box(children=children, className="children-content")
        ]
    )

fig_layout = dict(
    yaxis_tickprefix = '$ ', 
    barcornerradius=15,
    font=dict(
        family="verdana, arial, sans-serif",
        size=14,
        color='gray'
    ),
        template="plotly_white" ,     
        autosize = True,
        margin=dict( t=0, b=20),
)