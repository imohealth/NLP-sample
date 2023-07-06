class ImoNlpParser:
    def getItemByType(self, type: str):
        if 'indexes' in self.data:
            return {key: value for key, value in self.data['indexes'].items() if type in value}

    def getAllSentence(self):
        return self.sentence[:]

    def getAllEntity(self):
        return self.entities[:]

    def getAllRelation(self):
        return self.relations[:]

    def __init__(self, data={}):
        self.data = data
        self.sentence = []
        self.entities = []
        self.relations = []

        if 'indexes' in self.data:
            self.parse()

    def parse(self):
        for item in self.getItemByType('Sentence').items():
            if item[1] and 'Sentence' in item[1]:
                self.sentence.extend([value for value in item[1]['Sentence'].values()])

        idxdict = {'': []}

        idx = 0
        self.sentence[idx]['entities'] = []
        for item in self.getItemByType('Entity').items():
            if item[1] and 'Entity' in item[1]:
                tmplist = [value for value in item[1]['Entity'].values()]

                for en in tmplist:
                    while not (
                            self.sentence[idx]['begin'] <= en['begin'] and self.sentence[idx]['end'] >= en['end']):
                        idx += 1
                        self.sentence[idx]['entities'] = []

                    self.sentence[idx]['entities'].append(en)
                    self.entities.append(en)
                    idxdict[self.key(en)] = [len(self.entities) - 1, idx]

        idx = 0
        if len(self.entities) == 0:
            return
        ent = self.entities[idx]
        ent['relations'] = []
        for item in self.getItemByType('Relation').items():
            if item[1] and 'Relation' in item[1]:
                tmplist = [value for value in item[1]['Relation'].values()]
                self.relations.extend(tmplist)
                for rel in tmplist:
                    key = self.key(rel['fromEnt'])
                    if key in idxdict:
                        if 'relations' in self.entities[idxdict[key][0]]:
                            self.entities[idxdict[key][0]]['relations'].append(rel)
                        else:
                            self.entities[idxdict[key][0]]['relations'] = [rel]

    def key(self, en: dict):
        return str(en['begin']) + '_' + str(en['end']) + '_' + str(en['semantic'])
