# Training Guide for Parking Slot Detection Model

## Overview

This guide will help you train a custom YOLOv8 model for parking slot detection using your own data.

## Step 1: Collect Data

### Option 1: Use Your Own Parking Lot Images
1. Take photos/videos of your parking lots
2. Capture different times of day, weather conditions, and angles
3. Aim for at least 500-1000 images for good results

### Option 2: Use Public Datasets
- **PKLot Dataset**: https://web.inf.ufpr.br/vri/databases/parking-lot-database/
- **CNRPark+EXT**: https://github.com/fabiocarrara/CNRPark-EXT
- **Roboflow Universe**: https://universe.roboflow.com (search for parking datasets)

## Step 2: Annotate Your Data

### Using LabelImg (Recommended for beginners)

1. **Install LabelImg:**
```bash
pip install labelImg
labelImg
```

2. **Annotate images:**
   - Open image folder
   - Draw bounding boxes around:
     - Empty parking slots
     - Occupied parking slots (vehicles)
   - Save as YOLO format (.txt files)

### Using Roboflow (Recommended for collaborative annotation)

1. **Sign up at**: https://roboflow.com
2. **Upload images**
3. **Annotate online** (collaborative)
4. **Export in YOLOv8 format**

### Annotation Guidelines

- **Empty Slot**: Draw box around the parking space (no vehicle)
- **Occupied Slot**: Draw box around the vehicle in the space
- **Be consistent**: Same size boxes for similar objects
- **Multiple angles**: Annotate from different camera angles

## Step 3: Prepare Dataset Structure

```bash
# Run the preparation script
python prepare_dataset.py --prepare
```

This creates:
```
dataset/
├── images/
│   ├── train/    (70% of images)
│   ├── val/      (20% of images)
│   └── test/     (10% of images)
└── labels/
    ├── train/    (Corresponding labels)
    ├── val/
    └── test/
```

### Split Your Dataset

If you have all images in one folder:

```bash
python prepare_dataset.py --split /path/to/your/images
```

## Step 4: Configure Dataset

The script creates `dataset/dataset.yaml`:

```yaml
path: dataset
train: images/train
val: images/val
test: images/test
nc: 2
names: ['empty_slot', 'occupied_slot']
```

## Step 5: Train the Model

### Basic Training

```bash
python train_model.py --model-size n --epochs 100
```

### Advanced Training

```bash
# Larger model (better accuracy, slower)
python train_model.py --model-size m --epochs 200 --batch 32

# With GPU (much faster)
# Make sure CUDA is installed
python train_model.py --model-size s --epochs 150
```

### Training Parameters

- `--model-size`: n (nano), s (small), m (medium), l (large), x (xlarge)
  - **nano**: Fastest, least accurate, good for testing
  - **small**: Good balance
  - **medium/large**: Better accuracy, slower
  - **xlarge**: Best accuracy, very slow

- `--epochs`: Number of training iterations (100-300 recommended)
- `--batch`: Batch size (16-32 for most GPUs)
- `--imgsz`: Image size (640 is standard)

## Step 6: Monitor Training

Training creates:
- `runs/detect/parking_slot_detector/` - Training results
- `results.png` - Training curves
- `confusion_matrix.png` - Model performance
- `weights/best.pt` - Best model weights

### Check Training Progress

```bash
# View training plots
# Open runs/detect/parking_slot_detector/results.png
```

## Step 7: Evaluate Model

After training, the model is automatically saved to:
- `models/parking_slot_detector.pt`

### Test the Model

```python
from ultralytics import YOLO

model = YOLO('models/parking_slot_detector.pt')
results = model('path/to/test/image.jpg')
results[0].show()  # Display results
```

## Step 8: Deploy Model

The trained model is automatically used by the AI service:

```bash
# Start AI service
cd ai-service
python app.py
```

The service will load `models/parking_slot_detector.pt` automatically.

## Tips for Better Results

1. **More Data = Better Model**: Aim for 1000+ images minimum
2. **Diverse Data**: Include different:
   - Times of day (day, night, dusk)
   - Weather conditions
   - Camera angles
   - Parking lot types
3. **Quality Annotations**: Accurate bounding boxes are crucial
4. **Data Augmentation**: YOLOv8 does this automatically
5. **Transfer Learning**: Starts from pre-trained weights (faster training)

## Troubleshooting

### Low Accuracy
- Add more training data
- Check annotation quality
- Train for more epochs
- Use larger model size

### Training Too Slow
- Use smaller model (nano or small)
- Reduce batch size
- Use GPU if available
- Reduce image size

### Out of Memory
- Reduce batch size
- Use smaller model
- Reduce image size

## Next Steps

1. **Collect real parking lot images**
2. **Annotate using LabelImg or Roboflow**
3. **Train with your data**
4. **Deploy and test**
5. **Iterate and improve**

## Resources

- **YOLOv8 Docs**: https://docs.ultralytics.com
- **LabelImg**: https://github.com/heartexlabs/labelImg
- **Roboflow**: https://roboflow.com
- **YOLOv8 Training Guide**: https://docs.ultralytics.com/modes/train/


