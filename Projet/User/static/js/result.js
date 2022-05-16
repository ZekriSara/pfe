Chart.defaults.global.legend.display = false;
Chart.defaults.global.defaultFontColor = 'rgba(156,63,74, 1)';

var chartRadarDOM = $('#chartRadar');
var chartRadarData = {
  labels: ["Vitality", "Magic Power", "Dexterity", "Parry", "Skill Power", "Accuracy", "Luck"],
  datasets: [{
    label: "Skill Level",
    backgroundColor: "rgba(156,63,74,.5)",
    borderColor: "rgba(156,63,74,.8)",
    pointBackgroundColor: "rgba(156,63,74,1)",
    pointBorderColor: "#fff",
    pointHoverBackgroundColor: "#fff",
    pointHoverBorderColor: "rgba(156,63,74,1)",
    pointBorderWidth: 2,
    data: [9, 7, 6, 5, 10, 9, 8]
  }]
};
var chartRadarOptions = {
  scale: {
    ticks: {
      beginAtZero: true,
      maxTicksLimit: 6
    },
    pointLabels: {
      fontSize: 12
    },
    gridLines: {
      color: 'rgba(156,63,74,.1)'
    }
  }

};
var chartRadar = new Chart(chartRadarDOM, {
  type: 'radar',
  data: chartRadarData,
  options: chartRadarOptions
});