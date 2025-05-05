function fetchAndRender(chartId, selectorId, chartDivId) {
    const dataType = document.getElementById(selectorId).value;
    fetch(`/api/line_data?chart_id=${chartId}&data_type=${dataType}`)
        .then(res => res.json())
        .then(data => {
            const chart = echarts.init(document.getElementById(chartDivId));
            const option = {
                title: {
                    text: `图表${chartId} - 类型${data.data_type}`,
                    left: 'center'
                },
                tooltip: { trigger: 'axis' },
                xAxis: { type: 'category', data: data.x },
                yAxis: { type: 'value' },
                series: [{
                    data: data.y,
                    type: 'line',
                    smooth: true
                }]
            };
            chart.setOption(option);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // 初始化两个图表
    fetchAndRender(1, 'selector1', 'chart1');
    fetchAndRender(2, 'selector2', 'chart2');

    document.getElementById('selector1').addEventListener('change', function() {
        fetchAndRender(1, 'selector1', 'chart1');
    });
    document.getElementById('selector2').addEventListener('change', function() {
        fetchAndRender(2, 'selector2', 'chart2');
    });
}); 