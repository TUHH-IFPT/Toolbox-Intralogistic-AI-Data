"""
    ...
"""

import bpy
# pylint: disable=relative-beyond-top-level
from . Datenbank import Database
from . Objects import Objects
from . Randomiser import Randomiser
from . Transform import Transform
from . Settings import Settings
from . Lights_and_camera import Lights_and_Camera
from . Logic_checker import Logic_checker
# pylint: enable=relative-beyond-top-level

# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint: disable=trailing-whitespace
# pylint: disable=singleton-comparison
# pylint: disable=line-too-long
class Box_sim_4_main(bpy.types.Operator):
    """
        Box Sim main Function/Class
    """
    bl_idname = "view3d.box_sim_datenbank"
    bl_label = "Simple operator"
    bl_description = "box_sim_playground_zwei"
    bl_options = {"REGISTER"}


    database = Database()
    objects = Objects()
    randomiser = Randomiser()
    transform = Transform()
    settings = Settings()
    lights_and_camera = Lights_and_Camera()
    logic_checker = Logic_checker()
    
    object_database = []
    render_database = []

    background_picture_list = []
    packaging_picture_list= []
    passive_objects = []
    active_objects = []
    flip = []
    box = "Kiste"


    light_settings = []
    lights = []
    light_angle = [0,0]
    camera_settings = []
    camera_angle = [0,0]
    camera = "Camera"
    
    global_count = 17
    global_variation = 0
    picture_count = 0
    max_loop_count=0
    loop_count=0
    camera_sets=0
    light_sets=0

    is_doing_render = False
    cam_and_light_set = False
    scene_refreshed = False
    checking_items = False

    def execute(self, context):
        print("start execution")
        self.database = Database()
        self.database.load_database(self)
        self.settings.scene_settings(self)
        #bpy.data.scenes["Scene"].gravity[2]=-9.81
        bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'
        self.do_creation()

        # pylint: disable=unused-variable
        for i in range(len(bpy.app.handlers.frame_change_pre)):
            bpy.app.handlers.frame_change_pre.pop()
        bpy.app.handlers.frame_change_pre.append(self.frame_handler)
        # pylint: enable=unused-variable
        bpy.ops.screen.animation_play()
        return{'FINISHED'}

    def do_creation(self):
        """
            creates all objects in the scene
        """
        print("Scene creation is running")
        self.objects.delete_all_objects(self)
        self.settings.environment_config(250)
        if(self.global_count < 7):
            self.objects.add_picture(self)
            self.objects.add_box(self)
        if(self.global_count >= 7 and self.global_count < 14):
            self.objects.add_picture(self)
            self.objects.add_box(self)
            self.objects.add_bubble_wrap(self,self.passive_objects[-1])
        if(self.global_count >= 14 and self.global_count < 21):
            self.objects.add_picture(self)
            self.objects.add_box(self)
            self.objects.add_packaging(self, self.passive_objects[-1])
        
        self.objects.add_active_object(self, self.passive_objects[-1], "random")
        self.lights_and_camera.add_camera(self)
        self.lights_and_camera.set_obj_tracking(self.camera, self.box)
        self.scene_refreshed = True

    def frame_handler(self, scene, depsgraphe):
        """
            handles frame event
        """
        render_frame = 240
        if (scene.frame_current == render_frame-2) and self.checking_items == False:
            #check items in box, delete Flips and check for items in box
            self.checking_items=True
            self.logic_checker.delete_flips_out_of_box(self)
            self.checking_items = False
            for obj in self.active_objects:
                print("I try to find the name of the obj:", obj.name)
                obj_in_box = self.logic_checker.item_in_box_checker(self, obj, self.passive_objects[-1])
                if(obj_in_box == False):
                    self.is_doing_render = False
                    bpy.context.scene.frame_set(1)
                    print("The following objekt is out of bounds:", obj.name)
                    self.checking_items = False
                    self.do_creation()
                    return
            self.database.add_output_objects(self.global_count ,self.active_objects[0].name, "aktive_object",1 , self.active_objects[-1].matrix_world.to_translation(), self.active_objects[-1].matrix_world.to_euler(), self.active_objects[-1].dimensions)
            #main_class.global_count, bpy.context.object.name, "aktive_object" , 1, bpy.context.object.location, bpy.context.object.rotation_euler,bpy.context.object.dimensions)

        if self.global_count <21:
            if(scene.frame_current == render_frame and self.cam_and_light_set== False):
                #set camera
                self.lights_and_camera.set_camera(self, self.camera_settings[self.camera_sets])
                cam = bpy.data.objects['Camera']
                self.database.add_output_camera_settings(self.global_count, self.global_variation, cam.name, cam.location, cam.rotation_euler, 0, self.camera_angle)
                #set light
                self.lights_and_camera.add_light(self, self.light_settings[self.light_sets])
                for light in self.lights:
                    self.database.add_output_light_settings(self.global_count, self.global_variation, light.name, light.location, light.rotation_euler,0, self.light_angle)
                self.cam_and_light_set=True
            if(scene.frame_current == render_frame+1):
                #switch to camera
                #self.transform.get_pixel_cords()
                
                for area in bpy.context.window.screen.areas:
                    if area.type == 'VIEW_3D':
                        v3d = area.spaces[0]
                
                        rv3d = v3d.region_3d
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                rv3d.view_perspective = 'CAMERA'

            if(scene.frame_current == render_frame+2 and self.is_doing_render == False):
                #do render
                for obj in self.active_objects:
                    xy_pixel=self.transform.get_pixel_cords(obj)
                    self.database.add_output_bounding_box_settings(self.global_count,self.global_variation, obj.name,"aktive_object",xy_pixel)
                self.settings.execute_render(self, render_frame)
                self.lights_and_camera.delete_light(self)
                self.global_variation += 1
                
                if(self.global_variation < self.max_loop_count):
                    self.lights_and_camera.delete_light(self)
                    print(self.global_variation)
                    if(self.camera_sets <= len(self.camera_settings)):
                        if(self.light_sets < len(self.light_settings)):
                            self.light_sets += 1
                        if(self.light_sets == len(self.light_settings)):
                            self.light_sets = 0
                            self.camera_sets += 1
                    bpy.context.scene.frame_set(render_frame-1)
                    self.cam_and_light_set=False
                if(self.global_variation == self.max_loop_count):
                    self.global_count += 1
                    self.database.save_to_output_database()
                    bpy.context.scene.frame_set(1)
                    self.is_doing_render = False
                    self.cam_and_light_set=False
                    self.do_creation()
        return