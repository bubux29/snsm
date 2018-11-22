#!/bin/bash

set -xe

buildozer android debug deploy run
#adb install .buildozer/android/platform/build/dists/SnSm_Formation/bin/SnSm_Formation-1.0.0-debug.apk

echo "Logging in /tmp/mux"
adb logcat > /tmp/mux
