function renderGraph(title){
  data1 = []
  for(var cat in catData){
      dataPoints1 = []
      for(var i=0; i < catData[cat].length; i++){
          dataPoints1.push({x: new Date(catData[cat][i][1].replace(/-/g, "/")), y: catData[cat][i][0]})
      }

      data1.push({
          type: "line",
          name: cat,
          color: catColours[cat][0],
          showInLegend: true,
          axisYIndex: 1,
          dataPoints: dataPoints1
      })
  }

  var chart = new CanvasJS.Chart("chartContainer", {
  title:{
   text: title
  },
  axisY:[{
   title: "Points",
   lineColor: "#c24642",
   tickColor: "#C24642",
   labelFontColor: "#C24642",
   titleFontColor: "#C24642",
   },
  ],
  toolTip: {
   shared: true
  },
  legend: {
   cursor: "pointer",
   itemclick: toggleDataSeries
  },
  data: data1
  });
  chart.render();

  function toggleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
     e.dataSeries.visible = false;
    } else {
     e.dataSeries.visible = true;
    }
    e.chart.render();
  }

}
