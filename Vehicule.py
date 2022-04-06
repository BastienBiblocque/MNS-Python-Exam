class Vehicule:
    def __init__(self, data):
        self.type = data.get('type')
        self.nom = data.get('nom')
        self.marque = data.get('marque')
        self.vitesse = data.get('vitesse')
        self.km = data.get('km')

    def save(self, placeToSave: list):
        placeToSave.append(self)