Process for qcasTSLgenerator_awk

Process:

1. Read new games from XLS file 
	 - this needs to be converted to CSV file. 
	 	- From EXCEL: File > Save As... > Format: Windows Comma Separated (.csv)
	 
2. Generate TSL entries from CSV file

awk -f qcasTSLgenerator.awk 20131205\ Tech\ Services\ Item\ List.csv > tsl_entry.tsl

3. Use awk to merge the records & 4. Use sort to sort TSL file

cat qcas_2015_05_v01.tsl tsl_entry.tsl | sort -k 1,1 -k 3,3 -k 2,2 --field-separator=','

or Complete One Liner: 

awk -f qcasTSLgenerator.awk 20131205\ Tech\ Services\ Item\ List.csv | cat qcas_2015_05_v01.tsl | sort -k 1,1 -k 3,3 -k 2,2 --field-separator=',' -u > new_tsl_file.tsl

Utilise the bash script: qcasTSLgenerator.sh for simpler usage. 

Works 100% 
Speed 100% increase maybe even faster...
