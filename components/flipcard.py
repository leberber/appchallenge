from dash import  Input, clientside_callback, Output
import dash_mantine_components as dmc

class FlipCard:
    def __init__(self, front, back, button):
        self.front = front
        self.back = back
        self.button = button
        self.button_id = button.id

    def layout(self):
        return dmc.Box(
            children=[
                dmc.Box(
                    children=[
                        dmc.Box(
                            children=self.front,
                            id=f"{self.button_id}-front",
                            style={
                                'width': '100%',
                                'height': '100%',
                                'color': 'white',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'fontSize': '24px',
                                'position': 'absolute',
                                'backfaceVisibility': 'hidden',
                                'transform': 'rotateY(0deg)',
                                'transformOrigin': 'center',  # Ensures centered rotation
                                'transition': 'transform 0.6s',
                            }
                        ),
                        dmc.Box(
                            children=self.back,
                            id=f"{self.button_id}-back",
                            style={
                                'width': '100%',
                                'height': '100%',
                                'color': 'white',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'fontSize': '24px',
                                'position': 'absolute',
                                'backfaceVisibility': 'hidden',
                                'transform': 'rotateY(180deg)',
                                'transformOrigin': 'center',  # Ensures centered rotation
                                'transition': 'transform 0.6s',
                            }
                        )
                    ],
                    style={
                        'width': '100%',
                        'height': '100%',
                        'position': 'relative',
                        'transformStyle': 'preserve-3d',
                        'transform': 'rotateY(0deg)',
                        'transformOrigin': 'center',  # Ensures centered rotation
                        'transition': 'transform 0.6s',
                    },
                    id=f"{self.button_id}-inner"
                ),
                self.button
            ],
            style={
                'position': 'relative',
                'width': '100%',  # Parent container width
                'height': '100%',  # Parent container height
                'perspective': '1000px',  # This gives a 3D effect when flipping
                'overflow': 'hidden',  # Prevents any overflow issues
            }
        )

    def app_callbacks(self):
        clientside_callback(
            """
            function(n_clicks) {
              let map = {'props': {'icon': 'arcticons:50-us-states-map', 'width': 20, 'color':'grap'}, 'type': 'DashIconify', 'namespace': 'dash_iconify'}
            let bars = {'props': {'icon': 'healthicons:low-bars-outline', 'width': 20, 'color':'grap'}, 'type': 'DashIconify', 'namespace': 'dash_iconify'}
                const inner = document.getElementById('%s-inner');
              
                
                if (inner) {
                    const isFlipped = inner.style.transform === 'rotateY(180deg)';
                    inner.style.transform = isFlipped ? 'rotateY(0deg)' : 'rotateY(180deg)';
                }
                
                if (n_clicks & 1) {
           
                return ['Bars', bars]
                }
                return [ 'Maps', map]
            }
            """ % (self.button_id),
            Output(self.button_id, 'children'),
            Output(self.button_id, 'leftSection'),
            Input(self.button_id, 'n_clicks')
        )