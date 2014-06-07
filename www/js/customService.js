'use strict';

// platform-specific service
angular.module('app.customService', []).
    factory('customService', function() {
        return {
			trackPage: function(page) {
				// place platform-specific google analytics tracking code here
			},

			doCustomActions: function() {
				// place platform-specific custom actions here
			}
		}
	});
