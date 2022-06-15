import unittest

from qcasTSLgenerator_TestCase import qcasTSLgenerator_TestCase
from qcasTSLgenerator_gui import QCAS_batch_file

class test_QCAS_batch_file_functions(qcasTSLgenerator_TestCase): 

    def format_version_small(self): 

        version_number = 9
        formatted_vnum = QCAS_batch_file.format_version(self, version_number)

        self.assertEqual(formatted_vnum, '01')

    def format_version_small(self): 

        version_number = 15
        formatted_vnum = QCAS_batch_file.format_version(self, version_number)

        self.assertEqual(formatted_vnum, '15')