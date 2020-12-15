import bpy
import random

class Lights_and_Camera():

    def __init__(self):
        pass

    def add_camera(self, main_class, location=[0, 0, 0], rotation = [0, 0, 0]):
        """
            Function to add a camera to the scene
            Parameters:
                main_class (self): given to have acces to global variables
                location [float, float, float]: global coordinates of the camera
                rotation [float, float, float]: rotation of the camera around [x, y, z]
        """

        bpy.ops.object.camera_add(enter_editmode=False, location=location, rotation=rotation)
        #camera.append(bpy.data.objects['Camera'])
        main_class.camera = bpy.data.objects['Camera'].name

    def set_camera(self, main_class, new_location_spherical=[0, 0, 0, 0, 0], new_rotation = [0, 0, 0], auto_tracking=False):
        """
            Function to add set camera location an rotation
            Parameters:
                main_class (self): given to have acces to global variables
                new_location_spherical [float,float,float,float]: [polarangle_fix, polar_angle_random_intervall, azimut_fix, azimut_random_intervall] given in radiant
                new_rotation [float, float, float]: [x,y,z] if tracking is set to false
                auto_tracking (bool): camera tracking of an object
        """
        print("new_location_spherical in set Camera:", new_location_spherical)
        bpy.context.scene.camera = bpy.data.objects["Camera"]
        #bpy.context.scene.camera.location=new_location
        #bpy.context.scene.camera.rotation_euler=new_rotation
        polar = new_location_spherical[0] + random.uniform(-new_location_spherical[1], new_location_spherical[1])
        azi = new_location_spherical[2] + random.uniform(-new_location_spherical[3], new_location_spherical[3])
        radius = new_location_spherical[4]
        main_class.camera_angle = [polar,azi]
        new_location = main_class.transform.get_cartesian_coordinates_from_spherical([radius, polar, azi], [0,0,0])
        bpy.data.objects['Camera'].location = new_location
        print("Camera location set to:", bpy.data.objects["Camera"].location )
        if(auto_tracking == False):
            bpy.data.objects['Camera'].rotation_euler = new_rotation
        return

    def add_light(self, main_class, light_obj):
        """
        Functioncall for creating a light with position and rotation

        Parameters
            main_class (self): given to have acces to global variables
            light_object (database): light object, createt by the database
        """
        light_type = light_obj[0]
        radius_input = 1
        if(light_type != "SUN"):
            location_input = light_obj[1]
            polar=location_input[0] + random.uniform(-location_input[1], location_input[1])
            azi= location_input[2] + random.uniform(-location_input[3], location_input[3])
            radius= location_input[4]
            main_class.light_angle=[polar,azi]
            location_input= main_class.transform.get_cartesian_coordinates_from_spherical([radius, polar,azi], [0,0,0])
            #print("loction_input:", location_input)
        else:
            location_input = light_obj[1]

        bpy.ops.object.light_add(type=light_type, radius=radius_input, location=location_input, rotation= [0,0,0])
        main_class.lights.append(bpy.context.object)
        if bpy.context.object.name == "Spot":
            bpy.context.object.data.energy = 400000
            bpy.context.object.data.specular_factor = 2
            bpy.context.object.data.shadow_soft_size = 1
            bpy.context.object.data.spot_size = 1.5708
            print("power set")

        self.set_obj_tracking(bpy.context.object.name, main_class.box)
        return

    def set_light(self, main_class, light="Sun", location=[0,0,0], rotation=[0,0,0],auto_tracking=False):
        """
        Functioncall for setting position and rotation of the given light source

        Parameters
            main_class (self): given to have acces to global variables
            light (String): light obj, from database 
            location(float[x,y,z]): location of the light in global coordinates
            rotation(float[alpha,beta,gamma]): rotation of the light around [x,y,z] in degree
            auto_tracking (bool): camera tracking of an object
        """
        
        light.location=location
        light.rotation_euler=rotation
        return

    def delete_light(self, main_class):
        """
        Method to remove all lights from a scene

        Parameters
            main_class (self): given to have acces to global variables
        """
        for light in main_class.lights:
            bpy.ops.object.select_all(action="DESELECT")
            bpy.data.objects[light.name].select_set(True)
            print("deleted light: ", light.name)
            bpy.ops.object.delete()

        main_class.lights=[]
        return

    def set_obj_tracking(self, camera_or_light, obj_to_track):
        """
        Method to set tracking of one object to an other

        Parameters
            main_class (self): given to have acces to global variables
        """
        bpy.context.view_layer.objects.active = bpy.data.objects[camera_or_light]
        bpy.data.objects[camera_or_light].select_set(True)
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects[obj_to_track]
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
