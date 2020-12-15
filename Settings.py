import os
import bpy
import sys
import io

class Settings():
    """
    settings class
    """
    def __init__(self):
        pass

    def scene_settings(self, main_class):
        """
            Function for setting blender configs
            here the blender egine gets set to make use of the gpu
        """
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.render.tile_x = 256
        bpy.context.scene.render.tile_y = 256

        main_class.database.add_output_general_settings(main_class.global_count, bpy.context.scene.render.engine, 100)

    def environment_config(self, scene_frame_end):
        """
        Function to configure important variables of the blender environment
        more can be done here later
        """
        bpy.context.scene.frame_end = scene_frame_end
        return
    
    def execute_render(self, main_class, render_frame):
        """
            Method for executing a render

            Parameter:
               main_class (self): given to have acces to global variables
               render_frame (int): scene frame, which shall be used to render an image
        """
        #main_class.transform.get_pixel_cords()
        path_name = os.path.dirname(__file__)
        path_name = os.path.join(path_name, "Images")
        file_type = ".jpg" # blender chosses png by default, not affected by this part of the code

        bpy.context.scene.frame_current = render_frame

        path_final= "picture" + "_" + str(main_class.global_count) + "_" + str(main_class.global_variation) + file_type
        path_final= os.path.join(path_name,path_final)
        print("Image path generatet;", path_final)
        text_trap = io.StringIO()
        sys.stdout = text_trap
        bpy.context.scene.render.filepath = path_final
        bpy.ops.render.render(write_still = True)
        sys.stdout = sys.__stdout__
        print("done:", main_class.picture_count)


        main_class.picture_count += 1
        return
