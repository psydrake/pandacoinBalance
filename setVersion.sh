#!/bin/sh
# Run this script to set the versions in each platform to the values declared below

# Before packaging a new version for distribution:
# 1. Increment VERSION and VERSION_CODE 
# 2. run this script: ./setVersion.sh

# Universal version - in Android, this is versionName
VERSION=1.0

# Only used in Android. Appended as minor version number if avaliable
VERSION_CODE=5

perl -pi -e "s/\sversion=\"\d+\.\d+\"\s/\ version=\"${VERSION}\"\ /" www/config.xml
perl -pi -e "s/return\s\'\d+\.\d+\.\d+\'\;/return\ \'${VERSION}\.${VERSION_CODE}\'\;/" www/js/services.js 
perl -pi -e "s/android\:versionCode=\"\NaN\"/android\:versionCode=\"${VERSION_CODE}\"/" platforms/android/ant-build/AndroidManifest.xml
perl -pi -e "s/android\:versionCode=\"\NaN\"/android\:versionCode=\"${VERSION_CODE}\"/" platforms/android/AndroidManifest.xml
perl -pi -e "s/android\:versionCode=\"\d+\"/android\:versionCode=\"${VERSION_CODE}\"/" platforms/android/AndroidManifest.xml
perl -pi -e "s/version\=\"\d+.\d+\"/version\=\"${VERSION}\"/" platforms/android/cordova/defaults.xml
perl -pi -e "s/\"version\"\:\ \"\d+\.\d+\.\d+\"/\"version\"\:\ \"${VERSION}\.${VERSION_CODE}\"/" webapp/chrome/manifest.json
perl -pi -e "s/\"version\"\:\ \"\d+\.\d+\.\d+\"/\"version\"\:\ \"${VERSION}\.${VERSION_CODE}\"/" webapp/merges/manifest.webapp
perl -pi -e "s/\<appVersion\>\d+\.\d+\.\d+\<\/appVersion\>/\<appVersion\>${VERSION}\.${VERSION_CODE}\<\/appVersion\>/" platforms/wp8/analytics.xml
perl -pi -e "s/\sVersion\=\"\d+\.\d+\"/ Version=\"${VERSION}\"/" platforms/wp8/Properties/WMAppManifest.xml
