from django.db import models

MALE = 'M'
FEMALE = 'F'
OTHERS = 'O'

GENDERS = (
    ("F", "Female"),
    ("M", "Male"),
    ("O", "Others"),
)

STATES = (
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
)


class UnitStudent(models.Model):
    enroll_number = models.CharField(max_length=31)
    name = models.CharField(max_length=127)
    cpf = models.CharField(max_length=11)
    email = models.EmailField()
    phone_01 = models.CharField(max_length=15, blank=True, null=True)
    phone_02 = models.CharField(max_length=15, blank=True, null=True)
    phone_03 = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS)
    address = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(choices=STATES)
    recieves_sms_or_email = models.BooleanField(default=False)
    rg = models.CharField(max_length=10, blank=True, null=True)
    campus = models.CharField(max_length=255)
    course_code = models.IntegerField()
    course = models.CharField(max_length=255)
    period = models.CharField(max_length=255)
    enrollment_year = models.IntegerField()
    semester = models.IntegerField()
    max_semester = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.name} - {self.enroll_number}"

