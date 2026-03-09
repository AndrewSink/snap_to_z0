# Snap to Z=0

A simple Blender add-on for rotating a mesh using the active face and placing that face at Z=0 for faster 3D print setup.

https://github.com/user-attachments/assets/cca609a8-30ea-43c2-9da2-d289b396a977

## What it does

Snap to Z=0 uses the **active face** of a mesh in **Edit Mode** to:

- rotate the object so the selected face points downward
- move the object so that face sits at **Z=0**

This makes it easy to place models flat on the build plate before exporting for 3D printing.

## Features

- Simple one-click workflow
- Uses the active face for placement
- Rotates and translates automatically
- Lives in the **Tool** tab of the 3D Viewport sidebar
- Lightweight single-file add-on

## Installation

1. Download `snap_to_z0.py`
2. Open Blender
3. Go to **Edit > Preferences > Add-ons**
4. Click **Install...**
5. Select `snap_to_z0.py`
6. Enable the **Snap to Z=0** add-on

## Usage

1. Select a mesh object
2. Enter **Edit Mode**
3. Select a face and make it the **active face**
4. Open the **3D Viewport Sidebar**
5. Go to the **Tool** tab
6. Find **Snap to Z=0**
7. Click **Snap to Z=0**

## License

MIT License
