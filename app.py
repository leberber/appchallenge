#print(dmc.Checkbox(label="I agree to sell my privacy", size="sm", checked=True),.to_plotly_json())
# PlayStation 5 Console, Apple AirPods Pro, NordicTrack T Series Treadmills	
from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback, _dash_renderer, no_update, ctx, State, set_props
import pandas as pd
_dash_renderer._set_react_version("18.2.0")
import dash_mantine_components as dmc
import plotly.graph_objects as go
from utils import iconify, CheckboxChip, expendable_box, fig_layout
import json
import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)

from utils import iconify
from sidebar_layout import sidebar
from client_side_callbacks import drawer_sidebar_togle, theme_switcher_callback
from components.shadowbox import ShadowBox
from components.flipcard import FlipCard

app = Dash(__name__)
print(dmc.Checkbox(label="I agree to sell my privacy", size="sm", checked=True).to_plotly_json())
# Helper functions
def make_filter(filters):
    s = ""
    for key, value in filters.items():
        if value:
            s = s + f"`{key}` == { value} & "
    s = s[:-3]
    return s

def filter_df(df, products,  feature, product_or_category):

    df = df[df[product_or_category].isin(products)]
    if feature:
        groupby = [product_or_category, feature]

    else:
        groupby = product_or_category

    df = df.groupby(groupby).agg(
        unique_orders=('Category', 'count'),
        price=('Purchase Price Per Unit', 'sum'),
        quantity=('Quantity', 'sum')
    ).reset_index()
    return df

def _underscores(text):
    parts = text.split('_')
    result = []

    for i, part in enumerate(parts):
        result.append(part)
        if i < len(parts) - 1:  
            if i % 2 == 0:
                result.append(' ')
            else:
                result.append('<br>')

    return ''.join(result)

def make_data_traces(df, feature, product_or_category):
    data = []
    if feature:
        groups = list(df[feature].unique())
        for c in groups:
            _f = df[df[feature]==c] 
            data.append(
                go.Bar(name=c, x=_f[product_or_category], y=_f['price'],  marker=dict(line=dict(width=0.01))),
            )
    else:
        data.append(
            go.Bar( x=df[product_or_category], y=df['price'],  marker=dict(line=dict(width=0.01))),
    )
    return data 

def plotly_bar_layout():
    fig = go.Figure([])
    fig.update_layout(yaxis_tickprefix = '$ ',  barcornerradius=15)
    fig.update_layout(
        font=dict(
            family="verdana, arial, sans-serif",
            size=14,
            color='gray'
        ),
        template="plotly_white" ,     
        autosize = True,
        margin=dict( t=0, b=20),
        xaxis=dict(),
        yaxis=dict(),
        )
    return fig


# reading and processing the data

df = pd.read_csv("data/survey.csv")
df.columns = [i.replace('-', '_') for i in df.columns]

m= pd.merge(pd.read_pickle('data/amazon-purchases.pkl'), df, on='Survey ResponseID',  how='inner')
m= pd.merge(pd.read_csv('data/states.csv', sep='\t'), m, left_on='state',  right_on='Shipping Address State', how='inner')
m = m.dropna(subset=['Title', 'Category'])
m.columns = [i.replace('-', '_') for i in m.columns]

m = m[m['Q_demos_state'] != 'I did not reside in the United States']
m = m[m['shipping_state'] != 'Puerto Rico']
states = sorted(m['shipping_state'].unique())

products =   [str(item )for item in m['Title'].unique() if item ]
product_category = [str(item )for item in m['Category'].unique() if item ]

m = m.rename(columns={'Title': 'Product'})
f = pd.read_csv("data/fields.csv", header=1)

f['Survey ResponseID'] = f['Survey ResponseID'].str.replace('-', '_')
_filters= dict(zip(f['Survey ResponseID'],f['Response ID']))

shadow_box =   dmc.CheckboxGroup(
    id="sub-graphs-chips",
    value = [],
    children=[
        dmc.Box(
                mt = 35,
                style = {    'whiteSpace': 'nowrap'},
                children =  ShadowBox().layout(
                    children = [
                    dmc.Box(
                
                        style = { 'boxShadow': 'rgba(219, 166, 232, 0.1) 0px 3px 12px', "borderRadius":'20px',  "margin":'10px 10px', "padding":'5px 10px 5px 0px', },

                        children = [
                            CheckboxChip(label = f"{i.replace('Q_',' ').replace('demos',' ').replace('_',' ').title()}", value=f"{i}", size= 'lg', className='check-box-group-id',) 
                        ]
                    )
                    
                    for i in _filters
                ]
                )
            )
    ]
)

search_component = dmc.Box(
        id = "outer-search",
        style = {
            'position': 'fixed',
            'left': '50%',
            'top': '0px',
            'transform': 'translateX(-50%)',
            'zIndex':10000
        },
        children = [
            dmc.Popover(
                width=650,
                position="bottom-start",
                withArrow=False,
                shadow="md",   
                transitionProps={
                    "transition": "slide-up", 
                    "duration": 200,
                    "timingFunction": "ease"
                },
                zIndex=2000,
                children = [    
                    dmc.PopoverTarget(
                        dmc.Box(
                            p=15,
                            w= 650,
                            children = [
                                dmc.TextInput(
                                    leftSection=iconify(icon="iconamoon:search-thin"),
                                    rightSection=dmc.SegmentedControl(
                                            id = 'segmented-product-or-category',
                                            value = "Category",
                                            data = [
                                                {"value": "Category", "label": dmc.Center([iconify(icon='iconamoon:category-thin', width=16), html.Span('Category')],style={"gap": 10})},
                                                {"value": "Product", "label":  dmc.Center([iconify(icon='weui:shop-outlined', width=16), html.Span('Product')],style={"gap": 10})},

                                                ], size='xs', radius='lg'),
                                    id='input-box',  
                                    placeholder='Search by Product or Category',
                                    styles={
                                        "root": { 'boxShadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px', 'borderRadius':'20px', 'position': 'relative', 'zIndex':10000},
                                        "input": { 'height': '45px', 'borderRadius':'20px', },
                                        "section": {'padding':'10px', 'width':'auto'}
                                    }
                                )
                            ]
                        )
                    ),
                    dmc.PopoverDropdown(
                        id ='search-output', 
                        style = {
                            'marginTop': '-80px', 'paddingTop': '70px',
                            'borderRadius': '20px 20px 10px 10px'
                        },
                        styles={"root": { 'boxShadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'}},
                        children= dmc.CheckboxGroup(
                            id="search-checkbox-group",
                            children = [],
                            value =[]
                        )
                    )
                ]
            )
        ]
    )


back = dmc.Paper(
    h = '100%',
    w = '100%',
    shadow = 'xs',
    radius = 'lg',
    pos = 'relative',  
    className = 'bg-switch-darker',
    id='sub-graphs',
    children = []
)

front=  dmc.Box(
    h = '100%',
    w = '100%',
    id = 'map-container',
    pos = "relative",
    children = [
        dmc.Box(id= 'map', h = '100%'),
        dmc.Box(
            id = 'legend',
            style={"position": "absolute", "bottom": "20px","left": "2%", "zIndex": "20",},
            children = [   
            ]
        ),
        dmc.SegmentedControl(
            id="map-select-product",
            style={"position": "absolute", "bottom": "10px","left": "30%", "zIndex": "30",  'transform': 'translateX(-50%)'},
            radius='lg',
            styles={"root":{'backgroundColor':'#efeaea'}},
            data=[],
            mb=10,
        ),
        dmc.Paper(
            h = '100%',
            w = '100%',
            shadow="lg",
            children = [
                expendable_box(
                    "state-filter",  
                    "expandable-box", 
                    dmc.Text('FILTERS', p =10), 
                    dmc.CheckboxGroup(  
                        children =dmc.Paper(
                            style = {'boxShadow':'rgba(0, 0, 0, 0.1) 0px 0px 5px 0px, rgba(0, 0, 0, 0.1) 0px 0px 1px 0px !important',      
                                     "position": "absolute", "top": "0px",
                                    "height":" 100%",
                                    "width": "100%" 
                                    },
                            shadow = 'lg',
                            p = 10,
                            children =[
                                dmc.Box(
                                    dmc.Switch(
                                        id = 'select-all-states',
                                        size="sm",
                                        radius="lg",
                                        label="Select ALL",
                                        mb = 10,
                                        p = 8,
                                        checked = True,
                                        styles={"label": {"color": 'gray'}},
                                    ),      
                                    style = {"position": "absolute",  "top": "0px","width": "100%"},
                                    p = 8,
                                ),
                                dmc.Box(
                                    id = 'states-check-data',
                                    mt = 50,
                                     style={
                                        "height": "100%",
                                        "overflow": "scroll"
                                    }
                                )
                            ]
                        )
                    ) 
                )
            ]
        )    
    ]
)

flip_card = FlipCard(
    front=front,
    back=back,
    button=dmc.Button(
        id='flip-button',  
        variant="outline", 
        n_clicks=0,  
        size = 'sm', 
        color= 'grape', 
        style={"position": "absolute", "top": "0px", "right": "70px"}
    )
)

content =   dmc.Box(
    id = 'content',
    children= [
        dmc.Box(
            id = 'main-content-top-section',
            children=[
                dmc.ActionIcon(
                    id = 'color-scheme-toggle',
                    n_clicks=0, 
                    variant= "transparent",
                    style = {'position':'absolute','right':'0px','top':'1px' },
                ),
                dmc.ActionIcon(
                    size="md",
                    variant="transparent",
                    id="drawer-sidebar-button",
                    n_clicks=0,
                ),
                search_component,
                shadow_box,
            ]
        ),
        dmc.Box(
            id = 'main-content-graph-section',
            p ='10px',
            style = {'position': 'relative','width': '100%','height': '100%' },
            children=[
                dcc.Store('map-data'),
                flip_card.layout()           
            ]
        )   
    ]
)


app.layout =  dmc.MantineProvider(
    id="mantine-provider",
    children = [
        dmc.Box(
            children = [
                sidebar(df, _filters),
                content,
                dcc.Store(id = 'sto', data = {'initila':'my data'}),
            ]
        )
    ]
)


@callback(
    Output("search-checkbox-group", "children"), 
    Input('input-box', 'value'),
    Input('segmented-product-or-category', 'value'),
    Input("search-checkbox-group", "value"), 
    prevent_intial_call = True
)
def update_output(value, segmented, selected_prodcuts):

    if ctx.triggered_id =='segmented-product-or-category':
        set_props("map-select-product", {'value': []})
        set_props("map-select-product", {'data': []})
        selected_prodcuts = []
    if ctx.triggered_id =='search-checkbox-group':
        if selected_prodcuts:
            set_props("map-select-product", {'value': selected_prodcuts[-1]})
        set_props("map-select-product", {'data': selected_prodcuts})
        
    if segmented =='Product':
        items = products
    else:
        items = product_category

    def found_items(items):
        return  dmc.ScrollArea(
                    h=350, 
                    w='100%',
                    mt=10,
                    children =  dmc.Stack(
                        children = [
                            dmc.Checkbox(
                                label=str(i).replace("_"," ").title(), 
                                value=i, 
                                size = 'sm',
                                styles={"label": {"paddingInlineStart": 8, 'color':'gray'}}
                            ) 
                            for i in items
                        ]
                    ) 
                )

    if value:  
        return found_items(
            sorted(set(sorted([i for i in items if value.lower() in i.lower() ])[:30] + selected_prodcuts))
        ) 
 
    return found_items(
        sorted(set(items[:30] + selected_prodcuts))
    ) 

def make_bar_chart(m, products,  feature, product_or_category):
   
    df = filter_df(m, products,  feature, product_or_category)
    df[product_or_category] = df[product_or_category].apply(_underscores)
    data = make_data_traces(df, feature, product_or_category)

    fig = go.Figure(
        data=data, 
        layout= fig_layout
    )
    fig.update_layout(legend=dict(orientation="h"))
    g = dcc.Graph(  
        figure= fig, 
        config={'displayModeBar': False}, 
        style={'width': '100%',  'height': '100%' },  className = "outer-graph",
    )
    return dmc.Box(
        style={'width': '100%',  'height': '50%', "position":"relative" },
        p='2%',
        id={"type": "maximize-graph", "index":'my_index' if not feature else feature},
        children = [
            dcc.Store(id = {"type": "remember-graph-setting", "index": 'my_index' if not feature else feature}),
            dmc.ActionIcon(
                iconify ('system-uicons:fullscreen', width = 15),
                size="lg",
                style = { "position":"absolute",  "right":"0px",  "top":"0px" },
                variant="subtle",
                id={"type": "action-maximize-graph", "index": 'my_index' if not feature else feature},
                n_clicks=0,
            ),
            dmc.Paper(
                p = 5,
                style={'width': '100%',  'height': '100%',   'borderRadius': '15px'  },
                shadow='sm',
                children =[
                   g
                ]
            )
        ]
    )

@callback(
    Output("sub-graphs", "children"),
    Input({"type": "checkbox-options", "index": ALL}, "value"),
    Input("search-checkbox-group", "value"),
    Input('sub-graphs-chips', 'value'),
    Input('segmented-product-or-category', 'value'),
    
    prevent_intial_call = True
)
def display_output(_filters,   products, features, product_or_category): 
    
    if not products:
        return []
    
    converted_dict = {item['id']['index']: item.get('value') for item in ctx.inputs_list[0] if item.get('value')}
    filters = make_filter(converted_dict)

    if filters:
        df = m.query(filters)
    else:
        df = m

    def make_map_series (df, products, product_or_category):

        df = df.groupby(["shipping_state", "Q_demos_state", product_or_category]).agg(
                    lat=('lat', 'first'),
                    lon=('lon', 'first'),
                    unique_orders=(f"{product_or_category}", 'count'),
                    price=('Purchase Price Per Unit', 'sum'),
            ).reset_index()
        df['id'] = df['shipping_state']
      
        points = df[[ "id", "lat", "lon", "Q_demos_state"]].drop_duplicates(subset = ['id']).to_dict('records')
        points = json.dumps(points)
        df = df[[ "id", "Q_demos_state", product_or_category, "price",  'unique_orders']]
        arrows = df[df[product_or_category].isin(products)].values.tolist()
        return points, arrows
    
    points, arrow = make_map_series (df, products, product_or_category)

    set_props("map-data", {'data': {'points':points, 'arrow':arrow}})
    
    _chidren = Patch()

    if ctx.triggered_id == 'search-checkbox-group':
        if not features:

            g = make_bar_chart(df, products,  '', product_or_category)
            _chidren.clear()
            _chidren.append(g)
        else:
            _chidren.clear()
            for feature in features:
                g = make_bar_chart(df, products,  feature, product_or_category)
                _chidren.append(g)
    else:
        if not features:
            g = make_bar_chart(df, products,  '', product_or_category)
            _chidren.clear()
            _chidren.append(g)
        else:
            _chidren.clear()
            for feature in features:
                g = make_bar_chart(df, products,  feature, product_or_category)
                _chidren.append(g)

    return _chidren

ShadowBox().callback()
flip_card.app_callbacks()

drawer_sidebar_togle()
theme_switcher_callback()

if __name__ == "__main__":
    app.run(debug=True)



