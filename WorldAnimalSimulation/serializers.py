import json

from animals import Animal, Lion, Zebra
from plants import Plant


class Serializer:
    fields = {'Place': [], 'Animal': [], 'Plant': []}

    def make_dict(self, object):
        if type(object).__name__ == "Place":
            self.fields['Place'].append({'target': f'{object.target}',
                                         'occupied': f'{object.occupied}',
                                         'x': f'{object.x}', 'y': f'{object.y}'})
        elif issubclass(type(object), Animal):
            self.fields['Animal'].append({'class_type': f'{type(object).__name__}', 'speed': f'{object.speed}',
                                          'hp': f'{object.hp}',
                                          'damage': f'{object.damage}',
                                          'max_hunger': f'{object.max_hunger}',
                                          'hunger': f'{object.hunger}',
                                          'type_of_pray': f'{object.type_of_pray}',
                                          'x': f'{object.x}',
                                          'y': f'{object.y}',
                                          })
        else:
            self.fields['Plant'].append({
                'x': f'{object.x}',
                'y': f'{object.y}',
                'fresh': f'{object.fresh}',
                'hp': f'{object.hp}'})

    def serialize(self, plain):
        for es in plain.essensials:
            self.make_dict(es)
        for es in plain.plants:
            self.make_dict(es)
        with open('data.json', 'w') as outfile:
            json.dump(self.fields, outfile)

    def deserialize(self, plain):
        with open('data.json') as json_file:
            data = json.load(json_file)
            for p in data['Animal']:
                essence = p['class_type']
                if essence == 'Zebra':
                    es = Zebra(int(p['x']), int(p['y']))
                else:
                    es = Lion(int(p['x']), int(p['y']))
                es.speed = int(p['speed'])
                es.hp = int(p['hp'])
                es.damage = int(p['damage'])
                es.hunger = int(p['hunger'])
                if p['type_of_pray'] == "<class 'animals.Animal'>":
                    es.type_of_pray = Animal
                else:
                    es.type_of_pray = Plant
                plain.essensials.append(es)
                plain.grid[int(p['x'])][int(p['y'])].is_occupied(es)
            for p in data['Plant']:
                es = Plant(int(p['x']), int(p['y']))
                es.fresh = int(p['fresh'])
                plain.plants.append(es)
                plain.grid[int(p['x'])][int(p['y'])].is_occupied(es)
                ''' for p in data['Place']:
                place = plain.grid[int(p['x'])][int(p['y'])]
                place.target = p['target']
                place.occupied = p['occupied']'''