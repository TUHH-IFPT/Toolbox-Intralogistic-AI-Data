import bpy

class Logic_checker():

    def __init__(self):
        pass

    def item_in_box_checker(self, main_class, item, box):
        """
            Method to check if an object is inside of a given box

            Parameters
                main_class (self): given to have acces to global variables
                item (blender object): the object, which should be checked
                box (blender object): the box, where an item shall be found
        """
        bpy.data.objects[item.name].select_set(True)
        if((item.matrix_world.translation[0]) > (box.location[0]-box.dimensions[0]/2) and (item.matrix_world.translation[0]) < (box.location[0]+box.dimensions[0]/2) ):
                ### check in y direction ###
            if((item.matrix_world.translation[1]) > (box.location[1]-box.dimensions[1]/2) and (item.matrix_world.translation[1]) < (box.location[1]+box.dimensions[1]/2) ):
                    ### check in z direction ###
                if((item.matrix_world.translation[2]) > (box.location[2]) and (item.matrix_world.translation[2]) < (box.location[2]+box.dimensions[2]) ):
                    return True
                else:
                    print("object checker function returned FALSE in Z-direction")
                    return False
            else:
                print("object checker function returned FALSE in Y-direction")
                return False
        else:
            print("object checker function returned FALSE in X-direction")
            return False

    def delete_flips_out_of_box(self, main_class):
        """
        Method to remove all packaing material out of the transportbox

        Parameters
            main_class (self): given to have acces to global variables
        """
        flip_to_delete=[]

        for flip in main_class.flips:
            bpy.ops.object.select_all(action="DESELECT")
            bpy.data.objects[flip.name].select_set(True)
            flip_in_box = self.item_in_box_checker(bpy.context, flip, main_class.passive_objects[-1])
            if flip_in_box == False:
                flip_to_delete.append(flip)

        for obj in flip_to_delete:
            bpy.ops.object.select_all(action="DESELECT")
            bpy.data.objects[obj.name].select_set(True)
            print("deleted: ", obj.name)
            bpy.ops.object.delete()
