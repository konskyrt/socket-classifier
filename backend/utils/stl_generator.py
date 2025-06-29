import numpy as np
from stl import mesh
import math
import json

class STLGenerator:
    def __init__(self):
        self.default_wall_thickness = 2.0  # mm
        self.default_depth = 20.0  # mm
    
    def generate_outlet_stl(self, product_specs, arrangement, custom_options, output_path):
        """Generate STL file for power outlet"""
        try:
            # Get dimensions and geometry
            dimensions = product_specs.get('dimensions', {})
            geometry_data = product_specs.get('geometry_data', {})
            
            # Calculate arrangement multipliers
            arrangement_config = self._get_arrangement_config(arrangement)
            
            # Generate mesh based on outlet type
            outlet_type = product_specs.get('outlet_type', 'NEMA_5-15R')
            vertices, faces = self._generate_outlet_geometry(
                outlet_type, dimensions, geometry_data, arrangement_config, custom_options
            )
            
            # Create STL mesh
            outlet_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
            
            for i, face in enumerate(faces):
                for j in range(3):
                    outlet_mesh.vectors[i][j] = vertices[face[j]]
            
            # Save to file
            outlet_mesh.save(output_path)
            
            print(f"STL file generated successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error generating STL: {e}")
            return False
    
    def _get_arrangement_config(self, arrangement):
        """Get configuration for outlet arrangement"""
        configs = {
            'single': {'count': 1, 'spacing': 0, 'layout': 'single'},
            'double': {'count': 2, 'spacing': 80, 'layout': 'horizontal'},
            'triple': {'count': 3, 'spacing': 60, 'layout': 'horizontal'},
            'quad': {'count': 4, 'spacing': 50, 'layout': 'grid'}
        }
        return configs.get(arrangement, configs['single'])
    
    def _generate_outlet_geometry(self, outlet_type, dimensions, geometry_data, arrangement_config, custom_options):
        """Generate 3D geometry for outlet"""
        
        width = dimensions.get('width', 70)
        height = dimensions.get('height', 70)
        depth = custom_options.get('depth', self.default_depth)
        wall_thickness = custom_options.get('wall_thickness', self.default_wall_thickness)
        
        vertices = []
        faces = []
        
        if outlet_type == 'NEMA_5-15R':
            vertices, faces = self._generate_nema_5_15r(width, height, depth, wall_thickness, geometry_data, arrangement_config)
        elif outlet_type == 'BS_1363':
            vertices, faces = self._generate_bs_1363(width, height, depth, wall_thickness, geometry_data, arrangement_config)
        elif outlet_type == 'CEE_7/4':
            vertices, faces = self._generate_cee_7_4(width, height, depth, wall_thickness, geometry_data, arrangement_config)
        elif outlet_type == 'USB_A':
            vertices, faces = self._generate_usb_a(width, height, depth, wall_thickness, geometry_data, arrangement_config)
        else:
            # Default to NEMA 5-15R
            vertices, faces = self._generate_nema_5_15r(width, height, depth, wall_thickness, geometry_data, arrangement_config)
        
        return vertices, faces
    
    def _generate_nema_5_15r(self, width, height, depth, wall_thickness, geometry_data, arrangement_config):
        """Generate NEMA 5-15R outlet geometry"""
        vertices = []
        faces = []
        
        # Convert mm to model units
        w, h, d = width/2, height/2, depth
        wt = wall_thickness
        
        count = arrangement_config['count']
        spacing = arrangement_config.get('spacing', 0)
        
        for i in range(count):
            x_offset = (i - (count-1)/2) * spacing if count > 1 else 0
            
            # Outer box vertices
            outer_vertices = [
                [-w + x_offset, -h, 0],      # 0: bottom-left-front
                [w + x_offset, -h, 0],       # 1: bottom-right-front
                [w + x_offset, h, 0],        # 2: top-right-front
                [-w + x_offset, h, 0],       # 3: top-left-front
                [-w + x_offset, -h, -d],     # 4: bottom-left-back
                [w + x_offset, -h, -d],      # 5: bottom-right-back
                [w + x_offset, h, -d],       # 6: top-right-back
                [-w + x_offset, h, -d]       # 7: top-left-back
            ]
            
            # Inner cavity vertices (for hollow outlet)
            inner_vertices = [
                [-w + wt + x_offset, -h + wt, -wt],        # 8: inner bottom-left-front
                [w - wt + x_offset, -h + wt, -wt],         # 9: inner bottom-right-front
                [w - wt + x_offset, h - wt, -wt],          # 10: inner top-right-front
                [-w + wt + x_offset, h - wt, -wt],         # 11: inner top-left-front
                [-w + wt + x_offset, -h + wt, -d + wt],    # 12: inner bottom-left-back
                [w - wt + x_offset, -h + wt, -d + wt],     # 13: inner bottom-right-back
                [w - wt + x_offset, h - wt, -d + wt],      # 14: inner top-right-back
                [-w + wt + x_offset, h - wt, -d + wt]      # 15: inner top-left-back
            ]
            
            base_idx = len(vertices)
            vertices.extend(outer_vertices + inner_vertices)
            
            # Add holes for plugs (simplified as cylinders)
            holes = geometry_data.get('holes', [])
            for hole in holes:
                hole_vertices, hole_faces = self._create_cylinder_hole(
                    hole['x'] + x_offset, hole['y'], 0, 
                    hole['diameter']/2, d, 12
                )
                hole_base_idx = len(vertices)
                vertices.extend(hole_vertices)
                faces.extend([[f[0] + hole_base_idx, f[1] + hole_base_idx, f[2] + hole_base_idx] for f in hole_faces])
            
            # Outer faces
            outer_faces = [
                # Front face (with holes cut out - simplified)
                [base_idx + 0, base_idx + 1, base_idx + 2], [base_idx + 0, base_idx + 2, base_idx + 3],
                # Back face
                [base_idx + 4, base_idx + 7, base_idx + 6], [base_idx + 4, base_idx + 6, base_idx + 5],
                # Left face
                [base_idx + 0, base_idx + 3, base_idx + 7], [base_idx + 0, base_idx + 7, base_idx + 4],
                # Right face
                [base_idx + 1, base_idx + 5, base_idx + 6], [base_idx + 1, base_idx + 6, base_idx + 2],
                # Top face
                [base_idx + 3, base_idx + 2, base_idx + 6], [base_idx + 3, base_idx + 6, base_idx + 7],
                # Bottom face
                [base_idx + 0, base_idx + 4, base_idx + 5], [base_idx + 0, base_idx + 5, base_idx + 1]
            ]
            
            # Inner faces (to create hollow interior)
            inner_faces = [
                # Inner front face
                [base_idx + 8, base_idx + 11, base_idx + 10], [base_idx + 8, base_idx + 10, base_idx + 9],
                # Inner back face
                [base_idx + 12, base_idx + 13, base_idx + 14], [base_idx + 12, base_idx + 14, base_idx + 15],
                # Inner walls
                [base_idx + 8, base_idx + 9, base_idx + 13], [base_idx + 8, base_idx + 13, base_idx + 12],
                [base_idx + 9, base_idx + 10, base_idx + 14], [base_idx + 9, base_idx + 14, base_idx + 13],
                [base_idx + 10, base_idx + 11, base_idx + 15], [base_idx + 10, base_idx + 15, base_idx + 14],
                [base_idx + 11, base_idx + 8, base_idx + 12], [base_idx + 11, base_idx + 12, base_idx + 15]
            ]
            
            faces.extend(outer_faces + inner_faces)
        
        return vertices, faces
    
    def _generate_bs_1363(self, width, height, depth, wall_thickness, geometry_data, arrangement_config):
        """Generate BS 1363 (UK) outlet geometry"""
        # Similar to NEMA but with different hole pattern
        return self._generate_nema_5_15r(width, height, depth, wall_thickness, geometry_data, arrangement_config)
    
    def _generate_cee_7_4(self, width, height, depth, wall_thickness, geometry_data, arrangement_config):
        """Generate CEE 7/4 (Schuko) outlet geometry"""
        # Similar to NEMA but with different hole pattern and ground clips
        return self._generate_nema_5_15r(width, height, depth, wall_thickness, geometry_data, arrangement_config)
    
    def _generate_usb_a(self, width, height, depth, wall_thickness, geometry_data, arrangement_config):
        """Generate USB-A outlet geometry"""
        vertices = []
        faces = []
        
        w, h, d = width/2, height/2, depth
        wt = wall_thickness
        
        count = arrangement_config['count']
        spacing = arrangement_config.get('spacing', 30)
        
        for i in range(count):
            y_offset = (i - (count-1)/2) * spacing if count > 1 else 0
            
            # Simple rectangular USB port
            usb_vertices = [
                [-w, -h + y_offset, 0], [w, -h + y_offset, 0],
                [w, h + y_offset, 0], [-w, h + y_offset, 0],
                [-w, -h + y_offset, -d], [w, -h + y_offset, -d],
                [w, h + y_offset, -d], [-w, h + y_offset, -d]
            ]
            
            base_idx = len(vertices)
            vertices.extend(usb_vertices)
            
            # Simple box faces
            usb_faces = [
                [base_idx + 0, base_idx + 1, base_idx + 2], [base_idx + 0, base_idx + 2, base_idx + 3],
                [base_idx + 4, base_idx + 7, base_idx + 6], [base_idx + 4, base_idx + 6, base_idx + 5],
                [base_idx + 0, base_idx + 3, base_idx + 7], [base_idx + 0, base_idx + 7, base_idx + 4],
                [base_idx + 1, base_idx + 5, base_idx + 6], [base_idx + 1, base_idx + 6, base_idx + 2],
                [base_idx + 3, base_idx + 2, base_idx + 6], [base_idx + 3, base_idx + 6, base_idx + 7],
                [base_idx + 0, base_idx + 4, base_idx + 5], [base_idx + 0, base_idx + 5, base_idx + 1]
            ]
            
            faces.extend(usb_faces)
        
        return vertices, faces
    
    def _create_cylinder_hole(self, x, y, z, radius, depth, segments=12):
        """Create cylindrical hole geometry"""
        vertices = []
        faces = []
        
        # Create cylinder vertices
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            cx = x + radius * math.cos(angle)
            cy = y + radius * math.sin(angle)
            vertices.append([cx, cy, z])  # Front circle
            vertices.append([cx, cy, z - depth])  # Back circle
        
        # Create cylinder faces
        for i in range(segments):
            next_i = (i + 1) % segments
            # Side faces
            faces.append([i*2, next_i*2, next_i*2 + 1])
            faces.append([i*2, next_i*2 + 1, i*2 + 1])
        
        return vertices, faces 