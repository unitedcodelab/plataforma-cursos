import pandas as pd
from apps.entities.extra_models.unit.students import UnitStudent
from config.settings import BASE_DIR


df = pd.read_excel(f'{BASE_DIR}/scripts/students_list.xlsx')


def clean_cpf(cpf):
    if len(cpf) == 10:
        cpf = '0' + cpf
    return cpf.replace('.', '').replace('-', '')


def clean_phones(phones):
    phones = phones.split()
    cleaned_phones = []

    for i in range(0, len(phones), 2):
        if i + 1 < len(phones):
            cleaned_phone = phones[i] + phones[i + 1]
            cleaned_phones.append(cleaned_phone)

        else:
            cleaned_phones.append(phones[i])

    return cleaned_phones


def clean_rg(rg):
    if len(rg) == 8:
        return rg.replace('.', '').replace('-', '')
    return None


def clean_line(field):
    cleaned_line = []
    for data in field:
        if str(data) == 'nan' or 'is empty' in field:
            cleaned_line.append(None)
        else:
            cleaned_line.append(data)
    return cleaned_line


def import_students_2024_01():
    for line in df.values:
        line = clean_line(line)

        enroll_number = line[0]
        name = line[1]
        cpf = clean_cpf(str(line[2]))
        email = line[3]
        phones = clean_phones(str(line[4]))
        birth_date = line[5]
        gender = line[6][0]
        address = line[7]
        neighborhood = line[8]
        cep = str(line[9])
        city = line[10]
        state = line[11]
        recieves_sms_or_email = line[12] == 'Sim'
        rg = clean_rg(str(line[13]))
        campus = line[16]
        course_code = line[17]
        course = line[18]
        period = line[19]
        enrollment_year = line[20] 
        semester = line[21] 
        max_semester = line[25]

        print(name, neighborhood)

        student = UnitStudent.objects.create(
            enroll_number=enroll_number,
            name=name,
            cpf=cpf,
            email=email,
            birth_date=birth_date,
            gender=gender,
            address=address,
            neighborhood=neighborhood,
            cep=cep,
            city=city,
            state=state,
            recieves_sms_or_email=recieves_sms_or_email,
            rg=rg,
            campus=campus,
            course_code=course_code,
            course=course,
            period=period,
            enrollment_year=enrollment_year,
            semester=semester,
            max_semester=max_semester
        )

        if len(phones) == 3:
            student.phone_01 = phones[0]
            student.phone_02 = phones[1]
            student.phone_03 = phones[2]
        elif len(phones) == 2:
            student.phone_01 = phones[0]
            student.phone_02 = phones[1]
        elif len(phones) == 1:
            student.phone_01 = phones[0]

        student.save()


        # Only for debugging purposes
        all_fields = [  
            "name", "cpf", "email", "phones", "birth_date", "gender","address", 
            "neighborhood", "cep", "city", "state", "recieves_sms_or_email", 
            "rg", "...", "...", "campus", "course_code","course", "period", 
            "enrollment_year", "semester", "...", "...", "...", "max_semester",
            "...", "...", "...", "...", "..." 
        ]

        not_important_fields = ["...", "birth_date", "cep", "rg"]

        counter = 0
        for field in line:
            if not field and all_fields[counter] not in not_important_fields:
                print(f'{line[1]} has no {all_fields[counter]} field.')
            counter += 1
