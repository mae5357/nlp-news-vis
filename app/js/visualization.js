OUTER_WIDTH = 1200;
OUTER_HEIGHT = 800;
MARGIN = {TOP: 100, RIGHT: 150, BOTTOM: 50, LEFT: 150};
INNER_WIDTH = OUTER_WIDTH - (MARGIN.LEFT + MARGIN.RIGHT);
INNER_HEIGHT = OUTER_HEIGHT - (MARGIN.TOP + MARGIN.BOTTOM);

DATA_PATH = "data/";
DATA_FILE = "huffpost1000.nltk.doc2vec.pca.json";

const toggleLoadingSpinner = () => {
    document.getElementById("data-spinner").classList.toggle("hidden");
}

$("#dropdown-dataset a").click(function() {
    event.preventDefault();
    set_selection("dataset", 0, $(this).text())
})

$("#dropdown-reducer a").click(function() {
    event.preventDefault();
    set_selection("vectorizer", 3, $(this).text())
})

const set_selection = (type, index, selection) => {
    proc_selections = DATA_FILE.split(".");
    proc_selections[index] = selection;
    DATA_FILE = proc_selections.join(".")
    $("#" + type).children(":first").html(selection + '<span class="caret">')
    console.log(DATA_FILE)
    get_samples()
}

const get_samples = () => {

    $("#chart-container").empty()

    d3.json(DATA_PATH + DATA_FILE).then(res => {
//        console.log(res);
        return res;
    }).then(data => {
//        console.log(data);
        toggleLoadingSpinner();

        var data_view = [...data];

        const colorPalette = ["#1b70fc", "#d50527", "#158940", "#f898fd", "#24c9d7", "#cb9b64", "#866888", "#22e67a", "#e509ae", "#9dabfa", "#437e8a", "#b21bff", "#ff7b91", "#94aa05", "#ac5906", "#82a68d", "#fe6616", "#7a7352", "#f9bc0f", "#b65d66", "#07a2e6", "#c091ae", "#8a91a7", "#88fc07", "#ea42fe", "#9e8010", "#10b437", "#c281fe", "#f92b75", "#07c99d", "#a946aa", "#bfd544", "#16977e", "#ff6ac8", "#a88178", "#5776a9", "#678007", "#fa9316", "#85c070", "#6aa2a9", "#989e5d", "#fe9169", "#cd714a", "#6ed014", "#c5639c", "#c23271", "#698ffc", "#678275", "#c5a121", "#a978ba", "#ee534e", "#d24506", "#59c3fa", "#ca7b0a", "#6f7385", "#9a634a", "#48aa6f", "#ad9ad0", "#d7908c", "#6a8a53", "#8c46fc", "#8f5ab8", "#fd1105", "#7ea7cf", "#d77cd1", "#a9804b", "#0688b4", "#6a9f3e", "#ee8fba", "#a67389", "#9e8cfe", "#bd443c", "#6d63ff", "#d110d5", "#798cc3", "#df5f83", "#b1b853", "#bb59d8", "#1d960c", "#867ba8", "#18acc9", "#25b3a7", "#f3db1d", "#938c6d", "#936a24", "#a964fb", "#92e460", "#a05787", "#9c87a0", "#20c773", "#8b696d", "#78762d", "#e154c6", "#40835f", "#d73656", "#1afd5c", "#c4f546", "#3d88d8", "#bd3896", "#1397a3", "#f940a5", "#66aeff", "#d097e7", "#fe6ef9", "#d86507", "#8b900a", "#d47270", "#e8ac48", "#cf7c97", "#cebb11", "#718a90", "#e78139", "#ff7463", "#bea1fd"];
        const categories = [...new Set(data.map(d => d['category']))]
        const sources = [...new Set(data.map(d => d['source']))]
        const dates = [...new Set(data.map(d => d['date']))]
//        const dates = [...new Set(data.map(d => d['date'].slice(0, 7)))]
        const gradient  = data.map(d => d['description'].length)
        const legendDimensions = {
            "category": {
                "values": categories,
                "scale": d3.scaleOrdinal().range(colorPalette.slice(0, categories.length)).domain(categories),
                "func": function(d) {return d["category"]}
            },
            "source": {
                "values": sources,
                "scale": d3.scaleOrdinal().range(colorPalette.slice(0, sources.length)).domain(sources),
                "func": function(d) {return d["source"]}
            },
            "date": {
                "values": dates,
                "scale": d3.scaleOrdinal().range(colorPalette.slice(0, dates.length)).domain(dates),
                "func": function(d) {return d["date"]}
            },
            "gradient": {
                "values": gradient,
                "scale": d3.scaleLinear().range(['#336077', '#c9cdd1', '#963e23']).domain([d3.max(gradient), d3.mean(gradient), d3.min(gradient)]),
                "func": function(d) {
                    return d['description'].length ? d['description'].length : 0
                }
            }
        }

        selectedLegendDimension = "category";

        var svg = d3.select("#chart-container")
            .append("svg")
            .attr("id", "svg")
            .attr("width", OUTER_WIDTH)
            .attr("height", OUTER_HEIGHT);

        var xScale = d3.scaleLinear()
            .range([0, INNER_WIDTH])
            .domain(d3.extent(data, d => d['coordinates'][0] + (d['coordinates'][0] * 0.25)));
        var xAxis = d3.axisBottom()
            .scale(xScale);
        var xAxisGroup = svg.append("g")
            .attr("id", "x-axis")
            .attr("class", "axis")
            .attr("transform", `translate(${MARGIN.LEFT}, ${INNER_HEIGHT + MARGIN.TOP})`)
            .call(xAxis)

        var yScale = d3.scaleLinear()
            .range([INNER_HEIGHT, 0])
            .domain(d3.extent(data, d => d['coordinates'][1] + (d['coordinates'][1] * 0.25)));
        var yAxis = d3.axisLeft()
            .scale(yScale)
        var yAxisGroup = svg.append("g")
            .attr("id", "y-axis")
            .attr("class", "axis")
            .attr("transform", `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`)
            .call(yAxis)

//        var colorScale = d3.scaleOrdinal()
//            .range(colorPalette.slice(0, categories.length))
//            .domain(categories);


        var scatterPlot = svg.append("g")
            .attr("id", "scatter-plot")
            .attr("width", INNER_WIDTH)
            .attr("height", INNER_HEIGHT)
            .attr("transform", `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`);

        

        // var legendContainer = svg.append("g")
        //     .attr("id", "legend-container")
        //     .attr("transform", `translate(${INNER_WIDTH + (MARGIN.LEFT / 2)}, ${MARGIN.TOP})`);

        // var legend = legendContainer.append("g")
        //     .attr("id", "legend");

        var legend = svg.append("g")
            .attr("id", "legend")
            .attr("transform", `translate(${INNER_WIDTH + (MARGIN.LEFT / 2)}, ${MARGIN.TOP})`);
        legend.append("g")
            .attr("id", "show-hide")
            .on("click", function(e, d) {
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
            })
            .append("text")
                .text("Show/Hide All");

        var legendItem = legend.selectAll(".legend-item")
            .data(legendDimensions[selectedLegendDimension]["values"])
//            .data(categories)
            .enter()
            .append("g")
            .attr("class", "legend-item")
            .append("circle")
                .attr("class", "legend-dot focused")
                .attr("r", 8)
                .attr("cy", (d, i) => (i + 1) * 25)
                .attr("fill", d => legendDimensions[selectedLegendDimension]["scale"](d))
//                .attr("fill", d => colorScale(d))
                .on("click", function(e, d) {
                    if (selectedLegendDimension !== "gradient") {
                        console.log(d);
                        e.target.classList.toggle("focused");

                        updateDataView(e, d);
                    }
                });

        legend.selectAll(".legend-item")
            .append("text")
            .text(d => d)
            .attr("alt", d => d)
            .attr("class", "legend-text")
            .attr("x", 15)
            .attr("y", (d, i) => (i + 1) * 25)
            .style("alignment-baseline", "central");

            updateScatterPlot(data);


        //// functions ////
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
            focused_data = data_view.filter(article => article[selectedLegendDimension] !== selection);
//            focused_data = data_view.filter(article => article['category'] !== selection);
            return focused_data;
        }

        function addToDataView(selection) {
            let focused_data = data.filter(article => article[selectedLegendDimension] === selection);
//            let focused_data = data.filter(article => article['category'] === selection);
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
                    .attr("r", 6)
                    .attr("cx", d => xScale(d['coordinates'][0]))
                    .attr("cy", d => yScale(d['coordinates'][1]))
                    .attr("fill", function(d) {
                        return legendDimensions[selectedLegendDimension]["scale"](legendDimensions[selectedLegendDimension]["func"](d))
                    })
//                    .attr("fill", d => colorScale(d['category']))
                    .on("click", function(e, d) {
//                        console.log(Object.keys(d));
//                        console.log(d['headline']);
//                        console.log(d['short_description']);
                        console.log(d['title']);
                        console.log(d['description']);
                    });

            scatterPlotUpdate.exit().remove();

            scatterPlotEnter.merge(scatterPlotUpdate)
        }
    });
};
get_samples();
