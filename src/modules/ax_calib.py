import open3d as o3d
import numpy as np
import os


''' This program creates a dummy point cloud of co-ordinate axis replaces the poses 
    with identity matrix for detecting the co-ordinate system of the viewer '''


OUTPUT_DIR = "output_data/diagnostics"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_calibration_test():

    
    # 1. Create Asymmetric Axis Point Cloud
    points = []
    colors = []
    
    # X Axis - Red (Shortest)
    for i in np.linspace(0, 1, 100):
        points.append([i, 0, 0])
        colors.append([1, 0, 0])
        
    # Y Axis - Green (Medium)
    for i in np.linspace(0, 2, 200):
        points.append([0, i, 0])
        colors.append([0, 1, 0])
        
    # Z Axis - Blue (Longest)
    for i in np.linspace(0, 3, 300):
        points.append([0, 0, i])
        colors.append([0, 0, 1])
        
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.array(points, dtype=np.float64))
    pcd.colors = o3d.utility.Vector3dVector(np.array(colors, dtype=np.float64))
    
    o3d.io.write_point_cloud(f"{OUTPUT_DIR}/calibration_axis.ply", pcd, write_ascii=True)
    
    # 2. Create Neutral Trajectory (Identity Matrix)
    identity_flat = np.eye(4, dtype=np.float64).flatten(order='C')
    line = " ".join(str(val) for val in identity_flat)
    
    # Write one line so the viewer loads the single cloud without moving it
    with open(f"{OUTPUT_DIR}/traj.txt", "w") as f_out:
        f_out.write(line + "\n")
        
    print(f"Dummy axis and poses are created, Find the files in folder : '{OUTPUT_DIR}'")

if __name__ == "__main__":
    create_calibration_test()