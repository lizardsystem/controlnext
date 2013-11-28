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

    // Add from history to now;
    for (var dt = moment(hist); dt.isBefore(now); dt.add({minutes: 15})) {
        fillData.push({
            arg: moment(dt).toDate(),
            y1: null,
            y2: null,
            y3: null,
            y4: 50
        });
    }

    // Add from now to future;
    var i = 0;
    for (var dt = moment(now); dt.isBefore(future); dt.add({minutes: 15})) {
        var y = Math.sin(i / 10) * 40 + 50;
        fillData.push({
            arg: moment(dt).toDate(),
            y1: y - 10,
            y2: y,
            y3: y + 10,
            y4: null
        });
        //if (i%5 == 0) {
        //    predictFillSplineData.push({
        //        arg: moment(dt).toDate(),
        //        y2: y,
        //    });
        //}
        i++;
    }

    var amountOfPoints = fillData.length;

    var argmin = moment(hist);
    var argmax = moment(future);
    var viewmin = moment(now).subtract({hours: 12});
    var viewmax = moment(now).add({hours: 48});
    var outflowmin = moment(now).add({minutes: 90});
    var outflowmax = moment(now).add({minutes: 120});

    // Build virtual demand data.
    var demandData = [];
    var demandDataLargeBlocks = [];
    for (var i=0, n=amountOfPoints; i<n; i+=2) {
        var rnd = Math.random();
        var arg = fillData[i].arg;
        demandData.push({arg: arg, y: rnd*10});
        if (i%20 == 0) {
            demandDataLargeBlocks.push({
                arg: arg,
                y: Math.random() * 30 + 20,
            });
        }
    }

    // Build virtual rain data.
    var precipitationData = [];
    var precipitationDataLargeBlocks = [];
    for (var i=0, n=amountOfPoints; i<n; i+=2) {
        var rnd = Math.random();
        var arg = fillData[i].arg;
        precipitationData.push({arg: arg, min: rnd*10, mean: rnd*30, max: rnd*35});
        if (arg >= now && i%20 == 0) {
            precipitationDataLargeBlocks.push({
                arg: arg,
                y: Math.random() * 60 + 60,
            });
        }
    }

    /* ************************************************************************ */
    /* ****************************** Main init ******************************* */
    /* ************************************************************************ */
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
            //advisedFill: ko.observable(60),             // number
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
                name: '',
                type: 'stepArea',
                //pane: 'defaultPane',
                data: demandDataLargeBlocks,
                color: '#ff0000',
                opacity: 0.1,
                label: {
                    visible: false
                },
            },
            {
                valueField: 'y',
                type: 'stepline',
                color: 'black',
                point: {
                    visible: false
                },
                data: demandData
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
                        font: { size: 14, color: 'rgb(51, 51, 51)', opacity: 1 }
                    },
                    min: 0,
                    max: 100,
                    minValueMargin: 0,
                    maxValueMargin: 0,
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
                valueMarginsEnabled: false,
                visible: false,
                label: {
                    visible: false
                },
                strips: [
                    {startValue: dashboardViewModel.dataTimespan().start.toDate(), endValue: dashboardViewModel.currentDate().toDate(), color: 'rgba(204, 204, 204, 0.2)', label: { text: 'gemeten', horizontalAlignment: 'right', verticalAlignment: 'top' }},
                    {startValue: dashboardViewModel.currentDate().toDate(), endValue: dashboardViewModel.dataTimespan().end.toDate(), color: 'white', label: { text: 'voorspeld', horizontalAlignment: 'left', verticalAlignment: 'top' }},
                ]
            },
            incidentOccured: function(message) {
                console.log(message);
            }
        };
        $("#demand-chart").dxChart(demandChartOptions);
        var demandChart = $("#demand-chart").dxChart('instance');

        /* ************************************************************************ */
        /* ************************** Precipitation Chart ************************* */
        /* ************************************************************************ */
        var precipitationChartSeries = [
            {
                valueField: 'y',
                name: '',
                type: 'stepArea',
                //pane: 'defaultPane',
                data: precipitationDataLargeBlocks,
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
                data: precipitationData,
                color: '#a3b6e0',
                opacity: 1
            },
            {
                valueField: 'mean',
                name: 'mean',
                type: 'stackedBar',
                //pane: 'defaultPane',
                data: precipitationData,
                color: '#4777c1',
                opacity: 1
            },
            {
                valueField: 'max',
                name: 'max',
                type: 'stackedBar',
                //pane: 'defaultPane',
                data: precipitationData,
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
                        font: { size: 14, color: 'rgb(51, 51, 51)', opacity: 1 }
                    },
                    //pane: 'defaultPane',
                    axisDivisionFactor: 30,
                    min: 0,
                    max: 140,
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
                min: dashboardViewModel.viewTimespan().start.toDate(),
                max: dashboardViewModel.viewTimespan().end.toDate(),
                //title: 'Tijd',
                label: {
                    visible: false,
                    format: 'H:mm\nd'
                },
                strips: [
                    {startValue: dashboardViewModel.dataTimespan().start.toDate(), endValue: dashboardViewModel.currentDate().toDate(), color: 'rgba(204, 204, 204, 0.2)'},
                    {startValue: dashboardViewModel.currentDate().toDate(), endValue: dashboardViewModel.dataTimespan().end.toDate(), color: 'white'},
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
        var precipitationChart = $("#precipitation-chart").dxChart('instance');

        /* ************************************************************************ */
        /* ******************************* Fill Chart ***************************** */
        /* ************************************************************************ */
        var fillChartSeries = [
            {
                //valueField: 'y2',
                name: 'y one and three',
                //pane: 'defaultPane',
                type: 'rangeArea',
                rangeValue1Field: 'y1',
                rangeValue2Field: 'y3',
                data: fillData,
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
                data: fillData
            },
            {
                name: 'gemeten',
                type: 'spline',
                valueField: 'y4',
                data: fillData,
                color: 'blue',
                opacity: 0.2,
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
                argumentField: 'arg'
            },
            valueAxis: [
                {
                    title: {
                        text: 'Vullingsgraad (%)',
                        font: { size: 14, color: 'rgb(51, 51, 51)', opacity: 1 }
                    },
                    //pane: 'defaultPane',
                    min: 0,
                    max: 120,
                    valueMarginsEnabled: false,
                    strips: [
                        {startValue: 100, endValue: 120, color: 'rgba(232, 10, 10, 0.05)', label: { text: 'max berging', horizontalAlignment: 'right' }},
                        {startValue: 20, endValue:0, color: 'rgba(232, 10, 10, 0.05)', label: { text: 'min berging', horizontalAlignment: 'right' }}
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
                min: dashboardViewModel.viewTimespan().start.toDate(),
                max: dashboardViewModel.viewTimespan().end.toDate(),
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
                    {startValue: dashboardViewModel.dataTimespan().start.toDate(), endValue: dashboardViewModel.currentDate().toDate(), color: 'rgba(204, 204, 204, 0.2)'},
                    {startValue: dashboardViewModel.currentDate().toDate(), endValue: dashboardViewModel.dataTimespan().end.toDate(), color: 'white'},
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

        /* ************************************************************************ */
        /* ***************************** Outflow selector ************************* */
        /* ************************************************************************ */
        $("#outflow-timespan-selector").dxRangeSelector({
            background: { color: 'red' },
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
                color: '#8be'
            },
            shutter: {
                color: '#8be',
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
        $("#fill-gauge").dxLinearGauge({
            //debugMode: true,
            animationEnabled: false,
            geometry: {
                orientation: 'vertical'
            },
            //commonNeedleSettings: {
            //    //indentFromCenter: 10,
            //    offset: 8
            //},
            //needles: [
            //    { value: dashboardViewModel.actualFill() },
            //    { value: dashboardViewModel.advisedFill() }
            //],
            commonMarkerSettings: {
                horizontalOrientation: 'right',
                offset: 80
            },
            markers: [
                {
                    value: dashboardViewModel.actualFill(),
                    text: {
                        customizeText: function() {
                            return 'actueel'
                        }
                    }
                },
                //{
                //    value: dashboardViewModel.advisedFill(),
                //    text: {
                //        customizeText: function() {
                //            return 'advies'
                //        }
                //    }
                //}
            ],
            scale: {
                startValue: 0,
                endValue: 120,
                //horizontalOrientation: 'left',
                label: {
                    //indentFromTick: -10
                    visible: false
                },
                minorTick: {
                    showCalculatedTicks: false,
                    visible: false
                },
                majorTick: {
                    showCalculatedTicks: true,
                    tickInterval: 10,
                    visible: false
                },
            },
            rangeContainer: {
                //horizontalOrientation: 'right',
                backgroundColor: '#adf',
                width: 80,
                offset: 0,
                ranges: [
                    {
                        startValue: 0,
                        endValue: dashboardViewModel.actualFill(),
                        color: '#8be'
                    }
                ]
            },
            size: {
                width: 160,
                height: 350
            },
            margin: {
                top: 0, left: 0, bottom: 0, right: 0
            },
            title: {
                position: 'bottom-center',
                visible: false,
                //text: 'Vullingsgraad',
                font: {
                    // match to chart control
                    family: "'Segoe UI', 'Helvetica Neue', 'Trebuchet MS', Verdana",
                    color: '#808080',
                    opacity: 0.75,
                    size: 16,
                    weight: 400
                }
            },
            incidentOccured: function(message) {
                console.log(message);
            }
        });
        var fillGauge = $("#fill-gauge").dxLinearGauge('instance');

        // Update needles and markers when the model changes.
        dashboardViewModel.actualFill.subscribe(function(newValue) {
            fillGauge.option('rangeContainer.ranges[0].endValue', newValue);
            fillGauge.markerValue(0, newValue);
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

        // Debug.
        window.dashboardViewModel = dashboardViewModel;
        window.precipitationChart = precipitationChart;
        window.fillChart = fillChart;
        window.outflowTimespanSelector = outflowTimespanSelector;
        window.fillGauge = fillGauge;
    }

    $(document).ready(init);
} (window.jQuery);
