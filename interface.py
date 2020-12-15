#um für den Benutzer eine Interface zu verfügung zustellen, werden hier alle benötigten Schritte vorgenommen

# bpy is die Bibliothek von Blender
import bpy

#einfügen der Klassen, um die hinterlegten Variablen nutzen zu können
#besonderes Augenmerk liegt hierbei auf der Variable "bl_idname"
#Blender nimmt viele Calls anhand des Namens oder Strings vor und nicht wie im klassischen programmieren
#mittels call by Value/ call by reference

#from . box_sim import box_sim_main

#from . box_sim_2 import box_sim_main_2

from . box_sim_4 import Box_sim_4_main


# haupt call für das interface, hier werden alle Knöpfe mit den entsprechenden Klassen verbunden
class OBJ_PT_maininterface(bpy.types.Panel):
#class _PT_maininterface(bpy.types.Panel):
    #Blender informationen verpackt als Strings
    #hier zeigt sich die Art wie Blender funktioniert, viele Informationen werden als String gespeichert
    #und der Inhalt wird für die Programmsteuerung genutzt
    #bl_idname = "main_interface"
    bl_label = "test_panel_2"
    bl_category = "Test Addon_2"
    bl_space_type = "VIEW_3D" # Ort wo das Addon wirken soll, hier das Hauptfenster von Blender
    bl_region_type = "UI"

    def draw(self, context):
        """
            Create interface button in the 3D-View of Blender at the right side

            Parameter:
                context (bpy.context): actuall context of blender
        """
        layout = self.layout
        row= layout.row()
        row.operator(Box_sim_4_main.bl_idname, text="Box_sim_4")
    
    