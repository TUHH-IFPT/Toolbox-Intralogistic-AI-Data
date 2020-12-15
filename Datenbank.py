import sys
import os
import csv
import sqlite3

class Database():
    """
    This is the class for controlling the Database for the Blender Addon
    The Goal is to create a database and have acces to the stored variables like camera positions, lights and obkects

    Classvariables:

    filepath (String): the Path to the actuall directory
    render_database (String): filename of the render database
    object_database (String): filename of the object database
    output_database (String): filename of the output database
    """

    filepath= ""
    render_database = "Render_database.db"
    object_database = "Object_database.db"
    output_database = "Output_database.db"

    filepath_render_database = ""
    filepath_object_database = ""
    filepath_output_database = ""

    """
    Variables to store all important data for the output file, variables can be accesed through the following functions:
        add_output_general_settings()
        add_output_objects()
        add_output_camera_settings()
        add_output_light_settings()

    after all important variables are saved, the database can be filled by using:

        save_output_database()

    if you want to remove all inputarguments from the variables, recommend at every new cycle of the scene generation use:

        clear_all_output_settings()
    """
    general_information = []
    object_information = []
    camera_information = []
    light_information = []
    bounding_box_information = []


    def __init__(self):
        """
            The constructor for the database, where the actuall directory gets assigned for further use
        """
        self.filepath = os.path.dirname(__file__)
        self.filepath = os.path.join(self.filepath, "Datenbank")
        self.filepath_render_database = os.path.join(self.filepath, self.render_database)
        self.filepath_object_database = os.path.join(self.filepath, self.object_database)
        self.filepath_output_database = os.path.join(self.filepath, self.output_database)
        self.create_database()

    def set_render_database_name(self, file_name):
        """
            method to set the name of the render_database

            Parameters:
                file_name(String): the name of the file, default is "Render_database.db"
        """
        try:
            self.render_database=file_name
            self.filepath_render_database = os.path.join(self.filepath, self.render_database)
            print("set render_database filename to", file_name)
        except:
            print("setting render database failed")
            self.render_database="Render_database.db"
            self.filepath_object_database = os.path.join(self.filepath, self.render_database)
            print("set render database name to default:", self.render_database)
        return

    def set_object_database (self, file_name):
        """
            method to set the name of the object_database

            Parameters:
                file_name(String): the name of the file, default is "Object_database.db"
        """
        try:
            self.object_database=file_name
            self.filepath_object_database = os.path.join(self.filepath, self.object_database)
            print("set object_database filename to", file_name)
        except:
            print("setting object database failed")
            self.object_database="Object_database.db"
            self.filepath_object_database = os.path.join(self.filepath, self.object_database)
            print("set object database name to default:", self.object_database)
        return

    def set_output_database (self, file_name):
        """
            method to set the name of the output_database

            Parameters:
                file_name(String): the name of the file, default is "Output_database.db"
        """
        try:
            self.object_database=file_name
            self.filepath_output_database = os.path.join(self.filepath, self.output_database)
            print("set output_database filename to", file_name)
        except:
            print("setting object database failed")
            self.output_database="Output_database.db"
            self.filepath_output_database = os.path.join(self.filepath, self.output_database)
            print("set output database name to default:", self.object_database)
        return

    def add_output_general_settings(self, image_id= 0, render_type = "No render type given", render_frame=0):
        """
            function to add information to the outputdatabase

            Parameters:
                image_id (int): unique number of a given scene composition, best chosen parameter is the global count
                render_type (String): Eevee or cycles, but name it what ever you like
                render_frame (int): The frame, when a given render was executet

            CAUTION: All information given to this function is only hold temporarily, to save the information
            "save_to_output_database()" needs to be called and cleaned up with "clear_all_output_settings()" afterwards
        """
        temp_array=[image_id,render_type,render_frame]
        self.general_information.append(temp_array)
        
    def add_output_objects(self, image_id = 0, object_type= "n.a.", object_name="n.a.", object_amount = 0, object_location = [0,0,0], object_rotation = [0,0,0], object_dimensions = [0,0,0]):
        """
            function to add object information to the outputdatabase

            Parameters:
                image_id (int): unique number of a given scene composition, best chosen parameter is the global count
                object_type (String): What type of object is it, we used it to keep track of active and passive objects of the rigid body simulation
                object_name (String): Name of the object
                object_amount (int): number of objects in the simulation
                object_location [int,int,int]: global position of an object
                object_rotation [int,int,int]: global rotation of an object
                object_dimensions = [int,int,int]: dimension in cm of an object

            CAUTION: All information given to this function is only hold temporarily, to save the information
            "save_to_output_database()" needs to be called and cleaned up with "clear_all_output_settings()" afterwards
        """
        temp_array= [image_id, object_type, object_name, object_amount, object_location[0],object_location[1],object_location[2], object_rotation[0], object_rotation[1], object_rotation[2], object_dimensions[0], object_dimensions[1], object_dimensions[2]]
        self.object_information.append(temp_array)

    def add_output_camera_settings(self, image_id = 0, image_variation = 0, camera_name="No name given", camera_location = [0,0,0], camera_rotation = [0,0,0], camera_focal_length=0, camera_pol_azi_angle= [0,0]):
        """
            function to add object information to the outputdatabase

            Parameters:
                image_id (int): unique number of a given scene composition, best chosen parameter is the global count
                image_variation (int): variation of light and camera in one scene composition
                camera_name (String): Name of the object
                light_location [int,int,int]: global position of the light source
                light_rotation [int,int,int]: global rotation of the light source
                camera_focal_length (float): the chosen focal length of the camera
                camera_pol_azi_angle [float,float]: angle of the light source in spherical coordinates
                
            CAUTION: All information given to this function is only hold temporarily, to save the information
            "save_to_output_database()" needs to be called and cleaned up with "clear_all_output_settings()" afterwards
        """
        temp_array = [image_id, image_variation, camera_name, camera_location[0], camera_location[1], camera_location[2], camera_rotation[0],camera_rotation[1],camera_rotation[2], camera_focal_length, float(camera_pol_azi_angle[0]),float(camera_pol_azi_angle[1])]
        self.camera_information.append(temp_array)

    def add_output_light_settings(self, image_id = 0,image_variation = 0, light_name="No name given", light_location=[0,0,0], light_rotation=[0,0,0], light_intensity=0, light_pol_azi_angle= [0,0]):
        """
            function to add object information to the outputdatabase

            Parameters:
                image_id (int): unique number of a given scene composition, best chosen parameter is the global count
                image_variation (int): variation of light and camera in one scene composition
                light_name (String): Name of the object
                light_location [int,int,int]: global position of the light source
                light_rotation [int,int,int]: global rotation of the light source
                light_intensity (int): brightness of the light
                light_pol_azi_angle [float,float]: angle of the light source in spherical coordinates

            CAUTION: All information given to this function is only hold temporarily, to save the information
            "save_to_output_database()" needs to be called and cleaned up with "clear_all_output_settings()" afterwards
        """
        temp_array=[image_id, image_variation, light_name, light_location[0], light_location[1], light_location[2], light_rotation[0], light_rotation[1], light_rotation[2], light_intensity, float(light_pol_azi_angle[0]), float(light_pol_azi_angle[1])]
        self.light_information.append(temp_array)
    
    def add_output_bounding_box_settings(self, image_id=0, image_variation=0, object_name="n.a.", object_type="n.a.", coordinates = [0,0,0,0]):
        """
            function to add object information to the outputdatabase

            Parameters:
                image_id (int): unique number of a given scene composition, best chosen parameter is the global count
                image_variation (int): variation of light and camera in one scene composition
                object_name (String): name of the object
                object_type (String): keep track of active and passive objects from the rigid body simulation
                coordinates [int,int,int,int]: pixelcoordinates of the boundingbox [x1, y1, x2, y2] Be aware of flipped axis, when working with this

            CAUTION: All information given to this function is only hold temporarily, to save the information
            "save_to_output_database()" needs to be called and cleaned up with "clear_all_output_settings()" afterwards
        """
        temp_array = [image_id, image_variation, object_name, object_name, coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
        self.bounding_box_information.append(temp_array)

    def clear_all_output_settings(self):
        """
            deletes all temporary stored date from the add_ouput_...() methods
            best used after save_to_output_database or recreation of a scene
        """
        self.general_information = []
        self.object_information = []
        self.camera_information = []
        self.light_information = []
        self.bounding_box_information = []

    def save_to_output_database(self):
        """
        Function to save alle given information to the output database
        The following functions need to be called first, to have all needed data:
            add_output_general_settings()
            add_output_objects()
            add_output_camera_settings()
            add_output_light_settings()
            add_output_bounding_box_settings()
        """
        connection = sqlite3.connect(self.filepath_output_database)
        pointer = connection.cursor()

        sql_anweisung = """
        INSERT INTO objects (
                    image_id,
                    object_name,
                    object_type,
                    object_amount,
                    object_location_x,
                    object_location_y,
                    object_location_z,
                    object_rotation_x,
                    object_rotation_y,
                    object_rotation_z,
                    object_dimensions_x,
                    object_dimensions_y,
                    object_dimensions_z
                )
                VALUES (
                    :image_id,
                    :object_name,
                    :object_type,
                    :object_amount,
                    :object_location_x,
                    :object_location_y,
                    :object_location_z,
                    :object_rotation_x,
                    :object_rotation_y,
                    :object_rotation_z,
                    :object_dimensions_x,
                    :object_dimensions_y,
                    :object_dimensions_z
                    )
                """
        pointer.executemany(sql_anweisung, self.object_information)
        connection.commit()

        sql_anweisung = """
        INSERT INTO camera_settings (
                    image_id,
                    image_variation,
                    camera_name,
                    camera_location_x,
                    camera_location_y,
                    camera_location_z,
                    camera_rotation_x,
                    camera_rotation_y,
                    camera_rotation_z,
                    camera_focal_length,
                    camera_polar_angle,
                    camera_azimuth_angle
                )
                VALUES (
                    :image_id,
                    :image_variation,
                    :camera_name,
                    :camera_location_x,
                    :camera_location_y,
                    :camera_location_z,
                    :camera_rotation_x,
                    :camera_rotation_y,
                    :camera_rotation_z,
                    :camera_focal_length,
                    :camera_polar_angle,
                    :camera_azimuth_angle
                    )
                """
        pointer.executemany(sql_anweisung, self.camera_information)
        connection.commit()

        sql_anweisung = """
        INSERT INTO light_settings (
                    image_id,
                    image_variation,
                    light_name,
                    light_location_x,
                    light_location_y,
                    light_location_z,
                    light_rotation_x,
                    light_rotation_y,
                    light_rotation_z,
                    light_intensity,
                    light_polar_angle,
                    light_azimuth_angle
                )
                VALUES (
                    :image_id,
                    :image_variation,
                    :light_name,
                    :light_location_x,
                    :light_location_y,
                    :light_location_z,
                    :light_rotation_x,
                    :light_rotation_y,
                    :light_rotation_z,
                    :light_intensity,
                    :light_polar_angle,
                    :light_azimuth_angle 
                    )
                """
        pointer.executemany(sql_anweisung, self.light_information)
        connection.commit()

        sql_anweisung = """
        INSERT INTO general_settings (
                    image_id,
                    render_type,
                    render_frame
                )
                VALUES (
                    :image_id,
                    :render_type,
                    :render_frame
                    )
                """
        pointer.executemany(sql_anweisung, self.general_information)
        connection.commit()
        sql_anweisung = """
        INSERT INTO bounding_boxes(
                image_id ,
                image_variation ,
                object_name,
                object_type,
                min_x,
                max_x,
                min_y,
                max_y
            )
            VALUES(
                :image_id ,
                :image_variation ,
                :object_name,
                :object_type,
                :min_x,
                :max_x,
                :min_y,
                :max_y
            )
            """
        pointer.executemany(sql_anweisung, self.bounding_box_information)
        connection.commit()
        print("outputdatabase saved")
        connection.close()
        print("Saved to output Database")
        pass

    def get_database_dict (self, database_type):
        """
        returns a dictonary for more readability in the programmcode

        Parameters:
            databasetype(String): Chose from [render,object,output]
        """
        if database_type == "render":
            dictionary = {
                "object_type" : 0,
                "name" : 1,
                "radius" : 2,
                "polar_angle_min" : 3,
                "polar_anglel_max" : 4,
                "polar_angle_segments" : 5,
                "polar_angle_random_rad" : 6,
                "azimuth_angle_min" : 7,
                "azimuth_angle_max" : 8,
                "azimuth_angle_segments" : 9,
                "azimuth_angle_random_rad": 10,
                "tracking_obj" : 11,
                "segmentation" : 12
            }
            return dictionary
        if database_type == "object":
            dictionary = {
                "obj_filepath" : 0,
                "obj_name" : 1,
                "obj_type" : 2,
                "obj_scale_factor" : 3,
                "obj_location_x" : 4,
                "obj_location_y" : 5,
                "obj_location_z" : 6,
                "obj_rotation_x" : 7,
                "obj_rotation_y" : 8,
                "obj_rotation_z" : 9,
                "obj_amount_percent":10,
                "obj_material_path" : 11,
                "obj_point_in_time" : 12,
                "maximum_random_rotation_degree_z": 13,
                "maximum_random_translation" : 14,
                "random_amount" : 15
            }
            return dictionary
    
    def get_background_pictures_names(self):
        """
        returns a dictonary for more readability in the programmcode

        Return Parameter:
            returns content of the background folder
        """
        file_path = os.path.dirname(__file__)
        file_path = os.path.join(file_path, "Background")
        return os.listdir(file_path)
        
    def get_bubble_wrap_pictures_names(self):
        """
        returns a dictonary for more readability in the programmcode

        Return Parameter:
            returns content of the Packaging folder
        """
        file_path = os.path.dirname(__file__)
        file_path = os.path.join(file_path, "Packaging")
        return os.listdir(file_path)

    def get_background_pictures_path(self):
        """
        returns a dictonary for more readability in the programmcode

        Return Parameter:
            filepath to the Background folder
        """
        file_path = os.path.dirname(__file__)
        file_path = os.path.join(file_path, "Background")
        return file_path
    
    def get_packaging_pictures_path(self):
        """
        returns a dictonary for more readability in the programmcode

        Return Parameter:
            filepath to the Background folder
        """
        file_path = os.path.dirname(__file__)
        file_path = os.path.join(file_path, "Packaging")
        return file_path

    def import_data_to_database(self, database_type, data):

        """
            method under construction, DON'T USE THIS   
            method to call data from database

            Parameters:
                database_type(String): Chose Database [render, object, output]
                data(see coresponding excelfile): all data for one entry into database
        """

        if database_type == "render":
            connection = sqlite3.connect(self.filepath_render_database)
            pointer = connection.cursor()
            pointer.executemany("""
                            INSERT INTO render_information
                            VALUES (?,?,?,?,?,?,?,?) 
                            """,
                            (data)
                            )
            connection.commit()
            connection.close()
            print("addet render information to database")
        if database_type == "object":
            connection = sqlite3.connect(self.filepath_object_database)
            pointer = connection.cursor()
            pointer.executemany("""
                            INSERT INTO object_information
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?) 
                            """,
                            (data)
                            )
            connection.commit()
            connection.close()
            print("addet objectinformation information to database")
        if database_type == "output":
            connection = sqlite3.connect(self.filepath_object_database)
            pointer = connection.cursor()
            pointer.executemany("""
                            INSERT INTO output_information
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,
                                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
                            """,
                            (data)
                            )
            connection.commit()
            connection.close()
            print("addet outputinformation information to database")
        

        return

    def get_data_from_database(self, database_type):
        """
            method to call data from database

            Parameters:
                database_type(String): Chose Database [render, object, output]

            Return:
                array with entrys
        """
        if database_type == "render":
            try:
                connection = sqlite3.connect(self.filepath_render_database)
                pointer=connection.cursor()

                pointer.execute("select * from render_information")

                conntent= pointer.fetchall()
                connection.commit()
                print(conntent)
                return conntent
            except:
                print("was not able to read data")
                return False
        if database_type == "object":
            try:
                connection = sqlite3.connect(self.filepath_object_database)
                pointer=connection.cursor()

                pointer.execute("select * from object_information")

                conntent= pointer.fetchall()
                connection.commit()
                print(conntent)
                return conntent
            except:
                print("was not able to read data from object database")
                return False         
        pass

        if database_type == "output":
            try:
                connection = sqlite3.connect(self.filepath_output_database)
                pointer=connection.cursor()

                pointer.execute("select * from output_information")

                conntent= pointer.fetchall()
                connection.commit()
                print(conntent)
                return conntent
            except:
                print("was not able to read data from output database")
                return False         
        pass

    def create_database(self):
        """
            Method to create all databases with their needed tables

            CAUTION: Call this before you use any database method from this class, structure is
            necessary for a proper function database
        """

        try: 
            connection = sqlite3.connect(self.filepath_render_database)
            pointer = connection.cursor()

            print(self.filepath_render_database)

            sql_instruction = """
            CREATE TABLE IF NOT EXISTS render_information(
                
                object_type VARCHAR(255),
                name VARCHAR(255),
                radius REAL,
                polar_angle_min REAL,
                polar_anglel_max REAL,
                polar_angle_segments REAL,
                polar_angle_random_rad REAL,
                azimuth_angle_min REAL,
                azimuth_angle_max REAL,
                azimuth_angle_segments REAL,
                azimuth_angle_random_rad REAL,
                tracking_obj VARCHAR(255),
                segmentation VARCHAR(255)


            );"""
            pointer.execute(sql_instruction)
            connection.commit()
            connection.close()
            print("Creating render database file")
        except:
            print("Was not able to create render database file")
        
        try: 
            connection = sqlite3.connect(self.filepath_object_database)
            pointer = connection.cursor()
            sql_instruction = """
            CREATE TABLE IF NOT EXISTS object_information(
                obj_filepath VARCHAR(255),
                obj_name VARCHAR(255),
                obj_type VARCHAR(255),
                obj_scale_factor REAL,
                obj_location_x REAL,
                obj_location_y REAL,
                obj_location_z REAL,
                obj_rotation_x REAL,
                obj_rotation_y REAL,
                obj_rotation_z REAL,
                obj_amount_percent REAL,
                obj_material_path VARCHAR(255),
                obj_point_in_time VARCHAR(255),
                maximum_random_rotation_degree_z REAL,
                maximum_random_translation REAL,
                random_amount REAL
            );"""
            pointer.execute(sql_instruction)
            connection.commit()
            connection.close()
            print("Creating object database file")
        except:
            print("Was not able to create object database file")

        try: 
            connection = sqlite3.connect(self.filepath_output_database)
            print("outputfilepath is:", self.filepath_output_database)
            pointer = connection.cursor()
            sql_instruction = """
            CREATE TABLE IF NOT EXISTS objects(
                image_id REAL,
                object_name VARCHAR(255),
                object_type VARCHAR(255),
                object_amount REAL,
                object_location_x REAL,
                object_location_y REAL,
                object_location_z REAL,
                object_rotation_x REAL,
                object_rotation_y REAL,
                object_rotation_z REAL,
                object_dimensions_x REAL,
                object_dimensions_y REAL,
                object_dimensions_z REAL
            );"""
            pointer.execute(sql_instruction)
            connection.commit()
            sql_instruction = """
            CREATE TABLE IF NOT EXISTS camera_settings(
                image_id REAL,
                image_variation REAL,
                camera_name VARCHAR(255),
                camera_location_x REAL,
                camera_location_y REAL,
                camera_location_z REAL,
                camera_rotation_x REAL,
                camera_rotation_y REAL,
                camera_rotation_z REAL,
                camera_focal_length REAL,
                camera_polar_angle REAL,
                camera_azimuth_angle REAL
            );"""
            pointer.execute(sql_instruction)
            connection.commit()
            sql_instruction = """
            CREATE TABLE IF NOT EXISTS light_settings(
                image_id REAL,
                image_variation REAL,
                light_name VARCHAR(255),
                light_location_x REAL,
                light_location_y REAL,
                light_location_z REAL,
                light_rotation_x REAL,
                light_rotation_y REAL,
                light_rotation_z REAL,
                light_intensity REAL,
                light_polar_angle REAL,
                light_azimuth_angle REAL
            );"""
            pointer.execute(sql_instruction)
            connection.commit()
            sql_instruction = """
            CREATE TABLE IF NOT EXISTS general_settings(
                image_id REAL,
                render_type VARCHAR(255),
                render_frame REAL
            );"""
            pointer.execute(sql_instruction)
            connection.commit()
            sql_instruction = """
            CREATE TABLE IF NOT EXISTS bounding_boxes(
                image_id REAL,
                image_variation REAL,
                object_name VARCHAR(255),
                object_type VARCHAR(255),
                min_x REAL,
                max_x REAL,
                min_y REAL,
                max_y REAL
            );"""
            pointer.execute(sql_instruction)
            connection.commit()
            connection.close()
            print("Creating output database file")
        except:
            print("Was not able to create output database file")

    def import_excel(self, filepath_excel,database_type):
        """
            method to import excel data to the correct database

            Parameters:
            filepath_excel(String): full path to the excel file for importing data
            database_type(String): Databasetype to chose from [render, object]
        """
        if database_type == "render":
            try:
                connection = sqlite3.connect(self.filepath_render_database)
                pointer = connection.cursor()

                sql_anweisung = """
                INSERT INTO render_information (
                    object_type,
                    name,
                    radius,
                    polar_angle_min,
                    polar_anglel_max,
                    polar_angle_segments,
                    polar_angle_random_rad,
                    azimuth_angle_min,
                    azimuth_angle_max,
                    azimuth_angle_segments,
                    azimuth_angle_random_rad,
                    tracking_obj,
                    segmentation
                )
                VALUES (
                    :object_type,
                    :name,
                    :radius,
                    :polar_angle_min,
                    :polar_anglel_max,
                    :polar_angle_segments,
                    :polar_angle_random_rad,
                    :azimuth_angle_min,
                    :azimuth_angle_max,
                    :azimuth_angle_segments,
                    :azimuth_angle_random_rad,
                    :tracking_obj,
                    :segmentation
                    )
                """
                with open(filepath_excel) as csvdatei:
                    csv_reader_object = csv.reader(csvdatei, delimiter=';')
                    next(csv_reader_object)
                    pointer.executemany(sql_anweisung, csv_reader_object)
                    connection.commit()
                    connection.close()
                print("render data addet from excel file")
            except :
                print("adding render data from excel file failed")

        elif database_type == "object":
            try:
                connection = sqlite3.connect(self.filepath_object_database)
                pointer = connection.cursor()

                sql_anweisung = """
                INSERT INTO object_information (
                    obj_filepath,
                    obj_name,
                    obj_type,
                    obj_scale_factor,
                    obj_type,
                    obj_location_x,
                    obj_location_y,
                    obj_location_z,
                    obj_rotation_x,
                    obj_rotation_y,
                    obj_rotation_z,
                    obj_amount_percent,
                    obj_material_path,
                    obj_point_in_time,
                    maximum_random_rotation_degree_z,
                    maximum_random_translation,
                    random_amount
                )
                VALUES (
                    :obj_filepath,
                    :obj_name,
                    :obj_type,
                    :obj_scale_factor,
                    :obj_type,
                    :obj_location_x,
                    :obj_location_y,
                    :obj_location_z,
                    :obj_rotation_x,
                    :obj_rotation_y,
                    :obj_rotation_z,
                    :obj_amount_percent,
                    :obj_material_path,
                    :obj_point_in_time,
                    :maximum_random_rotation_degree_z,
                    :maximum_random_translation,
                    :random_amount
                    )
                """
                with open(filepath_excel) as csvdatei:
                    csv_reader_object = csv.reader(csvdatei, delimiter=';')
                    print(csv_reader_object)
                    next(csv_reader_object)
                    pointer.executemany(sql_anweisung, csv_reader_object)
                    connection.commit()
                    connection.close()
                print("object data added from excel file")
            except :
                print("adding object data from excel file failed")

        else:
            print("no Database found, maybe check spelling in method call??")
        return

    def delete_all(self, database_type):
        """
            method to delete all elements from the chosen database

            Parameters:
                database_type(String): Chose Database [render, object, output, all]

            Return:
                array with entrys
        """
        if database_type == "render":
            try:
                connection = sqlite3.connect(self.filepath_render_database)
                pointer = connection.cursor()
                pointer.execute("DELETE FROM render_information")

                connection.commit()
                connection.close()
                print("deleted render database")

            except:
                print("was not able to delete render database")

        if database_type == "object":
            try:
                connection = sqlite3.connect(self.filepath_object_database)
                pointer = connection.cursor()
                pointer.execute("DELETE FROM object_information")

                connection.commit()
                connection.close()
                print("deleted object database")
            except:
                print("was not able to delete object database")
        if database_type == "output":
            try:
                connection = sqlite3.connect(self.filepath_output_database)
                pointer = connection.cursor()

                pointer.execute("DELETE FROM camera_settings")
                connection.commit()

                pointer.execute("DELETE FROM general_settings")
                connection.commit()

                pointer.execute("DELETE FROM light_settings")
                connection.commit()

                pointer.execute("DELETE FROM objects")
                connection.commit()

                pointer.execute("DELETE FROM bounding_boxes")
                connection.commit()

                connection.close()
                print("deleted output database")
            except:
                print("was not able to delete output database")

        if database_type == "all":
            
            try:
                connection = sqlite3.connect(self.filepath_render_database)
                pointer = connection.cursor()
                pointer.execute("DELETE FROM render_information")

                connection.commit()
                connection.close()
                print("deleted content of render database")

            except:
                print("was not able to delete render database")

        
            try:
                connection = sqlite3.connect(self.filepath_object_database)
                pointer = connection.cursor()
                pointer.execute("DELETE FROM object_information")

                connection.commit()
                connection.close()
                print("deleted content of object database")
            except:
                print("was not able to delete object database")

            try:
                connection = sqlite3.connect(self.filepath_output_database)
                pointer = connection.cursor()

                pointer.execute("DELETE FROM camera_settings")
                connection.commit()

                pointer.execute("DELETE FROM general_settings")
                connection.commit()

                pointer.execute("DELETE FROM light_settings")
                connection.commit()

                pointer.execute("DELETE FROM objects")
                connection.commit()

                connection.close()
                print("deleted content of output database")
            except:
                print("was not able to delete output database")

    def load_database(self, main_class):
            """
                Function call to load important data from the database
                the overall structur of the database is best seen in the coressponding Excel sheets

                Parameters:
                    main_class(object):   input "self" argument from Box sim main function
            """
            main_class.database.delete_all("render")
            main_class.database.delete_all("object")
            #main_class.database.delete_all("output")
            render_csv =  os.path.join(self.filepath, "Render_data.csv")
            object_csv =  os.path.join(self.filepath, "Obj_data.csv")
            main_class.database.import_excel(render_csv, "render")
            main_class.database.import_excel(object_csv, "object")

            render_dic=main_class.database.get_database_dict("render")

            main_class.render_database = main_class.database.get_data_from_database("render")
            main_class.object_database = main_class.database.get_data_from_database("object")

            main_class.background_picture_list = main_class.database.get_background_pictures_names()
            main_class.packaging_picture_list = main_class.database.get_bubble_wrap_pictures_names()

            main_class.camera_settings.append([0, 0, 0, 0, 100])
            for obj in main_class.render_database:
                """
                    extracting Camerasetting from Database and set all important angles and distances
                """
                if obj[render_dic["object_type"]] == "camera":
                    for i in range(0, int(obj[render_dic["polar_angle_segments"]])):
                        for j in range(0, int(obj[render_dic["azimuth_angle_segments"]])):
                            pol_min = obj[render_dic["polar_angle_min"]]
                            pol_max = obj[render_dic["polar_anglel_max"]]
                            pol_segments= obj[render_dic["polar_angle_segments"]]
                            pol_random=obj[render_dic["polar_angle_random_rad"]]
                            try:
                                pol_min = float( pol_min.replace(',','.'))
                            except:
                                pass
                            try:
                                pol_max = float( pol_max.replace(',','.'))
                            except:
                                pass
                            try:
                                pol_segments = float( pol_segments.replace(',','.'))
                            except:
                                pass
                            try:
                                pol_random = float( pol_random.replace(',','.'))
                            except:
                                pass
                            polar_angle = (pol_min + ((pol_max - pol_min)/(pol_segments))*i)

                            azi_min = obj[render_dic["azimuth_angle_min"]]
                            azi_max = obj[render_dic["azimuth_angle_max"]]
                            azi_segments= obj[render_dic["azimuth_angle_segments"]]
                            azi_random= obj[render_dic["azimuth_angle_random_rad"]]

                            try:
                                azi_min = float( azi_min.replace(',','.'))
                            except:
                                pass
                            try:
                                azi_max = float( azi_max.replace(',','.'))
                            except:
                                pass
                            try:
                                azi_segments = float( azi_segments.replace(',','.'))
                            except:
                                pass
                            try:
                                azi_random = float( azi_random.replace(',','.'))
                            except:
                                pass
                            azimuth_angle = (azi_min + ((azi_max - azi_min)/(azi_segments))*j)

                            position=[polar_angle, pol_random, azimuth_angle, azi_random, obj[render_dic["radius"]] ]
                            print("camera position added: ",position)
                            main_class.camera_settings.append(position)
                
                if obj[render_dic["object_type"]]=="light":

                    if obj[render_dic["name"]]=="SUN":
                        radius= obj[render_dic["radius"]]
                        try:
                            radius = float( radius.replace(',','.'))
                        except:
                            pass
                        light_obj=[ obj[render_dic["name"]] , [0,0, radius ] ]
                        main_class.light_settings.append(light_obj)
                        print("sun added to list")

                    if obj[render_dic["name"]]=="SPOT":
                        for i in range(0, int(obj[render_dic["polar_angle_segments"]])):
                            for j in range(0, int(obj[render_dic["azimuth_angle_segments"]])):
                                pol_min = obj[render_dic["polar_angle_min"]]
                                pol_max = obj[render_dic["polar_anglel_max"]]
                                pol_segments= obj[render_dic["polar_angle_segments"]]
                                pol_random=obj[render_dic["polar_angle_random_rad"]]
                                try:
                                    pol_min = float( pol_min.replace(',','.'))
                                except:
                                    pass
                                try:
                                    pol_max = float( pol_max.replace(',','.'))
                                except:
                                    pass
                                try:
                                    pol_segments = float( pol_segments.replace(',','.'))
                                except:
                                    pass
                                try:
                                    pol_random = float( pol_random.replace(',','.'))
                                except:
                                    pass
                                polar_angle = (pol_min + ((pol_max - pol_min)/(pol_segments))*i)

                                azi_min = obj[render_dic["azimuth_angle_min"]]
                                azi_max = obj[render_dic["azimuth_angle_max"]]
                                azi_segments= obj[render_dic["azimuth_angle_segments"]]
                                azi_random= obj[render_dic["azimuth_angle_random_rad"]]
                                try:
                                    azi_min = float( azi_min.replace(',','.'))
                                except:
                                    pass
                                try:
                                    azi_max = float( azi_max.replace(',','.'))
                                except:
                                    pass
                                try:
                                    azi_segments = float( azi_segments.replace(',','.'))
                                except:
                                    pass
                                try:
                                    azi_random = float( azi_random.replace(',','.'))
                                except:
                                    pass
                                azimuth_angle = (azi_min + ((azi_max - azi_min)/(azi_segments))*j)
                                position=[polar_angle, pol_random, azimuth_angle, azi_random, obj[render_dic["radius"]] ]
                                light_obj=[ obj[render_dic["name"]] , position, obj[render_dic["tracking_obj"]],1000 ]
                                print("added light_obj: ", light_obj)
                                main_class.light_settings.append(light_obj)
                                main_class.max_loop_count=len(main_class.camera_settings)*len(main_class.light_settings)
                                print("loop count is:", main_class.max_loop_count)
            return