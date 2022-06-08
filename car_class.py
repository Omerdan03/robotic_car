import numpy as np

tolerance = 2  # if the car is in the proximity of the target pos it will be considers to be exactly at the position


class Car:
    """
    This class contains all the needed physics about our car
    """

    drag_force = 0.5
    accelerating = 3
    MAX_SPEED = 10

    def __init__(self, start_pos=0, mode='simple'):
        self.speed = 0
        self.pos = start_pos
        self.target_pos = start_pos
        self.is_active = False

        self._mode = mode

    def __str__(self):
        """
        :return: all car's information for debugging
        """
        title = 'Car debug information: \n ~~~~~~~~~~~~'
        pos = f'position: {self.pos}'
        target_pos = f'target position: {self.target_pos}'
        speed = f'speed: {self.speed}'
        active = f'car is currently{"" if self.is_active else " not"} active'

        return "\n".join([title, pos, target_pos, speed, active, '\n'])

    def update_speed(self):
        """
        Changing speed according to target_pos and current pos
        """
        pos_delta = self.target_pos - self.pos
        self.speed += np.sign(pos_delta) * self.accelerating
        # todo update speed according to pos_delta value instead of just it's sign
        if abs(self.speed) > self.MAX_SPEED:
            self.speed = np.sign(self.speed) * self.MAX_SPEED

    def run(self):
        """
        This function will apply car's physics
        """
        if (self._mode == 'simple') & self.is_active:
            if abs(self.target_pos - self.pos) < self.speed:
                self.pos = self.target_pos
            else:
                self.pos += np.sign(self.target_pos - self.pos) * self.speed

        if self._mode == 'advance':
            if abs(self.target_pos - self.pos) < tolerance:
                # If the car is close to the position it will be considered as it arrived
                self.pos = self.target_pos
            # adding drag force in opposite direction of the car
            self.speed += -np.sign(self.speed) * self.drag_force

            if self.is_active:
                # Use car control to update speed
                self.update_speed()

            # updating the car position according to the speed
            self.pos += self.speed
