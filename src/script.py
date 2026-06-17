import open3d as o3d
import numpy as np
import os
import utils.loader as load


''' The program applies the transformation matrix to the raw pont cloud files 
and convert that into geometrically consistent and generate and replaces the 
poses with an identity matrix'''

INPUT_DIR = "input_data"
INPUT_TRAJ = "traj.txt"
OUTPUT_DIR = "./output_data/viewer_corrected"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def viewer_transformation():
    
    # Load original trajectory matrices to extract camera poses
    poses = load.load_traj_file(file_dir=INPUT_DIR, file_name=INPUT_TRAJ)
    
    # Load original pointcloud files
    ply_files = load.load_ply_files(INPUT_DIR)
    
    # Exact Matrix for Config Direct 10 (Local Fix)
    E = np.array([
        [-1,  0,  0,  0],
        [ 0,  0, -1,  0],
        [ 0,  1,  0,  0],
        [ 0,  0,  0,  1]
    ])
    
    # Open3d axis correction :  Flip along Z-axis, 90-degree rotation of X-axis, 180-degree rotation of Y-axis
    # R_o3d_correction = R_rot_y . R_tilt_x . R_flip_z
    
    R_o3d_corrections = np.array([
        [ 1,  0,  0,  0],
        [ 0,  0, -1,  0],
        [ 0, -1,  0,  0],
        [ 0,  0,  0,  1]
    ])
    
    # Adapting to viewer co-ordinate system : X-Horizontal, Y-Vertical, Z-Depth
    

    # Rotating Z-axis 180 degree along Y-axis
    
    R_y180 = np.array([
        [-1,  0,  0,  0],
        [ 0,  1,  0,  0],
        [ 0,  0, -1,  0],
        [ 0,  0,  0,  1]
    ])
    
    #  Inverting horizontal X-axis
    
    R_flip_x = np.array([
        [-1,  0,  0,  0],
        [ 0,  1,  0,  0],
        [ 0,  0,  1,  0],
        [ 0,  0,  0,  1]
    ])
    
    #Inverting Y-axis upside down (See the image in README.md for better understanding) 
    
    R_flip_y = np.array([
        [ 1,  0,  0,  0],
        [ 0, -1,  0,  0],
        [ 0,  0,  1,  0],
        [ 0,  0,  0,  1]
    ])

    R_viewer_correction = R_flip_y @ R_flip_x @ R_y180

    # Final orientation correction matrix.

    R_global = R_viewer_correction @ R_o3d_corrections
    
    print("Generating transformed world-space point clouds...")
    for i, ply_file in enumerate(ply_files):
        if i >= len(poses):
            continue
    
        pcd = o3d.io.read_point_cloud(ply_file)
        M = poses[i]
        
        # Mathematical inverse of pose to get Camera Pose (Camera-to-World)
        # M_pose = np.linalg.inv(M)
         
        # Apply E (Local Frame) -> Move to World (M_pose) -> Rotate Global Scene (R_global)
        T_world = R_global @ M @ E
        
        # Transform the points directly into their final Global World Space
        pcd.transform(T_world)
        
        # Save explicitly as an ASCII PLY file
        o3d.io.write_point_cloud(
            os.path.join(OUTPUT_DIR, os.path.basename(ply_file)), 
            pcd, 
            write_ascii=True
        )
    
    # The trajectory file must be filled with Identity matrices to prevent the viewer from applying the transformation a second time.
    print("Generating Identity traj.txt...")
    out_traj_path = os.path.join(OUTPUT_DIR, "traj.txt")
    with open(out_traj_path, "w") as f_out:
        identity_flat = np.eye(4).flatten(order='C')
        line = " ".join(str(val) for val in identity_flat)
        for _ in range(len(poses)):
            f_out.write(line + "\n")
            
    print(f"Viewer transformation of point clouds and poses completed. Find the files in '{OUTPUT_DIR}'")

if __name__ == "__main__":
    viewer_transformation()