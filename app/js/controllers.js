var app = angular.module("stock_scrapper", []);

app.controller("DataStocksCtrl", function($scope, $http) {

	$http.defaults.headers.put = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With'
    };

	$http.defaults.useXDomain = true;
	$http.defaults.withCredentials = true;

	$http.defaults.headers.common["Accept"] = "application/json";
	$http.defaults.headers.common["Content-Type"] = "application/json";
  	$http.defaults.headers.common["X-Custom-Header"] = "Angular.js";

  	$http.jsonp('http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=JSON_CALLBACK')
    	.success(function(data, status, headers, config) {
      		$scope.stocks = data.list.resources;
    	})
 		.error(function(error) {
    		alert( "error" );
 		});

 	 //initiate an array to hold all active tabs
    $scope.activeTabs = [];

 	//check if the tab is active
    $scope.isOpenTab = function (tab) {
        //check if this tab is already in the activeTabs array
        if ($scope.activeTabs.indexOf(tab) > -1) {
            //if so, return true
            return true;
        } else {
            //if not, return false
            return false;
        }
    }
    
    //function to 'open' a tab
    $scope.openTab = function (tab) {
        //check if tab is already open
        if ($scope.isOpenTab(tab)) {
            //if it is, remove it from the activeTabs array
            $scope.activeTabs.splice($scope.activeTabs.indexOf(tab), 1);
        } else {
            //if it's not, add it!
            $scope.activeTabs.push(tab);
        }
    }


});

