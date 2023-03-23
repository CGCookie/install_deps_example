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

import os
import pkg_resources
import subprocess
import sys
from functools import cache
from pathlib import Path


add_on_path = Path(__file__).parent                     # assuming this file is at root of add-on
requirements_txt = add_on_path / 'requirements.txt'     # assuming requirements.txt is at root of add-on
deps_path = add_on_path / 'deps_public'                 # might not exist until install_deps is called
deps_installed_path = deps_path / 'all_deps_installed'  # a touched file indicating all deps installed correctly

#XXX WARNING! This may cause modules to collide with system modules or modules imported by other add-ons!
sys.path.append(os.fspath(deps_path))


class Dependencies:
    @staticmethod
    def install():
        if Dependencies.check():
            return True

        # Create folder into which pip will install dependencies
        try:
            deps_path.mkdir(exist_ok=True)
        except Exception as e:
            print(f'Caught Exception while trying to create dependencies folder')
            print(f'  Exception: {e}')
            print(f'  Folder: {deps_path}')
            return False

        # Ensure pip is installed
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
        except subprocess.CalledProcessError as e:
            print(f'Caught CalledProcessError while trying to ensure pip is installed')
            print(f'  Exception: {e}')
            print(f'  {sys.executable=}')
            return False

        # Install dependencies from requirements.txt
        try:
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                os.fspath(requirements_txt),
                "--target",
                os.fspath(deps_path)
            ])
        except subprocess.CalledProcessError as e:
            print(f'Caught CalledProcessError while trying to install dependencies')
            print(f'  Exception: {e}')
            print(f'  Requirements: {requirements_txt}')
            print(f'  Folder: {deps_path}')
            return False

        return Dependencies.check(force=True)

    @staticmethod
    def check(*, force=False):
        if not deps_path.exists():
            return False
        if not force:
            return deps_installed_path.exists()

        deps_installed_path.unlink(missing_ok=True)

        try:
            deps = pkg_resources.parse_requirements(requirements_txt.open())
            for dependency in deps:
                pkg_resources.require(str(dependency))
            deps_installed_path.touch(exist_ok=True)
        except Exception as e:
            print(f'Caught Exception while trying to check dependencies')
            print(f'  Exception: {e}')
            return False

        return True

    @staticmethod
    @cache
    def requirements():
        deps = pkg_resources.parse_requirements(requirements_txt.open())
        return [ dep.project_name for dep in deps ]
