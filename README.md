# Snap to Z=0

A simple Blender add-on for 3D print setup.

Snap to Z=0 uses the active face of a mesh to rotate the part onto the build plate, place it at **Z=0**, and optionally center the part on the world origin in **X/Y**.

https://github.com/user-attachments/assets/8b7e5020-30bf-4b72-8d96-8338e2b60ea5

## Features

- **Snap to Z=0**  
  Rotates the object so the active face points downward and places that face at **Z=0**

- **Center on XY Origin**  
  Calculates the center of the mesh bounding box on the platform-facing side and moves the part so it sits on **X=0, Y=0**

- Lightweight and simple
- Built for fast 3D print prep
- Lives in the **Tool** tab of the 3D Viewport sidebar

## Installation

1. Download `snap_to_z0.py`
2. Open Blender
3. Go to **Edit > Preferences > Add-ons**
4. Click **Install...**
5. Select `snap_to_z0.py`
6. Enable the **Snap to Z=0** add-on

## Usage

### 3D Scan Example:
https://github.com/user-attachments/assets/89b302d4-ec48-43e2-8102-dfcdc8c21f87

### Snap to Z=0

1. Select a mesh object
2. Enter **Edit Mode**
3. Select a face and make it the **active face**
4. Open the **3D Viewport Sidebar**
5. Go to the **Tool** tab
6. Click **Snap to Z=0**

### Center on XY Origin

1. Select a mesh object
2. In **Object Mode** or **Edit Mode**, open the **3D Viewport Sidebar**
3. Go to the **Tool** tab
4. Click **Center on XY Origin**

## License

MIT License
