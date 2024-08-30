window.dash_clientside = Object.assign({}, window.dash_clientside, {
   
    theme: {

         theme_switcher_callback: function (n_clicks) {
            
            let lightIcon = {'props': {'icon': 'ic:baseline-light-mode', 'width': 40, 'color':'gold'}, 'type': 'DashIconify', 'namespace': 'dash_iconify'}
            let darkIcon = {'props': {'icon': 'ic:sharp-dark-mode', 'width': 40, 'color':'#e8e3e6'}, 'type': 'DashIconify', 'namespace': 'dash_iconify'}
            let custom_theme_colors = {
                "dark_blue": ["#4A5468","#465064","#424C60","#3E485B","#3A4457","#354053","#313C4F","#2D384A","#293446","#253042"],
                "dimmed_purple":[ "#F5F2F6","#E6DEEA", "#DAC9E1", "#CFB3DB", "#C1A6CD", "#B39ABE", "#A790B0", "#9A87A3","#8F7E96","#85778B" ]
               }
            let lightColorScheme =  { 
                "fontFamily": "'Roboto','Arial',sans-serif",
                "colorScheme": "light",
                "colors":custom_theme_colors,
                // "shadows": {
                //     "xs": "0px 4px 3px -3px rgba(0, 0, 0, 0.05)",
                //     "xl": "inset 0px 4px 3px -3px rgba(0, 0, 0, 0.05)",
                // },
                "components": {
                },
            }
            
            let darktColorScheme =  { 
                "colorScheme": "dark",
                "fontFamily": "'YouTube Sans','Roboto',sans-serif",
                "colors": custom_theme_colors,
                "components": {
                },

            }

            if (n_clicks % 2 === 0) { 
                const style = document.createElement('style');
                style.textContent = `
                    .ygrid, .xgrid , .yzl, .xzl {
                        stroke: rgb(242, 244, 249) !important;
                    }
                    .js-plotly-plot > div > div > svg:nth-child(1) {
                        background: white !important;
                    }
                    .hovertext path {
                        stroke: none !important;
                        fill: none !important;
                    }
                    .highcharts-background{
                        fill: rgb(255, 255, 255);
                    }
                    .highcharts-series.highcharts-map-series .highcharts-point {
                        fill: rgb(250, 250, 250);
                        stroke: rgb(245, 236, 245);
                    }
                `;
                document.head.appendChild(style);
                document.documentElement.style.setProperty('--theme-background', 'white');
                document.documentElement.style.setProperty('--theme-background-darker', 'white');
                document.documentElement.style.setProperty('--shadow-dk', 'rgba(219, 166, 232, 0.1) 0px 3px 12px');

               return [lightColorScheme, 'light', darkIcon]
            } 
            
               const style = document.createElement('style');
               style.textContent = `
                .ygrid, .xgrid , .yzl, .xzl {
                      stroke: #2e2e2e !important;
                  }
                  .js-plotly-plot > div > div > svg:nth-child(1) {
                    background: rgb(31, 31, 31) !important;
                }
                .highcharts-series.highcharts-map-series .highcharts-point {
                    fill:  #2e2e2e ;
                    stroke:  #333333 ;
                }
                .highcharts-background{
                    fill: rgb(31, 31, 31) ;
                    border-radius: 20px;
                }
              `;
              document.head.appendChild(style);
              document.documentElement.style.setProperty('--theme-background', '#2e2e2e');
              document.documentElement.style.setProperty('--theme-background-darker', 'rgb(31, 31, 31)');
              document.documentElement.style.setProperty('--shadow-dk', 'none');   

        return [ darktColorScheme, 'dark', lightIcon]
        }
  
    },
});
