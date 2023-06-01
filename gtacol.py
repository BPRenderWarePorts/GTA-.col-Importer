import bpy
import struct

def read_int(file):
    return struct.unpack("i", file.read(4))[0]

def read_float(file):
    return struct.unpack("f", file.read(4))[0]

def read_vector(file):
    x = read_float(file)
    y = read_float(file)
    z = read_float(file)
    return (x, y, z)

def import_col(filepath):
    bpy.ops.object.select_all(action='DESELECT')
    
    with open(filepath, "rb") as col_file:
        magic = col_file.read(4).decode("ascii")
        if magic != "COL ":
            print("Invalid COL file format")
            return

        num_spheres = read_int(col_file)
        num_boxes = read_int(col_file)
        num_planes = read_int(col_file)
        num_polys = read_int(col_file)
        
        for _ in range(num_spheres):
            position = read_vector(col_file)
            radius = read_float(col_file)
            
            bpy.ops.mesh.primitive_uv_sphere_add(location=position, radius=radius)
            sphere = bpy.context.active_object
            sphere.name = "Sphere"
        
        for _ in range(num_boxes):
            min_bound = read_vector(col_file)
            max_bound = read_vector(col_file)
            
            center = [(min_bound[i] + max_bound[i]) / 2 for i in range(3)]
            dimensions = [(max_bound[i] - min_bound[i]) for i in range(3)]
            
            bpy.ops.mesh.primitive_cube_add(location=center, size=1)
            box = bpy.context.active_object
            box.dimensions = dimensions
            box.name = "Box"
        
        for _ in range(num_planes):
            normal = read_vector(col_file)
            distance = read_float(col_file)
            
            bpy.ops.mesh.primitive_plane_add(size=1)
            plane = bpy.context.active_object
            plane.location = normal
            plane.rotation_euler = (normal[0], normal[1], normal[2], distance)
            plane.name = "Plane"
        
        for _ in range(num_polys):
            num_vertices = read_int(col_file)
            vertices = []
            for _ in range(num_vertices):
                vertex = read_vector(col_file)
                vertices.append(vertex)
            
            mesh = bpy.data.meshes.new("Polygon")
            obj = bpy.data.objects.new("Polygon", mesh)
            bpy.context.collection.objects.link(obj)
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            mesh.from_pydata(vertices, [], [])
            mesh.update()
    
    print("COL file imported successfully")

# Usage example
col_file_path = "example.col"
import_col(col_file_path)
