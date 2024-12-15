import time
from datetime import datetime, timedelta
import random


class Bus:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.is_on_route = False
        self.start_time = None
        self.end_time = None
        self.passengers = 0

    def start_route(self, simulated_time):
        self.is_on_route = True
        self.start_time = simulated_time
        self.end_time = simulated_time + timedelta(minutes=70)
        self.passengers = 0

    def end_route(self):
        self.is_on_route = False
        self.start_time = None
        self.end_time = None
        self.passengers = 0

    def get_status(self):
        if self.is_on_route:
            return f"Автобус {self.bus_id} на маршруте. Время начала: {self.start_time.strftime('%H:%M')}, " \
                   f"Ожидаемое время окончания: {self.end_time.strftime('%H:%M')}, Пассажиров: {self.passengers}"
        else:
            return f"Автобус {self.bus_id} не на маршруте."


class Driver:
    def __init__(self, driver_id, driver_type):
        self.driver_id = driver_id
        self.driver_type = driver_type
        self.is_on_duty = False
        self.start_time = None
        self.end_time = None
        self.lunch_break = False
        self.break_count = 0

    def start_duty(self, simulated_time):
        self.is_on_duty = True
        self.start_time = simulated_time
        if self.driver_type == 'A':
            self.end_time = simulated_time + timedelta(hours=9)
        elif self.driver_type == 'B':
            self.end_time = simulated_time + timedelta(hours=9)

    def end_duty(self):
        self.is_on_duty = False
        self.start_time = None
        self.end_time = None
        self.lunch_break = False
        self.break_count = 0

    def take_lunch_break(self):
        if not self.lunch_break:
            self.lunch_break = True
            print(f"Водитель {self.driver_id} ({self.driver_type}) берет перерыв на обед.")
            # time.sleep(LUNCH_BREAK_SIMULATED)  # Перерыв на обед в симулированном времени

    def take_short_break(self):
        if self.break_count < 6:  # Максимально 6 перерывов по 15 минут
            self.break_count += 1
            print(f"Водитель {self.driver_id} ({self.driver_type}) берет короткий перерыв.")
            # time.sleep(SHORT_BREAK_SIMULATED)  # Перерыв 15 минут в симулированном времени

    def get_status(self):
        if self.is_on_duty:
            return f"Водитель {self.driver_id} ({self.driver_type}) на смене. Время начала: {self.start_time.strftime('%H:%M')}, " \
                   f"Ожидаемое время окончания: {self.end_time.strftime('%H:%M')}"
        else:
            return f"Водитель {self.driver_id} ({self.driver_type}) не на смене."


# Константы
BUS_CAPACITY = 20  # Вместимость автобуса
BUS_DEPARTURE_INTERVAL = 70  # Интервал выезда автобусов в минутах
MIN_PASSENGERS_PER_STATION = 3  # Минимальное количество пассажиров на станции
MAX_PASSENGERS_PER_STATION = 5  # Максимальное количество пассажиров на станции


# Функция для генерации рандомного пассажиропотока на станции
def generate_passengers_per_station():
    return random.randint(MIN_PASSENGERS_PER_STATION, MAX_PASSENGERS_PER_STATION)


# Функция для имитации работы автобусов и водителей на всех станциях
def simulate_bus_route(buses, drivers_type_a, drivers_type_b, bus, num_stations, simulated_time):
    global NUM_BUSES_ON_ROUTE

    # Выбираем водителя для автобуса
    driver = None
    for d in drivers_type_a + drivers_type_b:
        if not d.is_on_duty:
            driver = d
            break
    if driver:
        driver.start_duty(simulated_time)
        print(driver.get_status())

        # Запускаем маршрут для автобуса
        bus.start_route(simulated_time)
        NUM_BUSES_ON_ROUTE += 1

        print(f"Автобус {bus.bus_id} выезжает из автопарка в {simulated_time.strftime('%H:%M')}")

        # Собираем пассажиров на всех станциях
        for station_id in range(1, num_stations + 1):
            passengers_to_board = generate_passengers_per_station()
            bus.passengers += passengers_to_board
            print(
                f"Станция {station_id}: Пассажиров - {passengers_to_board}, Всего пассажиров в автобусе - {bus.passengers}")

            # Пассажиры выходят на станциях от 1 до 4
            if 1 <= station_id <= 4:
                passengers_to_exit = random.randint(1,
                                                    min(bus.passengers, 5))  # Рандомное количество выходящих пассажиров
                bus.passengers -= passengers_to_exit
                print(
                    f"Пассажиры выходят на станции {station_id}: {passengers_to_exit}, Осталось пассажиров в автобусе - {bus.passengers}")

            # Задержка между станциями
            simulated_time += timedelta(minutes=10)

        # Автобус едет обратно
        print(f"Автобус {bus.bus_id} едет обратно в автопарк в {simulated_time.strftime('%H:%M')}")

        # Ждем время маршрута
        bus.end_route()
        NUM_BUSES_ON_ROUTE -= 1

        print(bus.get_status())
        print(f"Количество автобусов на маршруте: {NUM_BUSES_ON_ROUTE}")

        # Проверяем, нужно ли завершить смену водителя
        if (simulated_time - driver.start_time).total_seconds() / 3600 >= 9 or (
                driver.driver_type == 'B' and (simulated_time - driver.start_time).total_seconds() / 3600 >= 9):
            driver.end_duty()
            print(driver.get_status())
    else:
        print("Нет свободных водителей.")


# Функция для имитации работы автобусов и водителей на всех автобусах
def simulate_bus_routes(buses, drivers_type_a, drivers_type_b, num_stations):
    global NUM_BUSES_ON_ROUTE

    # Начало рабочего дня с 6:00 утра
    start_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    if datetime.now() > start_time:
        start_time += timedelta(days=1)

    simulated_time = start_time
    print(f"Начало симуляции: {simulated_time.strftime('%H:%M')}")

    NUM_BUSES_ON_ROUTE = 0

    # Вывод расписания для каждого автобуса
    print("Расписание автобусов:")
    for i, bus in enumerate(buses):
        departure_time = simulated_time + timedelta(minutes=i * BUS_DEPARTURE_INTERVAL)
        print(f"Автобус {bus.bus_id}: Время выезда - {departure_time.strftime('%H:%M')}")

    for bus in buses:
        simulate_bus_route(buses, drivers_type_a, drivers_type_b, bus, num_stations, simulated_time)
        simulated_time += timedelta(minutes=BUS_DEPARTURE_INTERVAL)


def main():
    global NUM_BUSES_ON_ROUTE

    # Базовое количество автобусов и водителей
    num_buses = 8
    num_drivers_type_a = 4
    num_drivers_type_b = 4

    # Количество станций
    num_stations = int(input("Введите количество станций: "))

    # Инициализация автобусов и водителей
    buses = [Bus(bus_id) for bus_id in range(1, num_buses + 1)]
    drivers_type_a = [Driver(driver_id, 'A') for driver_id in range(1, num_drivers_type_a + 1)]
    drivers_type_b = [Driver(driver_id, 'B') for driver_id in
                      range(num_drivers_type_a + 1, num_drivers_type_a + num_drivers_type_b + 1)]

    simulate_bus_routes(buses, drivers_type_a, drivers_type_b, num_stations)


if __name__ == "__main__":
    NUM_BUSES_ON_ROUTE = 0
    main()
