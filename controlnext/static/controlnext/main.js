// extend jQuery a bit
(function ($) {
    $.extend({
        getQueryString: function (name) {
            function parseParams() {
                var params = {},
                    e,
                    a = /\+/g,  // Regex for replacing addition symbol with a space
                    r = /([^&=]+)=?([^&]*)/g,
                    d = function (s) { return decodeURIComponent(s.replace(a, " ")); },
                    q = window.location.search.substring(1);

                while (e = r.exec(q))
                    params[d(e[1])] = d(e[2]);

                return params;
            }

            if (!this.queryStringParams)
                this.queryStringParams = parseParams();

            return this.queryStringParams[name];
        }
    });
})(jQuery);

$(document).ready(function () {
    var MS_SECOND = 1000;
    var MS_MINUTE = 60 * MS_SECOND;
    var MS_HOUR = 60 * MS_MINUTE;
    var MS_DAY = 24 * MS_HOUR;
    var MS_MONTH = 30 * MS_DAY;
    var MS_YEAR = 365 * MS_DAY;

    var tick_size_map = [
        [100 * MS_YEAR,  999 * MS_YEAR,   [50, 'year']],
        [ 10 * MS_YEAR,  100 * MS_YEAR,   [10, 'year']],
        [  1 * MS_YEAR,   10 * MS_YEAR,   [ 1, 'year']],
        [  1 * MS_MONTH,   1 * MS_YEAR,   [ 1, 'month']],
        [  1 * MS_DAY,     1 * MS_MONTH,  [ 1, 'day']],
        [ 12 * MS_HOUR,    1 * MS_DAY,    [ 2, 'hour']],
        [  1 * MS_HOUR,   12 * MS_HOUR,   [ 1, 'hour']],
        [ 15 * MS_MINUTE,  1 * MS_HOUR,   [15, 'minute']],
        [  1 * MS_MINUTE, 15 * MS_MINUTE, [ 1, 'minute']]
    ];

    /**
     * Note: use $.extend() for this.
     */
    var default_flot_options = {
        xaxis: {
            mode: 'time',
            position: 'bottom',
            zoomRange: [1 * MS_HOUR, 10 * MS_DAY],
            timeformat: '%H:%M<br/>%d %b<br/>(%a)',
            monthNames: ['jan', 'feb', 'mar', 'apr', 'mei', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'],
            dayNames: ['zo', 'ma', 'di', 'wo', 'do', 'vr', 'za']
        },
        legend: { position: 'ne' },
        grid: { hoverable: true, autoHighlight: false, labelMargin: 10 },
        crosshair: { mode: 'x' },
        pan: { interactive: true },
        zoom: { interactive: true }
    };
    var add_default_flot_options = function (options) {
        // first {} = make a copy instead of destroying original 
        return $.extend(true, {}, default_flot_options, options);
    };

    /**
     * Much faster than native .toFixed(), see http://jsperf.com/tofixed-vs-factor . 
     */
    var fastToFixed = function (v, decimals) {
        var factor = Math.pow(10, decimals);
        return Math.round(v * factor) / factor;
    };

    var fixIE8DrawBug = function (plot) {
        if (navigator.appName == 'Microsoft Internet Explorer') {
            var ua = navigator.userAgent;
            var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
            if (re.exec(ua) != null) {
                var rv = parseFloat(RegExp.$1);
                if (rv == 8) {
                    setTimeout(function () {
                        plot.resize();
                        plot.setupGrid();
                        plot.draw();
                    }, 100);
                }
            }
        }
    };

    var set_tick_size = function (plot) {
        var xaxis = plot.getOptions().xaxes[0];
        var tick_size = null;
        var diff = xaxis.max - xaxis.min;
        var len = tick_size_map.length;
        for (var i = 0; i < len; i++) {
            var ts = tick_size_map[i];
            if (diff > ts[0] && diff <= ts[1]) {
                tick_size = ts[2];
                break;
            }
        }
        if (tick_size) {
            xaxis.tickSize = tick_size;
        }
    };

    // grab url base
    var $urls = $('#data-urls');
    var url_base = $urls.attr('data-url-base');
    var data_url = $urls.attr('data-data-url');
    var debug = $.getQueryString('debug') !== undefined;

    // set up debug panel
    if (debug) {
        $('#debug-panel').show();
    }

    // set up information popovers
    $(".has_popover_east").popover({
        placement: 'right'
    });

    // set up the fill slider (the vertical one)
    {
        var $desired_fill_slider = $('#desired-fill-slider').slider({
            orientation: 'vertical',
            range: 'min',
            min: 0,
            max: 100,
            value: 50
        });

        // grab related DOM elements
        var $desired_fill_label = $('#desired-fill-label');
        var $desired_fill_val = $('#desired-fill-label .val');
        var $bg = $('#desired-fill-slider .ui-widget-header');
    
        // change label position, value and slider background color on slider value change
        var refresh_amount = function (value) {
            $desired_fill_label.css('bottom', (value - 2) + '%');
            $desired_fill_val.html(value);
    
            var scaled = value / 100.0;
            var r = 12;
            var g = Math.round(48 + scaled * 48); // g in range [48-96]
            var b = value + 155; // b in range [155-255]
            $bg.css('background-color', 'rgb(' + r + ', ' + g + ', ' + b + ')');
        };
    
        $desired_fill_slider.bind('slide', function (event, ui) {
            refresh_amount(ui.value);
        });
    
        // do an initial refresh of the fill slider
        refresh_amount($desired_fill_slider.slider('value'));
    }

    // set up the demand slider (the horizontal one)
    {
        var $demand_slider = $('#demand-diff-slider').slider({
            min: 50,
            max: 150,
            value: 100
        });

        // grab related DOM elements
        var $label = $('#demand-diff-label');
        var $val = $('#demand-diff-label .val');

        // change label value on slider value change
        var refresh_demand_diff = function (value) {
            $val.html(value);
        };
    
        $demand_slider.bind('slide', function (event, ui) {
            refresh_demand_diff(ui.value);
        });
    
        // do an initial refresh of the demand slider
        refresh_demand_diff($demand_slider.slider('value'));
    }

    // set up right flot graph
    // depends on jquery.flot.axislabels.js
    // depends on jquery.flot.fillbetween.js
    // depends on jquery.flot.crosshair.js
    // depends on jquery.flot.navigate.js
    // depends on jquery.flot.dashes.js
    var build_spinner = function () {
        var $spinner = $('<img width="32" height="32" />').attr('src', url_base + 'ajax-loader.gif');
        return $spinner;
    };
    var pad = function (val, len) {
        val = String(val);
        len = len || 2;
        while (val.length < len) val = "0" + val;
        return val;
    };
    var time_tick_formatter = function (number, axis) {
        var time = new Date(number);
        // presentation, so don't use UTC, but the localized date instead.
        return time.getDate() + '-' + pad(time.getMonth() + 1, 2) + '<br/>' + time.getHours() + ':' + pad(time.getMinutes(), 2);
    };
    var full_time_format = function (timestamp) {
        var time = new Date(timestamp);
        // presentation, so don't use UTC, but the localized date instead.
        return time.getDate() + '-'
               + (time.getMonth() + 1)
               + '-' + time.getFullYear()
               + ' ' + pad(time.getHours(), 2)
               + ':' + pad(time.getMinutes(), 2);
    };
    var add_tooltip = function (plot, values) {
        // build a tooltip element
        var $graph = plot.getPlaceholder();
        var $tt = $('<div class="flot-tooltip tickLabels" style="display:none; clear:none; position:fixed; left:0; top:0; z-index:1000;"/>');
        $graph.parent().append($tt);
        $graph.hover(
            function () { $tt.show(); },
            function () { $tt.hide(); }
        );

        // clean up after graph is deleted
        var cleanup = function () {
            $tt.remove();
        };
        plot.hooks.shutdown.push(cleanup);

        $graph.bind("plothover", function (event, pos, item) {
            var i;
            // find the nearest points, x-wise
            for (i = 0; i < values.length; ++i)
                if (values[i][0] > pos.x)
                    break;
            var p1 = values[i - 1];
            var p2 = values[i];
            // now interpolate
            var y;
            if (p1 == null || p2 == null)
                y = null; //p2[1] || p1[1];
            else
                y = p1[1] + (p2[1] - p1[1]) * (pos.x - p1[0]) / (p2[0] - p1[0]);
            // format the label
            // presentation, so don't use UTC, but the localized date instead.
            var time = new Date(pos.x);
            time = time.getDate() + '-'
                 + (time.getMonth() + 1)
                 + '-' + time.getFullYear()
                 + ' ' + pad(time.getHours(), 2)
                 + ':' + pad(time.getMinutes(), 2)
                 + ' uur';
            var y_formatted;
            if (y !== null)
                y_formatted = plot.getYAxes()[0].tickFormatter(fastToFixed(y, 2));
            else
                y_formatted = 'n.v.t.';
            var label = time + ": " + y_formatted;
            // position it
            $tt.css({
                top: pos.pageY,
                left: pos.pageX + 20
            });
            // set label content
            $tt.html(label);
        });
    };
    var plot_fill_graph = function (graph_info, $fill_graph_container) {
        // build a new element
        var $fill_graph = $('<div id="fill-graph"/>');
        $fill_graph_container.append($fill_graph);
        // order of following elements is also drawing order
        var lines = [
            { id: 'min',     data: graph_info.data.min,     yaxis: 1, lines: { show: true, lineWidth: 1, fill: 0.4 }, color: "#7FC9FF", fillBetween: 'mean' },
            { id: 'mean',    data: graph_info.data.mean,    yaxis: 1, lines: { show: true, lineWidth: 7 }, color: "#0026FF", label: 'voorspelling vulgraad' },
            { id: 'max',     data: graph_info.data.max,     yaxis: 1, lines: { show: true, lineWidth: 1, fill: 0.4 }, color: "#EFC9FF", fillBetween: 'mean' },
            { id: 'history', data: graph_info.data.history, yaxis: 1, lines: { show: true, lineWidth: 7 }, color: "yellow", label: 'meting vulgraad' },
            { id: 'dummy1',  data: [0, 0],                  yaxis: 2 }
        ];
        var markings = [
            { color: '#f6f6f6', yaxis: { from: graph_info.y_marking_min, to: 0 } },
            { color: '#f6f6f6', yaxis: { from: 120, to: graph_info.y_marking_max } },
            { color: '#12d',    yaxis: { from: graph_info.y_marking_min, to: graph_info.y_marking_min } },
            { color: '#e22',    yaxis: { from: graph_info.y_marking_max, to: graph_info.y_marking_max } },
            { color: '#2a2',    yaxis: { from: graph_info.desired_fill, to: graph_info.desired_fill } },
            { color: '#000',    xaxis: { from: graph_info.x0, to: graph_info.x0 }, lineWidth: 1 }
        ];
        var omslagpunt = graph_info.x_marking_omslagpunt;
        if (omslagpunt) {
            var m = { color: '#2a2', xaxis: { from: omslagpunt, to: omslagpunt }, lineWidth: 2 };
            markings.push(m);
        }
        var xmin = graph_info.x0 - 2 * MS_DAY;
        var xmax = graph_info.x0 + 5 * MS_DAY;
        var options = {
            series: {
                curvedLines: {
                    active: false
                }
            },
            xaxes: [
                {
                    min: xmin,
                    max: xmax
                }
            ],
            yaxes: [
                {
                    min: 0,
                    max: 120,
                    labelWidth: 30,
                    tickFormatter: function (v, axis) { return v + " %"; },
                    panRange: false,
                    zoomRange: false,
                    position: 'left'
                },
                {
                    min: 0,
                    max: 120,
                    labelWidth: 100,
                    ticks: [
                        [graph_info.y_marking_min, 'Min. berging'],
                        [graph_info.y_marking_max, 'Max. berging'],
                        [graph_info.desired_fill, 'Gewenste vulgraad']
                    ],
                    panRange: false,
                    zoomRange: false,
                    position: 'right'
                }
            ],
            grid: { markings: markings }
        };
        options = add_default_flot_options(options);
        var plot = $.plot($fill_graph, lines, options);
        add_tooltip(plot, graph_info.data.mean);

        // add marking labels
        var add_label = function (text, left, top) {
            var $label = $('<div class="marking-label"/>').css({
                left: left,
                top: top
            }).html(text);
            $fill_graph_container.append($label);
        };
        var o;
        o = plot.pointOffset({ x: plot.getOptions().xaxis.max, y: graph_info.y_marking_min});
        add_label('Min. berging', o.left, o.top);
        o = plot.pointOffset({ x: plot.getOptions().xaxis.max, y: graph_info.y_marking_max});
        add_label('Max. berging', o.left, o.top);
        o = plot.pointOffset({ x: plot.getOptions().xaxis.max, y: graph_info.desired_fill});
        add_label('Gewenste vulgraad', o.left, o.top);
        fixIE8DrawBug(plot);
        return plot;
    };

    var get_query_params = function (graph_type) {
        // build query string based on user input
        var query = {
            graph_type: graph_type,
            format: 'json',
            desired_fill: $desired_fill_slider.slider('value'),
            demand_diff: $demand_slider.slider('value'),
            date: new Date().getTime() // add dummy date to simulate REST like behaviour, but in reality the server-time is used
        };

        // append debug parameters
        if (debug) {
            $.extend(query, {
                hours_diff: eval($('#debug-hours-diff').val()),
                rain_exaggerate_factor: eval($('#debug-rain-exaggerate-factor').val())
            });
        }

        return $.param(query);
    };

    var $fill_graph_container = $('#fill-graph-container');
    var $rain_graph_container = $('#rain-graph-container');
    var $overflow_visualization_container = $('#overflow-visualization-container');
    var $overflow_visualization = $('#overflow-visualization');
    var refresh_prediction_data = function () {
        // clear the graph container
        var $spinner = build_spinner();
        $fill_graph_container.empty().append($spinner);
        var $spinner2 = build_spinner();
        $rain_graph_container.empty().append($spinner2);

        // hide the 'bakjes' visualization
        $overflow_visualization_container.hide();

        // generate query
        var query_params = get_query_params('prediction');

        // submit requests to the server
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                // clear the graph container (remove spinner)
                $fill_graph_container.empty();

                // plot the graph
                plot_fill_graph(response.graph_info, $fill_graph_container);

                // show the 'bakjes' visualization
                // draw_overflow_visualization(response.overflow);

                // set current fill label
                var current_fill = response.current_fill.toFixed();
                $('#current-fill-label').html(current_fill + ' % -');
                $('#current-fill-label').css({bottom: current_fill + '%'});

                // show the demand
                $('#demand-value').html(Math.round(response.demand_24h) + ' m<sup>3</sup>');

                // show the "omslagpunt"
                var omslagpunt = response.graph_info.x_marking_omslagpunt;
                if (omslagpunt) {
                    $('#omslagpunt-value').html(full_time_format(omslagpunt));
                }
                else {
                    $('#omslagpunt-value').html('N.v.t.');
                }

                $('#overflow-value').html(Math.round(response.overflow_24h) + ' m<sup>3</sup>');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: ' + errorThrown + '</p>');
                $fill_graph_container.empty().append($error);
            }
        });
        var query_params2 = get_query_params('rain');
        $.ajax({
            url: data_url + '?' + query_params2,
            success: function (response) {
                // clear the graph container (remove spinner)
                $rain_graph_container.empty();

                // plot the graph
                plot_rain_graph(response.rain_graph_info, $rain_graph_container);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: ' + errorThrown + '</p>');
                $rain_graph_container.empty().append($error);
            }
        });
    };

    var draw_overflow_visualization = function (amount) {
        $overflow_visualization.empty();
        if (amount === 0) {
            $('<p class="no-overflow">Geen</p>').appendTo($overflow_visualization);
        }
        else {
            for (var i = 0; i < amount; i++) {
                var $image = $('<img width="64" height="64" />').attr('src', url_base + 'bakje.jpg');
                $overflow_visualization.append($image);
            }
        }
        // show self
        $overflow_visualization_container.show();
    };

    // var refresh_tick_size = function (plot) {
        // var width = plot.width();
        // var labelWidth = 40;
        // var max_ticks = width / labelWidth;
// 
        // var xaxis = plot.getOptions().xaxes[0];
// 
        // var xaxis = plot.getAxes().xaxis;
        // var diff_quarter = (xaxis.max - xaxis.min) / (15 * 60 * 1000);
        // console.log(diff_hour + ' ' + max_ticks);
    // };

    var plot_rain_graph = function (graph_info, $rain_graph_container) {
        // build a new element
        var $rain_graph = $('<div id="rain-graph"/>');
        $rain_graph_container.append($rain_graph);

        // order of following elements is also drawing order
        var lines = [
            { id: 'min',  data: graph_info.data.min,  lines: { show: true, lineWidth: 1, fill: 0.4 },
              color: "#7FC9FF", label: 'min', fillBetween: 'mean' },
            { id: 'mean', data: graph_info.data.mean, lines: { show: true, lineWidth: 2 },
              color: "#222222", label: 'regen in mm/h' },
            { id: 'max',  data: graph_info.data.max,  lines: { show: true, lineWidth: 1, fill: 0.4 },
              color: "#FF696F", label: 'max', fillBetween: 'mean' }
        ];
        var markings = [
            { color: '#000', lineWidth: 1, xaxis: { from: graph_info.x0, to: graph_info.x0 } }
        ];
        var xmin = graph_info.x0 - 2 * MS_DAY;
        var xmax = graph_info.x0 + 5 * MS_DAY;
        var options = {
            series: {
                curvedLines: {
                    active: false
                }
            },
            xaxes: [
                {
                    min: xmin,
                    max: xmax
                }
                // {
                    // min: xmin,
                    // max: xmax,
                    // //mode: 'time',
                    // ticks: [[graph_info.x0, 'asd']],
                    // //tickSize: [2, 'hour'],
                    // labelHeight: 10,
                    // position: 'bottom',
                    // //panRange: false,
                    // zoomRange: false
                // }

            ],
            yaxes: [
                {
                    //min: -0.2,
                    //max: 4,
                    tickSize: 0.5,
                    tickFormatter: function (v) { return v.toFixed(1) + " mm"; },
                    labelWidth: 30,
                    panRange: false,
                    zoomRange: false,
                    position: 'left'
                },
                {
                    reserveSpace: true,
                    labelWidth: 100,
                    position: 'right'
                }
            ],
            grid: { markings: markings },
        };
        //set_tick_size(initial_options, xmin, xmax);
        options = add_default_flot_options(options);
        var plot = $.plot($rain_graph, lines, options);

        add_tooltip(plot, graph_info.data.mean);
        $rain_graph.bind('plotzoom', function (event, plot) {
            // get a 'bound' options dataset
            // var options = plot.getOptions();
            // set_tick_size(options, options.xaxis.min, options.xaxis.max);
            // plot.setupGrid();
            // plot.draw();
            //set_tick_size(plot);
            //refresh_tick_size(plot);
        });
        fixIE8DrawBug(plot);
        return plot;
    };

    var get_advanced_graph = function (graph_type) {
        // generate query
        var query_params = get_query_params(graph_type);
        var $container = $('#advanced-graph-container');
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                $container.empty();
                $container.show();
                plot_advanced_graph(response.graph_info, $container);
            }
        });
    };

    var plot_advanced_graph = function (graph_info, $container) {
        // build a new element
        var $graph = $('<div id="advanced-graph"/>');
        $container.append($graph);

        // order of following elements is also drawing order
        var lines = [
            { id: 'value', data: graph_info.data, lines: { show: true, lineWidth: 1 },
              color: "#222222", label: 'waarde in ' + graph_info.unit }
        ];
        var xmin = graph_info.x0 - 2 * MS_DAY;
        var xmax = graph_info.x0 + 5 * MS_DAY;
        var options = {
            xaxis: {
                min: xmin,
                max: xmax
                // mode: 'time',
                // tickSize: [2, 'hour'],
                // tickFormatter: time_tick_formatter,
                // zoomRange: [4 * MS_HOUR, 24 * MS_HOUR] // 4 hours - 24 hours
            },
            yaxes: [
                {
                    //min: -1,
                    //max: 4,
                    //tickSize: 1,
                    tickFormatter: function (v) { return fastToFixed(v, 2) + " " + graph_info.unit; },
                    //panRange: [-1, null], // no upper limit
                    zoomRange: false
                },
                {
                    reserveSpace: true,
                    labelWidth: 100,
                    position: 'right'
                }
            ],
            grid: { hoverable: true, autoHighlight: false, labelMargin: 10 }
        };
        options = add_default_flot_options(options);
        var plot = $.plot($graph, lines, options);
        add_tooltip(plot, graph_info.data);
        fixIE8DrawBug(plot);
        return plot;
    };

    // set up start button
    {
        $('#start-btn').click(function (event) {
            refresh_prediction_data();
        });
    }

    // set up advanced graph buttons
    {
        $('.advanced-graph').click(function (event) {
            var graph_type = $(this).attr('data-graph-type');
            get_advanced_graph(graph_type);
            return false;
        });
    }

    // initial data on page load
    refresh_prediction_data();
});
