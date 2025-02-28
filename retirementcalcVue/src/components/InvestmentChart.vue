<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, toRefs } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const props = defineProps({
  currentAge: { type: Number, required: true },
  retirementAge: { type: Number, required: true },
  currentRetirementAccount: { type: Number, required: true },
  monthlyRetirementAccountContribution: { type: Number, required: true },
  currentInvestments: { type: Number, required: true },
  monthlyInvestments: { type: Number, required: true },
  retirementAccountAnnualRate: { type: Number, required: true },
  investmentAnnualRate: { type: Number, required: true },
  inflationRate: { type: Number, required: true },
  compoundingFrequency: { type: Number, required: true },
  currency: { type: String, required: true }
});

const { 
  currentAge, retirementAge, currentRetirementAccount, monthlyRetirementAccountContribution,
  currentInvestments, monthlyInvestments, retirementAccountAnnualRate, investmentAnnualRate,
  inflationRate, compoundingFrequency, currency
} = toRefs(props);

const chartCanvas = ref(null);
let chart = null;

// Calculate future value for a given year
const calculateFutureValue = (P, r, n, t, PMT) => {
  return P * Math.pow(1 + r/n, n*t) + PMT * ((Math.pow(1 + r/n, n*t) - 1) / (r/n));
};

// Generate data for chart
const generateChartData = () => {
  const labels = [];
  const nominalNetWorthData = [];
  const realNetWorthData = [];
  
  const years = retirementAge.value - currentAge.value;
  
  for (let i = 0; i <= years; i++) {
    // Add age label
    labels.push(currentAge.value + i);
    
    // Calculate nominal values
    const retirementValue = calculateFutureValue(
      Number(currentRetirementAccount.value),
      retirementAccountAnnualRate.value,
      compoundingFrequency.value,
      i,
      monthlyRetirementAccountContribution.value
    );
    
    const investmentValue = calculateFutureValue(
      Number(currentInvestments.value),
      investmentAnnualRate.value,
      compoundingFrequency.value,
      i,
      monthlyInvestments.value
    );
    
    // Calculate total nominal net worth
    const nominalNetWorth = retirementValue + investmentValue;
    nominalNetWorthData.push(nominalNetWorth);
    
    // Calculate real (inflation-adjusted) values
    const inflationFactor = Math.pow(1 + inflationRate.value, i);
    const realNetWorth = nominalNetWorth / inflationFactor;
    realNetWorthData.push(realNetWorth);
  }
  
  return {
    labels,
    nominalNetWorthData,
    realNetWorthData
  };
};

// Format currency for tooltips
const formatCurrency = (value) => {
  return `${currency.value}${value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`;
};

// Create or update chart
const createOrUpdateChart = () => {
  const { labels, nominalNetWorthData, realNetWorthData } = generateChartData();
  
  if (chart) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = realNetWorthData;
    chart.data.datasets[1].data = nominalNetWorthData;
    chart.update();
  } else if (chartCanvas.value) {
    chart = new Chart(chartCanvas.value, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: ` Real Net Worth`,
            data: realNetWorthData,
            borderColor: '#4DB6AC',
            backgroundColor: 'rgba(55, 182, 172, .4)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
          },
          {
            label: ` Nominal Net Worth`,
            data: nominalNetWorthData,
            borderColor: '#BDBDBD',
            backgroundColor: 'rgba(189, 189, 189, .0001)',
            borderWidth: .2,
            borderDash: [5, 5],
            fill: false,
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          tooltip: {
            bodyFont: {
              weight: 'bold',
              size: 25,
            },
            titleFont: {
              size: 25,
            },
            callbacks: {
              label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += formatCurrency(context.parsed.y);
                }
                return label;
              },
              title: function(tooltipItems) {
                return `Age: ${tooltipItems[0].label}`;
              }
            }
          },
          legend: {
            labels: {
              usePointStyle: true,
              boxWidth: 6,
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Age'
            }
          },
          y: {
            title: {
              display: true,
              text: `Value (${currency.value})`
            },
            ticks: {
              callback: function(value) {
                if (value >= 1000000) {
                  return currency.value + (value / 1000000).toFixed(1) + 'M';
                } else if (value >= 1000) {
                  return currency.value + (value / 1000).toFixed(0) + 'K';
                }
                return currency.value + value;
              }
            }
          }
        }
      }
    });
  }
};

// Watch for changes in props to update chart
watch(
  [
    currentAge, retirementAge, currentRetirementAccount, monthlyRetirementAccountContribution,
    currentInvestments, monthlyInvestments, retirementAccountAnnualRate, investmentAnnualRate,
    inflationRate, compoundingFrequency, currency
  ],
  () => {
    createOrUpdateChart();
  },
  { deep: true }
);

onMounted(() => {
  createOrUpdateChart();
});
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
  margin-top: 20px;
}
</style>