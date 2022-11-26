// margin convention, though bootstrap/css is handling most of this now
OUTER_WIDTH = 1200;
OUTER_HEIGHT = 800;
MARGIN = {TOP: 100, RIGHT: 150, BOTTOM: 50, LEFT: 150};
INNER_WIDTH = OUTER_WIDTH - (MARGIN.LEFT + MARGIN.RIGHT);
INNER_HEIGHT = OUTER_HEIGHT - (MARGIN.TOP + MARGIN.BOTTOM);

// since we're serving data from a stati, preprocessed file
// just splitting the filename on "." and recomposing based on
// dropdown selections to locate/display
DATA_PATH = "data/";
DATA_FILE = "huffpost1000.none.bert.umap.json";

// this isn't necessary with static files, but saving for posterity
const toggleLoadingSpinner = () => {
    document.getElementById("data-spinner").classList.toggle("hidden");
};

$("#plot-container").click(function() {
    if ("tooltip" != $(this).attr("id"))
        $("#tooltip").css("visibility", "hidden");
});

// dataset selector
$("#dropdown-dataset a").click(function() {
    event.preventDefault();
    set_selection("dataset", 0, $(this).text());
});

// vectorizer selector
$("#dropdown-vectorizer a").click(function() {
    event.preventDefault();
    set_selection("vectorizer", 2, $(this).text());
});

// reducer selector
$("#dropdown-reducer a").click(function() {
    event.preventDefault();
    set_selection("reducer", 3, $(this).text());
});

// determine new file name and reload viz
const set_selection = (type, index, selection) => {
    proc_selections = DATA_FILE.split(".");
    proc_selections[index] = selection.toLowerCase();
    if (index === 2) {
        if ("bert" === selection.toLowerCase())
            proc_selections[1] = "none";
        else
            proc_selections[1] = "nltk";
    }
    DATA_FILE = proc_selections.join(".");
    $("#" + type).children(":first").html(selection + '<span class="caret">');
    $("#legend-menu").children(":first").html("Legend" + '<span class="caret">');
    $("#plot-title").text(proc_selections[0] + "\xa0\xa0 /  \xa0\xa0" + proc_selections[2] + "\xa0\xa0 / \xa0\xa0" + proc_selections[3]);
    get_samples();
}

// main function to load file and render everything
const get_samples = () => {

    // currently just wiping everything before recreating
    // though really this could be a more elegant d3 update somehow
    $("#plot-container").empty()
    $("#legend-container").empty()

    d3.json(DATA_PATH + DATA_FILE).then(res => {
        return res;
    }).then(data => {
        toggleLoadingSpinner();

        // creating a copy of data to be used for display (based on legend selection)
        // without touching raw data
        var data_view = [...data];

        // attempt at creating color customization
        // (color palettes are just a big pool of colors for some scales to choose from)
        // grab the various data/dimensions that could be used as color scales
        // create color scales based on those buckets/labels/classifications
        const catPalette = ["#1b70fc", "#d50527", "#158940", "#f898fd", "#24c9d7", "#cb9b64", "#866888", "#22e67a", "#e509ae", "#9dabfa", "#437e8a", "#b21bff", "#ff7b91", "#94aa05", "#ac5906", "#82a68d", "#fe6616", "#7a7352", "#f9bc0f", "#b65d66", "#07a2e6", "#c091ae", "#8a91a7", "#88fc07", "#ea42fe", "#9e8010", "#10b437", "#c281fe", "#f92b75", "#07c99d", "#a946aa", "#bfd544", "#16977e", "#ff6ac8", "#a88178", "#5776a9", "#678007", "#fa9316", "#85c070", "#6aa2a9", "#989e5d", "#fe9169", "#cd714a", "#6ed014", "#c5639c", "#c23271", "#698ffc", "#678275", "#c5a121", "#a978ba", "#ee534e", "#d24506", "#59c3fa", "#ca7b0a", "#6f7385", "#9a634a", "#48aa6f", "#ad9ad0", "#d7908c", "#6a8a53", "#8c46fc", "#8f5ab8", "#fd1105", "#7ea7cf", "#d77cd1", "#a9804b", "#0688b4", "#6a9f3e", "#ee8fba", "#a67389", "#9e8cfe", "#bd443c", "#6d63ff", "#d110d5", "#798cc3", "#df5f83", "#b1b853", "#bb59d8", "#1d960c", "#867ba8", "#18acc9", "#25b3a7", "#f3db1d", "#938c6d", "#936a24", "#a964fb", "#92e460", "#a05787", "#9c87a0", "#20c773", "#8b696d", "#78762d", "#e154c6", "#40835f", "#d73656", "#1afd5c", "#c4f546", "#3d88d8", "#bd3896", "#1397a3", "#f940a5", "#66aeff", "#d097e7", "#fe6ef9", "#d86507", "#8b900a", "#d47270", "#e8ac48", "#cf7c97", "#cebb11", "#718a90", "#e78139", "#ff7463", "#bea1fd"];
        const sourcePalette = catPalette.slice(10);

        const categories = [...new Set(data.map(d => d['category']))].sort();
        const categoryScale = d3.scaleOrdinal().range(catPalette.slice(0, categories.length)).domain(categories);

        const sources = [...new Set(data.map(d => d['source']))].sort();
        const sourceScale = d3.scaleOrdinal().range(sourcePalette.slice(0, sources.length)).domain(sources);

        const dates = [...new Set(data.map(d => d['date']))];
        const dateScale = d3.scaleOrdinal().range(catPalette.slice(0, dates.length)).domain(dates);

        // this is an example gradient/quantile-based coloring. right now it is using
        // the length of the cleaned tokens list (content) from the vectorizer
        const lengths  = data.map(d => d['content'].length);
        const lengthsScale = d3.scaleQuantile().range(['#649ac7', '#78b1cd', '#a7c4d1', '#d3d3d3', '#d0b5a4', '#cc9471', '#cb703b']).domain(lengths);
        const lengthsQuantiles = lengthsScale.quantiles().map(q => Math.round(q));
        // prepend/append min and max to intermediary thresholds
        lengthsQuantiles.unshift(d3.min(lengths));
        lengthsQuantiles.push(d3.max(lengths));
        // this is just to create the "x - y" labels
        quantileRanges = [];
        for (let i = 1; i < lengthsQuantiles.length; i++) {
            quantileRanges.push(`${lengthsQuantiles[i - 1]} - ${lengthsQuantiles[i]}`);
        }

        // this can probably be vastly improved
        // allows the legend and plot coloring to operate on generalized
        // "selectedDimension" almost like classes of an interface to return
        // its versions of values/labels/colors
        const legendDimensions = {
            "category": {
                "values": categories,
                "getLegendLabel": function(d) {return d},
                "getLabel": function(d) {return d["category"];},
                "getLegendColor": function(d) {return categoryScale(d);},
                "getDotColor": function(d) {return categoryScale(d["category"]);}
            },
            "source": {
                "values": sources,
                "getLabel": function(d) {return d["source"];},
                "getLegendLabel": function(d) {return d;},
                "getLegendColor": function(d) {return sourceScale(d);},
                "getDotColor": function(d) {return sourceScale(d["source"]);}
            },
            "date": {
                "values": [...new Set(dates.map(d => d.slice(0, 7)))],
                "getLabel": function(d) {return d['date'].slice(0, 7);},
                "getLegendLabel": function(d) {return d;},
                "getLegendColor": function(d) {return dateScale(d.slice(0, 7));},
                "getDotColor": function(d) {return dateScale(d["date"].slice(0, 7));}
            },
            "length": {
                "values": lengthsQuantiles.slice(0, -1),
                "getLabel": function(d) {
                    value = d["content"] ? d["content"].length : 0;
                    for (let i = 0; i < lengthsQuantiles.length; i++) {
                        if (value < lengthsQuantiles[i])
                            return lengthsQuantiles[i - 1];
                    }
                },
                "getLegendLabel": function(d) {
                    for (let i = 0; i < lengthsQuantiles.length; i++) {
                      if (d < lengthsQuantiles[i])
                          return `${lengthsQuantiles[i - 1]} - ${lengthsQuantiles[i]}`;
                    }
                },
                "getLegendColor": function(d) {
                    return lengthsScale(d);
                },
                "getDotColor": function(d) {
                    return lengthsScale(d["content"] ? d["content"].length : 0);
                }
            }
        };

        // default to "category" and this will be updated via dropdown of above map options
        selectedLegendDimension = "category";

        // create scatterplot and container
        var svg = d3.select("#plot-container")
            .append("svg")
            .attr("id", "svg")
//            .attr("viewbox", "0 0 1000 1000")
            .attr("width", "100%")
            .attr("height", "100%")

        var scatterPlot = svg.append("g")
            .attr("id", "scatter-plot")
            .attr("width", INNER_WIDTH)
            .attr("height", INNER_HEIGHT);

        // zoom and pan. initial zoom call and then use zoom translate so all
        // future zooms are relative
        var zoom = d3.zoom()
            .scaleExtent([1, 8])
            .on("zoom", function(e) {
                currentScale = e.transform.k // hack to access current scale from outside
                scatterPlot.attr("transform", e.transform);
                scatterPlot.selectAll(".dot").attr("r", 6 / currentScale);
//                scatterPlot.selectAll(".dot").attr("r", 6 / (1 + Math.log(currentScale) * 2));
            });
        svg.call(zoom);
        svg.call(zoom.transform, d3.zoomIdentity.translate(0, 100).scale(1));

        // scales based on min/max data with 5% buffer (so dots not clipped)
        var xScale = d3.scaleLinear()
            .range([0, INNER_WIDTH])
            .domain(
                [d3.min(data, d => d['coordinates'][0] - Math.abs(d['coordinates'][0] * 0.05)),
                d3.max(data, d => d['coordinates'][0] + Math.abs(d['coordinates'][0] * 0.05))]);

        var yScale = d3.scaleLinear()
            .range([INNER_HEIGHT, 0])
            .domain(
                [d3.min(data, d => d['coordinates'][1] - Math.abs(d['coordinates'][1] * 0.05)),
                d3.max(data, d => d['coordinates'][1] + Math.abs(d['coordinates'][1] * 0.05))]);

//        the axes don't add any value at the moment, but keeping for posterity
//        var xAxis = d3.axisBottom()
//            .scale(xScale);
//        var xAxisGroup = svg.append("g")
//            .attr("id", "x-axis")
//            .attr("class", "axis")
//            .attr("transform", `translate(${MARGIN.LEFT}, ${INNER_HEIGHT + MARGIN.TOP})`)
//            .call(xAxis)
//        var yAxis = d3.axisLeft()
//            .scale(yScale)
//        var yAxisGroup = svg.append("g")
//            .attr("id", "y-axis")
//            .attr("class", "axis")
//            .attr("transform", `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`)
//            .call(yAxis)


        var tooltip = d3.select("#plot-container")
              .append("div")
              .attr("class", "tooltip")
              .attr("id", "tooltip")
              .style("visibility", "hidden")
              .style("opacity", 1)
              .style("max-width", "200px")
              .style("background-color", "#fff")
              .style("border", "2px solid gray")
              .style("border-radius", "5px")
              .style("padding", "8px");


        // create legend with dots and labels using selectedDimension mapping
        // currently there is duplicate code that could be moved to an update method
        // like the "updateScatterPlot"
        var legend = d3.select("#legend-container").append("svg")
            .attr("id", "legend")
            .attr("width", 200)
            .attr("height", "1100")
            .attr("transform", `translate(10, 10)`)
            .append("g")
                .attr("id", "legend-group-container")
                .attr("height", "100%")
                .attr("transform", `translate(10, 20)`);

        legend.append("g")
            .attr("id", "show-hide")
            .on("click", showHideFilter)
            .append("text")
                .text("Show/Hide All");

        var legendItem = legend.selectAll(".legend-item")
            .data(legendDimensions[selectedLegendDimension]["values"])
            .enter()
            .append("g")
            .attr("class", "legend-item")
            .append("circle")
                .attr("class", "legend-dot focused")
                .attr("r", 8)
                .attr("cx", 20)
                .attr("cy", (d, i) => (i + 1) * 25)
                .attr("fill", d => legendDimensions[selectedLegendDimension]["getLegendColor"](d))
                .on("click", function(e, d) {
                    e.target.classList.toggle("focused");

                    updateDataView(e, d);
                });

        legend.selectAll(".legend-item")
            .append("text")
            .text(d => legendDimensions[selectedLegendDimension]["getLegendLabel"](d))
            .attr("alt", d => d)
            .attr("class", "legend-text")
            .attr("x", 35)
            .attr("y", (d, i) => (i + 1) * 25)
            .style("alignment-baseline", "central");

            // when Legend dropdown is updated, update legend colors
            // put here for now to make calls to functions defined in this block
            $("#dropdown-legend a").click(function() {
                event.preventDefault();
                selectedLegendDimension = $(this).text().toLowerCase();
                $("#legend-menu").children(":first").html(selectedLegendDimension + '<span class="caret">');
                data_view = [...data];
                updateScatterPlot(data);
                updateLegend(selectedLegendDimension);
            });

            // init call to render plot
            updateScatterPlot(data);



        //// functions ////
        function showHideFilter() {
            let circles = legend.selectAll("circle");
            if (circles.classed("focused")) {
                circles.classed("focused", false);
                data_view = [];
            }
            else {
                circles.classed("focused", true);
                data_view = [...data];
            }
            updateScatterPlot(data_view);
        }

        function updateLegend(dimension) {
            legend.selectAll(".legend-item").remove();

            var legendUpdate = legend.selectAll(".legend-item")
                .data(legendDimensions[selectedLegendDimension]["values"])

            var legendEnter = legendUpdate
                .enter()
                .append("g")
                .attr("class", "legend-item")
                .append("circle")
                    .attr("class", "legend-dot focused")
                    .attr("r", 8)
                    .attr("cy", (d, i) => (i + 1) * 25)
                    .attr("fill", d => legendDimensions[selectedLegendDimension]["getLegendColor"](d))
                    .on("click", function(e, d) {
                        e.target.classList.toggle("focused");

                        updateDataView(e, d);
                    });


            legendUpdate.exit().remove();

            legendEnter.merge(legendUpdate)

            legend.selectAll(".legend-item")
                        .append("text")
                        .text(d => legendDimensions[selectedLegendDimension]["getLegendLabel"](d))
                        .attr("alt", d => d)
                        .attr("class", "legend-text")
                        .attr("x", 15)
                        .attr("y", (d, i) => (i + 1) * 25)
                        .style("alignment-baseline", "central");
        }

        function updateDataView(event, selection) {
            target = event.target;

            if (legend.selectAll(".focused")?.size() == 0) {
                data_view = [...data];
                updateScatterPlot(data_view);
                legend.selectAll("circle").classed("focused", true);
            }
            else if (target.classList.contains("focused")) {
                data_view = getDataView(target, selection);
                updateScatterPlot(data_view);
            }
            else {
                data_view = getDataView(target, selection);
                updateScatterPlot(data_view);
            }

        }

        function getDataView(target, selection) {
            if (target.classList.contains("focused")) {
                return addToDataView(selection);
            }

            return removeFromDataView(selection);
        }

        function removeFromDataView(selection) {
            focused_data = data_view.filter(article => {
                return legendDimensions[selectedLegendDimension]["getLabel"](article) !== selection;
            });
            return focused_data;
        }

        function addToDataView(selection) {
            let focused_data = data.filter(article => {
                return legendDimensions[selectedLegendDimension]["getLabel"](article) === selection;
            });
            return [...data_view, ...focused_data];
        }

        function updateScatterPlot(selected_data) {
            scatterPlot.selectAll(".dot").remove();

            var scatterPlotUpdate = scatterPlot.selectAll(".dot")
                .data(selected_data);

            var scatterPlotEnter = scatterPlotUpdate.enter()
                .append("circle")
                    .attr("id", `dot-${(d, i) => i}`)
                    .attr("class", "dot")
                    .attr("r", 6 / currentScale)
                    .attr("cx", d => xScale(d['coordinates'][0]))
                    .attr("cy", d => yScale(d['coordinates'][1]))
                    .attr("fill", function(d) {
                        return legendDimensions[selectedLegendDimension]["getDotColor"](d);
                    })
                    .on("click", function(e, d) {
                        e.stopPropagation();
                        tooltip.style("visibility", "visible")
                            .style("left", `${e.pageX + 15}px`)
                            .style("top", `${e.pageY}px`)
                            .html(
                                `<div>
                                    Category: ${d['category']}<br/>
                                    Source: ${d['source']}<br/>
                                    <p>Date: ${d['date']}</p>
                                    <p>Title: ${d['title']}</p>
                                    <p>Description:
                                      ${d['description']}</p>
                                </div>`
                            )
                    });

            scatterPlotUpdate.exit().remove();

            scatterPlotEnter.merge(scatterPlotUpdate)
        }
    });
};
get_samples();
