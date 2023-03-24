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

import sys
import bpy
from bpy.types import Operator


class EXAMPLE_OT_operate(Operator):
    bl_idname = "example.operate"
    bl_label = "Test import operator"
    bl_description = ("Tests our dependencies install by trying to import an installed module")
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        print(f'Executing')
        print(f'  {sys.path=}')

        try:
            import six
            self.report({"INFO"}, "Success! Module imported! Commence joyous celebration!")

        except Exception as e:
            self.report({"WARNING"}, "Failure importing our test module. Sadness abounds!")
            print(f'Caught Exception while trying to import six')
            print(f'  Exception: {e}')

        return {"FINISHED"}
