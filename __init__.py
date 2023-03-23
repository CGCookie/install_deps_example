'''
Copyright (C) 2023 Orange Turbine
https://orangeturbine.com
orangeturbine@cgcookie.com

Created by Jason van Gumster

    This file is part of an Install Dependencies Example.

    This example is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.
   
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
   
    You should have received a copy of the GNU General Public License
    along with this program; if not, see <https://www.gnu.org/licenses/>.

'''

bl_info = {
    "name": "Install Dependencies Example",
    "author": "Jason van Gumster",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "Preferences",
    "description": "A simple example of how to install external Python modules locally",
    "warning": "This is only an example!",
    "doc_url": "",
    "category": "Example",
}


import bpy
from bpy.types import AddonPreferences, Operator
import sys
import os

# Local imports
from . import global_vars
global_vars.initialize()
from .install_dependencies import install_deps, check_deps
from .example_operator import EXAMPLE_OT_operate


classes = (EXAMPLE_OT_operate,)


class EXAMPLE_OT_install_dependencies(Operator):
    bl_idname = "preferences.example_install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required Python packages for this add-on. "
                      "Internet connection is required. Packages are installed locally to "
                      "this add-on, not to the system Python or Blender's Python.")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not global_vars.dependencies_installed

    def execute(self, context):
        if not install_deps():
            return {'CANCELLED'}
        global_vars.dependencies_installed = check_deps()

        # Register any classes that need registering once dependencies are installed
        for cls in classes:
            bpy.utils.register_class(cls)

        return {"FINISHED"}


class EXAMPLE_AddonPreferences(AddonPreferences):
    """ Preferences for this dummy add-on """
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        lines = [f"This add-on requires a couple Python packages to be installed:",
                 f"  -six",
                 f"Click the Install Dependencies button below to install."]

        for line in lines:
            layout.label(text=line)

        layout.operator(EXAMPLE_OT_install_dependencies.bl_idname, icon="CONSOLE")


pref_classes = (EXAMPLE_OT_install_dependencies,
                EXAMPLE_AddonPreferences)


def register():
    for cls in pref_classes:
        bpy.utils.register_class(cls)

    deps_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "deps_public")
    if os.path.exists(deps_path):
        #XXX WARNING! This may cause modules to collide with system modules or modules imported by other add-ons!
        sys.path.append(deps_path)

    global_vars.dependencies_installed = check_deps()

    if global_vars.dependencies_installed:
        for cls in classes:
            bpy.utils.register_class(cls)


def unregister():
    for cls in pref_classes:
        bpy.utils.unregister_class(cls)

    if global_vars.dependencies_installed:
        for cls in classes:
            bpy.utils.unregister_class(cls)
