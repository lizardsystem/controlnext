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

    var isIE = false;
    var ieVersion = 0;
    var determine_ie_version = function () {
        if (navigator.appName == 'Microsoft Internet Explorer') {
            isIE = true;
            var ua = navigator.userAgent;
            var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
            if (re.exec(ua) != null) {
                var rv = parseFloat(RegExp.$1);
                ieVersion = rv;
            }
        }
    };
    determine_ie_version();

    // var tick_size_map = [
        // [100 * MS_YEAR,  999 * MS_YEAR,   [50, 'year']],
        // [ 10 * MS_YEAR,  100 * MS_YEAR,   [10, 'year']],
        // [  1 * MS_YEAR,   10 * MS_YEAR,   [ 1, 'year']],
        // [  1 * MS_MONTH,   1 * MS_YEAR,   [ 1, 'month']],
        // [  1 * MS_DAY,     1 * MS_MONTH,  [ 1, 'day']],
        // [ 12 * MS_HOUR,    1 * MS_DAY,    [ 2, 'hour']],
        // [  1 * MS_HOUR,   12 * MS_HOUR,   [ 1, 'hour']],
        // [ 15 * MS_MINUTE,  1 * MS_HOUR,   [15, 'minute']],
        // [  1 * MS_MINUTE, 15 * MS_MINUTE, [ 1, 'minute']]
    // ];

    /**
     * Default options for all flot graphs.
     * Use add_default_flot_options to overwrite with custom options.
     */
    var default_flot_options = {
        xaxis: {
            mode: 'time',
            position: 'bottom',
            zoomRange: [1 * MS_HOUR, 40 * MS_DAY],
            timeformat: '%H:%M<br/>%d %b<br/>(%a)',
            monthNames: ['jan', 'feb', 'mar', 'apr', 'mei', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'],
            dayNames: ['zo', 'ma', 'di', 'wo', 'do', 'vr', 'za'],
            labelWidth: 24,
            labelHeight: null // font line height
        },
        yaxis: {
            labelWidth: 24,
            labelHeight: null // font line height
        },
        legend: { position: 'ne' },
        grid: { hoverable: true, autoHighlight: false, labelMargin: 10 },
        crosshair: { mode: 'x' },
        pan: { interactive: true },
        zoom: { interactive: true }
    };

    // fix IE messing up crosshair
    if (isIE && ieVersion < 9) {
        delete default_flot_options.crosshair;
    }

    /**
     * Combine custom flot options with the default option set.
     */
    var add_default_flot_options = function (options) {
        // first {} = make a copy instead of destroying original
        return $.extend(true, {}, default_flot_options, options);
    };

    /**
     * Much faster than native .toFixed(), see http://jsperf.com/tofixed-vs-factor.
     */
    var fastToFixed = function (v, decimals) {
        var factor = Math.pow(10, decimals);
        return Math.round(v * factor) / factor;
    };

    /**
     * Fixes a weird redraw bug, which only occurs in IE8...
     */
    var fixIE8DrawBug = function (plot) {
        if (isIE && ieVersion == 8) {
            setTimeout(function () {
                plot.resize();
                plot.setupGrid();
                plot.draw();
            }, 100);
        }
    };

    /**
     * Sets xaxis min and max the same as given parameter graph, for all
     * other graphs in the document.
     */
    var panAndZoomOtherGraphs = function (plot) {
        var axes = plot.getAxes();
        var xmin = axes.xaxis.min;
        var xmax = axes.xaxis.max;
        $('.zoompanlinked-flot-graph').each(function () {
            var otherPlot = $(this).data('plot');
            if (plot !== otherPlot) {
                var otherXAxisOptions = otherPlot.getAxes().xaxis.options;
                otherXAxisOptions.min = xmin;
                otherXAxisOptions.max = xmax;
                otherPlot.setupGrid();
                otherPlot.draw();
            }
        });
    };
    var bindPanZoomEvents = function ($graph) {
        // fix IE performance
        if (isIE && ieVersion < 9) {
            return;
        }

        $graph.bind('plotzoom', function (event, plot) {
            panAndZoomOtherGraphs(plot);
        });

        $graph.bind('plotpan', function (event, plot) {
            panAndZoomOtherGraphs(plot);
        });
    };

    // var set_tick_size = function (plot) {
        // var xaxis = plot.getOptions().xaxes[0];
        // var tick_size = null;
        // var diff = xaxis.max - xaxis.min;
        // var len = tick_size_map.length;
        // for (var i = 0; i < len; i++) {
            // var ts = tick_size_map[i];
            // if (diff > ts[0] && diff <= ts[1]) {
                // tick_size = ts[2];
                // break;
            // }
        // }
        // if (tick_size) {
            // xaxis.tickSize = tick_size;
        // }
    // };

    // setup an hourly page reload
    window.setTimeout(function () {
        window.location.reload(true);
    }, MS_HOUR);

    // grab url bases from the DOM
    var $constants = $('#data-constants');
    var url_base = $constants.attr('data-url-base');
    var data_url = $constants.attr('data-data-url');
    var max_voorraad = parseInt($constants.attr('data-max-voorraad'));
    var oppervlakte = parseInt($constants.attr('data-oppervlakte'));

    // set up a simple debug panel when ?debug=true is passed in the URL
    var debug = $.getQueryString('debug') !== undefined;
    if (debug) {
        $('#debug-panel').show();
    }

    // set up information popovers on hover
    // content and title are read from data attributes in the DOM
    $(".has_popover_east").popover({
        placement: 'right',
        animation: false
    });

    /**
     * Set up the fill slider (the vertical one).
     */
    var setup_fill_slider = function () {
        // load initial value of this slider from a cookie, if present
        var initialValue = 50;
        var cookieValue = $.cookie('desired_fill');
        if (cookieValue !== null) {
            initialValue = cookieValue;
        }

        // construct the jQuery UI slider
        var $slider = $('#desired-fill-slider').slider({
            orientation: 'vertical',
            range: 'min',
            min: 0,
            max: 100,
            value: initialValue
        });

        // grab related DOM elements
        var $label = $('#desired-fill-label');
        var $val = $('#desired-fill-label .val');
        var $bg = $('#desired-fill-slider .ui-widget-header');

        // updates the label position, value and background color
        var max_voorraad_per_oppervlakte_m3_ha = max_voorraad / (oppervlakte / 10000);
        var update_label = function (value) {
            $label.css('bottom', (value - 2) + '%');
            var vulgraad_ha = fastToFixed(value / 100 * max_voorraad_per_oppervlakte_m3_ha, 0);
            $val.html(value + ' % (' + vulgraad_ha + ' m<sup>3</sup>/ha)');

            var scaled = value / 100.0;
            var r = 12;
            var g = Math.round(48 + scaled * 48); // g in range [48-96]
            var b = value + 155; // b in range [155-255]
            $bg.css('background-color', 'rgb('+r+','+g+','+b+')');
        };

        // smoothly update the label when user is 'sliding'
        $slider.bind('slide', function (event, ui) {
            update_label(ui.value);
        });

        // update the cookie, when slider is released
        $slider.bind('slidechange', function (event, ui) {
            $.cookie('desired_fill', ui.value, { expires: 14 });
        });

        // do an initial update of the label
        update_label($slider.slider('value'));

        return $slider;
    };
    var $fill_slider = setup_fill_slider();

    /**
     * Set up the demand slider (the horizontal one).
     */
    var setup_demand_slider = function () {
        // construct the jQuery UI slider
        var $slider = $('#demand-exaggerate-slider').slider({
            min: 50,
            max: 150,
            value: 100
        });

        // grab related DOM elements
        var $label = $('#demand-exaggerate-label');
        var $val = $('#demand-exaggerate-label .val');

        // updates the label value
        var update_label = function (value) {
            $val.html(value);
        };

        // change label value on slider change
        $slider.bind('slide', function (event, ui) {
            update_label(ui.value);
        });

        // do an initial update of the label
        update_label($slider.slider('value'));

        return $slider;
    };
    var $demand_slider = setup_demand_slider();

    /**
     * Set up the rain slider (the second horizontal one).
     */
    var setup_rain_slider = function () {
        // construct the jQuery UI slider
        var $slider = $('#rain-exaggerate-slider').slider({
            min: 10,
            max: 500,
            value: 100
        });

        // grab related DOM elements
        var $label = $('#rain-exaggerate-label');
        var $val = $('#rain-exaggerate-label .val');

        // updates the label value
        var update_label = function (value) {
            $val.html(value);
        };

        // change label value on slider change
        $slider.bind('slide', function (event, ui) {
            update_label(ui.value);
        });

        // do an initial update of the label
        update_label($slider.slider('value'));

        return $slider;
    };
    var $rain_slider = setup_rain_slider();

    /**
     * Build a spinner (animated gif) element.
     */
    var build_spinner = function () {
        var $spinner = $('<img width="32" height="32" />').attr('src', url_base + 'ajax-loader.gif');
        return $spinner;
    };

    /**
     * Pad a value with leading zeros.
     */
    var pad = function (val, len) {
        val = String(val);
        len = len || 2;
        while (val.length < len) val = "0" + val;
        return val;
    };

    /**
     * Formatter for Flot graphs which adds a newline between date and time.
     */
    var time_tick_formatter = function (number, axis) {
        var time = new Date(number);
        // presentation, so don't use UTC, but the localized date instead.
        return time.getDate() + '-' + pad(time.getMonth() + 1, 2) + '<br/>' + time.getHours() + ':' + pad(time.getMinutes(), 2);
    };

    /**
     * Format a timestamp to a Dutch representation.
     */
    var full_time_format = function (timestamp) {
        var time = new Date(timestamp);
        // presentation, so don't use UTC, but the localized date instead.
        return time.getDate() + '-'
               + (time.getMonth() + 1)
               + '-' + time.getFullYear()
               + ' ' + pad(time.getHours(), 2)
               + ':' + pad(time.getMinutes(), 2);
    };

    var shutdownOldPlot = function ($el) {
        $el.children().each(function () {
            var plot = $(this).data('plot');
            if (plot)
                plot.shutdown();
        });
    };
    /**
     * Add a mouse tooltip to flot graphs.
     */
    var add_tooltip = function (plot, values) {
        // build a tooltip element
        var $graph = plot.getPlaceholder();
        var $tt = $('<div class="flot-tooltip tickLabels" style="display:none; clear:none; position:absolute; left:0; top:0; z-index:1000;"/>');
        $('body').append($tt);
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
                 + ':' + pad(time.getMinutes(), 2);
            var y_formatted = null;
            if (y !== null)
                // y_formatted = plot.getYAxes()[0].tickFormatter(fastToFixed(y, 2));
                y_formatted = fastToFixed(y, 2);
            else
                y_formatted = 'n.v.t.';
            var label = time + ": " + y_formatted;
            // var label = time;
            // position it
            $tt.css({
                top: pos.pageY + 20,
                left: pos.pageX + 20
            });
            // set label content
            $tt.html(label);
        });
    };

    /**
     * Set up the top graph showing the fill percentage.
     */
    var plot_fill_graph = function (graph_info, $container) {
        // build a new element
        var $graph = $('<div id="fill-graph" class="zoompanlinked-flot-graph"/>');
        $container.append($graph);
        // order of following elements is also drawing order
        var lines = [
            { id: 'min',     data: graph_info.data.min,     yaxis: 1, lines: { show: true, lineWidth: 1, fill: 0.4 }, color: "#7FC9FF", fillBetween: 'mean' },
            { id: 'mean',    data: graph_info.data.mean,    yaxis: 1, lines: { show: true, lineWidth: 7 }, color: "#0026FF", label: 'voorspeld' },
            { id: 'max',     data: graph_info.data.max,     yaxis: 1, lines: { show: true, lineWidth: 1, fill: 0.4 }, color: "#7FC9FF", fillBetween: 'mean' },
            { id: 'history', data: graph_info.data.history, yaxis: 1, lines: { show: true, lineWidth: 7 }, color: "yellow", label: 'gemeten' }
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
        // if (omslagpunt) {
            // var m = { color: '#2a2', xaxis: { from: omslagpunt, to: omslagpunt }, lineWidth: 2 };
            // markings.push(m);
        // }
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
                    // static ticks due to speed (IE)
                    //tickFormatter: function (v, axis) { return v + " %"; },
                    ticks: [
                        [0,   '0'],
                        [25,  '25'],
                        [50,  '50'],
                        [75,  '75'],
                        [100, '100'],
                    ],
                    panRange: false,
                    zoomRange: false,
                    position: 'left'
                }
            ],
            grid: { markings: markings }
        };
        options = add_default_flot_options(options);
        var plot = $.plot($graph, lines, options);
        add_tooltip(plot, graph_info.data.mean);

        // add marking labels
        // position labels (unused, but useful for x labels)
        var position_labels = function () {
            var left = $graph.width();
            $('div.marking-label', $container).each(function() {
                var y_value = parseFloat($(this).attr('data-y-value'));
                var o = plot.pointOffset({ y: y_value});
                $(this).css({
                    position:'absolute',
                    left: left,
                    top: o.top + 15
                });
            });
        };
        var add_label = function (text, y_value) {
            var o = plot.pointOffset({ y: y_value});
            var $label = $('<div class="marking-label"/>')
                .css({
                    position:'absolute',
                    width: 120,
                    right: -120,
                    top: o.top - 8
                })
                .attr('data-y-value', y_value)
                .html(text);
            $graph.append($label);
        };
        add_label('Min. voorraad', graph_info.y_marking_min);
        add_label('Max. voorraad', graph_info.y_marking_max);
        add_label('Gewenste vulgraad', graph_info.desired_fill);

        fixIE8DrawBug(plot);
        bindPanZoomEvents($graph);
        return plot;
    };

    /**
     * Set up the bottom graph showing the rain predictions.
     */
    var plot_rain_graph = function (graph_info, $container) {
        // build a new element
        var $graph = $('<div id="rain-graph" class="zoompanlinked-flot-graph"/>');
        $container.append($graph);

        // order of following elements is also drawing order
        var lines = [
            { id: 'min',  data: graph_info.data.min,  lines: { show: true, lineWidth: 1, fill: 0.4 },
              color: "#7FC9FF", fillBetween: 'mean' },
            { id: 'mean', data: graph_info.data.mean, lines: { show: true, lineWidth: 2 },
              color: "#222222", label: 'regen in mm / h' },
            { id: 'max',  data: graph_info.data.max,  lines: { show: true, lineWidth: 1, fill: 0.4 },
              color: "#7FC9FF", fillBetween: 'mean' }
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
            ],
            yaxes: [
                {
                    tickSize: 0.5,
                    tickFormatter: function (v) { return v.toFixed(1); },
                    panRange: false,
                    zoomRange: false,
                    position: 'left'
                }
            ],
            grid: { markings: markings }
        };
        options = add_default_flot_options(options);
        var plot = $.plot($graph, lines, options);

        add_tooltip(plot, graph_info.data.mean);
        fixIE8DrawBug(plot);
        bindPanZoomEvents($graph);
        return plot;
    };

    /**
     * Set up the optional bottom graph showing some advanced calculation data.
     */
    var plot_advanced_graph = function (graph_info, $container) {
        // build a new element
        var $graph = $('<div id="advanced-graph" class="zoompanlinked-flot-graph"/>');
        $container.append($graph);

        // order of following elements is also drawing order
        var lines = [
            { id: 'value', data: graph_info.data, lines: { show: true, lineWidth: 1 },
              color: "#222222", label: 'waarde' }
        ];
        var markings = [
            { color: '#000',    xaxis: { from: graph_info.x0, to: graph_info.x0 }, lineWidth: 1 }
        ];
        var xmin = graph_info.x0 - 2 * MS_DAY;
        var xmax = graph_info.x0 + 5 * MS_DAY;
        var options = {
            xaxis: {
                min: xmin,
                max: xmax
            },
            yaxes: [
                {
                    tickFormatter: function (v) { return fastToFixed(v, 2); },
                    panRange: false,
                    zoomRange: false
                }
            ],
            grid: { markings: markings }
        };
        options = add_default_flot_options(options);
        var plot = $.plot($graph, lines, options);
        add_tooltip(plot, graph_info.data);
        fixIE8DrawBug(plot);
        bindPanZoomEvents($graph);
        return plot;
    };

    /**
     * Get the value of a GET parameter from the URL.
     *
     * @param name name of the url parameter
     * @return parameter value
     *
     */
    var getURLParameter = function getURLParameter(name) {
        return decodeURIComponent(
            (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,""])[1]
        );
    };

    /**
     * Parse values from the UI's input controls and return a query string for them.
     */
    var get_query_params = function (graph_type) {
        // build query string based on user input
        var query = {
            graph_type: graph_type,
            format: 'json',
            desired_fill: $('#desired-fill-slider').slider('value'),
            demand_exaggerate: $('#demand-exaggerate-slider').slider('value'),
            rain_exaggerate: $('#rain-exaggerate-slider').slider('value'),
            date: new Date().getTime() // add dummy date to simulate REST like behaviour, but in reality the server-time is used
        };

        // if given, add the crop type to the query
        var crop_type = getURLParameter('crop');
        if (crop_type) {
            $.extend(query, {
                crop: crop_type
            });
        }

        // append debug parameters
        if (debug) {
            $.extend(query, {
                hours_diff: eval($('#debug-hours-diff').val()),
                basin_surface: eval($('#debug-basin-surface').val()),
                basin_storage: eval($('#debug-basin-storage').val())
            });
        }
        return $.param(query);
    };

    var $overflow_visualization_container = $('#overflow-visualization-container');
    var $overflow_visualization = $('#overflow-visualization');

    var load_prediction_data = function () {
        var $container = $('#fill-graph-container');
        shutdownOldPlot($container);
        var $spinner = build_spinner();
        $container.empty().append($spinner);

        // hide the 'bakjes' visualization
        //$overflow_visualization_container.hide();

        // submit requests to the server
        var query_params = get_query_params('prediction');
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                // clear the graph container (remove spinner)
                $container.empty();

                // plot the graph
                plot_fill_graph(response.graph_info, $container);

                // show the 'bakjes' visualization
                // draw_overflow_visualization(response.overflow);

                // set current fill slider label position and text
                var current_fill = response.current_fill.toFixed();
                $('#current-fill-label').html(current_fill + ' % -');
                $('#current-fill-label').css({bottom: (current_fill - 2) + '%'});

                // set the demand text
                $('#demand-value-24h').html(Math.round(response.demand_24h) + ' m<sup>3</sup>');
                $('#demand-value-week').html(Math.round(response.demand_week) + ' m<sup>3</sup>');

                // set the "omslagpunt" text
                var omslagpunt = response.graph_info.x_marking_omslagpunt;
                if (omslagpunt) {
                    $('#omslagpunt-value').html(full_time_format(omslagpunt));
                }
                else {
                    $('#omslagpunt-value').html('N.v.t.');
                }

                $('#overflow-24h-value').html(Math.round(response.overflow_24h) + ' m<sup>3</sup>');
                $('#overflow-5d-value').html(Math.round(response.overflow_5d) + ' m<sup>3</sup>');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: ' + errorThrown + '</p>');
                $container.empty().append($error);
            }
        });
    };

    var load_rain_data = function () {
        var $container = $('#rain-graph-container');
        shutdownOldPlot($container);
        var $spinner = build_spinner();
        $container.empty().append($spinner);

        var query_params = get_query_params('rain');
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                // clear the graph container (remove spinner)
                $container.empty();

                // plot the graph
                plot_rain_graph(response.rain_graph_info, $container);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: ' + errorThrown + '</p>');
                $container.empty().append($error);
            }
        });
    };

    var load_advanced_data = function (graph_type) {
        var $container = $('#advanced-graph-container');
        shutdownOldPlot($container);
        var $spinner = build_spinner();
        $container.empty().append($spinner);

        var query_params = get_query_params(graph_type);
        $.ajax({
            url: data_url + '?' + query_params,
            success: function (response) {
                // clean and show the container
                $container.empty();
                $container.show();
                plot_advanced_graph(response.graph_info, $container);
            }
        });
    };

    var update_advanced_graph = function () {
        var $radio = $('#advanced-graph-form input[name="advanced-graph-radio"]:checked')
        var graph_type = $radio.attr('data-graph-type');
        var title = $radio.attr('data-graph-title');

        var $panel = $('#advanced-graph-panel');
        var $graph_container = $('#advanced-graph-container');

        if (graph_type === 'none') {
            $panel.hide();
            $graph_container.empty();
        }
        else {
            $('h3', $panel).html(title);
            $panel.show();
            load_advanced_data(graph_type);
        }
    };

    var refresh_graphs = function () {
        load_prediction_data();
        load_rain_data();
        update_advanced_graph();
    };

    // var draw_overflow_visualization = function (amount) {
        // $overflow_visualization.empty();
        // if (amount === 0) {
            // $('<p class="no-overflow">Geen</p>').appendTo($overflow_visualization);
        // }
        // else {
            // for (var i = 0; i < amount; i++) {
                // var $image = $('<img width="64" height="64" />').attr('src', url_base + 'bakje.jpg');
                // $overflow_visualization.append($image);
            // }
        // }
        // // show self
        // $overflow_visualization_container.show();
    // };

    /**
     * Set up advanced graph form.
     */
    var setup_advanced_graph_form = function () {
        // disable submitting the form
        $('#advanced-graph-form').submit(function () { return false; });
        $('#advanced-graph-form input[name="advanced-graph-radio"]').change(update_advanced_graph);
    };
    setup_advanced_graph_form();

    // set up start button
    $('#start-btn').click(function (event) {
        refresh_graphs();
    });

    // initial data on page load
    refresh_graphs();
});
