import os
import sys
import numpy as np
import itertools
import math
sys.path.append("/opt/openrobots/lib/python3.8/site-packages")
from pinocchio import visualize
import pinocchio
import example_robot_data
import crocoddyl
from pinocchio.robot_wrapper import RobotWrapper

# current_directory = os.getcwd()
# print("上层路径：", current_directory)

# change path ??
modelPath = '/home/lee/humanoid-gym/resources/robots/pandaman/'
URDF_FILENAME = "urdf/pandaman.urdf"

# Load the full model
rrobot = RobotWrapper.BuildFromURDF(modelPath + URDF_FILENAME, [modelPath], pinocchio.JointModelFreeFlyer())  # Load URDF file
rmodel = rrobot.model

rightFoot = 'right_ankle_link'
leftFoot = 'left_ankle_link'

display = crocoddyl.MeshcatDisplay(
    rrobot, frameNames=[rightFoot, leftFoot]
)
q0 = pinocchio.utils.zero(rrobot.model.nq)
print(rrobot.model.nq)
display.display([q0])
#print(1)

rdata = rmodel.createData()
pinocchio.forwardKinematics(rmodel, rdata, q0)
pinocchio.updateFramePlacements(rmodel, rdata)

rfId = rmodel.getFrameId(rightFoot)
lfId = rmodel.getFrameId(leftFoot)

rfFootPos0 = rdata.oMf[rfId].translation
lfFootPos0 = rdata.oMf[lfId].translation

comRef = pinocchio.centerOfMass(rmodel, rdata, q0)


#print(1)

initialAngle = np.array([0.,0.,0.54,-1.06,-0.4,0.,0.,-0.54,1.06,0.4])
q0 = pinocchio.utils.zero(rrobot.model.nq)
q0[6] = 1  # q.w
q0[2] =0.5848  # z
q0[ 7:17] = initialAngle
display.display([q0])

for i in range(rrobot.model.nq-7):
    q0 = pinocchio.utils.zero(rrobot.model.nq)
    q0[6] = 1  # q.w
    q0[2] = 0  # z
    q0[i+7] = 1
    display.display([q0])
    #print(1)


for i in range(5000):
    phase = i * 0.005
    sin_pos = np.sin(2 * np.pi * phase)
    sin_pos_l = sin_pos.copy()
    sin_pos_r = sin_pos.copy()

    ref_dof_pos = np.zeros((1,10))
    scale_1 = 0.26
    scale_2 = 2 * scale_1
    # left foot stance phase set to default joint pos
    if sin_pos_l > 0 :
        sin_pos_l = sin_pos_l * 0
    ref_dof_pos[:, 2] = -sin_pos_l * scale_1+initialAngle[2]
    ref_dof_pos[:, 3] = sin_pos_l * scale_2+initialAngle[3]
    ref_dof_pos[:, 4] = sin_pos_l * scale_1+initialAngle[4]
    # right foot stance phase set to default joint pos
    if sin_pos_r < 0:
        sin_pos_r = sin_pos_r * 0
    ref_dof_pos[:, 7] = -sin_pos_r * scale_1+initialAngle[7]
    ref_dof_pos[:, 8] = sin_pos_r * scale_2+initialAngle[8]
    ref_dof_pos[:, 9] = sin_pos_r * scale_1+initialAngle[9]
    # Double support phase
    ref_dof_pos[np.abs(sin_pos) < 0.1] = 0

    q0 = pinocchio.utils.zero(rrobot.model.nq)
    q0[6] = 1  # q.w
    q0[2] = 0  # z
    q0[7:17] = ref_dof_pos
    display.display([q0])
    # print(1)





for i in range(rrobot.model.nq-7):
    q0 = pinocchio.utils.zero(rrobot.model.nq)
    q0[6] = 1  # q.w
    q0[2] = 0  # z
    q0[i+7] = 1
    display.display([q0])
    #print(1)
