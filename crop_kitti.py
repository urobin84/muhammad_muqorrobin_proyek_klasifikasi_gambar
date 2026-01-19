import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from glob import glob

# Configuration
XML_DIR = "tracklets"
IMAGE_BASE_DIR = "raw_data"
OUTPUT_BASE_DIR = "dataset"
TARGET_SIZE = (150, 150)

class KittiProjection:
    def __init__(self, drive_path):
        calib_dir = os.path.join(drive_path, "calib")
        calib_cam_to_cam = os.path.join(calib_dir, "calib_cam_to_cam.txt")
        calib_velo_to_cam = os.path.join(calib_dir, "calib_velo_to_cam.txt")
        
        if not os.path.exists(calib_cam_to_cam) or not os.path.exists(calib_velo_to_cam):
            raise FileNotFoundError(f"Calibration files not found in {calib_dir}")

        self.P2 = self._read_calib_cam_to_cam(calib_cam_to_cam)
        self.Tr_velo_to_cam = self._read_calib_velo_to_cam(calib_velo_to_cam)
        self.R0_rect = self._read_R0_rect(calib_cam_to_cam)

    def _read_calib_cam_to_cam(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('P_rect_02:'):
                    data = line.split()[1:]
                    return np.array(data, dtype=np.float32).reshape(3, 4)
        raise ValueError("P_rect_02 not found in calibration file.")

    def _read_R0_rect(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('R_rect_00:'):
                    data = line.split()[1:]
                    R = np.array(data, dtype=np.float32).reshape(3, 3)
                    R0_rect = np.eye(4)
                    R0_rect[:3, :3] = R
                    return R0_rect
        raise ValueError("R_rect_00 not found in calibration file.")

    def _read_calib_velo_to_cam(self, filepath):
        R, T = None, None
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('R:'):
                    R = np.array(line.split()[1:], dtype=np.float32).reshape(3, 3)
                elif line.startswith('T:'):
                    T = np.array(line.split()[1:], dtype=np.float32).reshape(3, 1)
            
            if R is not None and T is not None:
                Tr = np.hstack((R, T))
                Tr_velo_to_cam = np.vstack((Tr, [0, 0, 0, 1]))
                return Tr_velo_to_cam
        raise ValueError("Transformation data not found in calib_velo_to_cam.")

    def project_velo_to_image(self, points):
        pts_3d_hom = np.hstack((points, np.ones((points.shape[0], 1))))
        pts_3d_rect = self.R0_rect @ self.Tr_velo_to_cam @ pts_3d_hom.T
        pts_2d_hom = self.P2 @ pts_3d_rect
        pts_2d = pts_2d_hom[:2, :] / pts_2d_hom[2, :]
        return pts_2d.T

def compute_3d_box_corners(h, w, l, tx, ty, tz, rz):
    R = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz),  np.cos(rz), 0],
        [0,           0,          1]
    ])
    x_corners = [l/2, l/2, -l/2, -l/2, l/2, l/2, -l/2, -l/2]
    y_corners = [w/2, -w/2, -w/2, w/2, w/2, -w/2, -w/2, w/2]
    z_corners = [0, 0, 0, 0, h, h, h, h]
    corners_3d = np.vstack([x_corners, y_corners, z_corners])
    corners_3d = R @ corners_3d + np.array([[tx], [ty], [tz]])
    return corners_3d.T

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def crop_objects():
    xml_files = glob(os.path.join(XML_DIR, "*.xml"))
    
    for xml_path in xml_files:
        print(f"Processing {xml_path}...")
        seq_id = os.path.basename(xml_path).split('_')[-1].replace('.xml', '')
        drive_path = os.path.join(IMAGE_BASE_DIR, f"drive_{seq_id}")
        
        try:
            projector = KittiProjection(drive_path)
        except Exception as e:
            print(f"Skipping sequence {seq_id}: {e}")
            continue

        img_dir = os.path.join(drive_path, "image_02", "data")
        if not os.path.exists(img_dir):
            img_dir = os.path.join(drive_path, "image_00", "data")
            if not os.path.exists(img_dir): continue

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for tracklet_idx, tracklet in enumerate(root.findall(".//tracklets/item")):
            obj_type = tracklet.find("objectType").text
            if obj_type not in ["Car", "Pedestrian", "Cyclist", "Van"]: continue
            
            h = float(tracklet.find("h").text)
            w = float(tracklet.find("w").text)
            l = float(tracklet.find("l").text)
            first_frame = int(tracklet.find("first_frame").text)

            category_dir = os.path.join(OUTPUT_BASE_DIR, obj_type.lower())
            ensure_dir(category_dir)

            for i, pose in enumerate(tracklet.findall(".//poses/item")):
                frame_idx = first_frame + i
                tx, ty, tz = float(pose.find("tx").text), float(pose.find("ty").text), float(pose.find("tz").text)
                rz = float(pose.find("rz").text)

                corners_3d = compute_3d_box_corners(h, w, l, tx, ty, tz, rz)
                corners_2d = projector.project_velo_to_image(corners_3d)
                
                xmin, ymin = np.min(corners_2d, axis=0)
                xmax, ymax = np.max(corners_2d, axis=0)

                img_path = os.path.join(img_dir, f"{frame_idx:010d}.png")
                if not os.path.exists(img_path): continue
                
                img = cv2.imread(img_path)
                if img is None: continue
                
                img_h, img_w = img.shape[:2]
                xmin, xmax = int(max(0, xmin)), int(min(img_w, xmax))
                ymin, ymax = int(max(0, ymin)), int(min(img_h, ymax))
                
                if xmax <= xmin or ymax <= ymin: continue
                
                crop = img[ymin:ymax, xmin:xmax]
                resized = cv2.resize(crop, TARGET_SIZE)
                
                save_name = f"{seq_id}_{tracklet_idx:03d}_{frame_idx:06d}.png"
                cv2.imwrite(os.path.join(category_dir, save_name), resized)

    print("Success: Dataset created!")

if __name__ == "__main__":
    crop_objects()
