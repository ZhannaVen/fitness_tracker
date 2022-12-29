
from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """The message about the workout."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Workout type:: {training_type}; '
        'Duration: {duration:.3f} hours; '
        'Distance: {distance:.3f} km; '
        'Average speed: {speed:.3f} km/hour; '
        'Calories burned: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Base class of training."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINS_PER_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """The function gets the distance in kilometers."""
        return (
            self.action
            * self.LEN_STEP
            / self.M_IN_KM
        )

    def get_mean_speed(self) -> float:
        """The function gets the average speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """The functions gets the number of calories burned."""
        pass

    def show_training_info(self) -> InfoMessage:
        """The functions returns a message about the completed workout."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Workout: running."""
    COEFF_RUN1: int = 18
    COEFF_RUN2: int = 20

    def get_spent_calories(self) -> float:
        """The functions gets the number of calories burned."""
        return (
            (
                self.COEFF_RUN1
                * self.get_mean_speed()
                - self.COEFF_RUN2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MINS_PER_HOUR
        )


class SportsWalking(Training):
    """Training: sportswalking."""

    COEFF_WLK1: int = 0.035
    COEFF_WLK2: int = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.COEFF_WLK1
                * self.weight
                + (
                    self.get_mean_speed() ** 2
                    // self.height
                )
                * self.COEFF_WLK2
                * self.weight
            )
            * self.duration
            * self.MINS_PER_HOUR
        )


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38
    COEFF_SWM1: float = 1.1
    COEFF_SWM2: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (
            self.action
            * self.LEN_STEP
            / self.M_IN_KM
        )

    def get_mean_speed(self) -> float:
        return (
            self.lenght_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (
                self.get_mean_speed()
                + self.COEFF_SWM1
            )
            * self.COEFF_SWM2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """The function reads the data received from the sensors."""

    workout_types_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    appropriate_trainings = ' '.join(workout_types_dict)
    if workout_type not in workout_types_dict:
        raise ValueError(
            'Unknown workout type. Allowed: '
            f'{appropriate_trainings}'
        )
    return workout_types_dict[workout_type](*data)


def main(training: Training) -> None:
    """The main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
