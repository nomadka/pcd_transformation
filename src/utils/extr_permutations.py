import open3d as o3d
import numpy as np
import itertools
import o3d_viewer as lift


INPUT_DIR = "input_data"
INPUT_TRAJ = "traj.txt"

def generate_extrinsic_permutations():
    """Generates all 24 possible 3x3 axis swapping and flipping matrices."""
    matrices = []
    for perm in itertools.permutations([0, 1, 2]):
        for signs in itertools.product([-1, 1], repeat=3):
            E = np.zeros((3, 3))
            for i in range(3):
                E[i, perm[i]] = signs[i]
            E4 = np.eye(4)
            E4[:3, :3] = E
            matrices.append(E4)
    return matrices

def main():

    # Load original trajectory matrices to extract camera poses
    poses = lift.load_standard_trajectory(INPUT_TRAJ)
    # Load original pointcloud files
    ply_files = lift.load_ply_files(INPUT_DIR)

    E_candidates = generate_extrinsic_permutations()
    
    matrix_formats = ["direct", "inverse"]

    for fmt in matrix_formats:
        for idx, E in enumerate(E_candidates):
            combined = o3d.geometry.PointCloud()
            
            for i, ply_file in enumerate(ply_files):
                pcd = o3d.io.read_point_cloud(ply_file)
                
                # Select trajectory matrix format
                if fmt == "direct":
                    M = poses[i]
                elif fmt == "inverse":
                    M = np.linalg.inv(poses[i])
                
                # Apply Extrinsic E first, then Trajectory M
                pcd.transform(E)
                pcd.transform(M)
                combined += pcd
            
            print(f"Testing Format: {fmt} | Extrinsic Config #{idx+1}")
            print(f"Extrinsic Matrix: \n{E}")
            print("Close window to check the next configuration...")
            
            coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
            o3d.visualization.draw_geometries([combined, coord_frame], 
                                              window_name=f"{fmt} - Config {idx+1}")

if __name__ == "__main__":
    main()