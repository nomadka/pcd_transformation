import open3d as o3d
import numpy as np
import os
import o3d_viewer as lift


INPUT_DIR = "input_data"
INPUT_TRAJ = "traj.txt"
OUTPUT_DIR = "./output_data/o3d_corrected"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():

    
    # Load original trajectory matrices to extract camera poses
    poses = lift.load_standard_trajectory(INPUT_TRAJ)
    
    # Load original pointcloud files
    ply_files = lift.load_ply_files(INPUT_DIR)
    
    # Exact Matrix for Config Direct 10
    E = np.array([
        [-1,  0,  0,  0],
        [ 0,  0, -1,  0],
        [ 0,  1,  0,  0],
        [ 0,  0,  0,  1]
    ])
    
    # Global Z-Axis Reflection Matrix (Flips the combined world scene along Z)
    R_z = np.array([
        [1,  0,  0,  0],
        [0,  1,  0,  0],
        [0,  0, -1,  0],
        [0,  0,  0,  1]
    ])
    # Global X axis rotation by 90 degree 

    R_d90 = np.array([
        [1,  0,  0,  0],
        [0,  0, -1,  0],
        [0,  1,  0,  0],
        [0,  0,  0,  1]
    ])

    R_rotx = np.array([
        [1,  0,  0,  0],
        [0, -1,  0,  0],
        [0,  0, -1,  0],
        [0,  0,  0,  1]
    ])


    R_global = R_rotx @ R_d90 @ R_z
    
    # # Final Global Matrix: Handles Z-Mirroring, 90-degree tilt, facing direction, and right-side up orientation
    # R_global = np.array([
    #     [ 1,  0,  0,  0],
    #     [ 0,  0, -1,  0],
    #     [ 0, -1,  0,  0],
    #     [ 0,  0,  0,  1]
    # ])
    print("Generating globally mirrored point clouds (ASCII)...")
    for i, ply_file in enumerate(ply_files):
        if i >= len(poses):
            continue
            
        pcd = o3d.io.read_point_cloud(ply_file)
        M = poses[i]
        
        # Calculate the mathematical inverse of the current camera position
        M_inv = np.linalg.inv(M)
        
        # Cancel the pose, apply global reflection, re-apply pose, apply local shift
        T_composite = M_inv @ R_global @ M @ E
        
        # Transform the local points using the composite matrix
        pcd.transform(T_composite)
        
        # Save explicitly as an ASCII PLY file
        o3d.io.write_point_cloud(
            f"./{OUTPUT_DIR}/{os.path.basename(ply_file)}", 
            pcd, 
            write_ascii=True
        )
    
    # Copying the trajectory file to the outout directory
    print("Copying traj.txt for easy access...")
    with open(os.path.join(INPUT_DIR, INPUT_TRAJ), "r") as f_in, open(f"./{OUTPUT_DIR}/traj.txt", "w") as f_out:
        for line in f_in:
            f_out.write(line)
            
    print(f"Point cloud transformation completed. Find the transformed files in '{OUTPUT_DIR}'")

if __name__ == "__main__":
    main()