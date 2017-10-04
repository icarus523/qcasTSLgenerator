from qcasTSLgenerator_gui import QCAS_batch_file

outputstrs = list()
batch_file = QCAS_batch_file("qcas.bat", "qcas_2017_10_v01.tsl")
# get batch_file generated entries
entries = batch_file.read_qcas_bat_file()

# replace lines
batch_file.replace_qcas_command(entries)
