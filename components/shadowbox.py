
from dash import Input, Output,  clientside_callback, dcc
import dash_mantine_components as dmc
from utils import iconify

class ShadowBox:
    def layout(self, children):
        
        scroll_shadow_left_style = {
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'width': '80px',
            'height': '100%',
            'background': 'linear-gradient(to right, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0))',
            'pointerEvents': 'none'
        }

        scroll_shadow_right_style = {
            'position': 'absolute',
            'top': '0',
            'right': '0',
            'width': '80px',
            'height': '100%',
            'background': 'linear-gradient(to left, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0))',
            'pointerEvents': 'none'
        }
        return  dmc.Box(
                    style={'padding': '0 35px', 'position':'relative'},
                    children = [
                        dmc.ActionIcon(
                            iconify(icon = 'mage:chevron-left', width = 40, color = 'gray'),
                                id = 'scroll-left',
                                n_clicks=0, 
                                variant= "subtle",
                                   size  = 'lg',
                                radius='lg',
                                color = 'gray',
                                style = {
                                    'position':'absolute',
                                    'left':'0px',
                                    'top':'50%',
                                    'transform': 'translateY(-50%)',
                                    'zIndex': '2000px',
                                    
                                },
                                
                            ),
                            dmc.ActionIcon(
                                iconify(icon = 'mage:chevron-right', width = 30, color = 'gray'),
                                id = 'scroll-right',
                                n_clicks=0, 
                                variant= "subtle",
                                   size  = 'lg',
                                radius='lg',
                                color = 'gray',
                                style = {
                                    'position':'absolute',
                                    'right':'0px',
                                    'top':'50%',
                                    'transform': 'translateY(-50%)',
                                      'zIndex': '2000px',
                                },
                                
                            ),
                        dmc.Box(
                            style={'position': 'relative', 'overflow': 'auto'},
                            children = [
                                dmc.Box(
                                    id="scroll-container",
                                    style={
                                        'display': 'flex', 
                                        'overflowX': 'scroll',
                                         'scrollbarWidth': 'none',  # Firefox
                 'msOverflowStyle': 'none'  # IE and Edge
                                        },
                                    children=children, 
                                ),
                                dmc.Box( darkHidden = True, style = scroll_shadow_left_style),
                                dmc.Box( darkHidden = True, style = scroll_shadow_right_style ),
                                # dmc.Box(id = 'scroll-container')
                            ]
                        ),
                        dcc.Store(id='dummy-output', data='') ,
                    ]
                )

    def callback(self):
        clientside_callback(
            """
            function(_, _, _, _) {
                const scrollContainer = document.getElementById('scroll-container');
                const scrollLeftBtn = document.getElementById('scroll-left');
                const scrollRightBtn = document.getElementById('scroll-right');
                const scrollAmount = 400;

                function updateButtonVisibility() {
                    scrollLeftBtn.style.display = scrollContainer.scrollLeft <= 0 ? 'none' : 'block';
                    scrollRightBtn.style.display = scrollContainer.scrollLeft + scrollContainer.clientWidth >= scrollContainer.scrollWidth ? 'none' : 'block';
                }

                // Initialize button visibility on page load
                updateButtonVisibility();

                // Scroll left button click
                scrollLeftBtn.onclick = function() {
                    scrollContainer.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
                    setTimeout(updateButtonVisibility, 300);
                };

                // Scroll right button click
                scrollRightBtn.onclick = function() {
                    scrollContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' });
                    setTimeout(updateButtonVisibility, 300);
                };

                // Update button visibility on scroll
                scrollContainer.onscroll = updateButtonVisibility;

                // Returning no_update since we handle everything client-side
                return [window.dash_clientside.no_update, window.dash_clientside.no_update];
            }
            """,
            [Output('scroll-left', 'style'), Output('scroll-right', 'style')],
            [Input('scroll-left', 'n_clicks'), Input('scroll-right', 'n_clicks')]
        )

