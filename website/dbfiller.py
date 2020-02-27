from website.models import Candidate
import pandas as pd
from pandas import ExcelWriter, ExcelFile


candidates_file = pd.read_excel('candidates.xlsx')

for i in candidates_file.index:
    c = Candidate(
        first_name=candidates_file['first_name'][i],
        family_name=candidates_file['family_name'][i],
        grade=candidates_file['grade'][i],
        choice=candidates_file['choice'][i],
        location=candidates_file['location'][i],
        year=candidates_file['year'][i],
    )
    c.save()
    print('Candidat ajouté : {}'.format(candidates_file['first_name'][i]))