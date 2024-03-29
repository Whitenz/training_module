from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __str__(self) -> str:
        """Строковое представление объекта класса InfoMessage."""
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.'
                )

    def get_message(self) -> str:
        """Получить строку с информацией о тренировке."""
        return str(self)


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # how meters in one kilometer
    MIN_IN_HOUR: int = 60  # how minutes in one hour
    LEN_STEP: float = 0.65  # distance for one step

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18  # coeff for calculating calories spent
    COEFF_CALORIE_2: int = 20  # coeff for calculating calories spent

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                                 - self.COEFF_CALORIE_2) * self.weight
                                 / self.M_IN_KM * self.duration
                                 * self.MIN_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035  # coeff for calculating calories spent
    COEFF_CALORIE_2: float = 0.029  # coeff for calculating calories spent

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = ((self.COEFF_CALORIE_1 * self.weight
                                 + (self.get_mean_speed()**2 // self.height)
                                 * self.COEFF_CALORIE_2 * self.weight)
                                 * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # distance for one stroke
    COEFF_CALORIE_1: float = 1.1  # coeff for calculating calories spent
    COEFF_CALORIE_2: int = 2  # coeff for calculating calories spent

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                                 * self.COEFF_CALORIE_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dictionary: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                      'RUN': Running,
                                                      'WLK': SportsWalking
                                                      }
    parameters: list = data
    if workout_type in training_dictionary:
        return training_dictionary[workout_type](*parameters)
    raise ValueError('Неизвестный код тренировки.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
