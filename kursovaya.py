import time
from datetime import datetime, timedelta
import random
import tkinter as tk
from tkinter import scrolledtext


class Bus:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.is_on_route = False
        self.start_time = None
        self.end_time = None
        self.passengers = 0
        self.capacity = 2

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

    def is_full(self):
        return self.passengers >= self.capacity

    def manage_bus_capacity(bus, station_id, buses, param, simulated_time):
        pass

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
            print_to_textbox(f"Водитель {self.driver_id} ({self.driver_type}) берет перерыв на обед.")

    def take_short_break(self):
        if self.break_count < 6:
            self.break_count += 1
            print_to_textbox(f"Водитель {self.driver_id} ({self.driver_type}) берет короткий перерыв.")

    def get_status(self):
        if self.is_on_duty:
            return f"Водитель {self.driver_id} ({self.driver_type}) на смене. Время начала: {self.start_time.strftime('%H:%M')}, " \
                   f"Ожидаемое время окончания: {self.end_time.strftime('%H:%M')}"
        else:
            return f"Водитель {self.driver_id} ({self.driver_type}) не на смене."


class GeneticAlgorithm:
    def __init__(self, num_stations, population_size=20, generations=100,
                 min_drivers=1, max_drivers=10):
        self.num_stations = num_stations
        self.population_size = population_size
        self.generations = generations
        self.min_drivers = min_drivers
        self.max_drivers = max_drivers
        self.population = []

    def initialize_population(self):
        """Инициализация начальной популяции случайных решений."""
        for _ in range(self.population_size):
            num_drivers = random.randint(self.min_drivers, self.max_drivers)
            solution = {"num_drivers": num_drivers}
            self.population.append(solution)

    def fitness_function(self, solution):
        num_drivers = solution["num_drivers"]
        covered_stations = min(num_drivers * 2, self.num_stations)
        # Цель - покрыть как можно больше станций, но не использовать слишком много водителей
        coverage_score = covered_stations / self.num_stations
        driver_penalty = num_drivers / self.max_drivers

        fitness = (coverage_score * 1.5) - driver_penalty

        return fitness

    def select_parents(self):
        sorted_population = sorted(self.population, key=self.fitness_function, reverse=True)
        return sorted_population[:2]

    def crossover(self, parent1, parent2):
        child_drivers = (parent1["num_drivers"] + parent2["num_drivers"]) // 2
        child_drivers = max(self.min_drivers, min(child_drivers, self.max_drivers))
        child = {"num_drivers": child_drivers}
        return child

    def mutate(self, solution):
        if random.random() < 0.2:
            mutation_amount = random.randint(-2, 2)
            mutated_drivers = solution["num_drivers"] + mutation_amount
            mutated_drivers = max(self.min_drivers, min(mutated_drivers, self.max_drivers))
            solution["num_drivers"] = mutated_drivers
        return solution

    def run(self):
        self.initialize_population()
        for generation in range(self.generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))
            self.population = new_population
            best_solution = max(self.population, key=self.fitness_function)

        return max(self.population, key=self.fitness_function)


def main():
    num_stations = int(input("Введите количество станций: "))
    ga = GeneticAlgorithm(num_stations=num_stations)
    best_solution = ga.run()
    best_drivers = max(ga.population, key=ga.fitness_function)["num_drivers"]
    print(f"Оптимальное количество водителей: {best_drivers}")


# Константы
BUS_CAPACITY = 20
BUS_DEPARTURE_INTERVAL = 70
MIN_PASSENGERS_PER_STATION = 3
MAX_PASSENGERS_PER_STATION = 5
WORKDAY_END_TIME_HOUR = 18
STATION_INTERVAL = 10  # Задержка между станциями в минутах


# Функция для генерации рандомного пассажиропотока на станции
def generate_passengers_per_station():
    return random.randint(MIN_PASSENGERS_PER_STATION, MAX_PASSENGERS_PER_STATION)


# Функция для имитации работы автобусов и водителей на всех станциях
def simulate_bus_route(buses, drivers_type_a, drivers_type_b, bus, num_stations, simulated_time):
    global NUM_BUSES_ON_ROUTE
    global next_driver_id

    while simulated_time.hour < WORKDAY_END_TIME_HOUR:
        # Выбираем водителя для автобуса
        driver = None
        for d in drivers_type_a + drivers_type_b:
            if not d.is_on_duty:
                driver = d
                break

        if driver:
            driver.start_duty(simulated_time)
            print_to_textbox(driver.get_status())

            while simulated_time.hour < WORKDAY_END_TIME_HOUR: # Автобус ездит пока не закончится рабочий день
              # Запускаем маршрут для автобуса
                bus.start_route(simulated_time)
                NUM_BUSES_ON_ROUTE += 1

                print_to_textbox(f"Автобус {bus.bus_id} выезжает из автопарка в {simulated_time.strftime('%H:%M')}")

                # Собираем пассажиров на всех станциях
                for station_id in range(1, num_stations + 1):
                    passengers_to_board = generate_passengers_per_station()
                    bus.passengers += passengers_to_board
                    print_to_textbox(
                        f"Станция {station_id}: Пассажиров - {passengers_to_board}, Всего пассажиров в автобусе - {bus.passengers}")

                    # Пассажиры выходят на станциях от 1 до 4
                    if 1 <= station_id <= 4:
                        passengers_to_exit = random.randint(1,
                                                            min(bus.passengers,
                                                                5))  # Рандомное количество выходящих пассажиров
                        bus.passengers -= passengers_to_exit
                        print_to_textbox(
                            f"Пассажиры выходят на станции {station_id}: {passengers_to_exit}, Осталось пассажиров в автобусе - {bus.passengers}")

                    # Задержка между станциями
                    simulated_time += timedelta(minutes=STATION_INTERVAL)

                # Автобус едет обратно
                print_to_textbox(f"Автобус {bus.bus_id} едет обратно в автопарк в {simulated_time.strftime('%H:%M')}")

                # Ждем время маршрута
                bus.end_route()
                NUM_BUSES_ON_ROUTE -= 1

                print_to_textbox(bus.get_status())
                print_to_textbox(f"Количество автобусов на маршруте: {NUM_BUSES_ON_ROUTE}")
                if simulated_time.hour >= WORKDAY_END_TIME_HOUR:
                    break  # Выход из внутреннего цикла, если конец рабочего дня

                simulated_time += timedelta(minutes=BUS_DEPARTURE_INTERVAL) # Задержка перед новым маршрутом
            # Проверяем, нужно ли завершить смену водителя
            if (simulated_time - driver.start_time).total_seconds() / 3600 >= 9 or (
                    driver.driver_type == 'B' and (simulated_time - driver.start_time).total_seconds() / 3600 >= 9):
                driver.end_duty()
                print_to_textbox(driver.get_status())


        else:
            # Добавление нового водителя
            new_driver_type = 'A' if random.random() < 0.5 else 'B'
            if new_driver_type == 'A':
                 new_driver = Driver(next_driver_id, new_driver_type)
                 drivers_type_a.append(new_driver)
            else:
                 new_driver = Driver(next_driver_id, new_driver_type)
                 drivers_type_b.append(new_driver)
            print_to_textbox(f"Добавлен новый водитель {next_driver_id} ({new_driver_type})")
            next_driver_id += 1



# Функция для имитации работы автобусов и водителей на всех автобусах
def simulate_bus_routes(buses, drivers_type_a, drivers_type_b, num_stations):
    global NUM_BUSES_ON_ROUTE

    # Начало рабочего дня с 6:00 утра
    start_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    if datetime.now() > start_time:
        start_time += timedelta(days=1)

    simulated_time = start_time
    print_to_textbox(f"Начало симуляции: {simulated_time.strftime('%H:%M')}")

    NUM_BUSES_ON_ROUTE = 0

    # Вывод расписания для каждого автобуса
    print_to_textbox("Начало работы автобусов:")
    for i, bus in enumerate(buses):
        departure_time = simulated_time + timedelta(minutes=i * BUS_DEPARTURE_INTERVAL)
        print_to_textbox(f"Автобус {bus.bus_id}: Время выезда - {departure_time.strftime('%H:%M')}")


    for bus in buses:
        simulate_bus_route(buses, drivers_type_a, drivers_type_b, bus, num_stations, simulated_time)


def print_to_textbox(text):
    textbox.insert(tk.END, text + "\n")
    textbox.see(tk.END)


def main():
    global NUM_BUSES_ON_ROUTE, buses, drivers_type_a, drivers_type_b, next_driver_id

    # Базовое количество автобусов и водителей
    num_buses = 8
    num_drivers_type_a = 4
    num_drivers_type_b = 4
    next_driver_id = num_drivers_type_a + num_drivers_type_b + 1

    # Получение количества станций из поля ввода
    try:
        num_stations = int(stations_entry.get())
    except ValueError:
        print_to_textbox("Ошибка: Введите корректное число станций.")
        return

    # Инициализация автобусов и водителей
    buses = [Bus(bus_id) for bus_id in range(1, num_buses + 1)]
    drivers_type_a = [Driver(driver_id, 'A') for driver_id in range(1, num_drivers_type_a + 1)]
    drivers_type_b = [Driver(driver_id, 'B') for driver_id in
                      range(num_drivers_type_a + 1, num_drivers_type_a + num_drivers_type_b + 1)]

    simulate_bus_routes(buses, drivers_type_a, drivers_type_b, num_stations)


# Настройка графического интерфейса
root = tk.Tk()
root.title("Симулятор Автобусного Маршрута")

# Поле для ввода количества станций
stations_label = tk.Label(root, text="Введите количество станций:")
stations_label.pack()
stations_entry = tk.Entry(root)
stations_entry.pack()

# Кнопка запуска симуляции
start_button = tk.Button(root, text="Запустить симуляцию", command=main)
start_button.pack()

# Текстовое поле для вывода результатов
textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80)
textbox.pack(padx=10, pady=10)


if __name__ == "__main__":
    NUM_BUSES_ON_ROUTE = 0
    buses = []
    drivers_type_a = []
    drivers_type_b = []
    next_driver_id = 0
    root.mainloop()
