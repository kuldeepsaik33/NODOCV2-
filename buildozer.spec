[app]
title = NODOC
package.name = nodoc
package.domain = org.nodoc
source.dir = .
source.include_exts = py,png,jpg,kv,txt,md
version = 2.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
