$(function() {
    $("#search-button").click(function(event) {
	event.preventDefault();
	var query = $("#search-field").val();
	$.ajax({
	    type: "POST",
	    url: "/search/",
	    data: JSON.stringify({ query: query }),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data) {  updateSearchResults(data); },
	    failure: function(errMsg) {
		alert(errMsg);
	    }
	});
    });
    function updateSearchResults(results) {
	$("#search-result-container").empty();
	var results_html = "";
	if (results.length > 0) {
	    for (var i = 0; i < results.length; i++) {
		var curr_res = '' +
		    '<div class="row search-result-item">' +
		    '<div class="ten columns">' +
		    '<span class="category-title">' + results[i][4] + '</span>' +
		    '<a class="file-link" href="/uploads/' + results[i][3] + '" target="_blank">'  +
		    '<h4 class="file-title">' + results[i][1] + '</h4></a>' +
		    '<p class="file-tags">' + results[i][2] + '</p>' +
		    '</div>' +
		    '<div class="two columns" style="float: right">' +
		    '<span class="file-edit"><a href="/edit/' + results[i][0] + '">edit</a></span>' +
		    '</div>' +
		    '</div>'
		results_html = results_html + curr_res;
	    }
	} else {
	    var no_res = '' +
		'<div class="row search-result-item">' +
		'<div class="ten columns">' +
		'<h4 class="file-title">No matching files found!</h4></a>' +
		'</div>' +
		'</div>'
	    results_html = results_html + no_res;
	}
	$("#search-result-container").append(results_html);
    }
});

