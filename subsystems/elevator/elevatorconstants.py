class ElevatorConstants:
    GEAR_RATIO = 20.0

    # Constants for MotionMagicTorqueCurrentFOC configuration
    MM_START_POSITION_ROTATIONS = 0.0
    """ Elevator starts at bottom which is considered 0 rotations. """

    # ROT = rotation of the mechanism, not motor. See gear ratio above. TODO verify
    MM_CRUISE_VELOCITY_ROT_PER_SEC = 5.0
    """ 5 mechanism rotations per second cruise """
    MM_ACCELERATION_ROT_PER_SEC2 = 10.0
    """ Take approximately 0.5 seconds to reach max vel (10 r/sec^2 * 0.5 sec = 5 r/sec) """
    MM_JERK_ROT_PER_SEC3 = 100.0
    """ Take approximately 0.1 seconds to reach max accel (100 r/sec^3 * 0.1 sec = 10 r/sec^2) """
    # Gains start at 0 and need to be tuned.
    MM_KG_AMPS = 0.0
    """ Gravity feedforward in amps """
    MM_KS_AMPS = 0.0
    """ Feedforward to overcome static friction in amps """
    MM_KV_AMPS_PER_UNIT_OF_TARGET_VELOCITY = 0.0
    """ Closed-loop gain amps per target velocity unit: amps/(rot/sec) """
    MM_KA_AMPS_PER_UNIT_OF_TARGET_ACCEL = 0.0
    """ Closed-loop gain amps per target acceleration unit: amps/(rot/sec^2) """
    MM_KP_AMPS_PER_UNIT_OF_ERROR_IN_POSITION = 0.0
    """ Closed-loop gain amps per unit of error in position: amp/rot """
    MM_KI_AMPS_PER_UNIT_OF_INTEGRATED_ERROR_IN_POSITION = 0.0
    """ Closed-loop gain amps per unit of integrated error in position: amp/rot^2 """
    MM_KD_AMPS_PER_UNIT_OF_ERROR_IN_VELOCITY = 0.0
    """ Closed-loop gain amps per unit of error in velocity: amp/(rot/sec) """
