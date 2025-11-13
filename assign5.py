import open3d as o3d
import numpy as np
import copy
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def print_info(geometry, step_name):
    print(f"\n=== {step_name} ===")

    if isinstance(geometry, o3d.geometry.TriangleMesh):
        print(f"Vertices: {len(geometry.vertices)}")
        print(f"Triangles: {len(geometry.triangles)}")
        print(f"Has colors: {geometry.has_vertex_colors()}")
        print(f"Has normals: {geometry.has_vertex_normals()}")

    elif isinstance(geometry, o3d.geometry.PointCloud):
        print(f"Points: {len(geometry.points)}")
        print(f"Has colors: {geometry.has_colors()}")
        print(f"Has normals: {geometry.has_normals()}")

    elif isinstance(geometry, o3d.geometry.VoxelGrid):
        try:
            print(f"Voxels: {len(geometry.get_voxels())}")
        except:
            print("Could not count voxels.")


def main():

    # ===========================================================
    print("\n===== TASK 1: Load and Visualize Teapot =====")
    # ===========================================================

    mesh_path = "teapot.obj"
    mesh = o3d.io.read_triangle_mesh(mesh_path)

    if len(mesh.vertices) == 0:
        raise RuntimeError("Teapot OBJ not found or could not load.")

    mesh.compute_vertex_normals()
    print_info(mesh, "Original Teapot Mesh")

    o3d.visualization.draw_geometries([mesh], window_name="Task 1: Teapot Mesh")


   # ===========================================================
    print("\n===== TASK 2: Convert Mesh to Point Cloud =====")
# ===========================================================

# Convert mesh → point cloud (Poisson disk sampling)
    pcd = mesh.sample_points_poisson_disk(5000)

# Print required info
    print("\n=== Teapot Point Cloud ===")
    print(f"Vertices: {len(pcd.points)}")          # assignment wants "vertices"
    print(f"Has colors: {pcd.has_colors()}")
    print(f"Has normals: {pcd.has_normals()}")

# Display point cloud
    o3d.visualization.draw_geometries(
        [pcd],
        window_name="Task 2: Point Cloud"
)



    # ===========================================================
    print("\n===== TASK 3: Poisson Surface Reconstruction =====")
    # ===========================================================

    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )

    mesh_rec, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=7
    )

    # Crop artifacts
    bbox = pcd.get_axis_aligned_bounding_box()
    mesh_rec = mesh_rec.crop(bbox)

    mesh_rec.remove_degenerate_triangles()
    mesh_rec.remove_duplicated_triangles()
    mesh_rec.remove_duplicated_vertices()
    mesh_rec.remove_non_manifold_edges()

    print_info(mesh_rec, "Reconstructed Teapot Mesh")

    o3d.visualization.draw_geometries([mesh_rec], window_name="Task 3: Reconstructed Teapot")


    # ===========================================================
    print("\n===== TASK 4: Voxelization =====")
    # ===========================================================

    voxel_size = 0.25
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)

# === Print the required information ===
    num_vertices = len(voxel_grid.get_voxels())     # assignment calls them "vertices"
    has_color = hasattr(voxel_grid, "colors")       # voxel grid normally has no colors

    print(f"\n=== Voxel Grid (voxel size={voxel_size}) ===")
    print(f"Vertices (voxels): {num_vertices}")
    print(f"Has colors: {has_color}")

# Display voxel model
    o3d.visualization.draw_geometries(
        [voxel_grid],
        window_name="Task 4: Voxel Grid"
)



# ===========================================================
    print("\n===== TASK 5: Plane Creation (Matplotlib) =====")
# ===========================================================

    points = np.asarray(pcd.points)

    y_min, y_max = points[:, 1].min(), points[:, 1].max()
    z_min, z_max = points[:, 2].min(), points[:, 2].max()

    padding = 0.2

# Plane vertices (x=0)
    plane_vertices = np.array([
        [0, y_min - padding, z_min - padding],
        [0, y_max + padding, z_min - padding],
        [0, y_max + padding, z_max + padding],
        [0, y_min - padding, z_max + padding]
    ])

    print("\nPlotting plane + point cloud (Matplotlib)...")

    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

# Plot point cloud
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, c="blue")

# Plot plane using a polygon
    plane_collection = Poly3DCollection([plane_vertices], alpha=0.4)
    plane_collection.set_facecolor((0.6, 0.6, 0.6))
    ax.add_collection3d(plane_collection)

    ax.set_title("Task 5: Plane + Teapot (Matplotlib)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()


    print("\n===== TASK 6: Surface Clipping =====")

# Remove points on the right side of plane x > 0
    mask = points[:, 0] <= 0
    clipped_points = points[mask]

# Create clipped point cloud
    clipped_cloud = o3d.geometry.PointCloud()
    clipped_cloud.points = o3d.utility.Vector3dVector(clipped_points)

# If original had normals/colors — keep them
    if pcd.has_normals():
        clipped_cloud.normals = o3d.utility.Vector3dVector(np.asarray(pcd.normals)[mask])

    if pcd.has_colors():
        clipped_cloud.colors = o3d.utility.Vector3dVector(np.asarray(pcd.colors)[mask])

# === Print information required by assignment ===
    print("\n=== Clipped Point Cloud ===")
    print(f"Remaining vertices: {len(clipped_cloud.points)}")
    print(f"Triangles: 0   (point cloud has no triangles)")
    print(f"Has colors: {clipped_cloud.has_colors()}")
    print(f"Has normals: {clipped_cloud.has_normals()}")

# === Show clipped model ===
    o3d.visualization.draw_geometries(
        [clipped_cloud],
        window_name="Task 6: Clipped Point Cloud"
)


    print("\n===== TASK 7: Height Coloring + Extremes (Matplotlib) =====")

# Convert point cloud to numpy
    points = np.asarray(pcd.points)

# Compute Z values
    z_vals = points[:, 2]
    z_min, z_max = z_vals.min(), z_vals.max()

# Normalize Z values for coloring
    norm_z = (z_vals - z_min) / (z_max - z_min + 1e-8)

# Create colors
    colors = np.zeros((len(points), 3))
    colors[:, 0] = norm_z         # Red = high Z
    colors[:, 2] = 1 - norm_z     # Blue = low Z

# Apply colors
    colored = copy.deepcopy(pcd)
    colored.colors = o3d.utility.Vector3dVector(colors)

# --- FIND EXTREME POINTS ---
    idx_min = np.argmin(z_vals)
    idx_max = np.argmax(z_vals)

    min_point = points[idx_min]
    max_point = points[idx_max]

# Print required assignment info
    print(f"Min Z point: {min_point}  (Z = {z_min:.3f})")
    print(f"Max Z point: {max_point}  (Z = {z_max:.3f})")

# --- Plot using Matplotlib ---
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(points[:,0], points[:,1], points[:,2], c=colors, s=2)

# Mark extreme points
    ax.scatter(min_point[0], min_point[1], min_point[2], c='green', s=80, label="Min Z")
    ax.scatter(max_point[0], max_point[1], max_point[2], c='magenta', s=80, label="Max Z")

    ax.set_title("Task 7: Z-Coloring + Extremes")
    ax.legend()

    plt.show()

if __name__ == "__main__":
    main()
