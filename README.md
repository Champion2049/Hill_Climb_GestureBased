# Hill Climb Gesture-Based Control

Simple OpenCV-based Hill Climb Racing game control using MediaPipe Hand Landmarker.

## Quantized TFLite Pipeline

This project now uses the MediaPipe Tasks `HandLandmarker` pipeline backed by a
TFLite model bundle (`hand_landmarker.task`).

- Default mode: int8 (expects a local int8 task bundle).
- Default int8 path: `models/hand_landmarker_int8.task`.
- Float16 fallback mode is available when explicitly selected.

### Model Selection

Use environment variables:

- `HAND_LANDMARKER_VARIANT=int8|float16` (default: `int8`)
- `HAND_LANDMARKER_MODEL_PATH=...` to use any local `.task` model file
- `HAND_LANDMARKER_MODEL_URL=...` optional download URL when model file is missing

Notes:

- Public MediaPipe hand landmarker bundle is currently available as float16.
- For true int8, provide your own int8-compatible `.task` model bundle.

## Run

Install dependencies:

```bash
pip install mediapipe opencv-python
```

Start the controller:

```bash
python main.py
```

Run in float16 mode (auto-download from MediaPipe):

```bash
set HAND_LANDMARKER_VARIANT=float16
python main.py
```

Run in int8 mode with local model file:

```bash
set HAND_LANDMARKER_VARIANT=int8
set HAND_LANDMARKER_MODEL_PATH=models\hand_landmarker_int8.task
python main.py
```

## Startup Self-Check Output

At startup, the app prints model verification details, including:

- requested variant
- model source
- resolved model path
- model size
- model last-modified timestamp (UTC)
- SHA-256 hash

This helps confirm that the project is actually running the expected model.

Press `q` to quit.
