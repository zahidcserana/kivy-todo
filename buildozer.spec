[app]
title = Todo App
package.name = todoapp
package.domain = org.kivytodo
source.dir = .
source.include_exts = py,kv,db
source.include_patterns = ui.kv
version = 1.0

requirements = python3,kivy==2.3.1,peewee

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
