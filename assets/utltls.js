function iconify(icon, color='dark', width=20){
    return {
        'props': {
            'icon': icon, 
            'width':width, 
            'color': color },
        'type': 'DashIconify',
        'namespace': 'dash_iconify'
    }
}

function badge(props){
                                                                                                                                        
    return {
        'props': props, 
        'type': 'Badge',
         'namespace': 'dash_mantine_components'
    }
}



