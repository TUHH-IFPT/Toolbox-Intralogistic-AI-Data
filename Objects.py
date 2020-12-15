import bpy
from math import radians
from random import randint
import random
import sys
import io
import numpy as np

class Objects():

    def __init__(self):
        pass

    def add_picture(self,main_class):
        """
            Function to create the floor from a picture
            A random picture from ...//Images gets chosen

            Parameter:
                main_class (self): given to have acces to global variables
        """
        obj_dic = main_class.database.get_database_dict("object")

        for obj in main_class.object_database:
            if obj[obj_dic["obj_type"]] == "background":
                picture_path = main_class.database.get_background_pictures_path()
                random_file_name = main_class.background_picture_list[randint(0,len(main_class.background_picture_list)-1)]
                # pylint: disable=no-member
                # pylint: disable=duplicate-key
                bpy.ops.import_image.to_plane(files=[{"name":random_file_name, "name":random_file_name}], directory=picture_path, relative=False)
                # pylint: enable=duplicate-key
                # pylint: enable=no-member
                scale = obj[obj_dic["obj_scale_factor"]]
                random_translation = obj[obj_dic["maximum_random_translation"]]
                try:
                    scale = float(scale.replace(',','.'))
                except:
                    pass
                try:
                    random_translation = float(random_translation.replace(',','.'))
                except:
                    pass
                bpy.ops.transform.resize(value=(scale,scale,1))
                print("values are:", scale, random_translation)
                random_translation_x = randint(-int(scale*random_translation), int(scale*random_translation))
                random_translation_y = randint(-int(scale*random_translation), int(scale*random_translation))
                bpy.ops.transform.translate(value=(obj[obj_dic["obj_location_x"]] + random_translation_x, obj[obj_dic["obj_location_y"]] + random_translation_y, obj[obj_dic["obj_location_z"]]))
                random_rotation = randint(0, obj[obj_dic["maximum_random_rotation_degree_z"]])
                bpy.ops.transform.rotate(value= random_rotation, orient_axis= "Z")
                #bpy.ops.transform.rotate(0,0, radians( randint(0,obj[obj_dic["maximum_random_rotation_degree_z"]])) )
                bpy.ops.rigidbody.object_add()
                main_class.passive_objects.append(bpy.context.object)
                bpy.context.object.rigid_body.type = 'PASSIVE'
                bpy.context.object.rigid_body.collision_shape = 'BOX'
                bpy.context.object.rigid_body.collision_margin= 0.1

                #add information for output database
                main_class.database.add_output_objects(main_class.global_count, bpy.context.object.name, "background_picture", 1, bpy.context.object.location, bpy.context.object.rotation_euler,bpy.context.object.dimensions)

    def add_box(self, main_class):
        """
            Function to create the needed Box

            Parameter:
                main_class (self): given to have acces to global variables
        """
        obj_dic = main_class.database.get_database_dict("object")

        for obj in main_class.object_database:
            if obj[obj_dic["obj_type"]] == "box":
                text_trap = io.StringIO()
                sys.stdout = text_trap
                bpy.ops.import_scene.obj(filepath=obj[obj_dic["obj_filepath"]], filter_glob="*.obj")
                sys.stdout = sys.__stdout__
                
                scale = obj[obj_dic["obj_scale_factor"]]
                print("scale is: ", scale)
                try:
                    scale = float(scale.replace(',', '.'))
                except:
                    pass
                print("bpy dings", bpy.context.object.dimensions)
                print("bpy dings", bpy.context.object.name)
                print("maximum dimension is", max(bpy.context.object.dimensions))
                # scale = scale/max(bpy.context.object.dimensions)
                # print("scale_factor for box is:", scale)
                # bpy.ops.transform.resize(value=(scale, scale, scale))
                
                bpy.ops.rigidbody.objects_add()
                

                bpy.context.view_layer.objects.active = bpy.data.collections[0].all_objects[-1]

                scale = scale/max(bpy.context.object.dimensions)
                bpy.ops.transform.resize(value=(scale, scale, scale))
                
                # activeObject = bpy.context.active_object #Set active object to variable
                # mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
                # activeObject.data.materials.append(mat) #add the material to the object
                # bpy.context.object.active_material.diffuse_color = (1, 0, 0,0) #change color

                print("scale_factor for box is:", scale)

                bpy.context.object.location = [obj[obj_dic["obj_location_x"]], obj[obj_dic["obj_location_y"]], obj[obj_dic["obj_location_z"]]]
                bpy.context.object.rotation_euler = [obj[obj_dic["obj_rotation_x"]], obj[obj_dic["obj_rotation_y"]], obj[obj_dic["obj_rotation_z"]]]
                main_class.passive_objects.append(bpy.context.object)
                print("passive obj added:", main_class.passive_objects)
                
                bpy.context.object.rigid_body.type = 'PASSIVE'
                bpy.context.object.rigid_body.collision_shape = 'MESH'
                bpy.context.object.rigid_body.use_margin = True
                bpy.context.object.rigid_body.collision_margin = 0.1
                
                #add information for output database
                main_class.database.add_output_objects(main_class.global_count, bpy.context.object.name, "Box", 1, bpy.context.object.location, bpy.context.object.rotation_euler, bpy.context.object.dimensions)

                main_class.box = bpy.context.object.name

    def add_active_object(self, main_class, passive_box, pose="random"):
        """
            Functioncall for adding active object into the simulation

            Parameters:
                main_class (self): given to have acces to global variables
                passive_box(object): the box, which shall be used to put aktive objects in
                pose(string): chose between [random, fixed] pose for the object (fixed will be added later on)

        """

        obj_dic = main_class.database.get_database_dict("object")

        for obj in main_class.object_database:
            if obj[obj_dic["obj_type"]]=="active":
                print("The pose input is:", pose)
                text_trap = io.StringIO()
                sys.stdout = text_trap
                bpy.ops.import_scene.obj(filepath=obj[obj_dic["obj_filepath"]], filter_glob="*.obj")
                sys.stdout = sys.__stdout__
                scale = obj[obj_dic["obj_scale_factor"]]
                try:
                    scale = float(scale.replace(',','.'))
                except:
                    pass
                #scale = scale/max(bpy.context.object.dimensions)
                print("name of the active object in creation is: ", bpy.context.object.name)
                print("aktive obj scale variable:", scale)
                #bpy.ops.transform.resize(value=(scale,scale,scale))
                print("aktive obj dimensions:", bpy.context.object.dimensions)
                bpy.ops.rigidbody.objects_add()
                bpy.context.view_layer.objects.active= bpy.data.collections[0].all_objects[-1]
                scale = scale/max(bpy.context.object.dimensions)
                bpy.ops.transform.resize(value=(scale, scale, scale))

                #bpy.context.view_layer.objects.active= bpy.data.collections[0].all_objects[-1]
                main_class.active_objects.append(bpy.context.object)
                print(bpy.context.object.name)
                if pose == "random":
                    safty_margin=[bpy.context.object.dimensions[0]/passive_box.dimensions[0], bpy.context.object.dimensions[1]/passive_box.dimensions[1], bpy.context.object.dimensions[2]/passive_box.dimensions[2]]
                    print("safty Margin ist: ", safty_margin)
                    max_value= np.max(safty_margin)
                    safty_margin= [max_value,max_value,max_value]
                    print("max safty Margin ist: ", safty_margin)
                    loc, rotation = main_class.randomiser.do_random_object_pose(bpy.context, passive_box, safty_margin,[0,0,0])
                    bpy.context.object.location = loc
                    bpy.context.object.rotation_euler = rotation
                elif pose == "fixed":
                    bpy.context.object.location=[obj[obj_dic["obj_location_x"]],obj[obj_dic["obj_location_y"]],obj[obj_dic["obj_location_z"]]]
                    bpy.context.object.rotation_euler=[obj[obj_dic["obj_rotation_x"]],obj[obj_dic["obj_rotation_y"]],obj[obj_dic["obj_rotation_z"]]]
                else:
                    print("please chose from random or fixed modifier as input argumant")
                bpy.context.object.rigid_body.type="ACTIVE"
                bpy.context.object.rigid_body.mass=20
                bpy.context.object.rigid_body.collision_shape='CONVEX_HULL'
                bpy.context.object.rigid_body.friction = 1
                bpy.context.object.rigid_body.use_margin = True
                bpy.context.object.rigid_body.collision_margin = 0.5
                bpy.context.object.rigid_body.linear_damping = 0.35
                bpy.context.object.rigid_body.angular_damping=0.6
                bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN", center="MEDIAN")

                #main_class.database.add_output_objects(main_class.global_count, bpy.context.object.name, "aktive_object" , 1, bpy.context.object.location, bpy.context.object.rotation_euler,bpy.context.object.dimensions)

                print("added active object from:", obj[obj_dic["obj_filepath"]])
        return

    def add_packaging(self, main_class, passive_box, point_in_time="before_obj"):
        """
            Functioncall for adding packaging materials to the simulation
            
            Parameters:
                main_class (self): given to have acces to global variables
                passive_box(object): the box, which shall be used to put packaging in
                point_in_time(string): select between ["before_obj" or "after_obj"], to chose when packaging shall be added (under construction)
        """

        obj_dic = main_class.database.get_database_dict("object")

        for obj in main_class.object_database:
            if obj[obj_dic["obj_type"]]=="packaging" and (obj[obj_dic["obj_point_in_time"]] == point_in_time) and (obj[obj_dic["obj_amount_percent"]]!=0):
                text_trap = io.StringIO()
                sys.stdout = text_trap
                bpy.ops.import_scene.obj(filepath=obj[obj_dic["obj_filepath"]], filter_glob="*.obj")
                sys.stdout = sys.__stdout__
                scale = obj[obj_dic["obj_scale_factor"]]
                try:
                    scale = float(scale.replace(',','.'))
                except:
                    pass
                #scale = scale/max(bpy.context.object.dimensions)
                #print("the replaced number is:", scale)
                #bpy.ops.transform.resize(value=(scale, scale, scale))
                bpy.ops.rigidbody.objects_add()
                bpy.context.view_layer.objects.active= bpy.data.collections[0].all_objects[-1]
                print("after added flip:",bpy.context.object.name)
                scale = scale/max(bpy.context.object.dimensions)
                print("scale:", scale)
                bpy.ops.transform.resize(value=(scale, scale, scale))

                #bpy.context.view_layer.objects.active= bpy.data.collections[0].all_objects[-1]
                #active_objects.append(bpy.context.object)

                mat = bpy.data.materials.new("mat")
                mat.use_nodes = True
                #bsdf = mat.node_tree.nodes["Principled BSDF"]
                texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpy.data.images.load(obj[obj_dic["obj_material_path"]])
                flip = bpy.context.active_object

                bpy.context.object.location=[0, 0, 0]
                bpy.context.object.rotation_euler=[obj[obj_dic["obj_rotation_x"]], obj[obj_dic["obj_rotation_y"]], obj[obj_dic["obj_rotation_z"]]]
                bpy.context.object.rigid_body.type="ACTIVE"
                bpy.context.object.rigid_body.mass=1
                bpy.context.object.rigid_body.collision_shape='BOX'
                bpy.context.object.rigid_body.friction = 1
                bpy.context.object.rigid_body.use_margin = True
                bpy.context.object.rigid_body.collision_margin = 0.1
                bpy.context.object.rigid_body.linear_damping = 0.35
                bpy.context.object.rigid_body.angular_damping=0.6
                
                box_volume= passive_box.dimensions[0]*passive_box.dimensions[1]*passive_box.dimensions[2]
                flip_volume= flip.dimensions[0]*flip.dimensions[1]*flip.dimensions[2]
                flip_amount=round((box_volume/flip_volume)*(obj[obj_dic["obj_amount_percent"]]+random.uniform(0,obj[obj_dic["random_amount"]])))

                main_class.flips.append(bpy.context.object)

                print("box volume:", box_volume, "flip_volume:", flip_volume, "Flip amount:", flip_amount )

                safty_margin=[bpy.context.object.dimensions[0]/passive_box.dimensions[0],bpy.context.object.dimensions[1]/passive_box.dimensions[1],bpy.context.object.dimensions[2]/passive_box.dimensions[2]]
                max_value= np.max(safty_margin)*2
                safty_margin= [max_value,max_value,max_value]
                
                # pylint: disable=unused-variable
                for j in range(flip_amount):
                    loc,pose = main_class.randomiser.do_random_object_pose(bpy.context,passive_box, safty_margin)
                    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(-0.108603, -0.245817, 5.3335e-05), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
                    bpy.context.object.location=loc
                    bpy.context.object.rotation_euler=pose
                    main_class.flips.append(bpy.context.object)
                # pylint: enable=unused-variable
                main_class.database.add_output_objects(main_class.global_count, bpy.context.object.name, "packaging", flip_amount+1, bpy.context.object.location, bpy.context.object.rotation_euler,bpy.context.object.dimensions)
                print("dimension of the box is:", passive_box.dimensions)
                print("location of the box is:", passive_box.location)
        return

    def add_bubble_wrap(self, main_class, box_obj):
        """
            Function to create bubble wrap from a picture
            A random picture from ...//Packaging gets chosen

            Parameter:
                main_class (self): given to have acces to global variables
                box_obj (blender object): transportbox, which shall be used to create üackaging inside
        """
        obj_dic = main_class.database.get_database_dict("object")
        for obj in main_class.object_database:
            if obj[obj_dic["obj_type"]] == "background":
                picture_path = main_class.database.get_packaging_pictures_path()
                random_file_name = main_class.packaging_picture_list[randint(0,len(main_class.packaging_picture_list)-1)]
                # pylint: disable=no-member
                # pylint: disable=duplicate-key
                bpy.ops.import_image.to_plane(files=[{"name":random_file_name, "name":random_file_name}], directory=picture_path, relative=False)
                # pylint: enable=duplicate-key
                # pylint: enable=no-member
                scale = [((box_obj.dimensions[0]*0.9)/float(bpy.context.object.dimensions[0])),((box_obj.dimensions[1]*0.9)/float(bpy.context.object.dimensions[1]))]
                bpy.ops.transform.resize(value=(scale[0],scale[1],1))
                bpy.ops.transform.translate(value=(0,0, -4.5))#obj[obj_dic["obj_location_z"]]))
                
                main_class.database.add_output_objects(main_class.global_count, bpy.context.object.name, "bubble_wrap", 1, bpy.context.object.location, bpy.context.object.rotation_euler,bpy.context.object.dimensions)

    def delete_all_objects(self, main_class):
        """
        This function should be called EVERY TIME a set gets generated!!!

        Function Call to delete all objects from the blender workspace, to have a clean start
        Also removes entrys from global variables to track objects
        and sets output database entrys for later saving to empty

        Parameter:
                main_class (self): given to have acces to global variables
        """

        main_class.passive_objects = []
        main_class.active_objects = []
        main_class.flips = []
        main_class.lights = []

        main_class.global_variation = 0
        main_class.light_sets = 0
        main_class.camera_sets = 0

        main_class.database.clear_all_output_settings()

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)
        
        return