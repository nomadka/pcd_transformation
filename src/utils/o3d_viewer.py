import open3d as o3d
import numpy as np
import glob
import os

INPUT_DIR = "input_data"
INPUT_TRAJ = "traj.txt"

def load_standard_trajectory(filepath):
    matrices = []
    with open(os.path.join(INPUT_DIR, filepath), 'r') as f:
        for line in f:
            values = list(map(float, line.strip().split()))
            if len(values) == 16:
                # Reshape standard row-major 4th-column matrix directly
                matrices.append(np.array(values).reshape(4, 4))
    return matrices
def load_ply_files(file_dir):
    
    return sorted(glob.glob(os.path.join(file_dir, '*.ply')))

def main():
 
    
    # Load the standard layout matrices
    poses = load_standard_trajectory(INPUT_TRAJ)
    
    # Load point cloud files
    ply_files = load_ply_files(INPUT_DIR)  
    
    combined_pcd = o3d.geometry.PointCloud()
    
    print("Loading and compiling developed files...")
    for i, ply_file in enumerate(ply_files):
        if i >= len(poses):
            break
            
        # Load the already corrected local point cloud
        pcd = o3d.io.read_point_cloud(ply_file)
        
        # Apply the standard trajectory matrix directly
        pcd.transform(poses[i])
        
        # Merge into master verification cloud
        combined_pcd += pcd
    
    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
    
    print("Opening Open3D verification window...")
    o3d.visualization.draw_geometries([combined_pcd, coord_frame])
    
    # o3d.io.write_point_cloud(
    #         f"./open3d_corrected/combined_pcd.ply", 
    #         combined_pcd, 
    #         write_ascii=True
    #     )

if __name__ == "__main__":
    main()