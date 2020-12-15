import math
import numpy
from bpy_extras.view3d_utils import location_3d_to_region_2d
import bpy

class Transform():

    def __init__(self):
        pass

    def get_cartesian_coordinates_from_spherical(self,spherical=[0,0,0],origin=[0,0,0]):
        """
            method to get cartesian coordinates around a certain point

            Parameters:
                spherical[radius(float),theta(float),phi(float)]: radius[0,inf) (distanz to center), theta[0,pi] (angle away from Z-Axis), phi [0,2pi) (angle away from x achsis)
                origin[x(float),y(float),z(float)]: point to center the cartesian coordinates [x,y,z]
        """
        radius = spherical[0]
        theta = spherical[1]
        phi = spherical[2]
        x = radius*math.sin(theta)*math.cos(phi) + origin[0]
        y = radius*math.sin(theta)*math.sin(phi) + origin[1]
        z = radius*math.cos(theta) + origin[2]
        cartesian_coordinates = [x,y,z]
        return cartesian_coordinates

    def get_pixel_cords(self,obj):
        
        """
            method for geting the outermost pixels of an object on a picture, to create boundingboxes

            Parameter:
            	obj (blender object): the object which shall be checked

            Return:
                return_value [int, int, int, int]: [x1, x2, y1, y2] pixel koordinates, be aware of flipped koordinates in further analyses
        """
        def view3d_find():
            # returns first 3d view, normally we get from context
            for area in bpy.context.window.screen.areas:
                if area.type == 'VIEW_3D':
                    v3d = area.spaces[0]
            
                    rv3d = v3d.region_3d
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            #rv3d.view_perspective = 'CAMERA'
                            return region, rv3d
            return None, None

        region, rv3d = view3d_find()

        def view3d_camera_border(scene):
            obj = scene.camera
            cam = obj.data
            frame = cam.view_frame(scene=scene)
            #print(frame)
            # move into object space
            frame = [obj.matrix_world @ v for v in frame]
            # move into pixelspace
            frame_px = [location_3d_to_region_2d(region, rv3d, v) for v in frame]
            return frame_px

        # put the region into camera perspective
        rv3d.view_perspective = 'CAMERA'


        frame_px = view3d_camera_border(bpy.context.scene)
        #print("Camera frame:", frame_px)

        # this is the camera bounds
        blc = min(frame_px)
        cambounds = [v - blc for v in frame_px]
        #print("camera is on screen as :", max(cambounds))

        #obj = bpy.data.objects["Switch"] #bpy.context.object # the context object.
        objloc = location_3d_to_region_2d(
                            region,
                            rv3d,
                            obj.matrix_world.to_translation()) - blc
        #print("obj_loc",objloc)

        bounding_box = [v[:] for v in obj.bound_box]
        bbox_px = [location_3d_to_region_2d(region, rv3d, v) 
                                - blc for v in bounding_box]

        #min_x = min(v.x for v in bbox_px)
        #max_x = max(v.x for v in bbox_px)
        #bbox_width = max_x - min_x 

        #... etc to get the coords of bbox.

        mw = obj.matrix_world
        #global vert locs
        verts = [mw @ v.co for v in obj.data.vertices]
        # vert locations in "region camera coords"
        verts_px = [location_3d_to_region_2d(region, rv3d, v) 
                                - blc for v in verts]
        min_x_verts=min(v.x for v in verts_px)
        max_x_verts=max(v.x for v in verts_px)
        min_y_verts=min(v.y for v in verts_px)
        max_y_verts=max(v.y for v in verts_px)

        max_cam=max(cambounds)
        scale_x = bpy.context.scene.render.resolution_x/max_cam[0]
        min_x=min_x_verts*scale_x
        max_x=max_x_verts*scale_x
        scale_y = bpy.context.scene.render.resolution_y/max_cam[1]
        min_y=min_y_verts*scale_y
        max_y=max_y_verts*scale_y
        #print("scale_x", scale_x)
        #print("scale_y", scale_y)

        return_value=[min_x, max_x, min_y, max_y]
        return return_value