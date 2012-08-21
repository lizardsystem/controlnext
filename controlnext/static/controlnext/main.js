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
    var MS_HOUR = 60 * 60 * 1000;

    var set_tick_size = function (options, x_min, x_max) {
        var tick_size = [];
        var diff_time = x_max - x_min;
        var diff_seconds = diff_time/1000;
        var diff_minutes = diff_time/1000/60;
        var diff_hours = diff_time/1000/60/60;
        if (diff_hours > 24*30*12) {
            $.merge(tick_size, [1, "year"]);
        } else if (diff_hours > 24*30) {
            $.merge(tick_size, [1, "month"]);
        } else if (diff_hours > 24) {
            $.merge(tick_size, [1, "day"]);
        } else if (diff_hours > 20) {
            $.merge(tick_size, [2, "hour"]);
        } else if (diff_hours > 1) {
            $.merge(tick_size, [1, "hour"]);
        } else if (diff_minutes > 45) {
            $.merge(tick_size, [15, "minute"]);
        } else if (diff_minutes > 10) {
            $.merge(tick_size, [10, "minute"]);
        } else if (diff_minutes > 5) {
            $.merge(tick_size, [5, "minute"]);
        } else if (diff_minutes > 1) {
            $.merge(tick_size, [1, "minute"]);
        } else if (diff_seconds > 45 ) {
            $.merge(tick_size, [15, "second"]);
        } else if (diff_seconds > 10) {
            $.merge(tick_size, [10, "second"]);
        } else {
            $.merge(tick_size, [1, "second"]);
        }
        options.xaxis.tickSize = tick_size;
    };

    // grab url base
    var $urls = $('#data-urls');
    var url_base = $urls.attr('data-url-base');
    var prediction_url = $urls.attr('data-prediction-url');
    var rain_url = $urls.attr('data-rain-url');
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
            value: 60
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
                y = 0; //p2[1] || p1[1];
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
            var y_formatted = plot.getYAxes()[0].tickFormatter(y.toFixed(2));
            var label = "waarde op " + time + ": " + y_formatted;
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
            { id: 'min',     data: graph_info.data.min, lines: { show: true, lineWidth: 0, fill: 0.4 }, color: "#7FC9FF", fillBetween: 'mean' },
            { id: 'mean',     data: graph_info.data.mean, lines: { show: true, lineWidth: 7 }, color: "#0026FF", label: 'vulgraad' },
            { id: 'max',     data: graph_info.data.max, lines: { show: true, lineWidth: 0, fill: 0.4 }, color: "#7FC9FF", fillBetween: 'mean' }
        ];
        var markings = [
            { color: '#12d', yaxis: { from: graph_info.y_marking_min, to: graph_info.y_marking_min } },
            { color: '#e22', yaxis: { from: graph_info.y_marking_max, to: graph_info.y_marking_max } },
            { color: '#000', lineWidth: 1, xaxis: { from: graph_info.x0, to: graph_info.x0 } }
        ];
        var xmin = graph_info.x0;
        var xmax = graph_info.x0 + 24 * MS_HOUR;
        var options = {
            series: {
                curvedLines: {
                    active: false
                }
            },
            xaxis: {
                min: xmin,
                max: xmax,
                mode: 'time',
                tickSize: [2, 'hour'],
                tickFormatter: time_tick_formatter,
                zoomRange: [4 * MS_HOUR, 24 * MS_HOUR] // 4 hours - 36 hours
                //axisLabel: 'tijd vanaf',
                //axisLabelUseCanvas: true,
                //axisLabelFontFamily: 'Verdana,Arial,sans-serif',
                //axisLabelFontSizePixels: 10
            },
            yaxis: {
                min: 0,
                max: 120,
                panRange: [0, 120],
                tickFormatter: function (v) { return v + " %"; },
                zoomRange: false
            },
            legend: { position: 'ne' },
            grid: { hoverable: true, autoHighlight: false, markings: markings, labelMargin: 10 },
            crosshair: { mode: 'x' },
            pan: {
                interactive: true
            },
            zoom: {
                interactive: true
            }
        };
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
        return plot;
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

        // build query string based on user input
        var query = {
            format: 'json',
            desired_fill: $desired_fill_slider.slider('value'),
            demand_diff: $demand_slider.slider('value'),
            date: new Date().getTime() // add dummy date to simulate REST like behaviour, but in reality the server-time is used
        };

        // append debug parameters
        if (debug) {
            $.extend(query, {
                hours_diff: eval($('#debug-hoursdiff').val())
            });
        }

        // submit requests to the server
        $.ajax({
            url: prediction_url + '?' + $.param(query),
            success: function (response) {
                // clear the graph container (remove spinner)
                $fill_graph_container.empty();

                // plot the graph
                plot_fill_graph(response.graph_info, $fill_graph_container);

                // show the 'bakjes' visualization
                draw_overflow_visualization(response.overflow);

                // show the demand
                $('#demand-value').html(Math.round(response.demand24h) + ' m<sup>3</sup>');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var $error = $('<p>Fout bij het laden van de grafiekdata: ' + errorThrown + '</p>');
                $fill_graph_container.empty().append($error);
            }
        });
        $.ajax({
            url: rain_url + '?' + $.param(query),
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
        var xmin = graph_info.x0;
        var xmax = graph_info.x0 + 36 * MS_HOUR;
        var initial_options = {
            series: {
                curvedLines: {
                    active: true
                }
            },
            xaxis: {
                min: xmin,
                max: xmax,
                mode: 'time',
                tickSize: [2, 'hour'],
                tickFormatter: time_tick_formatter,
                zoomRange: [4 * MS_HOUR, 36 * MS_HOUR] // 4 hours - 36 hours
            },
            yaxis: {
                min: -1,
                max: 10,
                tickSize: 1,
                tickFormatter: function (v) { return v + " mm"; },
                panRange: [-1, null], // no upper limit
                zoomRange: false
            },
            legend: { position: 'ne' },
            grid: { hoverable: true, autoHighlight: false, markings: markings, labelMargin: 10 },
            crosshair: { mode: 'x' },
            pan: {
                interactive: true
            },
            zoom: {
                interactive: true
            }
        };
        //set_tick_size(initial_options, xmin, xmax);
        var plot = $.plot($rain_graph, lines, initial_options);

        add_tooltip(plot, graph_info.data.mean);
        //$rain_graph.bind('plotzoom', function (event, plot) {
            // get a 'bound' options dataset
            //var options = plot.getOptions();
            //set_tick_size(options, options.xaxis.min, options.xaxis.max);
            //plot.setupGrid();
            //plot.draw();
        //});
        return plot;
    };

    // set up start button
    {
        $('#start-btn').click(function (event) {
            refresh_prediction_data();
        });
    }
});
