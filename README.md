# qcasTSLgenerator

This is a script to generate the TSL file, to be used for the generation of new MSL/PSL files for Queensland Casinos. 

## Version 1.2.3a (22/8/2018) 

Addresses bugs related to qcas.bat autogeneration

Will now prompts users if a new Game is being generated in a new month (refer to diagram in WI01)

No - updates versions only

Yes - creates new MSL entry and uses new month PSL as current month PSL while updating versions.

Skips first line of TAB delimited file automatically

## Version 1.2.2 (5/7/2018)

Updated to handle leading "0" on Month file for MSL and PSL

## Version 1.2.1

Updated to handle abortion on qcas.bat selection

## Version 1.2

Updated to remove non-ASCII characters from game names

## Version 1.1 

This version removes the dependency on most text file processing, there will only be the final TSL file generated (no more: new_games, concat, sorted, removed_duplicate text files). 
[New Feature] This version also prompts the user to auto-generate the qcas.bat file, using the generated TSL file and current qcas.bat file. 
-	It will increment PSL version numbers and months based on current qcas.bat file. 
-	You will need to confirm the output when generating on the new month, in between months the PSL files should be appropriately incremented. 
-	You need to ensure you have a mapped G:\ or default QCAS_DIRECTORY needs to be modified for your workstation environment.

[Bug fixes] Fixed wonky gui, and gui-related bugs (i.e. cancel a file select dialogue then errors spew out, default directories)
This version will prompt the user to search for and delete any “Approval Withdrawn” games as per procedure (WI01) 
