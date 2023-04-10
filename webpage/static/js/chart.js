
var myChart = echarts.init(document.getElementById('chart'));

function joinHandler(data) {
    var option = {
        title: {
            text: data.street + ',' + data.city + ',' + data.state
        },
        tooltip: {},
        legend: {
            data: ["Effective Rent"]
        },
        xAxis: {
            data: data.xdata,
            name: "Year-Quarter"
        },
        yAxis: {},
        series: [{
            name: "Effective Rent",
            type: 'line',
            data: data.ydata,
            itemStyle: {
                normal: {
                    color: '#81BF3F'
                }
            },
        }]
    };

    myChart.setOption(option);
}

function join(addr) {
    $.ajax({
        url: '/join?address='
            + addr,
        dataType: 'json',
        success: joinHandler
    });

}

let clickselected = null;
map.on('singleclick', function (e) {
    if (clickselected !== null) {
        myChart.setOption({});
        clickselected = null;
    }
    map.forEachFeatureAtPixel(e.pixel, function (f) {
        if (f.get('Address') == undefined) return false;
        clickselected = f;
        join(f.get('Address'))
        return false;
    });
});