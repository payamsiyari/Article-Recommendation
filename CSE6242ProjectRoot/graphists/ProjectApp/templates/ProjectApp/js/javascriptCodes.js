$( document ).ready(function() {
    $("#query").keyup(function(event){
        if(event.keyCode == 13){
            $("#submitButton").click();
        }
    });
    $("#nodes_max_number").keyup(function(event){
        if(event.keyCode == 13){
            $("#submitButton").click();
        }
    });
    $("#hop_max_number").keyup(function(event){
        if(event.keyCode == 13){
            $("#submitButton").click();
        }
    });
    $("#centMaxLimit").keyup(function(event){
        if(event.keyCode == 13){
            $("#refineButton").click();
        }
    });
    $("#clearBrowserButton").click(function () {
        document.getElementById("selectedPaper").innerHTML = ""
        document.getElementById("citations").innerHTML = ""
    });
    $("#clearCentralsButton").click(function () {
        document.getElementById("output_algorithms").innerHTML = ""
        text.style("visibility","hidden");
    });
    $("#submitButton").click(function () {
        document.getElementById("selectedPaper").innerHTML = ""
        document.getElementById("citations").innerHTML = ""
        document.getElementById("loading").style.visibility = 'visible'
        var xhttp = new XMLHttpRequest();
        var queryValue = document.getElementById("query").value
        var nodesValue = document.getElementById("nodes_max_number").value
        var hopsValue = document.getElementById("hop_max_number").value
        var minYearValue = $( "#slider_range" ).slider( "values", 0 )
        var maxYearValue = $( "#slider_range" ).slider( "values", 1 )
        $.ajax({
            type: "GET",
            url: "/search",
            data: {
                query: queryValue,
                nodes: nodesValue,
                hops: hopsValue,
                minYear: minYearValue,
                maxYear: maxYearValue
            },
            success: function (newData) {
                document.getElementById("loading").style.visibility = 'hidden'
                document.getElementById("output_graph").innerHTML = newData;
                eval(document.getElementById("graphViewScriptMain").innerHTML);
            }
        });
        document.getElementById("loading").style.visibility = 'visible'
        $.ajax({
            type: "GET",
            url: "/searchList",
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("some error " + errorThrown.toString());
            },
            data: {
                query: queryValue,
                nodes: nodesValue,
                hops: hopsValue,
                minYear: minYearValue,
                maxYear: maxYearValue
            },
            success: function (newData) {
                document.getElementById("loading").style.visibility = 'hidden'
                document.getElementById("interface_search").innerHTML = newData;
                eval(document.getElementById("listViewScriptMain").innerHTML);
            }
        });
        history.replaceState(null, null, 'search?query='+queryValue+'&nodes='+nodesValue+'&hops='+hopsValue+"&minYear="+minYearValue+"&maxYear="+maxYearValue);
        $("#clearBrowserButton").click()
        $("#clearCentralsButton").click()
    })
    $(function() {
        $( "#slider_range" ).slider({
            range: true,
            //Set these based on a query
            min: 1834,
            max: 2010,
            values: [ 1980, 2010 ],
            slide: function( event, ui ) {
                $( "#year_span" ).val( "" + ui.values[ 0 ] + " - " + ui.values[ 1 ] );

            }
        });
        $( "#year_span" ).val( "" + $( "#slider_range" ).slider( "values", 0 ) +
            " - " + $( "#slider_range" ).slider( "values", 1 ) );
    });
    $("#refineButton").click(function (event) {
        event.preventDefault();
        document.getElementById("loading").style.visibility = 'visible'
        var xhttp = new XMLHttpRequest();
        $.ajax({
            url: '/getCentralNodes',
            type: 'POST',
            data: {graphJson: JSON.stringify(graph), centrality: $('input[name=cent]:checked', '#cents').val(), centMax: document.getElementById("centMaxLimit").value},
            // data: {graphJson: graph, centrality: $('input[name=cent]:checked', '#cents').val()},
            // data: {centrality: $('input[name=cent]:checked', '#cents').val()},
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("some error " + errorThrown.toString());
            },
            success: function (newData) {
                document.getElementById("loading").style.visibility = 'hidden'
                document.getElementById("output_algorithms").innerHTML = newData;
                eval(document.getElementById("centralityViewScriptMain").innerHTML);
            }
        });
        return false;
    });
})