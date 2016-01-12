$(function () {
    $('#container').highcharts({
        title: {
            text: 'Beaver Attendance',
            x: -20 //center
        },
        xAxis: {
            categories: dates,
        },
        yAxis: {
            title: {
                text: 'Percent Attendance'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }],
            min:0,
            max:100
        },
        tooltip: {
            valueSuffix: '%',
            valueDecimals: 2
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Attendance',
            data: attendance_data
        }]
    });
});
