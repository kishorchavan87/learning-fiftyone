#!/usr/bin/env python3
import os, random
from PIL import Image, ImageDraw
import fiftyone as fo
import fiftyone.core.labels as fol
from fiftyone.core.dataset import dataset_exists, load_dataset

DATASET_NAME = "demo_synthetic"
APP_PORT = 5151
IMG_DIR = os.path.expanduser("~/fiftyone-demo/images")
os.makedirs(IMG_DIR, exist_ok=True)

def make_image(path, width=640, height=480, rects=[]):
    img = Image.new("RGB", (width, height), color=(255,255,255))
    draw = ImageDraw.Draw(img)
    for r in rects:
        draw.rectangle(r, outline=(255,0,0), width=3)
    img.save(path)

def create_synthetic_dataset(num_images=120):
    labels = ["person","car","bike"]
    if dataset_exists(DATASET_NAME):
        return load_dataset(DATASET_NAME)

    ds = fo.Dataset(DATASET_NAME)
    ds.persistent = True

    samples = []
    for i in range(num_images):
        w, h = 640, 480
        n_objs = random.randint(1,4)
        rects, detections = [], []
        for _ in range(n_objs):
            rw, rh = random.randint(40,180), random.randint(40,160)
            x1, y1 = random.randint(0, w-rw-1), random.randint(0, h-rh-1)
            x2, y2 = x1+rw, y1+rh
            rects.append((x1,y1,x2,y2))
            bbox = [x1/w, y1/h, rw/w, rh/h]
            label = random.choice(labels)
            detections.append(fol.Detection(label=label, bounding_box=bbox))
        img_path = os.path.join(IMG_DIR, f"img_{i:04d}.jpg")
        make_image(img_path, width=w, height=h, rects=rects)
        samples.append(fo.Sample(filepath=img_path,
                                 ground_truth=fol.Detections(detections=detections)))
    ds.add_samples(samples)
    return ds

def add_fake_predictions(dataset):
    for sample in dataset:
        if not sample.ground_truth: continue
        preds = []
        for det in sample.ground_truth.detections:
            x,y,w,h = det.bounding_box
            b = [x+random.uniform(-0.02,0.02), y+random.uniform(-0.02,0.02),
                 max(0.02,w*random.uniform(0.8,1.1)),
                 max(0.02,h*random.uniform(0.8,1.1))]
            preds.append(fol.Detection(label=det.label, bounding_box=b,
                                       confidence=random.uniform(0.5,0.95)))
        sample["predictions"] = fol.Detections(detections=preds)
        sample.save()

if __name__ == "__main__":
    ds = create_synthetic_dataset()
    add_fake_predictions(ds)
    session = fo.launch_app(ds, address="127.0.0.1", port=APP_PORT)
    session.wait()
