#Agregue id_sesion
class Adoption:
    def __init__(self, id, image, type, name, sex, age, size, color, sterilized, vaccinated, description, id_sesion):
        self.id = id
        self.image = image 
        self.name = name
        self.type = type
        self.sex = sex
        self.age = age
        self.size = size
        self.color = color
        self.sterilized = sterilized
        self.vaccinated = vaccinated
        self.description = description
        self.id_sesion = id_sesion