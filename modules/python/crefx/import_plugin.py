import sys

path = "/home/aurorafreir/github/crefx/modules/python"
if path not in sys.path:
    sys.path.insert(0, path)

sys.path

# import crefx.blockBuilder as bb
# reload(bb)
import crefx.UI
reload(crefx.UI)