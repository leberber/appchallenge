
import dash_mantine_components as dmc

scroll_shadow_start_style = {
    'position': 'absolute',
    'top': '5%',
    'left': '0',
    'width': '100%',
    'height': '80px',
    'background': 'linear-gradient(to bottom, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0))',
    'pointerEvents': 'none'
}
scroll_shadow_end_style = {
    'position': 'absolute',
    'bottom': '4%',
    'left': '0',
    'width': '100%',
    'height': '80px',
    'background': 'linear-gradient(to top, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0))',
    'pointerEvents': 'none'
}

def sidebar(df, _filters):

    def make_accordion_filters(df, value, _filters):
        return dmc.AccordionItem(
            m = 5,
            className='bg-switch shadow-dk',
            value=value,
            children = [
                    dmc.AccordionControl(
                        styles = {
                            'label':{
                                'padding':'10px'
                                }
                        },
                        children = [
                            dmc.NavLink(
                                label= dmc.Text(value.replace('Q_',' ').replace('_',' ').title().replace("Demos ", ""),  fz=14, c= "rgb(107, 107, 107)"),
                                childrenOffset=28,
                                children=[
                                    dmc.Text(_filters[value], size="sm", fw=200, c="dimmed", ml = '-15px')
                                ]
                            )
                        ],
                        icon = dmc.Badge(0, 
                            size="xl", 
                            color = 'grape',  fw=150,  fz=13, 
                            circle=True, 
                            style = { 'boxShadow': 'rgba(0, 0, 0, 0.09) 0px 3px 12px', },id={"type": "badge-num-filters", "index": value}, 
                            variant="light"
                        ), 
                        id={"type": "accordion-checkbox-filters", "index": value},
                    ),
                    dmc.AccordionPanel(
                        children=  dmc.CheckboxGroup(
                            id={"type": "checkbox-options", "index": value},
                            children=dmc.Stack(
                                children =[
                                    dmc.Checkbox(label=i, value=str(i), styles={"label": {"paddingInlineStart": 8, 'color':'gray'}}) for i in list(df[value].unique()) 
                                ], 
                                style = {'gap':'3px'}
                            ),
                        )
                    )
                ] 
            )

    sidebar=dmc.Box(
        id = "sidebar",
        p = '5px 20px',
        children =[
            dmc.Box(
                className='sidebar-style',
                children = [
                    dmc.Text( "Filters", pl = 10, mb = 5, h='5%',c= "#2f2e38", fw = 700, fz =25 ),
                    dmc.Accordion(
                        pt = '20px',
                        pb = '20px',
                        chevronPosition="left",
                        id='checkbox-filters-accordion',
                        radius = 'md',
                        variant = "separated", 
                        style = { 'overflow': 'Scroll', 'height': '90%'},
                        children=[
                            dmc.Box( darkHidden=True, style = scroll_shadow_start_style),
                            dmc.Box( darkHidden=True,style = scroll_shadow_end_style ), 
                        ]+[
                            make_accordion_filters(df, value, _filters) for value in sorted(_filters)
                        ]
                    ),
                    dmc.Box(h='5%')
                ]
            )
        ]
    )
    return sidebar



