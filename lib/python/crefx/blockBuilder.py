import maya.cmds as cmds

# TODO Twist Joints
# TODO End joint orient constraint

class ThreeJointIK(object):
    def __init__(self,
                 prefix='L', # prefix is a prefix before the joint, group (and etc) names, e.g. 'L' or 'R'
                 start_location=(0, 0, 0), # start_location is the starting joint location in 3 axis e.g. (0,0,0)
                 end_location=(10, 0, 0), # end_location is the ending joint location in 3 axis e.g. (10,0,0)
                 mid_joint_push_back=1, # amount to push the middle joint backwards (in the Z axis) in Maya units
                 joint_one='Shoulder',
                 joint_two='Elbow',
                 joint_three='Wrist',
                 block_name='Arm' # overall name for the body part
                 ):
        self.prefix = prefix
        self.start_location = start_location
        self.end_location = end_location
        self.mid_joint_push_back = mid_joint_push_back
        self.joint_one = joint_one
        self.joint_two = joint_two
        self.joint_three = joint_three
        self.ext = ['GRP', 'CTRL', 'IK', 'PV']
        self.block_name=block_name

        self.sub_grps = ['Skel', 'Ctrls', 'Parts', 'In', 'Out']

    # TODO def group structure:
    def grp_structure(self):
        self.grp = cmds.createNode('transform', name=self.prefix + '_' + self.block_name + '_' + self.ext[0])
        for item in self.sub_grps:
            grp = cmds.createNode('transform', name=self.prefix + '_' + self.block_name + '_' + item + '_' + self.ext[0], p=self.grp)
            for attr in ['t', 's', 'r']:
                cmds.setAttr(grp + '.' + attr, lock=True)
        cmds.select(d=1)

    def build(self):
        # Create joints for chain
        cmds.joint(n=self.prefix + '_' + self.joint_one, p=self.start_location) # joint_one
        cmds.joint(n=self.prefix + '_' + self.joint_two,
                   p=((self.start_location[0] + self.end_location[0])/2, 0, 0 - self.mid_joint_push_back)) # joint_two
        cmds.joint(n=self.prefix + '_' + self.joint_three, p=self.end_location) # joint_three


        # Set Joint Orient so X points down the bone on joint_one and joint_two
        for joint in [self.joint_one, self.joint_two]:
            cmds.joint(self.prefix + '_' + joint, e=1, zso=1, oj="xyz")


        # Create IK handle from joint_one to joint_two
        cmds.ikHandle(n=self.prefix+'_' + self.block_name + '_' + self.ext[2], # IK Handle name (e.g. "L_Arm_IK")
                      sj=self.prefix + '_' + self.joint_one, # IK Handle starting joint (e.g. "L_Arm")
                      ee=self.prefix + '_' + self.joint_three) # IK Handle ending joint (e.g. "L_Wrist")


        # Create IK control circle, parent it to empty group, and move to Wrist joint
        IKCC = self.prefix + '_' + self.joint_three + '_' + self.ext[2] + '_'
        cmds.circle(n=IKCC + self.ext[1], nrx=1, nrz=0)
        cmds.group(n=IKCC + self.ext[0], em=1)
        cmds.parent(IKCC + self.ext[1], IKCC + self.ext[0])
        cmds.xform(IKCC + self.ext[0], t=(cmds.xform(self.prefix + '_' + self.joint_three, q=1, t=1, ws=1)))


        # Parent the IK Handle to the IK Controller   # e.g. "L_Arm_IK" > "L_Wrist_IK_CTRL"
        cmds.parent(self.prefix + '_' + self.block_name + '_' + self.ext[2],
                    self.prefix + '_' + self.joint_three + '_' + self.ext[2] + '_' + self.ext[1])


        # Create Shoulder controller, parent it to empty group, and move to Shoulder joint
        jnt_one_ctrl = self.prefix + '_' + self.joint_one + '_'
        cmds.circle(n=jnt_one_ctrl + self.ext[1], nrx=1, nrz=0)
        cmds.group(n=jnt_one_ctrl+ self.ext[0], em=1)
        cmds.parent(jnt_one_ctrl + self.ext[1],
                    jnt_one_ctrl + self.ext[0])
        cmds.xform(jnt_one_ctrl + self.ext[0], t=(cmds.xform(self.prefix + '_' + self.joint_one, q=1, t=1, ws=1)))
        # Parent constrain joint_one to the Controller
        cmds.parentConstraint(jnt_one_ctrl + self.ext[1], self.prefix + '_' + self.joint_one)


        # Create Pole Vector controller that looks visually distinct from the others
        #             e.g. "L_PV_IK_CTRL"
        cmds.circle(n=self.prefix + '_' + self.ext[3] + '_' + self.ext[2] + '_' + self.ext[1], nrx=1, nrz=0)
        cmds.select(d=1)
        for x in range(0, 7)[::2]:
            # select every second joint of the circle made to create the PV controller
            cmds.select(self.prefix + '_' + self.ext[3] + '_' + self.ext[2] + '_' + self.ext[1] + '.cv[{}]'.format(x), tgl=0, add=True)
        cmds.selectMode(co=1)
        cmds.xform(s=(.2, .2, .2))
        cmds.selectMode(o=1)

        # Create PV parent group and parent PV control to it, and move behind the elbow location
        cmds.group(n=self.prefix + '_' + self.ext[3] + '_' + self.ext[0], em=1)
        # parents PV control to PV Group    # e.g. "L_PV_IK_CTRL" > "L_PV_GRP"
        cmds.parent(self.prefix + '_' + self.ext[3] + '_' + self.ext[2] + '_' + self.ext[1],
                    self.prefix + '_' + self.ext[3] + '_' + self.ext[0])
        # Move the PV group to joint_two    # e.g. "L_PV_GRP > "L_Elbow"
        cmds.xform(self.prefix + '_' + self.ext[3] + '_' + self.ext[0],
                   t=(cmds.xform(self.prefix + '_' + self.joint_two, q=1, t=1, ws=1)))
            # e.g. "L_PV_GRP"
        cmds.xform(self.prefix + '_' + self.ext[3] + '_' + self.ext[0], t=(0, 0, - self.mid_joint_push_back*3), r=1)
        # Pole Vector constrain the IK to the PV Controller     # e.g. "L_PV_IK_CTRL" > "L_Arm_IK"
        cmds.poleVectorConstraint(self.prefix + '_' + self.ext[3] + '_' + self.ext[2] + '_' + self.ext[1],
                                  self.prefix + '_' + self.block_name + '_' + self.ext[2])


        # Cleanup
        # Hide the IK Handle    # e.g. "L_Arm_IK"
        cmds.hide(self.prefix+'_' + self.block_name + '_' + self.ext[2])
        # delete history on joint_one, joint_three, and PV controller   # e.g. "L_Wrist_IK_CTRL", "L_PV_IK_CTRL"
        cmds.bakePartialHistory(self.prefix + '_' + self.joint_three + '_' + self.ext[2] + '_' + self.ext[1])
        cmds.bakePartialHistory(self.prefix + '_' + self.joint_one + '_' + self.ext[1])
        cmds.bakePartialHistory(self.prefix + '_' + self.ext[3] + '_' + self.ext[2] + '_' + self.ext[1])
        # Lock the Scale and View attributes on the controllers
        # TODO set up for loops for these
            # e.g. "L_Wrist_IK_CTRL"
        cmds.setAttr(self.prefix+'_' + self.joint_three + '_' + self.ext[2] + '_' + self.ext[1] + '.scale', lock=True)
        cmds.setAttr(self.prefix+'_' + self.joint_three + '_' + self.ext[2] + '_' + self.ext[1] + '.visibility', lock=True)
            # e.g. "L_Shoulder_CTRL"
        cmds.setAttr(self.prefix+'_' + self.joint_one + '_' + self.ext[1] + '.scale', lock=True)
        cmds.setAttr(self.prefix+'_' + self.joint_one + '_' + self.ext[1] + '.visibility', lock=True)
        cmds.select(d=1)
