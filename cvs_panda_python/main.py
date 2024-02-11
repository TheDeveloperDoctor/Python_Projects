# # TODO: handling just like the file handling
# data = []
# with open("weather-data.csv") as weather:
#     for line in weather:
#         line = line.strip()
#         line = line.split(",")
#         data.append(line)
#
# print (data)
#
# # TODO: we are handling CSV here with inbuilt CSV library
# import csv
#
# with open("weather-data.csv") as data:
#     cvs_reader = csv.reader(data)
#     temperature = []
#     for row in cvs_reader:
#         if row[1] != 'temp':
#             temperature.append(row[1])
#     print(temperature)

# TODO: Panda library
import pandas

data = pandas.read_csv("weather-data.csv")
# print(data)
# print(data["temp"])

# dic_data = data.to_html()
# print(dic_data)
# list_data = data["temp"].to_list()
# # sum = sum(list_data)
# # print(sum/len(list_data))
# # print(data["temp"].max())
#
# # print(data.condition)
# # print(data[data.temp == data.temp.min()])
# monday = data[data.day == "Monday"]
# farhent =  (monday.temp * 9/5) + 32
# print(farhent)


# TODO: create dataframe from scratch
data_dict = {
    "students": ["roll_no_1", "roll_no_2", "roll_no_3"],
    "score" : [55,88,85]
    }
df = pandas.DataFrame(data_dict)
df.to_csv("new_data.csv")