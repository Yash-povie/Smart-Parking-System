# Installation Guide

## Python 3.13 Compatibility Issues

If you're using Python 3.13 and encounter issues with Pillow or other packages, follow these steps:

### Option 1: Install with pip (Recommended)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If Pillow fails to install, try installing it separately:

```bash
pip install pillow --upgrade
```

### Option 2: Use Minimal Requirements First

If you encounter build errors, install minimal requirements first:

```bash
pip install -r requirements-minimal.txt
```

Then install Pillow, NumPy, and OpenCV separately:

```bash
pip install pillow numpy opencv-python
```

### Option 3: Use Python 3.11 or 3.12 (Most Compatible)

For the best compatibility, use Python 3.11 or 3.12:

```bash
# Using pyenv (recommended)
pyenv install 3.12.0
pyenv local 3.12.0

# Or using conda
conda create -n parking-system python=3.12
conda activate parking-system
```

### Option 4: Install Pre-built Wheels

For Windows, you can try installing pre-built wheels:

```bash
pip install --only-binary :all: pillow
```

## Troubleshooting

### Pillow Build Error

If you get a build error with Pillow on Python 3.13:

1. **Upgrade pip and setuptools:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. **Install build dependencies:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

3. **Try installing from pre-built wheel:**
   ```bash
   pip install pillow --only-binary :all:
   ```

4. **If all else fails, use Python 3.12:**
   Python 3.12 has better package compatibility at the moment.

### Other Common Issues

- **psycopg2-binary**: If this fails, make sure you have Visual C++ Build Tools on Windows
- **opencv-python**: May require additional system dependencies on Linux

## Verify Installation

After installation, verify everything works:

```bash
python -c "import fastapi; import uvicorn; print('✓ Core packages installed')"
python -c "import PIL; print('✓ Pillow installed')"  # Optional
```


