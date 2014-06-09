# Pandacoin PND Balance

## About
Web / mobile app for checking the balance of your Pandacoin (PND) wallet address(es), as well as the currency value of Pandacoin.

## Technical
Pandacoin PND Balance consists of two parts:
* A pure HTML / CSS / JavaScript front end built with the [AngularJS](http://angularjs.org/) JavaScript framework.
* A [Google App Engine](https://developers.google.com/appengine/) back end, written in [Python](http://www.python.org/), that looks up wallet balance data from the [Pandacoin PND Blockchain](http://pnd.showed.us/) and caches currency price data from the [cryptocoincharts.info](http://www.cryptocoincharts.info/) API.

The front end communicates with the back end via [JSONP](http://en.wikipedia.org/wiki/JSONP) calls. The backend polls cryptocoincharts.info every 10 minutes, and it stores this data in [memcache](https://developers.google.com/appengine/docs/python/memcache/) for all subsequent client requests, in order to reduce load on the CryptoCoinCharts server. Wallet balance lookups from the Pandacoin (PND) Blockchain [API](http://pnd.showed.us/q) occur on demand.

## Project Structure
This project is organized to make use of the Cordova command line tools (version 3.1).
* `www`					- common web assets
* `merges/android`		- Android specific web assets to override those in `www`
* `merges/wp8`			- Windows Phone 8 specific web assets to override those in `www`
* `platforms/android`	- Android specific files
* `platforms/wp8`		- Windows Phone 8 specific files
* `webap`				- files for hosted web app (Chrome, Firefox OS)
* `webapp/chrome`		- metadata files for the Chrome hosted web app, including the manifest and icons

## Building and Running
I originally wrote this using Apache Cordova 2.9 solely for Android. I later reorganized it to use [Apache Cordova 3.1](http://cordova.apache.org/docs/en/3.1.0/) for multiple Operating Systems, and have been building and running the project using the [Cordova 3.1 CLI](http://cordova.apache.org/docs/en/3.1.0/guide_cli_index.md.html#The%20Command-line%20Interface).

If you don't have Cordova 3.1 installed, follow the [CLI instructions](http://cordova.apache.org/docs/en/3.1.0/guide_cli_index.md.html#The%20Command-line%20Interface). If you have an older version, you can [upgrade](http://cordova.apache.org/blog/releases/2013/10/02/cordova-31.html). If, by the time you read this, there is a newer version of Cordova, you can probably use that :).

I have had success running the project on my physical Android phone. On the command line, within the project directory:
* Android (plug your phone into your computer) - `cordova run android --verbose`

**UPDATE:** I updated cordova to version 3.5. Here are some issues that I've seen since then:
* For Android: If you run `cordova build android` and get the error: "platforms/android/ant-build/AndroidManifest.xml:2: error: Error: Float types not allowed (at 'versionCode' with value 'NaN').",
	run the `./setVersion.sh` script to overwrite the NaN value in that file.

## Install On Your Device
* [Android](https://play.google.com/store/apps/details?id=net.edrake.pandacoinbalance)
* [Amazon Kindle Fire](http://www.amazon.com/Drake-Emko-Pandacoin-PND-Balance/dp/B00KUH19EO)
* [Windows Phone](http://www.windowsphone.com/en-us/store/app/darkcoin-balance/e6f1ed12-542f-42eb-8b91-8fb85090c1e2)
* [Chrome App](https://chrome.google.com/webstore/detail/lnaeedppehgnilkbklifknpnnldpcmgm)
* [Firefox OS](https://marketplace.firefox.com/app/pandacoin-pnd-balance/)
* [Blackberry 10](http://appworld.blackberry.com/webstore/content/56531889/)
* [Browse As A Web Site](http://d1nhig552bjwdu.cloudfront.net/main.html)

## Author
Drake Emko - drakee (a) gmail.com
* [@DrakeEmko](https://twitter.com/DrakeEmko)
* [Wolfgirl Band](http://wolfgirl.bandcamp.com/)
