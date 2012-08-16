$(document).ready(function () {
    // grab url base
    var $urls = $('#data-urls');
    var url_base = $urls.attr('data-url-base');
    var prediction_url = $urls.attr('data-prediction-url');

    // set up information popovers
    $(".has_popover_east").popover({
        placement: 'right'
    });

    // set up the fill slider (vertical)
    {
        var $new_fill_slider = $('#new-fill-slider').slider({
            orientation: 'vertical',
            range: 'min',
            min: 0,
            max: 100,
            value: 60
        });

        // grab related DOM elements
        var $new_fill_label = $('#new-fill-label');
        var $new_fill_val = $('#new-fill-label .val');
        var $bg = $('#new-fill-slider .ui-widget-header');
    
        // change label position, value and slider background color on slider value change
        var refresh_amount = function (value) {
            $new_fill_label.css('bottom', (value - 2) + '%');
            $new_fill_val.html(value);
    
            var scaled = value / 100.0;
            var r = 12;
            var g = Math.round(48 + scaled * 48); // g in range [48-96]
            var b = value + 155; // b in range [155-255]
            // if (value > 80) {
                // // quickly ramp up red
                // var scaled = (value - 80) / 20.0;
                // r = Math.round(120 + scaled * (255 - 120));
                // b = Math.round(200 - (200 - 48) * scaled);
            // }
            $bg.css('background-color', 'rgb(' + r + ', ' + g + ', ' + b + ')');
        };
    
        $new_fill_slider.bind('slide', function (event, ui) {
            refresh_amount(ui.value);
        });
    
        // do an initial refresh of the fill slider
        refresh_amount($new_fill_slider.slider('value'));
    }

    // set up the demand slider (horizontal)
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

    // demonstration img refresh
    {
        var currentTimeout = null;
        var rightImages = [url_base + 'right_1.jpg', url_base + 'right_2.png'];
        var lowerImages = [url_base + 'lower_1.jpg', url_base + 'lower_2.gif'];
        var currentImagesIndex = 0;
    
        var loadGraphs = function () {
            currentTimeout = null;
    
            var $graph1 = $('<img width="420" height="300" style="width:420px;height:300px;" />').attr('src', rightImages[currentImagesIndex]);
            $('#right-img-container').empty().append($graph1);
            var $graph2 = $('<img width="700" height="270" style="width:700px;height:270px;" />').attr('src', lowerImages[currentImagesIndex]);
            $('#lower-img-container').empty().append($graph2);
    
            if (++currentImagesIndex >= rightImages.length) {
                currentImagesIndex = 0;
            }
        };

        var delayLoadGraphs = function () {
            // cancel old timeout
            if (currentTimeout !== null) {
                clearTimeout(currentTimeout);
                currentTimeout = null;
            }
    
            // show spinners
            var $spinner1 = $('<img width="32" height="32" />').attr('src', url_base + 'ajax-loader.gif');
            $('#right-img-container').empty().append($spinner1);
            var $spinner2 = $('<img width="32" height="32" />').attr('src', url_base + 'ajax-loader.gif');
            $('#lower-img-container').empty().append($spinner2);
    
            currentTimeout = setTimeout(loadGraphs, 1000);
        };
    }

    // set up right flot graph
    // depends on jquery.flot.axislabels.js
    // depends on jquery.flot.fillbetween.js
    // depends on jquery.flot.crosshair.js
    // depends on jquery.flot.navigate.js
    // depends on jquery.flot.dashes.js
    var pad = function (val, len) {
        val = String(val);
        len = len || 2;
        while (val.length < len) val = "0" + val;
        return val;
    };
    var build_spinner = function () {
        var $spinner = $('<img width="32" height="32" />').attr('src', url_base + 'ajax-loader.gif');
        return $spinner;
    };
    var time_tick_formatter = function (number, axis) {
        var time = new Date(number);
        return time.getUTCDate() + '-' + pad(time.getUTCMonth(), 2) + '<br/>' + time.getUTCHours() + ':' + pad(time.getUTCMinutes(), 2);
    };
    // show a tooltip
    var addToolTip = function ($container, $graph, values) {
        // build a tooltip element
        var $tt = $('<div class="flot-tooltip"/>');
        //$tt.offset({left: $fill_graph.offset().left + 60, top: $fill_graph.offset().top + 5});
        $container.append($tt);
        $graph.hover(
            function () { $tt.show(); },
            function () { $tt.hide(); }
        );

        // per-data point tooltips
        // var previousPoint = null;
        // var showTooltip = function (x, y, html) {
            // $tt.css({
                // display: 'block',
                // top: y,
                // left: x + 20
            // }).html(html);
        // };
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
            var time = new Date(pos.x);
            time = time.getUTCDate() + '-' + (time.getUTCMonth() + 1) + '-' + time.getUTCFullYear() + ' ' + time.getUTCHours() + ':00 uur';
            var label = "waarde op " + time + ": " + y.toFixed() + ' %';
            $tt.html(label);

            // per-data point tooltips
            // if (item) {
                // if (previousPoint != item.dataIndex) {
                    // previousPoint = item.dataIndex;
                    // $tt.hide();
                    // var x = item.datapoint[0].toFixed(2);
                    // var y = item.datapoint[1].toFixed(2);
                    // var label = "Vulgraad op " + x + " : " + y;
                    // //showTooltip(item.pageX, item.pageY, label);
                // }
            // }
            // else {
                // $tt.hide();
                // previousPoint = null;
            // }
        });
    };
    var plot_fill_graph = function (graph_info, $fill_graph_container) {
        // build a new element
        var $fill_graph = $('<div id="fill-graph"/>');
        $fill_graph_container.append($fill_graph);
        // order of following elements is also drawing order
        var lines = [
            //{ id: 'abs_min', data: graph_info.data['abs_min'], dashes: { show: true, lineWidth: 2 }, color: "rgb(190,190,190)", shadowSize: 0, label: 'min. berging' },
            //{ id: 'abs_max', data: graph_info.data['abs_max'], dashes: { show: true, lineWidth: 2 }, color: "rgb(90,90,90)", shadowSize: 0, label: 'max. berging' },
            //{ id: 't0',      data: graph_info.data['t0'],  dashes:  { show: true, lineWidth: 2 }, color: "rgb(50,205,50)", shadowSize: 0 },
            { id: 'val',     data: graph_info.data['val'], lines: { show: true, lineWidth: 7 }, color: "#0026FF", label: 'vulgraad' },
            { id: 'min',     data: graph_info.data['min'], lines: { show: true, lineWidth: 0, fill: 0.4 }, color: "#7FC9FF", fillBetween: 'val',},
            { id: 'max',     data: graph_info.data['max'], lines: { show: true, lineWidth: 0, fill: 0.4 }, color: "#7FC9FF", fillBetween: 'val' }
        ];
        var values = graph_info.data['val'];
        var markings = [
            { color: '#12d', yaxis: { from: graph_info.y_marking_min, to: graph_info.y_marking_min } },
            { color: '#e22', yaxis: { from: graph_info.y_marking_max, to: graph_info.y_marking_max } },
            { color: '#000', lineWidth: 1, xaxis: { from: graph_info.xmin, to: graph_info.xmin } }
        ];
        var options = {
            series: {
                curvedLines: {
                    active: false
                }
            },
            xaxis: {
                min: graph_info.xmin,
                max: graph_info.xmax,
                mode: 'time',
                tickSize: [4, 'hour'],
                tickFormatter: time_tick_formatter
                //axisLabel: 'tijd vanaf',
                //axisLabelUseCanvas: true,
                //axisLabelFontFamily: 'Verdana,Arial,sans-serif',
                //axisLabelFontSizePixels: 10
            },
            yaxis: {
                min: 0,
                max: 120,
                panRange: [0, 120],
                tickFormatter: function (v) { return v + " %"; }
            },
            legend: { position: 'ne' },
            grid: { hoverable: true, autoHighlight: false, markings: markings },
            //crosshair: { mode: 'x' },
            pan: {
                interactive: true
            }
            // zoom: {
                // interactive: true
            // }
        };
        var plot = $.plot($fill_graph, lines, options);
        addToolTip($fill_graph_container, $fill_graph, values);

        // add marking labels
        var addLabel = function (text, left, top) {
            var $label = $('<div class="marking-label"/>').css({
                left: left,
                top: top
            }).html(text);
            $fill_graph_container.append($label);
        };
        var o;
        o = plot.pointOffset({ x: graph_info.xmax, y: graph_info.y_marking_min});
        addLabel('Min. berging', o.left, o.top);
        o = plot.pointOffset({ x: graph_info.xmax, y: graph_info.y_marking_max});
        addLabel('Max. berging', o.left, o.top);
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
            new_fill: $new_fill_slider.slider('value'),
            demand_diff: $demand_slider.slider('value'),
            date: new Date().getTime() // add dummy date to simulate REST like behaviour, but in reality the server-time is used
        };

        // submit request to the server
        $.ajax({
            url: prediction_url + '?' + $.param(query),
            success: function (response) {
                // clear the graph container (remove spinner)
                $fill_graph_container.empty();
                $rain_graph_container.empty();

                // plot the graph
                plot_fill_graph(response.graph_info, $fill_graph_container);
                plot_rain_graph(response.graph_info, $rain_graph_container);

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
            { id: 'val', data: graph_info.data['val'], curvedLines: { show: true, lineWidth: 7 }, color: "#0026FF", label: 'regen' }
        ];
        var values = graph_info.data['val'];
        var markings = [
            { color: '#000', lineWidth: 1, xaxis: { from: graph_info.xmin, to: graph_info.xmin } }
        ];
        var options = {
            series: {
                curvedLines: {
                    active: true
                }
            },
            xaxis: {
                min: graph_info.xmin,
                max: graph_info.xmax,
                mode: 'time',
                tickSize: [4, 'hour'],
                tickFormatter: time_tick_formatter,
                zoomRange: [4 * 60 * 60 * 1000, 7 * 24 * 60 * 60 * 1000]
            },
            yaxis: {
                min: 0,
                max: 200,
                panRange: [0, 200],
                zoomRange: [10, 200],
                tickFormatter: function (v) { return v + " mm/s"; }
            },
            legend: { position: 'ne' },
            grid: { hoverable: true, autoHighlight: false, markings: markings },
            crosshair: { mode: 'x' },
            pan: {
                interactive: true
            },
            zoom: {
                interactive: true
            }
        };
        var plot = $.plot($rain_graph, lines, options);
        return plot;
    };

    // set up start button
    {
        $('#start-btn').click(function (event) {
            refresh_prediction_data();
        });
    }
});
