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
import subprocess
import os
from os.path import join, realpath, dirname
from pathlib import Path
import pkg_resources


def install_deps():
    project_root_dir = dirname(realpath(__file__))
    deps_dir = join(project_root_dir, "deps_public")

    os.makedirs(deps_dir, exist_ok=True)

    # Ensure pip is installed
    print(sys.executable)
    subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    
    # Install dependencies from requirements.txt
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        join(project_root_dir, "requirements.txt"),
        "--target",
        deps_dir
    ])


def check_deps():
    requirements_txt = Path(__file__).with_name("requirements.txt")

    deps = pkg_resources.parse_requirements(requirements_txt.open())

    for dependency in deps:
        dependency = str(dependency)

        try:
            pkg_resources.require(dependency)
        except:
            return False

    return True
