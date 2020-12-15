# Toolbox-Intralogistic-AI-Data

## Introduction

Welcome to the alpha release of the Intralogistic AI Data Generator. The application was developed for the 3D graphics suite Blender and allows you to recreate transport cases of intralogistics and generate synthetic images for training neural networks. 
Special attention of the development was paid to the extensive automation of the application and the generation of image databases with a minimum of human intervention.

## Roadmap

![Roadmap](https://github.com/TUHH-IFPT/Toolbox-Intralogistic-AI-Data/blob/main/git_images/Roadmap.JPG?raw=true)

The Intralogistic AI Data Generators has reached its first phase with its alpha release and will continue to evolve in the future to allow for more synthetic data generation capabilities in its feature set.
The next phase will be the development of a user interface to enable the most intuitive use of the tool. This will include specifying simulation parameters, objects used, lighting and camera options, and randomization intervals. This will be followed by the implementation of further use cases in intralogistics to generate more robust and diverse data sets.

## How to install

To integrate the version of the Data Generator presented here into Blender, the uploaded code can be downloaded as a ZIP file and installed within Blender under "Edit -> Preferences -> Add-ons -> Install". The following [link](https://www.youtube.com/watch?v=14G_YIVdBd0) shows the installation process for another addon and can be applied to this application.

## How to use

At the moment there are two Excel files available in the folder ../database.

**Obj_data.csv** : This file offers the possibility to define which objects should be in the simulation. The supplied version, provides a basic framework to create a simulation with an object. However, the file paths must still be created to the corresponding .obj files for the respective system. There are some models for testing in ../obj_file.

**Render_data.csv** : This file offers possibilities to define camera and light sources, as well as corresponding information about positions in spherical coordinates.

ATTENTION: The interface update will bring major changes in the applicability of the Data Generator. Previous control structures are designed for development purposes and their functionality will be significantly extended and made more accessible.
