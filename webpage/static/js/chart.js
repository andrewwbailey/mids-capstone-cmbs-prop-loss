
var myChart = echarts.init(document.getElementById('chart'));
const year = document.querySelector('.search-input');
const quarter = document.querySelector('.search-combobox');


function joinHandler(data) {
    var option = {
      title: {
        text: 'Effective Rent for ' + data.street + ', ' + data.city + ', ' + data.state,
        subtext: 'Data from ' + year.value + '-Q' + quarter.value + ' to 2022',
        textStyle: {
          fontSize: 24
        },
        subtextStyle: {
          fontSize: 18
        }
      },
      tooltip: {},
      legend: {
        data: ["Effective Rent"],
        textStyle: {
          fontSize: 16
        }
      },
      xAxis: {
        data: data.xdata,
        name: "Year-Quarter",
        axisLabel: {
          fontSize: 14
        },
        axisTick: {
          alignWithLabel: true,
          interval: 0,
          inside: true,
          length: 8,
          lineStyle: {
            color: '#999',
            width: 1
          }
        }
      },
      yAxis: {
        name: "Effective Rent (USD)",
        axisLabel: {
          fontSize: 14
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#eee',
            width: 1,
            type: 'solid'
          }
        },
        splitNumber: 5
      },
      grid: {
        backgroundColor: '#fff',
        left: '10%',
        right: '10%',
        top: '20%',
        bottom: '10%'
      },
      series: [{
        name: "Effective Rent",
        type: 'line',
        data: data.ydata,
        itemStyle: {
          normal: {
            color: '#5472ae'
          }
        },
      }]
    };

    myChart.setOption(option);
}

function join(addr) {
    var year_val = year.value;
    var quarter_val = quarter.value;

    $.ajax({
        url: '/join?address=' + addr + '&year=' + year_val + '&quarter=' + quarter_val,
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