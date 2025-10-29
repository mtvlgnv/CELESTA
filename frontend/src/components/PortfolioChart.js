import React, { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';
import '../styles/PortfolioChart.css';

function PortfolioChart({ data, title = "Portfolio Value" }) {
  const [chartOptions, setChartOptions] = useState({
    chart: {
      type: 'area',
      height: 400,
      background: 'transparent',
      toolbar: {
        show: true,
        tools: {
          download: true,
          selection: false,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: false,
        },
      },
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 800,
      },
    },
    theme: {
      mode: 'dark',
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth',
      width: 3,
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.2,
        stops: [0, 90, 100],
      },
    },
    xaxis: {
      type: 'datetime',
      labels: {
        style: {
          colors: '#8e8e93',
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: '#8e8e93',
        },
        formatter: (value) => `$${value.toFixed(2)}`,
      },
    },
    grid: {
      borderColor: '#2c2c2e',
      strokeDashArray: 4,
    },
    tooltip: {
      theme: 'dark',
      x: {
        format: 'dd MMM yyyy HH:mm',
      },
      y: {
        formatter: (value) => `$${value.toFixed(2)}`,
      },
    },
    colors: ['#0a84ff'],
  });

  const [series, setSeries] = useState([
    {
      name: title,
      data: [],
    },
  ]);

  useEffect(() => {
    if (data && data.length > 0) {
      const formattedData = data.map((point) => ({
        x: new Date(point.timestamp).getTime(),
        y: point.value || point.total_value || point.close || 0,
      }));

      setSeries([
        {
          name: title,
          data: formattedData,
        },
      ]);
    }
  }, [data, title]);

  return (
    <div className="portfolio-chart">
      <h3 className="chart-title">{title}</h3>
      <Chart options={chartOptions} series={series} type="area" height={400} />
    </div>
  );
}

export default PortfolioChart;

