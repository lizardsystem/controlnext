!function($) {
    /* ************************************************************************ */
    /* ****************************** Test data ******************************* */
    /* ************************************************************************ */
    var fillData = [];
    //var predictFillSplineData = [];

    var nowReal = moment();
    var now = moment(nowReal).startOf('hour');
    var hist = moment(now).subtract({days: 2});
    var future = moment(now).add({days: 2});
    var precipitationChart = null;

    var argmin = moment(hist);
    var argmax = moment(future);
    var viewmin = moment(now).subtract({hours: 12});
    var viewmax = moment(now).add({hours: 48});
    var outflowmin = moment(now).add({minutes: 90});
    var outflowmax = moment(now).add({minutes: 120});
    var outflowcapacity = 0;
    var osmosecapacity = 0;

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
	    + "date=" + dt + "&reverse_osmosis=" + osmosePer15min;
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                //set_rain_data(response.rain_graph_info.data);
		var data = [];
		var demandRaw = response.graph_info.data;
		for (var i = 0; i < demandRaw.length; i++){
		    var arg = new Date(demandRaw[i][0]);
		    data.push({arg: arg, y: demandRaw[i][1]});
		}	
		demandChart.beginUpdate();
		//demandChart.getSeriesByName("small block").reinitData(data);
		//demandChart._invalidate();
		demandChart.option("series.1.data", data);
		demandChart.endUpdate();
		//dashboardViewModel.viewTimespan({start: viewmin, end: viewmax});
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
	    + "date=" + dt + "&reverse_osmosis=" + osmosePer15min;
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
		//var min_rain = response.rain_graph_info.data.min;
		//var max_rain = response.rain_graph_info.data.max;
		for (var i = 0; i < mean_rain.length; i++){
		    var arg = new Date(mean_rain[i][0]);
		    meanData.push({arg: arg, mean: mean_rain[i][1]});
		}
		var priv_sum = -999;
		for (var i = 0; i < sum_rain.length; i++){
		    if ((priv_sum != sum_rain[i][1]) || (i == 0) || (i == sum_rain.length -1)) {
			var arg = new Date(sum_rain[i][0]);
			sumData.push({arg: arg, y: sum_rain[i][1]});
		    }
		    priv_sum = sum_rain[i][1];
		}
		
		// for (var i = 0; i < min_rain.length; i++){
		//     var arg = new Date(min_rain[i][0]);
		//     minData.push({arg: arg, min: min_rain[i][1]});
		// }
		// for (var i = 0; i < max_rain.length; i++){
		//     var arg = new Date(max_rain[i][0]);
		//     maxData.push({arg: arg, max: max_rain[i][1]});
		// }
		precipitationChart.beginUpdate();;
		//precipitationChart.option("series.3.data", maxData);
		precipitationChart.option("series.2.data", meanData);
		//precipitationChart.option("series.1.data", minData); 
		precipitationChart.option("series.0.data", sumData);
		precipitationChart.endUpdate();
		
		if ((kwadrant != null) && (kwadrant.length > 0)) {
		    $('#quadrant-control').quadrant('option', 'activequadrant', parseInt(kwadrant[0][1]));
		}
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: '
			       + errorThrown + '</p>');
            }
        });
    };

    var loadPredictedData = function() {
	//Vullingsgraad
	var $constants = $('#data-constants');
	var data_url = $constants.attr('data-data-url');
        //var query_params = get_query_params('rain');
	var dt = new Date().getTime();
	var osmosePer15min = convertCapacity(dashboardViewModel.osmoseCapacity());
	var outflowPer15min = convertCapacity(dashboardViewModel.outflowCapacity());
	var capacityPool = parseInt($("#basin-storage").val());
	var rainFloodSurface = parseInt($("#rain_flood_surface").val());
	osmosePer15min = parseInt(dashboardViewModel.osmoseCapacity());
	if (osmosePer15min >= 0) {
	    osmosePer15min = osmosePer15min / 4;
	} else {
	    osmosePer15min = 0;
	}

	var query_params = "graph_type=prediction&format=json&"
	    + "desired_fill=0&demand_exaggerate=100&rain_exaggerate=100&"
	    + "date=" + dt + "&reverse_osmosis=" + osmosePer15min + "&"
	    + "outflowOpen=" + dashboardViewModel.outflowOpened().toDate().getTime() + "&"
	    + "outflowClosed=" + dashboardViewModel.outflowClosed().toDate().getTime() + "&"
	    + "outflowCapacity=" + outflowPer15min;
	if (rainFloodSurface != 'NaN') {
	    query_params += "&rain_flood_surface=" + rainFloodSurface;
	}
	if (capacityPool != 'NaN'){
	    query_params += "&basin_storage=" + capacityPool;
	}
	$.ajax({
            url: data_url + '?' + query_params,
	    success: function (response) {
		//var minMaxData = [];
		var predictedData = [];
		var measuredData = [];
		var predictedNoRainData = [];
		//var min_predicted = response.graph_info.data.min;
		//var max_predicted = response.graph_info.data.max;
		var mean_predicted = response.graph_info.data.mean;
		var measured = response.graph_info.data.history;
		var no_rain = response.graph_info.data.no_rain;
		var actualwaterValue = 0;
		//var maxAmountOfMinMax = Math.max(
		//min_predicted.length,
		//    max_predicted.length
		//);
		// for (var i = 0; i < maxAmountOfMinMax; i++) {
		//     var y1 = null;
		//     var y3 = null;
		//     var dt = null;
		//     if (min_predicted.length > i) {
		// 	dt = min_predicted[i][0];
		// 	y1 = min_predicted[i][1];
		//     }
		//     if (max_predicted.length > i) {
		// 	dt = max_predicted[i][0];
		// 	y3 = max_predicted[i][1];
		//     }
		//     minMaxData.push({ arg: moment(dt).toDate(), y1: y1, y3: y3 });
		// }
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
		//fillChart.getSeriesByName("y one and three").reinitData(minMaxData);	
		//fillChart.getSeriesByName("gemeten").reinitData(measuredData);
		//fillChart.getSeriesByName("voorspeld").reinitData(predictedData);
		
		//fillChart.option("series.0.data", minMaxData);
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
		//dashboardViewModel.viewTimespan({start: viewmin, end: viewmax});
		$('#overflow-24h-value').html(Math.round(response.overflow_24h) + ' m<sup>3</sup>');
                $('#overflow-5d-value').html(Math.round(response.overflow_5d) + ' m<sup>3</sup>');
	    },
	    error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: '
			       + errorThrown + '</p>');
            }
	});
    }

    var setAvailableMM = function(actualwater) {
	var availableWaterPr = actualwater;
	var capacityPool = parseInt($("#basin-storage").text());
	var rainFloodSurface = parseInt($("#rain_flood_surface").text());
	if (rainFloodSurface != 'NaN') {
	   rainFloodSurface = parseInt($("#rain_flood_surface").val()); 
	}
	if (capacityPool != 'NaN'){
	    capacityPool = parseInt($("#basin-storage").val());;
	}
	var valueToRainPerMM = 0
	if (availableWaterPr > 0) {
	    var availableValue = (capacityPool * availableWaterPr / 100);
	    valueToRainPerMM = (availableValue / rainFloodSurface) * 1000;	    
	}
	$("#label-actual-water").text(parseInt(valueToRainPerMM) + " mm beschikbaar");	
    }

    // for (var i=0, n=amountOfPoints; i<n; i+=2) {
    //     var rnd = Math.random();
    //     var arg = fillData[i].arg;
    //     precipitationData.push({arg: arg, min: rnd*10, mean: rnd*30, max: rnd*35});
    //     if (arg >= now && i%20 == 0) {
    //         precipitationDataLargeBlocks.push({
    //             arg: arg,
    //             y: Math.random() * 60 + 60,
    //         });
    //     }
    // }

    /* ************************************************************************ */
    /* ****************************** Main init ******************************* */
    /* ************************************************************************ */
    var initPrecipitationChart = function(data, beginDate, endDate, currentDate) {
	/* ************************************************************************ */
        /* ************************** Precipitation Chart ************************* */
        /* ************************************************************************ */
        var precipitationChartSeries = [
            {
                valueField: 'y',
                name: 'y',
                type: 'stepArea',
                //pane: 'defaultPane',
                //data: precipitationDataLargeBlocks,
                color: '#2222ee',
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
                    alignment: 'center',
                    //customizeText: function() {
                        //var series = fillChart.getSeriesByName(this.seriesName);
                        //var point = series.getPointByArg(this.argument);
                        //return point.tag;
                    //}
                    //verticalOffset: 100
                },
            },
            {
                valueField: 'min',
                name: 'min',
                type: 'stackedBar',
                //pane: 'defaultPane',
                //data: precipitationData,
                color: '#a3b6e0',
                opacity: 1
            },
            {
                valueField: 'mean',
                name: 'mean',
                type: 'bar',
                //pane: 'defaultPane',
                data: [],// precipitationData,
                color: '#4777c1',
                opacity: 1
            },
            {
                valueField: 'max',
                name: 'max',
                type: 'stackedBar',
                //pane: 'defaultPane',
                //data: precipitationData,
		data: [],//data,
                color: '#a3b6e0',
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
                        font: { size: 14, color: 'rgb(151, 183, 199)', weight: 'bold', opacity: 1 }
                    },
                    //pane: 'defaultPane',
                    axisDivisionFactor: 30,
                    min: 0,
                    max: 15.0,
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
                visible: false,
                position: 'inside',
                verticalAlignment: 'top',
                horizontalAlignment: 'right',
                paddingLeftRight: 5,
                paddingTopBottom: 5
            },
            adjustOnZoom: false,
            argumentAxis: {
                //indentFromMin: 0.02,
                //indentFromMax: 0.02
                //minValueMargin: 0,
                //maxValueMargin: 0,
                valueType: 'datetime',
                valueMarginsEnabled: false,
		//min: moment(dashboardViewModel.viewTimespan().end).subtract("days", 31).toDate(),
		//max: moment(dashboardViewModel.viewTimespan().end).add("days", 5).toDate(),
                min: beginDate,//dashboardViewModel.viewTimespan().start.toDate(),
                max: endDate, //dashboardViewModel.viewTimespan().end.toDate(),
                //title: 'Tijd',
                label: {
                    visible: false,
                    format: 'H:mm\nd'
                },
                strips: [
                    // {startValue: dashboardViewModel.dataTimespan().start.toDate(), endValue: dashboardViewModel.currentDate().toDate(), color: 'rgba(204, 204, 204, 0.2)'},
                    // {startValue: dashboardViewModel.currentDate().toDate(), endValue: dashboardViewModel.dataTimespan().end.toDate(), color: 'white'},
		    {startValue: beginDate, endValue: currentDate,
		     color: 'rgba(204, 204, 204, 0.2)'},
                    {startValue: currentDate, endValue: endDate,
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
            //advisedFill: ko.observable(60),             // number
	    reset: function(model, event) {
            window.location = ".";
	    },
	    calculate: function(model, event) {
		loadGraphs();
	    },
            selectTimespan: function(model, event) {
                // Change the chart timespan to 48h, 4d, et cetera.
                var hours = $(event.target).data('timespan');
                var hoursRelative = Math.round(hours / 2);
                var start = moment().subtract({hours: hoursRelative});
                var end = moment().add({hours: hoursRelative});
                model.viewTimespan({start: start, end: end});
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
        /* ***************************** Demand Chart ***************************** */
        /* ************************************************************************ */
        var demandChartSeries = [
            {
                valueField: 'y',
                name: 'large block',
		//name: "",
                type: 'stepArea',
                //pane: 'defaultPane',
                data: [],//demandDataLargeBlocks,
                color: '#ff0000',
                opacity: 0.1,
                label: {
                    visible: false
                },
            },
            {
                valueField: 'y',
		name: 'small block',
                type: 'stepline',
                color: 'black',
                point: {
                    visible: false
                },
                data: [],//demandData
            }
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
                        text: 'Watervraag (m&sup3;/15m)',
                        font: { size: 14, color: 'rgb(151, 183, 199)', weight: 'bold', opacity: 1 }
                    },
                    min: 0,
                    max: 1,
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
            size: { height: 170 },
            series: demandChartSeries,
            legend: {
                visible: false
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
                    {startValue: dashboardViewModel.dataTimespan().start.toDate(),
		     endValue: dashboardViewModel.currentDate().toDate(),
		     color: 'rgba(204, 204, 204, 0.2)',
		     label: { text: 'gemeten', 
			      horizontalAlignment: 'right',
			      verticalAlignment: 'top' }},
                    {startValue: dashboardViewModel.currentDate().toDate(),
		     endValue: dashboardViewModel.dataTimespan().end.toDate(),
		     color: 'white',
		     label: { text: 'voorspeld',
			      horizontalAlignment: 'left',
			      verticalAlignment: 'top' }},
                ],
		tickInterval: {
                     hours: 3
                 },
                setTicksAtUnitBeginning: true,
		discreteAxisDivisionMode: 'crossLabels',
            },
            incidentOccured: function(message) {
                console.log(message);
            }
        };
        $("#demand-chart").dxChart(demandChartOptions);
        var demandChart = $("#demand-chart").dxChart('instance');

        

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
                color: 'blue',
                name: 'voorspeld',
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
                valueField: 'y5',
                data: [],
                color: 'rgb(178, 144, 200)',//L
                //opacity: 0.2,
                point: {
                    visible: false
                }
            },
	    {
                valueField: 'actueel',
                type: 'line',
		dashStyle: 'dash',
                color: '#46b4ff',
                name: 'actueel',
                point: {
                    visible: false,
                },
                data: [],
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
                    strips: [
                        {startValue: 100,
			 endValue: 120,
			 color: 'rgba(232, 10, 10, 0.05)',
			 //label: { text: 'max berging', horizontalAlignment: 'right' }
			}
                        // {startValue: 20,
			//  endValue:0,
			//  color: 'rgba(232, 10, 10, 0.05)',
			//  label: { text: 'min berging', horizontalAlignment: 'right' }}
                    ],
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
                visible: false,
                position: 'inside',
                verticalAlignment: 'top',
                horizontalAlignment: 'right',
                paddingLeftRight: 5,
                paddingTopBottom: 5
            },
            //adjustOnZoom: false,
            argumentAxis: {
                visible: true,
                grid: {
                    visible: false
                },
                //pane: 'defaultPane',
                valueType: 'datetime',
                discreteAxisDivisionMode: 'crossLabels',
                valueMarginsEnabled: false,
                //min: moment(dashboardViewModel.viewTimespan().start).subtract('days', 31).toDate(),
                //max: moment(dashboardViewModel.viewTimespan().end).add('days', 5).toDate(),
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
                    {startValue: dashboardViewModel.dataTimespan().start.toDate(),
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

	initPrecipitationChart([],
			       dashboardViewModel.viewTimespan().start.toDate(),
			       dashboardViewModel.viewTimespan().end.toDate(),
			       dashboardViewModel.currentDate().toDate());

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
                height: 25 //80
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

        /* ************************************************************************ */
        /* **************************** Vertical fill gauge *********************** */
        /* ************************************************************************ */
        // $("#fill-gauge").dxLinearGauge({
        //     //debugMode: true,
        //     animationEnabled: false,
        //     geometry: {
        //         orientation: 'vertical'
        //     },
        //     //commonNeedleSettings: {
        //     //    //indentFromCenter: 10,
        //     //    offset: 8
        //     //},
        //     //needles: [
        //     //    { value: dashboardViewModel.actualFill() },
        //     //    { value: dashboardViewModel.advisedFill() }
        //     //],
        //     commonMarkerSettings: {
        //         horizontalOrientation: 'right',
        //         offset: 80
        //     },
        //     markers: [
        //         {
        //             value: dashboardViewModel.actualFill(),
        //             text: {
        //                 customizeText: function() {
        //                     return 'actueel'
        //                 }
        //             }
        //         },
        //         //{
        //         //    value: dashboardViewModel.advisedFill(),
        //         //    text: {
        //         //        customizeText: function() {
        //         //            return 'advies'
        //         //        }
        //         //    }
        //         //}
        //     ],
        //     scale: {
        //         startValue: 0,
        //         endValue: 120,
        //         //horizontalOrientation: 'left',
        //         label: {
        //             //indentFromTick: -10
        //             visible: false
        //         },
        //         minorTick: {
        //             showCalculatedTicks: false,
        //             visible: false
        //         },
        //         majorTick: {
        //             showCalculatedTicks: true,
        //             tickInterval: 10,
        //             visible: false
        //         },
        //     },
        //     rangeContainer: {
        //         //horizontalOrientation: 'right',
        //         backgroundColor: '#adf',
        //         width: 80,
        //         offset: 0,
        //         ranges: [
        //             {
        //                 startValue: 0,
        //                 endValue: dashboardViewModel.actualFill(),
        //                 color: '#8be'
        //             }
        //         ]
        //     },
        //     size: {
        //         width: 160,
        //         height: 350
        //     },
        //     margin: {
        //         top: 0, left: 0, bottom: 0, right: 0
        //     },
        //     title: {
        //         position: 'bottom-center',
        //         visible: false,
        //         //text: 'Vullingsgraad',
        //         font: {
        //             // match to chart control
        //             family: "'Segoe UI', 'Helvetica Neue', 'Trebuchet MS', Verdana",
        //             color: '#808080',
        //             opacity: 0.75,
        //             size: 16,
        //             weight: 400
        //         }
        //     },
        //     incidentOccured: function(message) {
        //         console.log(message);
        //     }
        // });
        // var fillGauge = $("#fill-gauge").dxLinearGauge('instance');

        // Update needles and markers when the model changes.
        dashboardViewModel.actualFill.subscribe(function(newValue) {
            //fillGauge.option('rangeContainer.ranges[0].endValue', newValue);
            //fillGauge.markerValue(0, newValue);
            //fillGauge
            //    .markerValue(0, newValue)
            //    .needleValue(0, newValue);
        });
        //dashboardViewModel.advisedFill.subscribe(function(newValue) {
        //    fillGauge
        //        .markerValue(1, newValue)
        //        .needleValue(1, newValue);
        //});

        /*
        $("#timespan-selector").dxRangeSelector({
            background: { color: '#dedede' },
            chart: {
                series: [
                    {
                        valueField: 'y2',
                        data: data,
                        type: 'line',
                        color: 'blue'
                    },
                    {
                        valueField: 'y4',
                        data: data,
                        type: 'line',
                        color: 'yellow'
                    }
                ]
            },
            margin: {
                top: 0,
                left: 0,
                bottom: 0,
                right: 0
            },
            size: {
                height: 90
            },
            behavior: {
                //snapToTicks: false,
                //callSelectedRangeChanged: "onMoving",
                animationEnabled: false
            },
            scale: {
                startValue: argmin.toDate(),
                endValue: argmax.toDate(),
                minorTickInterval: { minutes: 15 },
                majorTickInterval: { days: 1 },
                minRange: { minutes: 15 },
                showMinorTicks: false,
                label: {
                    format: 'd\nMMM'
                },
                placeholderHeight: 40,
                valueType: 'datetime',
                useTicksAutoArrangement: false,
                marker: {
                    visible: false
                }
            },
            sliderMarker: {
                format: 'H:mm',
                padding: 2,
                placeholderSize: {
                    height: 20,
                    width: { left: 40, right: 40 }
                }
            },
            selectedRange: {
                startValue: viewmin.toDate(),
                endValue: viewmax.toDate()
            },
            selectedRangeChanged: function(e) {
                dashboardViewModel.timespan({start: moment(e.startValue), end: moment(e.endValue)});
            }
        });
        var timespanSelector = $("#timespan-selector").dxRangeSelector('instance');
        window.timespanSelector = timespanSelector;
        */

        /*
        function selectTimespan(startValue, endValue) {
            demandChart.zoomArgument(startValue, endValue);
            precipitationChart.zoomArgument(startValue, endValue);
            fillChart.zoomArgument(startValue, endValue);
            outflowTimespanSelector.option({
                scale: {
                    startValue: startValue,
                    endValue: endValue
                }
            });
        }
        */

        /*setInterval(function() {
            fillChart.beginUpdate();
            for (var i=0, n=y2data.length; i<n; i++) {
                y2data[i].y2 += i * 2;
            }
            //dataSource.shift();
            //fillChart.option({series: {0: {data: y2data}}});
            fillChart.getSeriesByName('y two').reinitData(y2data);
            fillChart._invalidate();
            timespanSelector.option({chart: {series: {data: y2data}}});
            fillChart.endUpdate();
            //var selRa = timespanSelector.getSelectedRange();
            //fillChart.zoomArgument(selRa.startValue, selRa.endValue);
        }, 4000000);*/

	var loadGraphs = function() {
	    loadDemandData();
	    loadRainData();
	    loadPredictedData();
	    setAvailableMM();
	}
        // Debug.
        window.dashboardViewModel = dashboardViewModel;
        window.precipitationChart = precipitationChart;
        window.fillChart = fillChart;
	window.demandChart = demandChart;
        window.outflowTimespanSelector = outflowTimespanSelector;
        //window.fillGauge = fillGauge;
	window.loadGraphs = loadGraphs;
	window.convertCapacity = convertCapacity
    }
        
    $(document).ready(function(){init(); loadGraphs()});
} (window.jQuery);