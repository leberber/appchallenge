
from dash import (Input, Output, 
    clientside_callback, MATCH,
    ClientsideFunction, 
)

def drawer_sidebar_togle():
    clientside_callback(
        ClientsideFunction(
            namespace='layout_callbacks',
            function_name='drawer_sidebar_togle'
        ),
    Output("drawer-sidebar-button", "children"),
    Output("drawer-sidebar-button", "style"),
    Input("drawer-sidebar-button", "n_clicks")
)

def theme_switcher_callback():
    clientside_callback(
        ClientsideFunction(
            namespace='theme',
            function_name='theme_switcher_callback'
        ),
        Output("mantine-provider", "theme"),
        Output("mantine-provider", "forceColorScheme"),
        Output("color-scheme-toggle", "children"),
        Input("color-scheme-toggle", "n_clicks")
    )
   
clientside_callback(
    """function update_badge_count(value) {
           const no_update = window.dash_clientside.no_update
           const objectLength = value ? Object.keys(value).length : 0;
        return objectLength
    }
    """,
    Output({"type": "badge-num-filters", "index": MATCH}, "children"),
    Input({"type": "checkbox-options", "index": MATCH}, "value"),
)


clientside_callback(
    """function maximize_chart(n_clicks) {
        const no_update = window.dash_clientside.no_update
        let ctx = window.dash_clientside.callback_context;
        if (ctx.triggered.length !=1 ) { 
            return no_update
        }
        const triggered_id = JSON.parse(ctx.triggered[0]['prop_id'].split(".")[0])
        if (n_clicks % 2 === 1) { 
            return {'height':'100%', 'position':'relative' }
        } 
        return {'height':'50%',  'position':'relative' }
    }
    """,
    Output({"type": "maximize-graph", "index": MATCH}, "style"),
    Input({"type": "action-maximize-graph", "index": MATCH}, "n_clicks"),
     prevent_intial_call = True
 
)


clientside_callback(
    ClientsideFunction(
        namespace='maps',
        function_name='map_renderer'
    ),


    Output('states-check-data', "children"),
    Output('legend', "children"),
    Output('select-all-states', "checked"),
    
    Input('map-select-product', "value"),
    Input('map-data', "data"),
)

