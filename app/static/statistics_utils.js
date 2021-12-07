function create_pie_chart(data, element, colors, title) {
    var data_object = {
        labels: Object.keys(data),
        datasets: [
            {
                backgroundColor: colors.slice(0, Object.keys(data).length),
                borderWidth: 1,
                data: Object.values(data)
            }
        ]
    };
    var pie_options = {
        cutoutPercentage: 0, 
        plugins: {
            title: {
                display: true,
                position: 'bottom',
                text: title,
                font: {size: 16},
            },
            legend: {
                position:'top',
                padding:51,
                labels: {
                    boxWidth: 10
                }
            }
        }
    };

    var element_obj = document.getElementById(element);
    if (element_obj) {
        new Chart(element_obj, {
            type: 'pie',
            data: data_object,
            options: pie_options
        });
    }
}
function create_bar_chart(data, element, colors, title, vertical=true) {
        var chartData = {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: colors[0]
            }]
        };
        var window_screen = $(window).width();
        var element_obj = document.getElementById(element);
        let gainConfig = {
                indexAxis: (vertical)? 'x' : 'y',
                scales: {
                    x: {
                        ticks: {
                            // For a category axis, the val is the index so the lookup via getLabelForValue is needed
                            callback: function(val, index) {
                              // Hide every 2nd tick label

                                if (this.getLabelForValue(val).length > 13) {
                                    return this.getLabelForValue(val).substring(0, 10) + '...'; //truncate
                                }
                                else {
                                    return this.getLabelForValue(val)
                                }
                                // return index % 2 === 0 ? this.getLabelForValue(val) : '';
                            }
                      }
                    }
                },
                plugins: {
                  legend: {
                    display: false
                  },
                  title: {
                      display: true,
                      position: 'bottom',
                      text: title,
                      font: {size: 16},
                  },
                  datalabels: {
                     display: ($(window).width() < 560)? false : true,
                     align: (vertical)? 'top' : 'right',
                     anchor: 'end',
                     offset: (vertical)? -4 : 0
                  }
                },
                maintainAspectRatio: false,
                responsive: true,
            };
        if (element_obj) {
            new Chart(element_obj, {
            type: 'bar',
            data: chartData,
            options: gainConfig
            });
        }
}