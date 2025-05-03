// 获取并渲染汇总数据
fetch('http://localhost:8000/api/summary')
  .then(res => res.json())
  .then(data => {
    document.getElementById('summary-bar').innerHTML = `
      <div class="summary-item">总访问量<br><b>${data.total_visits}</b></div>
      <div class="summary-item">总用户数<br><b>${data.total_users}</b></div>
      <div class="summary-item">总生成代码量<br><b>${data.total_code_lines}</b></div>
    `;
  });

// 日均活跃用户数折线图
fetch('http://localhost:8000/api/daily_stats')
  .then(res => res.json())
  .then(data => {
    let chart1 = echarts.init(document.getElementById('daily-users'));
    chart1.setOption({
      title: { text: '日均活跃用户数', left: 'center', top: 10, textStyle: { fontSize: 16 } },
      xAxis: { type: 'category', data: data.dates },
      yAxis: { type: 'value' },
      series: [{ data: data.daily_active_users, type: 'line', smooth: true }]
    });

    let chart2 = echarts.init(document.getElementById('daily-visits'));
    chart2.setOption({
      title: { text: '日均访问量', left: 'center', top: 10, textStyle: { fontSize: 16 } },
      xAxis: { type: 'category', data: data.dates },
      yAxis: { type: 'value' },
      series: [{ data: data.daily_visits, type: 'line', smooth: true }]
    });
  });

// 部门访问量环形图
fetch('http://localhost:8000/api/department_pie')
  .then(res => res.json())
  .then(data => {
    let chart = echarts.init(document.getElementById('dept-pie'));
    chart.setOption({
      title: { text: '各部门访问量占比', left: 'center', top: 10, textStyle: { fontSize: 16 } },
      tooltip: { trigger: 'item' },
      legend: { bottom: 0 },
      series: [{
        name: '访问量',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        label: { show: false },
        emphasis: { label: { show: true, fontSize: 18, fontWeight: 'bold' } },
        data: data.department_names.map((name, i) => ({
          value: data.visit_counts[i],
          name: name,
          itemStyle: { color: data.colors[i] }
        }))
      }]
    });
  });

// Top 10 user表
fetch('http://localhost:8000/api/top_users')
  .then(res => res.json())
  .then(data => {
    let html = `<table><tr><th>排名</th><th>部门</th><th>用户</th><th>用户数</th></tr>`;
    data.forEach(row => {
      html += `<tr><td>${row.rank}</td><td>${row.department}</td><td>${row.user}</td><td>${row.user_count}</td></tr>`;
    });
    html += `</table>`;
    document.getElementById('top-users').innerHTML = html;
  });

// Top 10 访问情况表
fetch('http://localhost:8000/api/top_visits')
  .then(res => res.json())
  .then(data => {
    let html = `<table><tr><th>排名</th><th>部门</th><th>访问数</th></tr>`;
    data.forEach(row => {
      html += `<tr><td>${row.rank}</td><td>${row.department}</td><td>${row.visit_count}</td></tr>`;
    });
    html += `</table>`;
    document.getElementById('top-visits').innerHTML = html;
  });

// 部门详情页的渲染（可根据实际API调整）
if (document.getElementById('dept-daily-users')) {
  // 这里可以根据部门ID等参数请求部门详情API
  fetch('http://localhost:8000/api/daily_stats')
    .then(res => res.json())
    .then(data => {
      let chart1 = echarts.init(document.getElementById('dept-daily-users'));
      chart1.setOption({
        title: { text: '部门日均活跃用户数', left: 'center', top: 10, textStyle: { fontSize: 16 } },
        xAxis: { type: 'category', data: data.dates },
        yAxis: { type: 'value' },
        series: [{ data: data.daily_active_users, type: 'line', smooth: true }]
      });

      let chart2 = echarts.init(document.getElementById('dept-daily-visits'));
      chart2.setOption({
        title: { text: '部门日均访问量', left: 'center', top: 10, textStyle: { fontSize: 16 } },
        xAxis: { type: 'category', data: data.dates },
        yAxis: { type: 'value' },
        series: [{ data: data.daily_visits, type: 'line', smooth: true }]
      });
    });

  fetch('http://localhost:8000/api/department_pie')
    .then(res => res.json())
    .then(data => {
      let chart = echarts.init(document.getElementById('dept-pie'));
      chart.setOption({
        title: { text: '部门访问量占比', left: 'center', top: 10, textStyle: { fontSize: 16 } },
        tooltip: { trigger: 'item' },
        legend: { bottom: 0 },
        series: [{
          name: '访问量',
          type: 'pie',
          radius: ['50%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
          label: { show: false },
          emphasis: { label: { show: true, fontSize: 18, fontWeight: 'bold' } },
          data: data.department_names.map((name, i) => ({
            value: data.visit_counts[i],
            name: name,
            itemStyle: { color: data.colors[i] }
          }))
        }]
      });
    });

  fetch('http://localhost:8000/api/top_users')
    .then(res => res.json())
    .then(data => {
      let html = `<table><tr><th>排名</th><th>部门</th><th>用户</th><th>用户数</th></tr>`;
      data.forEach(row => {
        html += `<tr><td>${row.rank}</td><td>${row.department}</td><td>${row.user}</td><td>${row.user_count}</td></tr>`;
      });
      html += `</table>`;
      document.getElementById('dept-top-users').innerHTML = html;
    });
} 