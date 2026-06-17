
import open3d as o3d
import numpy as np
import glob
import os

''' These are the helper functions which allows to load the poses and all the point clouds in a directory into a variable'''

def load_traj_file(file_dir, file_name):
    
    matrices = []
    with open(os.path.join(file_dir, file_name), 'r') as f:
        for line in f:
            values = list(map(float, line.strip().split()))
            if len(values) == 16:
                # Reshape standard row-major 4th-column matrix directly
                matrices.append(np.array(values, dtype=np.float64).reshape(4, 4))
    
    return matrices

def load_ply_files(file_dir):
    
    return sorted(glob.glob(os.path.join(file_dir, '*.ply')))