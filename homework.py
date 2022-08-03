from unicodedata import name
from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(  # создает объекты этого класса
        self,
        training_type: str,  # имя класса тренировки
        duration: float,  # длительность тренировки в часах
        distance: float,  # дистанция в километрах, которую преодолел пользователь за время тренировки
        speed: float,  # cредняя скорость, с которой двигался пользователь
        calories: float,
    ) -> None:
        # свойства класса:
        self.training_type = training_type
        self.duration = f"{duration:.3f}"
        self.distance = f"{distance:.3f}"
        self.speed = f"{speed:.3f}"
        self.calories = f"{calories:.3f}"

    # Числовые значения должны округляться при выводе до тысячных долей
    # (до третьего знака после запятой

    # Информационное сообщение должно включать такую информацию:
    # тип тренировки (бег, ходьба или плавание);
    # длительность тренировки
    # дистанция, которую преодолел пользователь, в километрах;
    # среднюю скорость на дистанции, в км/ч;
    # расход энергии, в килокалориях.

    def get_message(self) -> str:  # возвращает строку сообщения
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration} ч.; "
            f"Дистанция: {self.distance} км; "
            f"Ср. скорость: {self.speed} км/ч; "
            f"Потрачено ккал: {self.calories}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # при плавании 1.38
    M_IN_KM = 1000  # константа для перевода значений из метров в километры

    def __init__(
        self,
        action: int,  # число шагов при ходьбе и беге либо гребков — при плавании
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
        # spent_calories = (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        spent_calories = (
            (coeff_calorie_1 * self.get_mean_speed - coeff_calorie_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * 60
        )
        return spent_calories

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
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        M_IN_KM = 1000  # константа для перевода значений из метров в километры
        spent_calories = (
            (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
            * self.weight
            / M_IN_KM
            * (self.duration * 60)
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

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
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029

        spent_calories = coeff_calorie_1 * self.weight + (
            self.get_mean_speed() ** 2 // self.height
        ) * coeff_calorie_2 * self.weight * (self.duration * 60)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    # Чтобы определить дистанцию, которую преодолел спортсмен, нужно число шагов или гребков, переданное в action, перевести в километры.
    # Один шаг — это 0.65 метра, один гребок при плавании — 1.38 метра.
    LEN_STEP = 1.38
    coeff_calorie_1 = 1.1

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
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки = расчёт средней скорости
        M_IN_KM = 1000  # константа для перевода значений из метров в километры
        mean_speed = (
            self.length_pool * self.count_pool / M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        # (средняя_скорость + 1.1) * 2 * вес = расчёт израсходованных калорий
        spent_calories = (
            (self.get_mean_speed() + self.coeff_calorie_1) * 2 * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: dict) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_workout: Dict[str, type] = {
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
