"""
Script to help prepare dataset for training
Downloads sample data or helps structure existing data
"""

import os
import shutil
from pathlib import Path
import requests
from tqdm import tqdm


def download_sample_dataset():
    """
    Download sample parking lot images for training
    Note: In production, you'd use your own annotated dataset
    """
    print("📥 This would download sample dataset...")
    print("💡 For production, use your own parking lot images")
    print("💡 Annotate them using LabelImg or Roboflow")
    
    # Placeholder for dataset download
    # In real scenario, you'd download from:
    # - Roboflow Universe
    # - Your own data collection
    # - Public parking datasets
    
    print("\n📚 Recommended tools for annotation:")
    print("1. LabelImg: https://github.com/heartexlabs/labelImg")
    print("2. Roboflow: https://roboflow.com")
    print("3. CVAT: https://cvat.org")


def validate_dataset():
    """Validate dataset structure and files"""
    dataset_path = Path('dataset')
    
    if not dataset_path.exists():
        print("❌ Dataset directory not found")
        return False
    
    required_dirs = [
        'images/train',
        'images/val',
        'labels/train',
        'labels/val'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = dataset_path / dir_path
        if not full_path.exists():
            missing_dirs.append(str(full_path))
    
    if missing_dirs:
        print("❌ Missing directories:")
        for dir_path in missing_dirs:
            print(f"   - {dir_path}")
        return False
    
    # Check for images and labels
    train_images = list((dataset_path / 'images/train').glob('*.jpg')) + \
                   list((dataset_path / 'images/train').glob('*.png'))
    train_labels = list((dataset_path / 'labels/train').glob('*.txt'))
    
    val_images = list((dataset_path / 'images/val').glob('*.jpg')) + \
                 list((dataset_path / 'images/val').glob('*.png'))
    val_labels = list((dataset_path / 'labels/val').glob('*.txt'))
    
    print(f"\n📊 Dataset statistics:")
    print(f"   Training images: {len(train_images)}")
    print(f"   Training labels: {len(train_labels)}")
    print(f"   Validation images: {len(val_images)}")
    print(f"   Validation labels: {len(val_labels)}")
    
    if len(train_images) == 0:
        print("❌ No training images found!")
        return False
    
    if len(train_labels) == 0:
        print("❌ No training labels found!")
        return False
    
    if len(train_images) != len(train_labels):
        print("⚠️  Warning: Number of images and labels don't match!")
    
    print("✅ Dataset structure looks good!")
    return True


def split_dataset(source_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Split dataset into train/val/test sets
    
    Args:
        source_dir: Directory containing all images and labels
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        test_ratio: Ratio for test set
    """
    import random
    
    source_path = Path(source_dir)
    images = list(source_path.glob('*.jpg')) + list(source_path.glob('*.png'))
    
    random.shuffle(images)
    
    total = len(images)
    train_count = int(total * train_ratio)
    val_count = int(total * val_ratio)
    
    train_images = images[:train_count]
    val_images = images[train_count:train_count + val_count]
    test_images = images[train_count + val_count:]
    
    # Create directories
    for split in ['train', 'val', 'test']:
        os.makedirs(f'dataset/images/{split}', exist_ok=True)
        os.makedirs(f'dataset/labels/{split}', exist_ok=True)
    
    # Move images and corresponding labels
    splits = {
        'train': train_images,
        'val': val_images,
        'test': test_images
    }
    
    for split_name, image_list in splits.items():
        print(f"\n📦 Processing {split_name} set ({len(image_list)} images)...")
        for img_path in tqdm(image_list):
            # Copy image
            shutil.copy(img_path, f'dataset/images/{split_name}/{img_path.name}')
            
            # Copy corresponding label
            label_path = source_path / f'{img_path.stem}.txt'
            if label_path.exists():
                shutil.copy(label_path, f'dataset/labels/{split_name}/{label_path.name}')
            else:
                print(f"⚠️  Warning: No label found for {img_path.name}")
    
    print("✅ Dataset split completed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Prepare dataset for training')
    parser.add_argument('--validate', action='store_true', help='Validate dataset structure')
    parser.add_argument('--split', type=str, help='Split dataset from source directory')
    parser.add_argument('--download', action='store_true', help='Download sample dataset')
    
    args = parser.parse_args()
    
    if args.validate:
        validate_dataset()
    elif args.split:
        split_dataset(args.split)
    elif args.download:
        download_sample_dataset()
    else:
        print("Usage:")
        print("  python prepare_dataset.py --validate  # Validate dataset")
        print("  python prepare_dataset.py --split <dir>  # Split dataset")
        print("  python prepare_dataset.py --download  # Download sample data")


