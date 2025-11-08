"""
Training script for parking slot detection model using YOLOv8
"""

from ultralytics import YOLO
from pathlib import Path
import yaml
import os


def create_dataset_config():
    """Create dataset configuration file"""
    config = {
        'path': 'dataset',  # Path to dataset root
        'train': 'images/train',  # Training images
        'val': 'images/val',  # Validation images
        'test': 'images/test',  # Test images (optional)
        'nc': 2,  # Number of classes
        'names': ['empty_slot', 'occupied_slot']  # Class names
    }
    
    os.makedirs('dataset', exist_ok=True)
    with open('dataset/dataset.yaml', 'w') as f:
        yaml.dump(config, f)
    
    print("✅ Created dataset configuration at dataset/dataset.yaml")
    return config


def train_model(
    model_size='n',  # n=nano, s=small, m=medium, l=large, x=xlarge
    epochs=100,
    imgsz=640,
    batch=16,
    data='dataset/dataset.yaml'
):
    """
    Train YOLOv8 model for parking slot detection
    
    Args:
        model_size: Model size (n, s, m, l, x)
        epochs: Number of training epochs
        imgsz: Image size
        batch: Batch size
        data: Path to dataset config
    """
    print("🚀 Starting model training...")
    print(f"📊 Model size: YOLOv8{model_size}")
    print(f"🔄 Epochs: {epochs}")
    print(f"📐 Image size: {imgsz}")
    print(f"📦 Batch size: {batch}")
    
    # Load pre-trained model
    model = YOLO(f'yolov8{model_size}.pt')
    
    # Train the model
    results = model.train(
        data=data,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        name='parking_slot_detector',
        project='runs',
        patience=50,  # Early stopping patience
        save=True,
        save_period=10,  # Save checkpoint every 10 epochs
        val=True,  # Validate during training
        plots=True,  # Generate training plots
        device='cuda' if os.system('nvidia-smi') == 0 else 'cpu'  # Use GPU if available
    )
    
    # Save the best model
    best_model_path = Path('runs/detect/parking_slot_detector/weights/best.pt')
    target_path = Path('models/parking_slot_detector.pt')
    
    if best_model_path.exists():
        import shutil
        os.makedirs('models', exist_ok=True)
        shutil.copy(best_model_path, target_path)
        print(f"✅ Model saved to {target_path}")
    else:
        print("⚠️  Best model not found, check training results")
    
    print("✅ Training completed!")
    return results


def prepare_dataset_structure():
    """Create dataset directory structure"""
    dirs = [
        'dataset/images/train',
        'dataset/images/val',
        'dataset/images/test',
        'dataset/labels/train',
        'dataset/labels/val',
        'dataset/labels/test',
        'models'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("✅ Created dataset directory structure")
    print("\n📁 Dataset structure:")
    print("dataset/")
    print("├── images/")
    print("│   ├── train/  (Put training images here)")
    print("│   ├── val/    (Put validation images here)")
    print("│   └── test/   (Put test images here)")
    print("└── labels/")
    print("    ├── train/  (Put training labels here)")
    print("    ├── val/    (Put validation labels here)")
    print("    └── test/   (Put test labels here)")
    print("\n💡 Use LabelImg or Roboflow to annotate your images")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train parking slot detection model')
    parser.add_argument('--model-size', type=str, default='n', choices=['n', 's', 'm', 'l', 'x'],
                        help='Model size: n=nano, s=small, m=medium, l=large, x=xlarge')
    parser.add_argument('--epochs', type=int, default=100, help='Number of training epochs')
    parser.add_argument('--imgsz', type=int, default=640, help='Image size')
    parser.add_argument('--batch', type=int, default=16, help='Batch size')
    parser.add_argument('--prepare', action='store_true', help='Prepare dataset structure only')
    
    args = parser.parse_args()
    
    if args.prepare:
        prepare_dataset_structure()
        create_dataset_config()
    else:
        # Check if dataset exists
        if not Path('dataset/dataset.yaml').exists():
            print("⚠️  Dataset config not found. Creating structure...")
            prepare_dataset_structure()
            create_dataset_config()
            print("\n📝 Please add your images and labels to the dataset directories")
            print("💡 Then run this script again to start training")
        else:
            train_model(
                model_size=args.model_size,
                epochs=args.epochs,
                imgsz=args.imgsz,
                batch=args.batch
            )


