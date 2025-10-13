(function ($) {
  
    var tfLineChart = (function () {
  
      var chartBar = function () {
      
        var options = {
            series: [
              {
                data: [20, 50, 27, 100, 30, 80, 100],
              },
            ],
            colors: ["#161326"],
            chart: {
              type: "area",
              maxWidth: 96,
              height: 28,
              sparkline: { enabled: !0 },
            },
            plotOptions: { bar: { columnWidth: "50%" } },
            xaxis: { crosshairs: { width: 1 } },
  
            stroke: {
              show: true,
              curve: "smooth",
              lineCap: "butt",
              colors: undefined,
              width: 3,
              dashArray: 0,
            },
  
            // tooltip: {
            //     enabled: false,
            // },
            states: {
              hover: {
                filter: {
                  type: "none",
                  value: 0,
                },
              },
            },
        },

        chart = new ApexCharts(
          document.querySelector("#small-chart-6"),
          options
        );
        if ($("#small-chart-6").length > 0) {
          chart.render();
        }
      };
  
      /* Function ============ */
      return {
        init: function () {},
  
        load: function () {
          chartBar();
        },
        resize: function () {},
      };
    })();
  
    jQuery(document).ready(function () {});
  
    jQuery(window).on("load", function () {
      tfLineChart.load();
    });
  
    jQuery(window).on("resize", function () {});
})(jQuery);