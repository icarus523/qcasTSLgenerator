import unittest
import os

from qcasTSLgenerator_TestCase import qcasTSLgenerator_TestCase
from qcasTSLgenerator_gui import QCAS_batch_file, QCAS_TSL_Generator

class test_qcasTSLgenerator_functions(qcasTSLgenerator_TestCase): 

    def test_update_fname(self):
        base_name = 'qcas_2021_12_v01'

        expected_fname = 'qcas_2021_12_v02.tsl'

        self.assertEqual(QCAS_TSL_Generator.update_fname(self, base_name), expected_fname)

    def test_update_fname2(self):
        base_name = 'qcas_2021_12_v09'

        expected_fname = 'qcas_2021_12_v10.tsl'

        self.assertEqual(QCAS_TSL_Generator.update_fname(self, base_name), expected_fname)

    def test_genNewTSLEntries(self): 
        self.new_fname = '20211208 - Tech Services Item List_cleaned.txt' # cleaned tab delimited file
        
        self.new_games_tsl_entries_l = QCAS_TSL_Generator.genNewTSLEntries(self)
        self.assertTrue(len(self.new_games_tsl_entries_l) == 40) 

    def test_generateTSLfile(self):
        self.new_fname = '20211208 - Tech Services Item List_cleaned.txt' # cleaned tab delimited file

        expected_number_of_records = 7669

        # update text field
        # self.current_tsl_filename_tf.delete(0, END)
        # self.tab_delimited_filename_tf.insert(0, new_fname) 

        new_game_list = QCAS_TSL_Generator.genNewTSLEntries(self)
        concatenated_game_list = QCAS_TSL_Generator.concatenateTSLfiles(self, new_game_list)               
        sorted_game_list = QCAS_TSL_Generator.sortFile(self, concatenated_game_list)
        final_new_game_list = QCAS_TSL_Generator.sortFile(self, QCAS_TSL_Generator.dropDuplicates(sorted_game_list))
        QCAS_TSL_Generator.write_game_list_to_file(final_new_game_list)

        