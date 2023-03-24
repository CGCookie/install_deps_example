# Install Dependencies Example Blender Add-on

This base code serves as an example mechanism for loading external Python dependencies, should they happen to be necessary for your add-on to function. For the most part, this code should be pretty easy to bolt on to an existing add-on.

Features:

  * Relatively easy to incorporate to an existing add-on
  * Multi-platform (tested in Linux, OSX, and Windows)
  * Modules are installed to the add-on's path, not Blender's Python path
  * Uses Blender's Python/PIP to install modules
  * Makes use of `requirements.txt` workflow common in Python development
  * Requires user action to install modules (not automatic)

Known Issues:

  * Although modules are installed local to the add-on, they are _not_ sandboxed. Modules are accessible across all of Blender. This means that there is a chance that modules may collide if other add-ons use this mechanism to install their own modules. Unfortunately, this is an issue within Blender without an easy solution overall.
