// 将url返回的html挂到domId下
function loadContent(url, domId="main", data={}) {
    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        success: function (data) {
            $('#' + domId).html(data);
        },
        error:function (jqXHR, textStatus, errorThrown) {
            $('#' + domId).html(jqXHR.responseText);
        },
    });    
}

function loadContentV2(url, domId="main", data={}) {
    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        success: function (response) {
            $('#' + domId).html(response.data.html);
        },
        error:function (jqXHR, textStatus, errorThrown) {
            $('#' + domId).html(jqXHR.responseText);
        },
    });    
}

// ===============画图函数==================

/**
 * 公司收入曲线，双坐标轴，左边：金额   右边:同比
 * @param {*} domId : htm中的id,曲线图将被绑定到该id下
 * @param {*} data ： 绘图相关数据
 */
function plotIncomeMixLineBar(domId, data){
    // 解析参数
    var xLabels = data.xLabels;  // x轴标签序列
    var valueName = data.name;
    var values = data.values;
    // 计算同比
    var rateName = "同比";
    var rates = data.rates;
    if (typeof(rates) == "undefined") {
        var size = values.length;
        var rates = new Array(size);
        rates[0] = null;
        for (var i=1; i < size; i++) {
            rates[i] = 100 * (values[i] - values[i-1]) / values[i-1];
        }
    }

    var legendData = [valueName, rateName];

    // 构造echarts的option
    var myChart = echarts.init(document.getElementById(domId));
    var option = {
        tooltip: {
            trigger: 'axis',
        },
        legend: {
            data: legendData
        },
        xAxis: [
            {
                type: 'category',
                data: xLabels,
                axisPointer: {
                    type: 'shadow'
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '金额(元)',
                axisLabel: {
                    formatter: '{value}'
                }
            },
            {
                type: 'value',
                name: '百分比',
                splitLine: {
                    show: false,
                },
                axisLabel: {
                    formatter: '{value}%'
                }
            }
        ],
        series: [
            {
                name: valueName,
                type: 'bar',
                data: values
            },
            {
                name: rateName,
                type: 'line',
                yAxisIndex: 1,
                data: rates
            }
        ]
    };
    myChart.setOption(option);
}

/**
 * 绘制曲线图
 * @param {*} domId : htm中的id,曲线图将被绑定到该id下
 * @param {*} xTicks
 * @param {*} yLabel
 * @param {*} seriesData
 */
function plotLines(domId, xTicks, yLabel, seriesData) {
    var legends = seriesData.map(function(v, i, arr){return v.name});
    
    var seriesData2 = seriesData.map(function(v, i, arr){
        return {"name": v.name, "data": v.data, "type": "line", smooth:true};
    })

    option = {
        tooltip: {
            trigger: 'axis',
            // trigger: 'item', 
            // axisPointer: {
            //     type: 'cross',
            //     crossStyle: {
            //         color: '#999'
            //     }
            // }
        },
        grid : {
            top: '20%',
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                // restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data: legends
        },
        xAxis: [
            {
                type: 'category',
                data: xTicks,
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: yLabel,
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: seriesData2
    };
    var myChart = echarts.init(document.getElementById(domId));
    myChart.setOption(option);
}


//==================读取url返回数据并绘图===========================

function getDataAndPlotLines(data_url, domId){
    $.ajax({
        type: 'GET',
        url: data_url,
        data: JSON.stringify({}),
        contentType: 'application/json;charset=UTF-8',
        success: function (response) {
            var data = response.data.echarts_lines;
            var yLabel = data.y_label;
            var xTicks = data.x_ticks;
            var values = data.values;

            var series = new Array();
            for (key in values){
                series.push({"name":key, "data": values[key]})
            };

            plotLines(domId, xTicks, yLabel, series);
        }
    });
}

function getDataAndPlotBar(url, domId) {
    $.getJSON(url, function (response) {
        plotIncomeMixLineBar(domId, response.data["echarts_bar"]);
    })
}

// 验证
function validate_required(value,alerttxt="输入为空"){
    if (value==null||value==""){
        alert(alerttxt);
        return false;
    }
    else {
        return true;
    }
}
