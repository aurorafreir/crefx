import maya.cmds as cmds

def lerp(min, max, percent):
    return ((max-min)*percent)+min

def vector_lerp(min, max, percent):
    x = lerp(min[0], max[0], percent)
    y = lerp(min[1], max[1], percent)
    z = lerp(min[2], max[2], percent)
    return x, y, z

class build_spine(object):
    # todo create joint chain
    # todo create controllers
    # todo create spline
    # todo create Spline IK
    # todo create group structure
    def __init__(self):
        self.joint_count=8
        self.start_position=(0,0,0)
        self.end_position=(0,10,0)


    def build_spine_block(self):
        # Create joints
        # todo joint orients
        crnt_jnt_count = 0
        jnt_count_add = 1.0 / (self.joint_count)
        for joint in range(0, self.joint_count):
            cmds.joint(n="joint"+str(joint), p=vector_lerp(self.start_position, self.end_position, crnt_jnt_count), rad=0.5)
            crnt_jnt_count = crnt_jnt_count + jnt_count_add


        # Create Spline



        # Create Spline IK



    # create group structure
    def grp_structure(self):
        pass
