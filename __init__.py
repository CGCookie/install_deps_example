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
    "author": "Jason van Gumster, Jonathan Denning",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "Preferences",
    "description": "A simple example of how to install external Python modules locally",
    "warning": "This is only an example!",
    "doc_url": "https://github.com/CGCookie/install_deps_example/",
    "category": "Example",
}


import bpy
from bpy.types import AddonPreferences, Operator, Panel
import sys
import os

# Local imports
from .dependencies import Dependencies
from .example_operator import EXAMPLE_OT_operate


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
        return not Dependencies.check()

    def execute(self, context):
        if not Dependencies.install():
            return {'CANCELLED'}

        # Register any classes that need registering once dependencies are installed
        register_classes_with_dependencies()

        return {"FINISHED"}


class EXAMPLE_AddonPreferences(AddonPreferences):
    """ Preferences for this dummy add-on """
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        layout.label(text=f"This add-on requires a couple Python packages to be installed:")
        for name in Dependencies.requirements():
            layout.label(text=f'- {name}')

        layout.label(text=f"Click the Install Dependencies button below to install.")
        layout.operator(EXAMPLE_OT_install_dependencies.bl_idname, icon="CONSOLE")


class EXAMPLE_PT_Panel(Panel):
    bl_label = "Example Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Example Tab"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        if Dependencies.check():
            layout.operator("example.operate")
        else:
            layout.label(text="You need to install some packages before using this tool")
            layout.label(text="Click below to go to Preferences and install them.")
            layout.operator("screen.userpref_show")


classes_with_dependencies = [
    EXAMPLE_OT_operate,
]
registered_classes_with_dependencies = False

classes_example = [
    EXAMPLE_OT_install_dependencies,
    EXAMPLE_AddonPreferences,
    EXAMPLE_PT_Panel,
]


def register_classes_with_dependencies():
    global registered_classes_with_dependencies
    if registered_classes_with_dependencies:
        # Already registered classes
        return

    if not Dependencies.check(force=True):
        # Dependencies are not installed, so cannot register the classes
        return

    for cls in classes_with_dependencies:
        bpy.utils.register_class(cls)

    registered_classes_with_dependencies = True

def unregister_classes_with_dependencies():
    global registered_classes_with_dependencies
    if not registered_classes_with_dependencies:
        # No registered classes needing unregistered
        return

    for cls in reversed(classes_with_dependencies):
        bpy.utils.unregister_class(cls)

    registered_classes_with_dependencies = False


def register():
    for cls in classes_example:
        bpy.utils.register_class(cls)
    register_classes_with_dependencies()


def unregister():
    unregister_classes_with_dependencies()
    for cls in reversed(classes_example):
        bpy.utils.unregister_class(cls)

