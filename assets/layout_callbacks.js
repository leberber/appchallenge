window.dash_clientside = Object.assign({}, window.dash_clientside, {
    layout_callbacks: {
        drawer_sidebar_togle: function (maximize_action) {
          let minimize = {
                'props': {'icon': 'arcticons:hamburger-menu', 'width': 40, 'color': 'gray', },
                'type': 'DashIconify', 'namespace': 'dash_iconify'
            }
          let maximize = {
                'props': {
                    'icon': 'arcticons:hamburger-menu', 'width': 40, 'color': 'gray', },
                    'type': 'DashIconify', 'namespace': 'dash_iconify'
            }
            
            // const openWidth = getComputedStyle(root).getPropertyValue('--drawer-sidebar-width');
            const sidebarWidth = getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width')
       
          
          let mainContentTopSection = document.getElementById('main-content-top-section').offsetHeight;

          // document.documentElement.style.setProperty('--header-height', mainContentTopSection);
          document.getElementById("main-content-graph-section").style.height = `calc(100vh - ${mainContentTopSection}px)`;
            
          if (maximize_action % 2 === 0) { 
            
            
            // document.getElementById("main-app-layout").style.marginLeft=sidebarWidth;
            document.getElementById("content").classList.remove('content-extended');
            document.getElementById("content").classList.add('content-shrinked');
            document.getElementById("sidebar").classList.remove('sidebar-shrinked');
            document.getElementById("sidebar").classList.add('sidebar-extended');
            return  [ minimize, {
                 "zIndex": "1000"} ]
          } 
          
         
          document.getElementById("content").classList.remove('content-shrinked');
          document.getElementById("content").classList.add('content-extended');
          document.getElementById("sidebar").classList.remove('sidebar-extended');
          document.getElementById("sidebar").classList.add('sidebar-shrinked');

          return  [ maximize, {"marginLeft": "0px"}]
        }
    },
});
