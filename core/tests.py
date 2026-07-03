from django.test import TestCase
from .utility.table_extractor import * 
from .utility.atar_calculate_main import *

class CoreTestCase(TestCase):
    fixtures = ['data_dump.json']

    #def test_pdf_extractor(self):
        #extract_info('NSW ATAR Conversion Table', './core/source/scaling_pdf/nsw_scaling.pdf')

    def test_wa_atar_calculate(self):
        converted_marks = {'English': 99.0, 'English as an Additional Language or Dialect': 99.0, 'Literature': 99.0, 'Mathematics Applications': 99.0, 'Human Biology': 99.0, 'Biology': 99.0, 'Accounting and Finance': 99.0, 'Modern History': 99.0, 'Design': 99.0}
        print("atar:" + str(wa_calculate(converted_marks)))

    def test_sa_atar_calculate(self):
        converted_marks = {'English': 20.0, 'General Mathematics': 20.0, 'Mathematical Methods': 20.0, 'Biology': 20.0, 'Geography - Global Studies': 20.0, 'Media Studies': 20.0}
        print("atar:" + str(sace_calculate(converted_marks)))