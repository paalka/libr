function bindEditHandlers() {
    $(".file-edit-wrapper").hide();

    $(".search-result-item").mouseover(function() {
	var fileId = $(this).attr("data-file-id");
	$("#file-edit-" + fileId).show();
    });

    $(".search-result-item").mouseout(function() {
	var fileId = $(this).attr("data-file-id");
	$("#file-edit-" + fileId).hide();
    });
}
function updateSearchResults(results) {
    $("#search-result-container").empty();
    var results_html = results["html"];
    if (results_html.length < 10) {
	var no_res = '' +
	    '<div class="row search-result-item">' +
	    '<div class="ten columns">' +
	    '<h4 class="file-title">No matching files found!</h4></a>' +
	    '</div>' +
	    '</div>'
	results_html = no_res;
    }

    $("#search-result-container").append(results_html);
    $(".file-edit-wrapper").hide();
    bindEditHandlers();
}

$(function() {
    bindEditHandlers();

    $("#search-field").keyup(function(event) {
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
});

