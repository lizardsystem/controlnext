!function($) {
    /* ************************************************************************ */
    /* ****************************** Test data ******************************* */
    /* ************************************************************************ */
    var fillData = [];
    //var predictFillSplineData = [];
    var defaultTimeSpan = 96;
    var selectedTimeSpan = defaultTimeSpan;
    
    var nowReal = moment();
    var now = moment(nowReal).startOf('hour');
    var hist = moment(now).subtract({days: 2});
    var future = moment(now).add({days: 2});
    var precipitationChart = null;

    var argmin = moment(hist);
    var argmax = moment(future);
    var viewmin = moment(now).subtract({hours: 672});
    var viewmax = moment(now).add({hours: 672});
    var outflowmin = moment(now).subtract({minutes: 120});
    var outflowmax = moment(now);
    var osmosedatefrom = null;
    var demandmax = null;
    var precipitationmax = null;

    var lineWidth = 4;
    
    var convertCapacity = function(capacityPerHour) {
	capacityPer15min = parseInt(capacityPerHour);
	if (capacityPer15min >= 0) {
	    return (capacityPer15min / 4);
	} else {
	    return 0;
	}
    }

    var loadDemandData = function () {
	var $constants = $('#data-constants');
	var data_url = $constants.attr('data-data-url');
        //var query_params = get_query_params('rain');
	var dt = new Date().getTime();
	var osmosePer15min = convertCapacity(dashboardViewModel.osmoseCapacity());
	var query_params = "graph_type=demand&format=json&"
	    + "desired_fill=0&demand_exaggerate=100&rain_exaggerate=100&"
	    + "reverse_osmosis=" + osmosePer15min + "&"
	    + "rain_flood_surface=" + dashboardViewModel.rainFloodSurface() + "&"
	    + "basin_storage=" + dashboardViewModel.basinMaxStorage();
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                //set_rain_data(response.rain_graph_info.data);
		var data = [];
		var newDemandMax = 0;
		var demandRaw = response.graph_info.data;
		for (var i = 0; i < demandRaw.length; i++){
		    newDemandMax = (newDemandMax < demandRaw[i][1]) ? demandRaw[i][1]: newDemandMax;
		    var arg = new Date(demandRaw[i][0]);
		    data.push({arg: arg, y: demandRaw[i][1]});
		}	
		//demandChart.beginUpdate();
		//demandChart.getSeriesByName("small block").reinitData(data);
		//demandChart._invalidate();
		//demandChart.option("series.1.data", data);
		// add 1 voor visualization
		dashboardViewModel.demandMax(newDemandMax + 1);
		//demandChart.endUpdate();
		dashboardViewModel.viewTimespan({start: viewmin, end: viewmax});
		initDemandChart(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: '
			       + errorThrown + '</p>');
            }
        });
    };

    var loadRainData = function () {
	var $constants = $('#data-constants');
	var data_url = $constants.attr('data-data-url');
        //var query_params = get_query_params('rain');
	var dt = new Date().getTime();
	var osmosePer15min = convertCapacity(dashboardViewModel.osmoseCapacity());
	var query_params = "graph_type=rain&format=json&"
	    + "desired_fill=0&demand_exaggerate=100&rain_exaggerate=100&"
	    + "reverse_osmosis=" + osmosePer15min + "&"
	    + "rain_flood_surface=" + dashboardViewModel.rainFloodSurface() + "&"
	    + "basin_storage=" + dashboardViewModel.basinMaxStorage();
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                //set_rain_data(response.rain_graph_info.data);
		var meanData = [];
		var minData = [];
		var maxData = [];
		var sumData = []
		var mean_rain = response.rain_graph_info.data.mean;
		var sum_rain = response.rain_graph_info.data.sum;
		var kwadrant = response.rain_graph_info.data.kwadrant;
		var newPrecipitaionMax = 0;
		var priv_sum = -999;
		for (var i = 0; i < sum_rain.length; i++){
		    if ((priv_sum != sum_rain[i][1]) || (i == 0) || (i == sum_rain.length -1)) {
			
			var arg = new Date(sum_rain[i][0]);
			var sumPerHour = sum_rain[i][1] * 4;
			newPrecipitaionMax = (newPrecipitaionMax < sumPerHour) ? sumPerHour: newPrecipitaionMax;
			sumData.push({arg: arg, sum: sumPerHour});
		    }
		    priv_sum = sum_rain[i][1];
		}
		for (var i = 0; i < mean_rain.length; i++){
		    var arg = new Date(mean_rain[i][0]);
		    
		    var meanPerHour = mean_rain[i][1] * 4;
		    newPrecipitaionMax = (newPrecipitaionMax < meanPerHour) ? meanPerHour: newPrecipitaionMax;
		    meanData.push({arg: arg, mean: meanPerHour});
		}
		
		//precipitationChart.beginUpdate();
		//precipitationChart.option("series.2.data", meanData); 
		//precipitationChart.option("series.0.data", sumData);
		//precipitationChart.endUpdate();
		dashboardViewModel.precipitationMax(newPrecipitaionMax + 3);
		dashboardViewModel.viewTimespan({start: viewmin, end: viewmax});
		initPrecipitationChart(meanData, sumData);
		if ((kwadrant != null) && (kwadrant.length > 0)) {
		    $('#quadrant-control').quadrant('option', 'activequadrant',
						    parseInt(kwadrant[0][1]));
		}
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: '
			       + errorThrown + '</p>');
            }
        });
    };

    var emptyPrecipitationChart = function() {
	var series = precipitationChart.series;
	precipitationChart.beginUpdate();
	for (var i = 0; i < series.length; i++) {
	    precipitationChart.option("series." + i + ".data", []);
	}
	precipitationChart.endUpdate();
    }

    var emptyDemandChart = function() {
	var series = demandChart.series;
	demandChart.beginUpdate();
	for (var i = 0; i < series.length; i++) {
	    demandChart.option("series." + i + ".data", []);
	}
	demandChart.endUpdate();
    }

    var emptyFillChart = function() {
	var series = fillChart.series;
	fillChart.beginUpdate();
	for (var i = 0; i < series.length; i++) {
	    fillChart.option("series." + i + ".data", []);
	}
	fillChart.endUpdate();
    }

    var loadPredictedData = function() {
	//Vullingsgraad
	var osmoseDateFrom = $(".datepicker").val();
	var $constants = $('#data-constants');
	var data_url = $constants.attr('data-data-url');
        //var query_params = get_query_params('rain');
	var dt = new Date().getTime();
	var osmosePer15min = convertCapacity(dashboardViewModel.osmoseCapacity());
	var outflowPer15min = convertCapacity(dashboardViewModel.outflowCapacity());
	osmosePer15min = parseInt(dashboardViewModel.osmoseCapacity());
	if (osmosePer15min >= 0) {
	    osmosePer15min = osmosePer15min / 4;
	} else {
	    osmosePer15min = 0;
	}

	var query_params = "graph_type=prediction&format=json&"
	    + "desired_fill=0&demand_exaggerate=100&rain_exaggerate=100&"
	    + "reverse_osmosis=" + osmosePer15min + "&"
	    + "outflowOpen=" + dashboardViewModel.outflowOpened().toDate().getTime() + "&"
	    + "outflowClosed=" + dashboardViewModel.outflowClosed().toDate().getTime() + "&"
	    + "outflowCapacity=" + outflowPer15min + "&"
	    + "rain_flood_surface=" + dashboardViewModel.rainFloodSurface() + "&"
	    + "basin_storage=" + dashboardViewModel.basinMaxStorage() + "&"
	    + "osmose_date_till=" + $('.datepicker')[0].value;

	$.ajax({
            url: data_url + '?' + query_params,
	    success: function (response) {
		var predictedData = [];
		var measuredData = [];
		var predictedNoRainData = [];
		var mean_predicted = response.graph_info.data.mean;
		var measured = response.graph_info.data.history;
		var no_rain = response.graph_info.data.no_rain;
		var actualwaterValue = 0;
		for (var i = 0; i < no_rain.length; i++) {
		    var dt = no_rain[i][0];
		    var y5 = Math.round(no_rain[i][1] * 100) / 100;
		    predictedNoRainData.push({ arg: moment(dt).toDate(), y5: y5 });
		}
		for (var i = 0; i < mean_predicted.length; i++) {
		    var dt = mean_predicted[i][0];
		    var y2 = Math.round(mean_predicted[i][1] * 100) / 100;
		    predictedData.push({ arg: moment(dt).toDate(), y2: y2 });
		}
		for (var i = 0; i < measured.length; i++) {
		    var dt = measured[i][0];
		    var y4 = Math.round(measured[i][1] * 100) / 100;
		    actualwaterValue = y4;
		    measuredData.push({ arg: moment(dt).toDate(), y4: y4 });
		}
		fillChart.beginUpdate();
		fillChart.option("series.1.data", predictedData);
		fillChart.option("series.2.data", measuredData);
		fillChart.option("series.3.data", predictedNoRainData);
		fillChart.option("series.4.data", [
		    {arg: moment(new Date()).subtract('hours', 12).toDate(), actueel: actualwaterValue},
		    {arg: moment(new Date()).add('days', 2).toDate(), actueel: actualwaterValue}]);
		
		// convert value to scale actialwater to 120%
		fillChart.endUpdate();
		$('#fill-gauge').actualwater({
		    actualwater: (actualwaterValue * 100 / 120)
		});
		//$('#fill-gauge').actualwater({actualwater: 100});
		dashboardViewModel.viewTimespan({start: viewmin, end: viewmax});
		$('#overflow-24h-value').html(Math.round(response.overflow_24h) + ' m<sup>3</sup>');
                $('#overflow-5d-value').html(Math.round(response.overflow_5d) + ' m<sup>3</sup>');

		setAvailableMM(actualwaterValue);
	    },
	    error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: '
			       + errorThrown + '</p>');
            }
	});
    }

    var setAvailableMM = function(actualwater) {
	/**
	   Calculate mm per m2 may fall on the roof of the glass house to 
	   to reach the threshold of the basin.
	 */
	var availableWaterPr = 100 - actualwater;
	var valueToRainPerMM = 0
	if (availableWaterPr > 0) {
	    var availableValue = (dashboardViewModel.basinMaxStorage() * availableWaterPr / 100);
	    valueToRainPerMM = (availableValue / dashboardViewModel.rainFloodSurface()) * 1000;	    
	}
	$("#label-actual-water").text(parseInt(valueToRainPerMM) + " mm opvang capaciteit");	
    }

    // Initialize a bound Knockout.js model.
    var dashboardViewModel = {
	viewTimespan: ko.observable({start: viewmin, end: viewmax}), // moment.js objects
	dataTimespan: ko.observable({start: argmin, end: argmax}),   // moment.js objects
	currentDate: ko.observable(now),                             // moment.js object
	outflowOpened: ko.observable(outflowmin),   // moment.js object
	outflowClosed: ko.observable(outflowmax),   // moment.js object
	actualFill: ko.observable(40),              // number
	outflowCapacity: ko.observable(outflowcapacity),
	osmoseCapacity: ko.observable(osmosecapacity),
	osmoseTillDate: ko.observable(osmosetilldate),
	rainFloodSurface: ko.observable(rainfloodsurface),
	basinMaxStorage: ko.observable(basinmaxstorage),
	demandMax: ko.observable(demandmax),
	precipitationMax: ko.observable(precipitationmax),
	currentDemand: ko.observable(currentdemand),

	//advisedFill: ko.observable(60),             // number
	reset: function(model, event) {
	    window.location = ".";
	},
	calculate: function(model, event) {
	    var data = {};
	    data['osmose_till_date'] = $('.datepicker')[0].value;
	    setTimeSpan(selectedTimeSpan);
	    $.ajax({
		url: save_basin_data_url,
		type: "POST",
		data: data,
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		error: function (jqXHR, textStatus, errorThrown) {
                    var $error = $('<p>Fout bij het updaten van de demand tabel: '
				   + errorThrown + '</p>');
		}
            });
	    loadGraphs();
	},
	updateDemand: function(model, event) {
	    var $constants = $('#data-constants');
	    var data_url = $constants.attr('data-demand-url');
	    inputs = $('#demandForm :input');
	    data = {};
	    for (var i=0; i < inputs.length; i++){
		data[inputs[i].name] = inputs[i].value;
	    }
	    $('#bewerken').click();
	    emptyAllCharts();
	    
            $.ajax({
		url: data_url,
		type: "POST",
		data: data,
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		success: function (data, response) {
		    inputs = $('#demandForm :input');
		    for (var i=0; i < inputs.length; i++){
			inputs[i].setAttribute("value", data[inputs[i].name]);
			if (inputs[i].name == currentweek){
			    dashboardViewModel.currentDemand(data[inputs[i].name]);
			} 
		    }
		    loadGraphs();
		},
		error: function (jqXHR, textStatus, errorThrown) {
                    var $error = $('<p>Fout bij het updaten van de demand tabel: '
				   + errorThrown + '</p>');
		}
            });
	},
	selectTimespan: function(model, event) {
	    // Change the chart timespan to 48h, 4d, et cetera.
	    var hours = $(event.target).data('timespan');
	    var hoursRelative = Math.round(hours);
	    var start = moment().subtract({hours: hoursRelative});
	    var end = moment().add({hours: hoursRelative});
	    model.viewTimespan({start: start, end: end});
	    selectedTimeSpan = hours;
	    viewmin = moment(now).subtract({hours: hours});
	    viewmax = moment(now).add({hours: hours});
	   
	},
	browseTimespan: function(model, event) {
	    // Browse the chart timespan to the left or right.
	    var direction = $(event.target).data('direction') === 'fwd' ? 'fwd' : 'bwd';
	    var start = model.viewTimespan().start;
	    var end = model.viewTimespan().end;
	    // Browse 33% forwards or backwards.
	    var diff = end.diff(start) / 3.0;
	    if (direction === 'fwd') {
		var newStart = moment(start).add({milliseconds: diff});
		var newEnd = moment(end).add({milliseconds: diff});
	    }
	    else {
		var newStart = moment(start).subtract({milliseconds: diff});
		var newEnd = moment(end).subtract({milliseconds: diff});
	    }
	    model.viewTimespan({start: newStart, end: newEnd});
	}
    };

    /* ************************************************************************ */
    /* ***************************** Demand Chart ***************************** */
    /* ************************************************************************ */
    var initDemandChart = function(data) {
	var demandChartSeries = [
	// {
	//     valueField: 'y',
	//     name: 'large block',
	//     //name: "",
	//     type: 'stepArea',
	//     //pane: 'defaultPane',
	//     data: [],//demandDataLargeBlocks,
	//     color: '#ff0000',
	//     opacity: 0.1,
	//     label: {
	// 	visible: false
	//     },
	// },
	{
	    valueField: 'y',
	    name: 'watervraag',
	    type: 'stepline',
	    color: 'rgba(71, 119, 193, 0.8)', //'rgba(204, 204, 204, 0.2)'
	    width: lineWidth,
	    point: {
		visible: false,
		color: 'rgba(44, 62, 80, 0.4)' //'rgba(204, 204, 204, 0.2)'
	    },
	    data: data, 
	    hoverMode: 'none'
	},
    ];

    var demandChartOptions = {

	animation: { enabled: false },
	commonPaneSettings: {
	    backgroundColor: 'rgb(255, 255, 255)',
	    border: {
		visible: true
	    }
	},
	commonSeriesSettings: {
	    argumentField: 'arg'
	},
	valueAxis: [
	    {
		title: {
		    text: 'Watervraag (l/m&sup2;/etmaal)',
		    font: { size: 14, color: 'rgb(151, 183, 199)', weight: 'bold', opacity: 1 }
		},
		min: 0,
		max: dashboardViewModel.demandMax(),
		//minValueMargin: 0,
		//maxValueMargin: 0,
		label: {
		    font: {
			color: 'rgb(51, 51, 51)',
			opacity: 1
		    }
		}
	    }
	],
	scaleOverride: true,
	//scaleSteps: steps,
	//scaleStepWidth: Math.ceil(max / steps),
	//scaleStartValue: 0
	size: { height: 170 },
	series: demandChartSeries,
	legend: {
	        //customizeText: function() { return "tyest"; },
                visible: true,
                position: 'inside',
                verticalAlignment: 'top',
                horizontalAlignment: 'right',
                paddingLeftRight: 5,
                paddingTopBottom: 5
            },
	adjustOnZoom: false,
	argumentAxis: {
	    valueType: 'datetime',
	    min: dashboardViewModel.viewTimespan().start.toDate(),
	    max: dashboardViewModel.viewTimespan().end.toDate(),
	    //min: moment(dashboardViewModel.viewTimespan().end).subtract("days", 31).toDate(),
	    //max: moment(dashboardViewModel.viewTimespan().end).add("days", 5).toDate(),
	    valueMarginsEnabled: false,
	    visible: false,
	    label: {
		visible: false
	    },
	    strips: [
	    	{startValue: moment(now).subtract({days: 200}),
	    	 endValue: dashboardViewModel.currentDate().toDate(),
	    	 color: 'rgba(204, 204, 204, 0.2)',
	    	 // label: { text: '', 
	    	 // 	  horizontalAlignment: 'right',
	    	 // 	  verticalAlignment: 'top' }},
		 },
	    	{startValue: dashboardViewModel.currentDate().toDate(),
	    	 endValue: dashboardViewModel.dataTimespan().end.toDate(),
	    	 color: 'white'
	    	 // label: { text: '',
	    	 // 	  horizontalAlignment: 'left',
	    	 // 	  verticalAlignment: 'top' }
		},
	    ],
	    tickInterval: {
		hours: 3
	    },
	    setTicksAtUnitBeginning: true,
	    discreteAxisDivisionMode: 'crossLabels',
	},
	incidentOccured: function(message) {
	    console.log(message);
	},
	tooltip: {
                enabled: true,
                paddingLeftRight: 0,
                paddingTopBottom: 0
       }
    };


        $("#demand-chart").dxChart(demandChartOptions);
        self.demandChart = $("#demand-chart").dxChart('instance');
    };

    /* ************************************************************************ */
    /* ****************************** Main init ******************************* */
    /* ************************************************************************ */
    var initPrecipitationChart = function(meanData, sumData) {
	/* ************************************************************************ */
        /* ************************** Precipitation Chart ************************* */
        /* ************************************************************************ */
        var precipitationChartSeries = [
            {
                valueField: 'sum',
                name: 'opgeteld',
                type: 'stepArea',
                //pane: 'defaultPane',
                data: sumData,//precipitationDataLargeBlocks,
                color: 'rgb(70, 180, 255)',
                opacity: 0.07,
                label: {
                    visible: true,
                    format: 'fixedPoint',
                    backgroundColor: 'transparant',
                    font: {
                        color: '#565656',
                    },
                    connector: {
                        visible: false
                    },
                    precision: 0,
                    verticalOffset: -20,
		    //horizontalOffset: 100,
                    alignment: 'center',
                    // customizeText: function() {
                    //     var series = fillChart.getSeriesByName(this.seriesName);
                    //     var point = series.getPointByArg(this.argument);
                    //     return point.tag;
                    // }
                    //verticalOffset: 100
                },
            },
            {
                valueField: 'mean',
                name: 'gemiddeld',
                type: 'bar',
                //pane: 'defaultPane',
                data: meanData, //[],// precipitationData,
                color: '#4777c1',
                opacity: 1
            }
        ];
        var precipitationChartOptions = {
            //animation: { enabled: false },
            commonSeriesSettings: {
                argumentField: 'arg'
            },
            valueAxis: [
                {
                    title: {
                        text: 'Neerslag (mm/uur)',
                        font: { size: 14, color: 'rgb(151, 183, 199)',
				weight: 'bold', opacity: 1 }
                    },
                    //pane: 'defaultPane',
                    axisDivisionFactor: 30,
                    min: 0,
                    max: dashboardViewModel.precipitationMax(), //15.0,
                    minValueMargin: 0,
                    maxValueMargin: 0,
                    valueMarginsEnabled: false,
                    label: {
                        visible: true,
                        alignment: 'right',
                        font: {
                            color: 'rgb(51, 51, 51)',
                            opacity: 1
                        }
                    }
                }
            ],
            size: { height: 170 },
	    width: 1,
            series: precipitationChartSeries,
            legend: {
                visible: true,
                position: 'inside',
                verticalAlignment: 'top',
                horizontalAlignment: 'right',
                paddingLeftRight: 5,
                paddingTopBottom: 5
            },
	    tickInterval: {
		hours: 3
            },
            //adjustOnZoom: false,
            argumentAxis: {
                //indentFromMin: 0.02,
                //indentFromMax: 0.02
                //minValueMargin: 0,
                //maxValueMargin: 0,
                valueType: 'datetime',
                valueMarginsEnabled: false,
		//min: moment(dashboardViewModel.viewTimespan().end).subtract("days", 31).toDate(),
		//max: moment(dashboardViewModel.viewTimespan().end).add("days", 5).toDate(),
                min: dashboardViewModel.viewTimespan().start.toDate(),
                max: dashboardViewModel.viewTimespan().end.toDate(),
                //title: 'Tijd',
                label: {
                    visible: false,
                    format: 'H:mm\nd'
                },
                strips: [
		    {startValue: moment(now).subtract({days: 200}),
		     endValue: dashboardViewModel.currentDate(),
		     color: 'rgba(204, 204, 204, 0.2)'},
                    {startValue: dashboardViewModel.currentDate().toDate(),
		     endValue: dashboardViewModel.viewTimespan().end.toDate(),
		     color: 'white'},
                ]
            },
            commonPaneSettings: {
                backgroundColor: 'rgb(255, 255, 255)',
                border: {
                    visible: true
                }
            },
            incidentOccured: function(message) {
                console.log(message);
            }
        };
	
        $("#precipitation-chart").dxChart(precipitationChartOptions);
	precipitationChart = $("#precipitation-chart").dxChart('instance');
    }

    function init() {
        // Initialize info popups (the 'i' icons).
        $('.info-popup').popover({
            trigger: 'hover',
            container: 'body',
            placement: 'auto left'
        });
        
        ko.applyBindings(dashboardViewModel);
	
        // Update the Chart.js charts timespans when the model changes.
        dashboardViewModel.viewTimespan.subscribe(function(newValue) {
            console.log('viewTimespan changed', newValue);
            var startValue = newValue.start.toDate();
            var endValue = newValue.end.toDate();
            demandChart.zoomArgument(startValue, endValue);
            precipitationChart.zoomArgument(startValue, endValue);
            fillChart.zoomArgument(startValue, endValue);
            outflowTimespanSelector.option({
                scale: {
                    startValue: startValue,
                    endValue: endValue
                }
            });
        });

        // Randomize the vertical fill gauge when outflow changes.
        dashboardViewModel.outflowOpened.subscribe(function(newValue) {
            //dashboardViewModel.advisedFill(Math.random() * 100);
        });

        // Build a series containing labels only.
        var labelData = [{
            arg: dashboardViewModel.currentDate().toDate(),
            tag: 'T0',
            y: 0
        }];
        var labelSeriesItem = {
            showInLegend: false,
            valueField: 'y',
            type: 'line',
            color: 'red',
            label: {
                connector: {
                    visible: false
                },
                visible: true,
                customizeText: function() {
                    var series = fillChart.getSeriesByName(this.seriesName);
                    var point = series.getPointByArg(this.argument);
                    return point.tag;
                }
                //verticalOffset: 100
            },
            point: {
                visible: false
            },
            data: labelData
        };

        /* ************************************************************************ */
        /* ******************************* Fill Chart ***************************** */
        /* ************************************************************************ */
        var fillChartSeries = [
            {
                valueField: 'y2y3',
                name: 'y one and three',
                //pane: 'defaultPane',
                type: 'rangeArea',
                rangeValue1Field: 'y1',
                rangeValue2Field: 'y3',
                data: [],
                opacity: 0.1,
                color: 'blue',
                showInLegend: false
            },
            {
                valueField: 'y2',
                type: 'line',
		width: lineWidth,
                color: 'blue',
                name: 'verwacht',
                //pane: 'defaultPane',
                point: {
                    visible: false,
                    //size: 2
                },
                data: [],
            },
            {
                name: 'gemeten',
                type: 'line',
		width: lineWidth,
                valueField: 'y4',
                data: [],
                color: 'rgb(70, 180, 255)',//D
                opacity: 0.2,
                point: {
                    visible: false
                }
            },
	    {
                name: 'geen regen',
                type: 'line',
		width: lineWidth,
                valueField: 'y5',
                data: [],
                color: 'rgb(178, 144, 200)',//L
                //opacity: 0.2,
                point: {
                    visible: false
                }
            },
            labelSeriesItem
            /*
            {
                valueField: 'y3',
                name: 'y three'
            }
            {
                valueField: 'y',
                type: 'line',
                name: 'min berging',
                color: 'red',
                point: {
                    visible: false
                },
                data: [
                    {arg: argmin.toDate(), y: 0},
                    {arg: argmax.toDate(), y: 0}
                ]
            },
            {
                valueField: 'y',
                type: 'line',
                name: 'max berging',
                color: 'red',
                point: {
                    visible: false
                },
                data: [
                    {arg: argmin.toDate(), y: 100},
                    {arg: argmax.toDate(), y: 100}
                ]
            },
            */
        ];
        var fillChartOptions = {
            animation: { enabled: false },
            commonSeriesSettings: {
                argumentField: 'arg',
            },
            valueAxis: [
                {
                    title: {
                        text: 'Vullingsgraad (%)',
                        font: { size: 14, color: 'rgb(151, 183, 199)', weight:'bold', opacity: 1 }
                    },
                    //pane: 'defaultPane',
                    min: 0,
                    max: 120,
                    valueMarginsEnabled: false,
                    // strips: [
                    //     {startValue: 100,
		    // 	 endValue: 120,
		    // 	 color: 'rgba(232, 10, 10, 0.05)',
		    // 	 label: { text: 'max berging', horizontalAlignment: 'right' }
		    // 	},
                    //     {startValue: 20,
		    // 	 endValue:0,
		    // 	 color: 'rgba(232, 10, 10, 0.05)',
		    // 	 label: { text: 'min berging', horizontalAlignment: 'right' }}
                    // ],
                    label: {
                        font: {
                            color: 'rgb(51, 51, 51)',
                            opacity: 1
                        },
                        verticalAlignment: 'bottom'
                    }
                }
            ],
            size: { height: 400 },
            series: fillChartSeries,
            legend: {
                visible: true,
                position: 'inside',
                verticalAlignment: 'top',
                horizontalAlignment: 'right',
                paddingLeftRight: 5,
                paddingTopBottom: 5
            },
            adjustOnZoom: false,
            argumentAxis: {
                visible: true,
                grid: {
                    visible: false
                },
                //pane: 'defaultPane',
                valueType: 'datetime',
                discreteAxisDivisionMode: 'crossLabels',
                valueMarginsEnabled: false,
                //min: moment(dashboardViewModel.viewTimespan().start).subtract('days', 28).toDate(),
                //max: moment(dashboardViewModel.viewTimespan().end).add('days', 28).toDate(),
		min: dashboardViewModel.viewTimespan().start.toDate(),
                max: dashboardViewModel.viewTimespan().end.toDate(),
		//min: moment(1383228000000.0).toDate(),
		//max: moment(1385906400000.0).toDate(),
                //indentFromMin: 0.02,
                //indentFromMax: 0.02
                //title: 'Tijd',
                label: {
                   format: 'H:mm\nd MMM',
                   alignment: 'right'
		},
                tickInterval: {
                     hours: 3
                 },
                setTicksAtUnitBeginning: true,
                strips: [
                    {startValue: moment(now).subtract({days: 200}),
		     endValue: dashboardViewModel.currentDate().toDate(),
		     color: 'rgba(204, 204, 204, 0.2)'},
                    {startValue: dashboardViewModel.currentDate().toDate(),
		     endValue: dashboardViewModel.dataTimespan().end.toDate(),
		     color: 'white'},
                ]
            },
            commonPaneSettings: {
                backgroundColor: 'rgb(255, 255, 255)',
                border: {
                    visible: true
                }
            },
            //panes: [
            //    {name: 'defaultPane'}
            //],
            tooltip: {
                enabled: true,
                paddingLeftRight: 0,
                paddingTopBottom: 0
            },
            incidentOccured: function(message) {
                console.log(message);
            }
        };
        $("#fill-chart").dxChart(fillChartOptions);
        var fillChart = $("#fill-chart").dxChart('instance');

	initDemandChart([]);

	initPrecipitationChart([], []);

        /* ************************************************************************ */
        /* ***************************** Outflow selector ************************* */
        /* ************************************************************************ */
        $("#outflow-timespan-selector").dxRangeSelector({
            background: { color: '#46b4ff' },
            /*chart: {
                series: {
                    valueField: 'y2',
                    data: data,
                    type: 'line'
                }
            },*/
            margin: {
                top: 0,
                left: 58,
                bottom: 0,
                right: 0
            },
            size: {
                height: 25, //80
            },
            behavior: {
                //snapToTicks: false,
                //callSelectedRangeChanged: "onMoving",
                animationEnabled: false
            },
            scale: {
                startValue: dashboardViewModel.viewTimespan().start.toDate(),
                endValue: dashboardViewModel.viewTimespan().end.toDate(),
                minorTickInterval: { minutes: 15 },
                majorTickInterval: { days: 1 },
                minRange: { minutes: 15 },
                showMinorTicks: false,
                tick: {
                    opacity: 0.3,
                },
                label: {
                    //format: 'H:mm\nd MMM',
                    visible: false
                },
                //placeholderHeight: 40,
                valueType: 'datetime',
                //useTicksAutoArrangement: false,
                setTicksAtUnitBeginning: true,
                marker: {
                    visible: false
                }
            },
            sliderHandle: {
                color: '#f25039',
            },
            shutter: {
                color: '#f25039',
                opacity: 1.0
            },
            sliderMarker: {
                //format: "H:mm d MMM",
                //padding: 2,
                //placeholderSize: {
                //    height: 20,
                //    width: { left: 58, right: 1 }
                //},
                visible: false
            },
            selectedRange: {
                startValue: dashboardViewModel.outflowOpened().toDate(),
                endValue: dashboardViewModel.outflowClosed().toDate()
            },
            selectedRangeChanged: function(e) {
                dashboardViewModel
                    .outflowOpened(moment(e.startValue))
                    .outflowClosed(moment(e.endValue));
            }
        });
        var outflowTimespanSelector = $("#outflow-timespan-selector").dxRangeSelector('instance');

        // Update needles and markers when the model changes.
        dashboardViewModel.actualFill.subscribe(function(newValue) {
            //fillGauge.option('rangeContainer.ranges[0].endValue', newValue);
            //fillGauge.markerValue(0, newValue);
            //fillGauge
            //    .markerValue(0, newValue)
            //    .needleValue(0, newValue);
        });


	var loadGraphs = function() {
	    loadDemandData();
	    loadRainData();
	    loadPredictedData();
	}

	var emptyAllCharts = function() {
	    emptyPrecipitationChart();
	    emptyDemandChart();
	    emptyFillChart();
	}
        // Debug.
        window.dashboardViewModel = dashboardViewModel;
        window.precipitationChart = precipitationChart;
        window.fillChart = fillChart;
	//window.demandChart = demandChart;
        window.outflowTimespanSelector = outflowTimespanSelector;
        //window.fillGauge = fillGauge;
	window.loadGraphs = loadGraphs;
	window.convertCapacity = convertCapacity;
	window.demandmax = demandmax;
	window.initDemandChart = initDemandChart;
	window.emptyAllCharts = emptyAllCharts;
    }

    $('.popover-markup>.trigger').popover({
	html: true,
	title: function () {
            return $(this).parent().find('.head').html();
	},
	content: function () {
            return $(this).parent().find('.content').html();
	}
    });
    var resizeId;
    $(window).resize(function() {
	clearTimeout(resizeId);
	resizeId = setTimeout(doneResizing, 100);
    });

    function doneResizing(){
	window.location = ".";
    }

    function setTimeSpan(hoursRel){
	var hoursRelative = Math.round(hoursRel);
	var start = moment().subtract({hours: hoursRelative});
	var end = moment().add({hours: hoursRelative});
	dashboardViewModel.viewTimespan({start: start, end: end});
	$( "button[data-timespan='" + hoursRel + "']")[0].click()
    }

    $('.datepicker').datepicker(); 

    $(document).ready(function() {
	$("body").tooltip({ selector: '[data-toggle=tooltip]' });
    });
        
    $(document).ready(function(){init(); setTimeSpan(defaultTimeSpan); loadGraphs(); });

} (window.jQuery);
