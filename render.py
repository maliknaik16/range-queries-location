
from trie import Trie

t = Trie()

with open('cell_ids.txt') as f:

    cell_ids = []

    for line in f:
        cell_id = line.strip('\r\n').strip('\n').strip('')

        cell_ids.append(cell_id)

    cell_ids = list(set(cell_ids))

    for cell_id in cell_ids:
        t.insert(cell_id)

    t.render(prog='dot')

# df = pd.read_csv('new.csv')

# # df.sort_values(by=['cell_token'])

# tokens = df['cell_token']

# # tokens = tokens.sort()

# tokens.sort_values()

# tokens.unique()

# # for i in range(len(df)):

# #     token = df.iloc[i, 5]

# #     t.insert(token)
# #     # print(token)

# #     if i > 5:
# #         break

# for token in tokens:

#     t.insert(token)

# t.render(prog='dot')

