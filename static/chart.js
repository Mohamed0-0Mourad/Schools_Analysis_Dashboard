let root1, root2;
function fetch_achieve_bar() {
  const  inp = document.getElementById("achieve_drop").value; 
  fetch("/data_most_achieve", {
    method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
                achievement: inp,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
          const parsedData = data.map(item => ({
            ...item,
            value: parseInt(item.value, 10),
            Enrolment: parseInt(item.Enrolment, 10)  
          }));
            console.log(parsedData);
            update_most_achieve(parsedData);
        })
        .catch((error) => {
            console.error("Error:", error);
          });
}
function fetch_dist_map() {
  const  inp = document.getElementById("level_radio").value; 
  fetch("/data_dist_map", {
    method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
                level: inp,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
          const parsedData = data.map(item => ({
            ...item,
            latitude: parseInt(item.latitude, 10),
            longitude: parseInt(item.longitude, 10),
            Enrolment: parseInt(item.Enrolment, 10)  
          }));
            console.log(parsedData);
            update_dist_map(parsedData);
        })
        .catch((error) => {
            console.error("Error:", error);
          });
}

function update_most_achieve(data) {
    // Initialize amCharts
    am5.ready(function() {
        if(root1){
          console.log("Disposing of old chart instance...");
          root1.dispose();
        }
        console.log("Creating a new chart instance...");
        root1 = am5.Root.new("most_achieve");
        root1.setThemes([
          am5themes_Animated.new(root1)
        ]);
        
        var chart = root1.container.children.push(am5xy.XYChart.new(root1, {
          panX: true,
          panY: true,
          wheelY: "zoomY",
          wheelX: "panY",
          pinchZoomY: true
        }));
        
        var cursor = chart.set("cursor", am5xy.XYCursor.new(root1, {}));
        cursor.lineX.set("visible", false);
        
        var yRenderer = am5xy.AxisRendererY.new(root1, { minGridDistance: 30 });
        yRenderer.labels.template.setAll({
          rotation: 0,
          fontSize: 12,
          centerY: am5.p50,
          centerX: am5.p100,
          paddingRight: 5
        });
        
        yRenderer.grid.template.setAll({
          location: 1
        })
        
        var yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root1, {
          maxDeviation: 0.3,
          categoryField: "category",
          renderer: yRenderer,
          tooltip: am5.Tooltip.new(root1, {})
        }));
        
        var xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root1, {
          maxDeviation: 0.3,
          renderer: am5xy.AxisRendererX.new(root1, {
            strokeOpacity: 0.1
          })
        }));
        
        var series = chart.series.push(am5xy.ColumnSeries.new(root1, {
          name: "Series 1",
          xAxis: xAxis,
          yAxis: yAxis,
          valueXField: "value",
          sequencedInterpolation: true,
          categoryYField: "category",
          tooltip: am5.Tooltip.new(root1, {
            labelText: "{valueX}"
          })
        }));
        
        series.columns.template.setAll({ cornerRadiusTL: 0, cornerRadiusTR: 15, strokeOpacity: 50 });
        series.bullets.push(function(root) {
          return am5.Bullet.new(root, {
            locationX: 1,
            locationY: 0.5,
            sprite: am5.Label.new(root, {
              text: "{City}",
              centerX: am5.percent(100),
              centerY: am5.percent(50),
              populateText: true
            })
          });
        });
        series.bullets.push(function(root, series, dataItem) {
          return am5.Bullet.new(root, {
            locationX: 1.3,
            locationY: 0.5,
            sprite: am5.Circle.new(root, {
              radius: dataItem.dataContext.Enrolment / 100 -3,
              fill:series.get('fill'),
              centerX: am5.percent(50),
              centerY: am5.percent(50),
              populateText: true
            })
          });
        });
        
        yAxis.data.setAll(data);
        series.data.setAll(data);
        
        series.appear(1000);
        chart.appear(1000, 100);
        });
}
function update_dist_map(data) {
  // Initialize amCharts
  am5.ready(function() {
      if(root2){
        root2.dispose();
      }
      root2 = am5.Root.new("dist_map");
      root2.setThemes([
        am5themes_Animated.new(root2)
      ]);
      var chart = root2.container.children.push(
        am5map.MapChart.new(root2, {panX: "rotateX"})
      );
      // chart.set("center", [-84.51655, 46.636610000000005]); 
      chart.set("zoomLevel", 2);
      chart.chartContainer.events.on("ready", function () {
        chart.goHome(); 
      });      
      var polygonSeries = chart.series.push(
        am5map.MapPolygonSeries.new(root2, {
          geoJSON: am5geodata_canadaLow
        })
      );
      var pointSeries = chart.series.push(
        am5map.MapPointSeries.new(root2, {
          latitudeField: "latitude",
          longitudeField: "longitude",
          autoScale:true
        })
      );
      
      pointSeries.bullets.push(function(root2, series, dataItem) {
        return am5.Bullet.new(root2, {
          sprite: am5.Circle.new(root2, {
            radius: dataItem.dataContext.Enrolment / 1000 + 2,
            fill:am5.color(0x264653 )
          })
        });
      });
      pointSeries.data.setAll(data);
        
      pointSeries.appear(1000);
      chart.appear(1000, 100);
  })
}

document.addEventListener('DOMContentLoaded', function() {
  fetch_achieve_bar();
  document.getElementById("achieve_drop").addEventListener("change", () => {
    fetch_achieve_bar(); 
  });
  fetch_dist_map();
  document.getElementById("level_radio").addEventListener("change", () => {
    fetch_dist_map(); 
  });
});
