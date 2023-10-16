import matplotlib.pyplot as plt

def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read().splitlines()
        return [float(x) for x in data]

# Зчитування даних з файлів
data1 = read_file("ga.txt")
data2 = read_file("avg.txt")
data3 = read_file("crossover.txt")

# Побудова графіку
plt.plot(data1, label='Discrete recombination')
plt.plot(data2, label='Average recombination')
plt.plot(data3, label='Crossover')

# Додавання назв вісей і легенди
plt.xlabel('Count generation')
plt.ylabel('Fitness value')
plt.legend()

# Відображення графіку
plt.show()
