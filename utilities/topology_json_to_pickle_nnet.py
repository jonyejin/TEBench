import json

# Define the function to convert JSON data to the .nnet format
def json_to_nnet(json_data):
    lines = []
    for link in json_data['links']:
        source = link['source']
        target = link['target']
        capacity = link['capacity']
        line = f"{source},{target},{capacity}"
        lines.append(line)

    return "\n".join(lines)

json_data = json.loads(open('../TEAL/topologies/B4.json', 'r').read())

nnet_str = json_to_nnet(json_data)

with open("DOTE/networking_envs/data/B4_Zoe/B4_int.pickle.nnet", 'w') as file:
    file.write(nnet_str)