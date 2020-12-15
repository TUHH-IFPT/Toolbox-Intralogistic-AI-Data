import bpy
from math import radians
from random import randint

class Randomiser():

    def __init__(self):
        pass

    def do_random_object_pose(self, context, passive_box, safty_margin=[0,0,0], xyz_manipulator=[0,0,0]):
        """
            Functioncall to get a random location inside of a given box with a random angle
            
            Parameter:
                passive_box(object): the chosen box for the function to get information about the dimensions
                safty_margin(float[x,y,z]): Parameter to avoid, that objects get a random location 
                                            to close to the walls of the box. Increase for less collisions.
                                            chose interval from[0 ; 1]. 0 = no margin, 1 = all the margin
                xyz_manipulator(float[x,y,z]):  adding a x,y,z to the random location. 
                                                Be aware, that objects my be out of bounds
        
            Return:
                location(float[x,y,z]): location in global coordinates, relative to the given object
                rotation(float[alpha,beta,gamma])
        """
        x = passive_box.location[0] + xyz_manipulator[0] + randint(-round(passive_box.dimensions[0]*(0.5-(safty_margin[0]/2))), round(passive_box.dimensions[0]*(0.5-(safty_margin[0]/2))))
        y = passive_box.location[1] + xyz_manipulator[1] + randint(-round(passive_box.dimensions[1]*(0.5-(safty_margin[1]/2))), round(passive_box.dimensions[1]*(0.5-(safty_margin[1]/2))))
        z = passive_box.location[2] + xyz_manipulator[2] + randint(round(passive_box.dimensions[2]*safty_margin[2]), round(passive_box.dimensions[2]*safty_margin[2] + passive_box.dimensions[2]/2)) # randint(-round(passive_box.dimensions[2]*(0.5-(safty_margin[2]/2))), round(passive_box.dimensions[2]*(0.5-(safty_margin[2]/2))))
        alpha = radians(randint(-90, 90))
        beta = radians(randint(-90, 90))
        gamma = radians(randint(-90, 90))
        return [x, y, z], [alpha, beta, gamma]

        