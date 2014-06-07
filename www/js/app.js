'use strict';

// Declare app level module which depends on filters, and services
var app = angular.module('app', [
        'app.controllers',
        'app.services',
        'app.customService',
        'ngRoute',
		'ngTouch',
        'ui.bootstrap'
    ]).
	config(['$routeProvider', function($routeProvider) {
		$routeProvider.
            when("/home", {templateUrl: "partials/home.html", controller: "homeController"}).
            when("/add", {templateUrl: "partials/add.html", controller: "addController"}).
            when("/edit", {templateUrl: "partials/edit.html", controller: "editController"}).
            when("/settings", {templateUrl: "partials/settings.html", controller: "settingsController"}).
            when("/about", {templateUrl: "partials/about.html", controller: "aboutController"}).
			otherwise({redirectTo: "/home"});
}]);

app.run(function($rootScope, $location, $timeout, $log, settingsService, customService, utilService) {
	settingsService.setStore(new Persist.Store('Pandacoin PND Balance', {expires:36500}));

	$rootScope.loadingClass = '';

    $rootScope.getClass = function(path) {
        if ($location.path().substr(0, path.length) === path) {
            return "active";
        }
		else if ($location.path() === '/add' && path === '/edit') {
			return "active";
		}
        else {
            return "";
        }
    };

	$rootScope.openLink = customService.openLink;

	$rootScope.goto = function(pageName) {
		$location.path('/' + pageName);
	}

	$rootScope.currencySymbol = function(currency) {
		return utilService.currencySymbol(currency);
	}

    $rootScope.loadData = function() {
        $log.info('loadData! ' + $location.path());
        $rootScope.$broadcast('refresh', $location.path());
    };

	customService.doCustomActions(); // perform platform-specific javascript
});
