# Todo App

A cross-platform mobile todo app built with Python and Kivy, backed by a local SQLite database via Peewee ORM.

## Features

- Add, complete, and delete todos
- Persistent storage (survives restarts)
- Bulk-clear completed todos
- Dark-themed mobile UI
- Builds to Android APK via Buildozer

## Project Structure

```
todo/
├── main.py          # App logic, screens, and UI dialogs
├── database.py      # Peewee ORM models and DB helpers
├── ui.kv            # Kivy language UI layout and styles
├── buildozer.spec   # Android build configuration
└── kivy_env/        # Python virtual environment (not committed)
```

## Running on Desktop

```bash
source kivy_env/bin/activate
python main.py
```

## Building for Android

### Prerequisites

- Java 17+ JDK
- Cython 0.29.x (`pip install "cython==0.29.37"`)
- System packages: `git zip unzip autoconf libtool pkg-config zlib1g-dev cmake libffi-dev libssl-dev`

Install missing system packages:
```bash
sudo apt-get install -y openjdk-17-jdk libtool cmake libncurses5-dev libncursesw5-dev
```

### Build

```bash
source kivy_env/bin/activate
buildozer android debug
```

The first build downloads the Android SDK/NDK (~1 GB) and takes 20–40 minutes. Subsequent builds are fast.

The APK will be at `bin/TodoApp-1.0-arm64-v8a_armeabi-v7a-debug.apk`.

### Deploy to Device

Connect your phone with USB debugging enabled:

```bash
buildozer android debug deploy run
```

## Dependencies

| Package | Purpose |
|---|---|
| Kivy 2.3.1 | UI framework |
| Peewee | SQLite ORM |
| Cython 0.29.x | Required by python-for-android |
