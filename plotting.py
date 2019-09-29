import matplotlib.pyplot as plt
from mosaic import get_folders_content

# Refractor this! 
# Get_folders_contetn returns now list of images instead of
# number of elements in folder
def prepare_data(data):
    data.pop('other')
    result = []
    for key, value in data.items():
        if '\\' in key:
            continue
        result.append([key, value])
    return sorted(result, key=lambda kv: kv[1], reverse=True)


data = get_folders_content()
prepared_data = prepare_data(data)


# colors = []
# count = []
# bars = []
# for color, c in x:
#     colors.append(color[0])
#     count.append(c)
#     bars.append(f'xkcd:{color[0]}')
#     # print(color)

# # print(bars)


for key, value in prepared_data[:50]:
    plt.bar(key, value)

plt.xticks(rotation='vertical')
plt.show()

# # print(count[:5])
# # print(colors[:5])

# # # plt.bar(['a', 'b', 'c', 'd', 'e'], [1588, 1464, 965, 788, 720])
# limit = 300
# plt.bar(colors[:limit], count[:limit], color=bars[:limit])
# plt.xticks(rotation='vertical')
# plt.show()
