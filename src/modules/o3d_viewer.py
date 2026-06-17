import open3d as o3d
import numpy as np
import glob
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
import src.utils.loader as load 


INPUT_DIR = "input_data"
INPUT_TRAJ = "traj.txt"

def main():
 
    
    # Load the standard layout matrices
    poses = load.load_traj_file(file_dir=INPUT_DIR, file_name=INPUT_TRAJ)
    
    # Load point cloud files
    ply_files = load.load_ply_files(INPUT_DIR)  
    
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