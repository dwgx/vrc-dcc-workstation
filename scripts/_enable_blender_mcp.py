import addon_utils
import bpy
mod = "blender_mcp"
print("BEFORE", [(m.__name__, addon_utils.check(m.__name__)) for m in addon_utils.modules() if "mcp" in m.__name__.lower() or "MCP" in str(getattr(m,"bl_info",{}))])
addon_utils.enable(mod, default_set=True, persistent=True)
ok, loaded = addon_utils.check(mod)
print("AFTER_CHECK", ok, loaded)
bpy.ops.wm.save_userpref()
print("SAVED_PREFS")
