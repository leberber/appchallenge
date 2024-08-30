window.dash_clientside = Object.assign({}, window.dash_clientside, {
    maps: {
        map_renderer: function (res, map_data) {

            const no_update = window.dash_clientside.no_update;
            if (!map_data) {
                return no_update;
            }

            const points = JSON.parse(map_data['points']);
   
            const colors = [
                '#F00E0E', '#DE2819', '#CC4225', '#BA5D30', '#A8773B', '#969147', '#84AB52', '#72C65D', '#60E069', '#4EFA74'
            ];

            function decileValues(data) {
                const values = data.map(item => item[3]);
                values.sort((a, b) => a - b);
                
                // Add 0 as the minimum value if it isn't already in the list
                if (values[0] > 0) {
                    values.unshift(0);
                }
            
                // Calculate the deciles
                const deciles = [];
                for (let i = 0; i <= 10; i++) {
                    const percentileIndex = Math.floor(i * (values.length - 1) / 10);
                    deciles.push(values[percentileIndex]);
                }
                
                // Create an array of decile ranges
                const decileRanges = [];
                for (let i = 0; i < 10; i++) {
                    decileRanges.push({
                        decile: i + 1,
                        range: [deciles[i], deciles[i + 1]]
                    });
                }
                
                return decileRanges;
            }
            
            function getColorForValue(value, decileRanges, colors) {
                for (let i = 0; i < decileRanges.length; i++) {
                    const [min, max] = decileRanges[i].range;
                    // console.log(decileRanges[i].range, i,colors[i] )
                    if (value >= min && value <= max) {
                        return colors[i];
                    }
                }
                // Default color if value is out of range (just in case)
                return '#000000'; // black as default color
            }
            
            function maleLegendElement(color, range) {
                return {
                    'props': {
                        'children': [
                            {
                                'props': { 'bg': color, 'h': 15, 'w': 15, 'style': { 'borderRadius': '3px' }},
                                'type': 'Box',
                                'namespace': 'dash_mantine_components'
                            },
                            {
                                'props': { 
                                    'children': `[${range.join(', ')}] $`, 'c': 'rgb(178, 173, 179)', 'size':'sm' },
                                'type': 'Text',
                                'namespace': 'dash_mantine_components'
                            }
                        ],
                        'gap':'5px'
                    },
                    'type': 'Group',
                    'namespace': 'dash_mantine_components'
                };
            }

            const decileLegend = [];

            function getValuesByDecile(decileRanges) {
                // Initialize the result dictionary and last added range tracker
                let lastAddedRange = null;
            
                // Use reduce to build the final dictionary
                return decileRanges.reduce((acc, { decile, range }) => {
                    // Round the range values to two decimal places
                    const roundedRange = range.map(value => Math.round(value ));
            
                    // Add to the result if this range is not a duplicate of the last added one
                    if (JSON.stringify(roundedRange) !== JSON.stringify(lastAddedRange)) {
                        acc[decile] = roundedRange;
                        lastAddedRange = roundedRange;
                    }
            
                    return acc;
                }, {});
            }
            
            function filterData(data, filterValue) {
                const filterData = data.filter(item => item[2] === filterValue)
     
                const deciles = decileValues(filterData); 

                const decileDict = getValuesByDecile(deciles);
                Object.entries(decileDict).forEach(([decile, range]) => {
                    const color = colors[decile-1]; // Get the color for this decile
                    const legendElement = maleLegendElement(color, range); // Create the legend element
                    decileLegend.push(legendElement); // Append it to the decileLegend array
                });
                
                return filterData.map(item => {
                        return {
                            from: item[0],
                            to: item[1],
                            price: item[3],
                            quantity: item[4],
                            width: Math.log(item[4] + 1),  // Adjust line width based on quantity
                            color: getColorForValue(item[3], deciles, colors)
                        };
                    });
            }

            const arrows = filterData(map_data['arrow'], res);

            const filteredPoints = points.filter(point => arrows.some(arrow => arrow.from === point.id || arrow.to === point.id));

            const map = Highcharts.mapChart('map', {
                chart: {
                    map: basemap
                },
                title: {
                    text: 'Product Shipping Routes: Origins and Destinations',
                    align: 'center'
                },
                plotOptions: {
                    flowmap: {
                        tooltip: {
                            headerFormat: null,
                            pointFormat: `{point.options.from} \u2192
                            {point.options.to}<br>
                            Value Amount: ${'{point.price}'}<br>
                            Quantity: {point.quantity}`
                        },
                        lineWidth:1
                    },
                    mappoint: {
                        tooltip: {
                            headerFormat: '{point.point.id}<br>',
                        },
                        showInLegend: false
                    }
                },
                series: [
                    { name: 'Basemap', showInLegend: false },
                    {
                        type: 'mappoint',
                        color: 'rgb(224 189 233)',
                        data: filteredPoints,  
                        visible: true
                    },
                    {
                        type: 'flowmap',
                        data: arrows,  
                        showInLegend: false 
                    }
                ]
            });

            const available_states = [...new Set(arrows.map(subArray => subArray.from))];
            const checkChildren = available_states.map(element => ({
                props: {
                    checked: true,  // Ensure all checkboxes are checked by default
                    className: 'map-state-filter',
                    label: element,
                    mb: 2,
                    size: 'sm',
                    styles: {
                        label: {
                            paddingInlineStart: 8,
                            color: 'gray'
                        }
                    },
                    value: element
                },
                type: 'Checkbox',
                namespace: 'dash_mantine_components'
            }));

            function toggleCheckboxes() {
                const checkboxes = document.querySelectorAll('.map-state-filter .mantine-Checkbox-input');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = switchElement.checked;
                });
                updateChartData();
            }
            

            const switchElement = document.getElementById('select-all-states');
            switchElement.addEventListener('change', toggleCheckboxes);

            function getCheckedCheckboxes() {
                return Array.from(document.querySelectorAll('.map-state-filter .mantine-Checkbox-input'))
                    .filter(checkbox => checkbox.checked)
                    .map(checkbox => checkbox.value);
            }

            function updateChartData() {
                const checkedCheckboxes = getCheckedCheckboxes();
                const filteredData = arrows.filter(arrow => checkedCheckboxes.includes(arrow.from));

                const filteredPoints = points.filter(point => filteredData.some(arrow => arrow.from === point.id || arrow.to === point.id));

                if (Object.getOwnPropertyNames(map).length === 0) {
                    return;
                } else {
                    map.series[1].setData(filteredPoints, true);  // Update points data
                    map.series[2].setData(filteredData, true);  // Update arrows data
                }
            }

            
            // Attach event listeners after the checkboxes are rendered
            setTimeout(() => {
                const checkboxes = document.querySelectorAll('.map-state-filter .mantine-Checkbox-input');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = true; // Ensure they are checked
                    checkbox.addEventListener('change', updateChartData);
                });
                updateChartData(); // Call this to ensure the data is updated after setting the checkboxes
            }, 0); // This delay ensures that the checkboxes are rendered before attaching listeners

            const legend = [{'props': {'children': 'Total of Product Value', 'c':'rgb(178, 173, 179)'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}].concat( decileLegend)
     
            if (decileLegend.length ===1){
                return no_update
            }
            return [checkChildren, 
                legend, true
                 
            ]
        }
    },
});