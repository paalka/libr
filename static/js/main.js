(function() {
    'use strict';

    var imports = ['ngRoute'];
    var app = angular.module("FileSearch", imports);

    app.controller("FileSearchController", ["$scope", "$log", "$http", function($scope, $log, $http) {
	$scope.getResults = function() {
	    $log.log("Fetching results...");
	    var query = $scope.url;

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
