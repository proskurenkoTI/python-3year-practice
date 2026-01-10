import asyncio
import aiofiles
import csv 
import random
import statistics 

NUMBER_RANGE = 15;
for i in range (1, 6):
    filename = f"file_{i}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        for j in range(NUMBER_RANGE):
            letter = random.choice(['A', 'B', 'C', 'D'])
            value = round(random.uniform(0.0, 10.0), 2)
            writer.writerow([letter, value])


async def read_csv_file(filename):
    try:
        async with aiofiles.open(filename, mode='r', encoding='utf-8') as file:
            content = await file.read()
            csv_data = list(csv.reader(content.splitlines(), delimiter=';'))
            group_data = {}
            for row in csv_data:
                if len(row) == 2:
                    type = row[0]
                    value = float(row[1])
                    if type not in group_data:
                        group_data[type] = []
                    group_data[type].append(value)
            return {filename: group_data}
    except Exception as e:
        return {filename: f"Ошибка: {e}"}

def statistic_result(structure):
    dMedianSD = []
    for i in range(len(structure)):
        dMedianSD.append({})
        dictionary = structure[i]
        nameOfDiction = list(structure[i].keys())[0]
        if nameOfDiction not in dMedianSD[i]:
            dMedianSD[i][nameOfDiction] = {}
        for key in dictionary[nameOfDiction].keys():
            if key not in dMedianSD[i][nameOfDiction]:
                dMedianSD[i][nameOfDiction][key] = []
            median_val = statistics.median(dictionary[nameOfDiction][key])
            if len(dictionary[nameOfDiction][key]) >= 2:
                stdev_val = statistics.stdev(dictionary[nameOfDiction][key])
            else:
                stdev_val = 0.0
            dMedianSD[i][nameOfDiction][key].append(median_val)
            dMedianSD[i][nameOfDiction][key].append(stdev_val)
    return dMedianSD

def calculate_last(structure):
    dictionary = {}
    for i in range(len(structure)):
        filename = list(structure[i].keys())[0]
        for key in structure[i][filename]:
            if key not in dictionary:
                dictionary[key] = [[], []]
            dictionary[key][0].append(structure[i][filename][key][0])
            dictionary[key][1].append(structure[i][filename][key][1])
    for key in dictionary:
        rm = statistics.median(dictionary[key][0])
        rsd = statistics.stdev(dictionary[key][1])
        dictionary[key][0] = rm
        dictionary[key][1] = rsd
    return dictionary

def print_MedSD(structure):
    for i in range(len(structure)):
        filename = list(structure[i].keys())[0]
        print(filename)
        for key in structure[i][filename]:
            print(f'{key} - M: {structure[i][filename][key][0]} SD: {structure[i][filename][key][1]:.2f}')
            
def print_last_MedSD(structure):
    for key in structure:
        print(f'{key} - M: {structure[key][0]} SD: {structure[key][1]:.2f}')

async def main():
    tasks = list()
    for i in range(1, 6):
        file = f"file_{i}.csv"
        tasks.append(read_csv_file(file))
    resultsRead = await asyncio.gather(*tasks)
    resultsMedSD = statistic_result(resultsRead)
    result = calculate_last(resultsMedSD)
    print_MedSD(resultsMedSD)
    print('Последний: ')
    print_last_MedSD(result)

if __name__ == "__main__":
    asyncio.run(main())