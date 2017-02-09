(function() {
    'use strict';

    var imports = [];
    var app = angular.module("FileSearch", imports);

    app.controller("FileSearchController", ["$scope", "$log", "$http", function($scope, $log, $http) {
	$scope.getResults = function() {
	    $log.log("Fetching results...");
	    var query = $scope.query;

	    $http.post("/search/", {"query": query}).
		success(function(results) {
		    $log.log(results);
		    $scope.matchingFiles = results;
		}).
		error(function(error) {
		    $log.log(error);
		});
	};
    }]);
}());
