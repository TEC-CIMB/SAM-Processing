from numpy import split, cross, dot, arcsin, concatenate, apply_along_axis
from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R
from pandas import DataFrame, concat
# _______________________________________________________________________________


def ang_cal(pla_ang):
    """ 
    This function calculates angle between the plane of reference in comparison
    of the vector of the angle.
    """
    [a, b, r] = split(pla_ang, 3)
    n = cross(a, b)
    nr_dot = dot(n, r)
    nr_mag = norm(n)*norm(r)
    return arcsin(nr_dot/nr_mag)
# _______________________________________________________________________________


def Angles_Hip(hi, fe, leg):
    """
    This function calculates the angles of the knee joint using the Tibia and 
    Femur sensors.
    """
    rhi = R.from_euler('xyz', hi.loc[:, ['Roll', 'Pitch', 'Yaw']],
                       degrees=True).as_matrix()
    rfe = R.from_euler('xyz', fe.loc[:, ['Roll', 'Pitch', 'Yaw']],
                       degrees=True).as_matrix()
    v_fe = concatenate((rhi[:, 1, :], rhi[:, 0, :], rfe[:, 0, :]), axis=1)
    if leg == 'l':
        v_aa = concatenate(
            (rhi[:, 2, :], rhi[:, 0, :], -rfe[:, 0, :]), axis=1)
        v_ro = concatenate(
            (rhi[:, 2, :], rhi[:, 0, :], -rfe[:, 1, :]), axis=1)
    if leg == 'r':
        v_aa = concatenate(
            (rhi[:, 0, :], rhi[:, 2, :], -rfe[:, 0, :]), axis=1)
        v_ro = concatenate(
            (rhi[:, 0, :], rhi[:, 2, :], rfe[:, 1, :]), axis=1)
    # Flexion-Extension angles.
    f_e = DataFrame(apply_along_axis(
        ang_cal, 1, v_fe), columns=['Fle_Ext'])
    # Abduction-Adduction angles.
    a_a = DataFrame(apply_along_axis(
        ang_cal, 1, v_aa), columns=['Abd_Abb'])
    # Rotation angles.
    rot = DataFrame(apply_along_axis(ang_cal, 1, v_ro), columns=['Rot'])
    return concat([f_e, a_a, rot], axis=1)
# _______________________________________________________________________________


def Angles_Knee(fe, ti, leg):
    """
    This function calculates the angles of the knee joint using the Tibia and 
    Femur sensors.
    """
    rfe = R.from_euler('xyz', fe.loc[:, ['Roll', 'Pitch', 'Yaw']],
                       degrees=True).as_matrix()
    rti = R.from_euler('xyz', ti.loc[:, ['Roll', 'Pitch', 'Yaw']],
                       degrees=True).as_matrix()
    if leg == 'l':
        v_fe = concatenate(
            (rfe[:, 2, :], rfe[:, 0, :], rti[:, 0, :]), axis=1)
        v_aa = concatenate(
            (rfe[:, 1, :], rfe[:, 0, :], -rti[:, 0, :]), axis=1)
        v_ro = concatenate(
            (rfe[:, 1, :], rfe[:, 0, :], -rti[:, 1, :]), axis=1)
    if leg == 'r':
        v_fe = concatenate(
            (rfe[:, 0, :], rfe[:, 2, :], rti[:, 0, :]), axis=1)
        v_aa = concatenate(
            (rfe[:, 0, :], rfe[:, 1, :], -rti[:, 0, :]), axis=1)
        v_ro = concatenate(
            (rfe[:, 0, :], rfe[:, 1, :], rti[:, 1, :]), axis=1)
    # Flexion-Extension angles.
    f_e = DataFrame(apply_along_axis(
        ang_cal, 1, v_fe), columns=['Fle_Ext'])
    # Abduction-Adduction angles.
    a_a = DataFrame(apply_along_axis(
        ang_cal, 1, v_aa), columns=['Abd_Abb'])
    # Rotation angles.
    rot = DataFrame(apply_along_axis(ang_cal, 1, v_ro), columns=['Rot'])
    return concat([f_e, a_a, rot], axis=1)
# _______________________________________________________________________________


def Angles_Ankle(ti, fo, leg):
    """
    This function calculates the angles of the ankle joint using the Tibia and 
    Foot sensors.
    """
    rti = R.from_euler('xyz', ti.loc[:, ['Roll', 'Pitch', 'Yaw']],
                       degrees=True).as_matrix()
    rfo = R.from_euler('xyz', fo.loc[:, ['Roll', 'Pitch', 'Yaw']],
                       degrees=True).as_matrix()
    if leg == 'l':
        v_fe = concatenate(
            (rti[:, 1, :], rti[:, 2, :], -rfo[:, 0, :]), axis=1)
        v_aa = concatenate(
            (rti[:, 0, :], rti[:, 1, :], -rfo[:, 0, :]), axis=1)
        v_ro = concatenate(
            (rti[:, 1, :], rti[:, 2, :], -rfo[:, 1, :]), axis=1)
    if leg == 'r':
        v_fe = concatenate(
            (rti[:, 2, :], rti[:, 1, :], -rfo[:, 0, :]), axis=1)
        v_aa = concatenate(
            (rti[:, 1, :], rti[:, 0, :], -rfo[:, 0, :]), axis=1)
        v_ro = concatenate(
            (rti[:, 2, :], rti[:, 1, :], rfo[:, 1, :]), axis=1)
    # Flexion-Extension angles.
    f_e = DataFrame(apply_along_axis(
        ang_cal, 1, v_fe), columns=['Fle_Ext'])
    # Abduction-Adduction angles.
    a_a = DataFrame(apply_along_axis(
        ang_cal, 1, v_aa), columns=['Abd_Abb'])
    # Rotation angles.
    rot = DataFrame(apply_along_axis(ang_cal, 1, v_ro), columns=['Rot'])
    return concat([f_e, a_a, rot], axis=1)
