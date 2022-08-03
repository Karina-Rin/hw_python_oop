from typing import Dict
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    # создаем объекты этого класса и указываем свойства
    training_type: str  # имя класса тренировки
    duration: float  # длительность тренировки в часах
    distance: float  # дистанция в километрах
    speed: float  # cредняя скорость, с которой двигался пользователь
    calories: float  # количество килокалорий

    # Числовые значения должны округляться при
    # выводе до тысячных долей (до третьего знака после запятой)

    def get_message(self) -> str:  # возвращает строку сообщения
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # один шаг в метрах
    M_IN_KM = 1000  # константа для перевода значений из метров в километры
    H_IN_MIN = 60  # константа для перевода значений из часов в минуты
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def __init__(
        self,
        action: int,  # число шагов при ходьбе
        # и беге либо гребков — при плавании
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        dist_km = self.action * self.LEN_STEP / self.M_IN_KM
        return dist_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        # преодоленная_дистанция_за_тренировку / время_тренировки
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # spent_calories = (18 * средняя_скорость - 20)
        # * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        raise NotImplementedError(  # метод нужно реализовать в наследнике
            "Определите get_spent_calories в %s." % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_result = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return info_result


class Running(Training):
    """Тренировка: бег."""

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:

        spent_calories = (
            (
                self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.H_IN_MIN)
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029
    COEFF_CALORIE_3 = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,  # рост спортсмена
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # (0.035 * вес + (средняя_скорость**2 // рост)
        # * 0.029 * вес) * время_тренировки_в_минутах

        spent_calories = (
            self.COEFF_CALORIE_1 * self.weight
            + (self.get_mean_speed() ** self.COEFF_CALORIE_3 // self.height)
            * self.COEFF_CALORIE_2
            * self.weight
        ) * (self.duration * self.H_IN_MIN)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    # Чтобы определить дистанцию, которую преодолел спортсмен,
    # нужно число шагов или гребков, переданное в action, перевести в километры

    LEN_STEP = 1.38  # один гребок при плавании в метрах
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,  # длина бассейна в метрах
        count_pool: float,  # сколько раз пользователь переплыл бассейн
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        # длина_бассейна * count_pool / M_IN_KM
        # / время_тренировки = расчёт средней скорости

        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        # (средняя_скорость + 1.1) * 2 * вес = расчёт израсходованных калорий
        spent_calories = (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2
            * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: dict) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_workout: Dict[str, type] = {  # словарь
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    return types_of_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


# Имитация получения данных от блока датчиков фитнес-трекера:
if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
