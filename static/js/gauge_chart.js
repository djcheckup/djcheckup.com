var opts = {
  angle: -0.15, // The span of the gauge arc
  lineWidth: 0.4, // The line thickness
  radiusScale: 1, // Relative radius
  pointer: {
    length: 0.65, // // Relative to gauge radius
    strokeWidth: 0.066, // The thickness
    color: "#000000", // Fill color
  },
  limitMax: false, // If false, max value increases automatically if value > maxValue
  limitMin: false, // If true, the min value of the gauge will be fixed
  colorStart: "#dc3545", // Colors
  colorStop: "#30B32D", // just experiment with them
  strokeColor: "#ffc107", // to see which ones work best for you
  generateGradient: false,
  highDpiSupport: true, // High resolution support
  staticZones: [
    { strokeStyle: "#dc3545", min: 0, max: 50 }, // Red from 100 to 130
    { strokeStyle: "#ffc107", min: 50, max: 80 }, // Yellow
    { strokeStyle: "#30B32D", min: 80, max: 100 }, // Green
  ],
};
var target = document.getElementById("score"); // your canvas element
var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
gauge.maxValue = 100; // set max gauge value
gauge.setMinValue(0); // Prefer setter over gauge.minValue = 0
gauge.animationSpeed = 20; // set animation speed (32 is default value)
gauge.set(scorePercent); // set actual value
