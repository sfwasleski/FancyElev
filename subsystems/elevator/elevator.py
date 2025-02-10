from commands2 import Command, Subsystem
from phoenix6 import StatusCode, StatusSignal, ampere
from phoenix6.configs import TalonFXConfiguration
from phoenix6.controls import Follower, MotionMagicTorqueCurrentFOC
from phoenix6.hardware import TalonFX
from phoenix6.signals.spn_enums import GravityTypeValue
from wpilib import SmartDashboard

from constants import Constants
from subsystems.elevator.elevatorconstants import ElevatorConstants
from subsystems.elevator.floor import Floor


class Elevator(Subsystem):
    def __init__(self) -> None:
        # Left motor is the leader and will be configured below
        self.left = TalonFX(Constants.CanIds.ELEVATOR_LEFT_MOTOR)
        # Right follows left inverted
        self.right = TalonFX(Constants.CanIds.ELEVATOR_RIGHT_MOTOR)
        # Right follows left inverted
        self.right.set_control(Follower(Constants.CanIds.ELEVATOR_LEFT_MOTOR, True))

        # Configure the leader motion magic current control
        self.motionMagic = MotionMagicTorqueCurrentFOC(
            ElevatorConstants.MM_START_POSITION_ROTATIONS
        )

        cfg = TalonFXConfiguration()
        cfg.feedback.sensor_to_mechanism_ratio = ElevatorConstants.GEAR_RATIO
        cfg.motion_magic.motion_magic_cruise_velocity = (
            ElevatorConstants.MM_CRUISE_VELOCITY_ROT_PER_SEC
        )
        cfg.motion_magic.motion_magic_acceleration = (
            ElevatorConstants.MM_ACCELERATION_ROT_PER_SEC2
        )
        cfg.motion_magic.motion_magic_jerk = ElevatorConstants.MM_JERK_ROT_PER_SEC3
        # Configure motion magic gains on slot 0
        cfg.slot0.gravity_type = GravityTypeValue.ELEVATOR_STATIC
        cfg.slot0.k_g = ElevatorConstants.MM_KG_AMPS
        cfg.slot0.k_s = ElevatorConstants.MM_KS_AMPS
        cfg.slot0.k_v = ElevatorConstants.MM_KV_AMPS_PER_UNIT_OF_TARGET_VELOCITY
        cfg.slot0.k_a = ElevatorConstants.MM_KA_AMPS_PER_UNIT_OF_TARGET_ACCEL
        cfg.slot0.k_p = ElevatorConstants.MM_KP_AMPS_PER_UNIT_OF_ERROR_IN_POSITION
        cfg.slot0.k_i = (
            ElevatorConstants.MM_KI_AMPS_PER_UNIT_OF_INTEGRATED_ERROR_IN_POSITION
        )
        cfg.slot0.k_d = ElevatorConstants.MM_KD_AMPS_PER_UNIT_OF_ERROR_IN_VELOCITY

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.talonfx.configurator.apply(cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

    def floorCommand(self, floor: Floor) -> Command:
        return self.runOnce(lambda: self._setTargetFloor(floor))

    def _setTargetFloor(self, floor: Floor) -> None:
        self._setTargetPosition(floor.value)

    def _setTargetPosition(self, position) -> None:
        self.left.set_control(self.motionMagic.with_position(position))

    def periodic(self) -> None:
        """
        Overridden to monitor for reaching the bottom or top hard stop.
        If a hard stop is reached, encoder position is reset.

        For now, just some dashboard work.
        """
        current: StatusSignal[ampere] = self.left.get_torque_current()
        SmartDashboard.putNumber("Elevator left amps", current.value())
        current = self.right.get_torque_current()
        SmartDashboard.putNumber("Elevator right amps", current.value())
