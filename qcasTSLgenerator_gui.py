# Version 1.0 - rewrote in AWK, then ported to Python.
# Version 1.0.1 - now removes commas in game names, and any duplicate entries.
# Version 1.0.2 - Monolith version. Utilises a single python script to generate, combine, sort and filter the TSL file. 
# Version 1.0.3 - Converted to a Class
# Version 1.1 - Updated GUI
# Last Modified date: 12/5/2015
import csv
import sys
import operator
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

VERSION = "1.1"

class QCAS_TSL_Generator:
    
    # default constructor
    def __init__(self, f1, f2):
        self.filename = f1
        self.filename2 = f2
        self.final_filename = ""

        # 1. Generate New TSL game entries using input parameter 1
        # 2. Concatenate TSL files using input parameter 1 & 2
        # 3. Sort Files
        # 4. Drop duplicates
        
        self.genNewTSLEntries()
        self.concatenateTSLfiles()
        self.sortFile()
        self.dropDuplicates()

    # GUI constructor
    def __init__(self):
        self.root = Tk()
        self.setup_GUI()
    
    def handleButtonPress(self, myButtonPress):
        if myButtonPress == '__tab_delimited_file__':
            tmp = filedialog.askopenfile()
            self.filename = tmp.name

            self.tab_delimited_filename_tf.delete(0, END)
            self.tab_delimited_filename_tf.insert(0, self.filename)
            
        elif myButtonPress == '__current_tsl_file__':
            tmp = filedialog.askopenfile()
            self.filename2 = tmp.name

            self.current_tsl_filename_tf.delete(0, END)
            self.current_tsl_filename_tf.insert(0, self.filename2)

        elif myButtonPress == '__start__':
            if (os.path.isfile(self.filename)) or (os.path.isfile(self.filename2)):
                self.filename = self.tab_delimited_filename_tf.get()
                self.filename2 = self.current_tsl_filename_tf.get()
                self.final_filename = self.new_tsl_filename_tf.get()
                            
                self.genNewTSLEntries()
                self.concatenateTSLfiles()
                self.sortFile()
                self.dropDuplicates()

                openfile = messagebox.askquestion("qcasTSLgenerator: Finished!", "Generated new TSL file: " + self.final_filename +
                                                  "\nOpen the file?")
                if (openfile == 'yes'):
                    if (os.name == 'nt'): # Windows OS
                        os.system("start "+self.final_filename)
                    elif (os.name == 'posix'): # Linux OS
                        os.system("open " + self.final_filename)
                    else: 
                        print("Can't open file: " + self.final_filename)
                        messagebox.showerror("Unknown Operating system: " + os.name , "Sorry, could not open file: " + self.final_filename)
                else:
                    print("Generated new TSL file: " + self.final_filename)

            else:
                messagebox.showerror("Files not Chosen!", "Please select files first")
                

    def setup_GUI(self):
        self.root.wm_title("qcasTSLgenerator v"+VERSION)
        self.root.resizable(0,0)
        help_text = "This script automates the generation of the QCOM Casino Datafile TSL file.\n"
        ttk.Label(self.root, justify=LEFT,
                  text = help_text).grid(row = 0, columnspan=2, padx=3, pady=3)

        # Button
        button_Choose_TAB_delimited_file = ttk.Button(self.root,
                                                      text = "Choose TAB delimited file...",
                                                      width = 30,
                                                      command = lambda: self.handleButtonPress('__tab_delimited_file__'))                                             
        button_Choose_TAB_delimited_file.grid(row=1, column=0, padx=3, pady=3, sticky='e')

        # Text Entry
        self.tab_delimited_filename_tf = ttk.Entry(self.root, width = 50)
        self.tab_delimited_filename_tf.grid(row=1, column=1)

        # Button
        button_Choose_Current_TSL_file = ttk.Button(self.root,
                                                    text = "Choose Current TSL file...",
                                                    width = 30,
                                                    command = lambda: self.handleButtonPress('__current_tsl_file__'))                                                    
        button_Choose_Current_TSL_file.grid(row=2, column=0, padx=3, pady=3, sticky='e')

        # Text Entry       
        self.current_tsl_filename_tf = ttk.Entry(self.root, width = 50)
        self.current_tsl_filename_tf.grid(row=2, column=1)

        ttk.Label(self.root, text = 'Enter new TSL filename: ').grid(row = 3, column=0, sticky='e', padx=3, pady=3)

        self.v = StringVar()
        self.v.set("qcas_2015_05_v02.tsl")
        self.new_tsl_filename_tf = ttk.Entry(self.root, width = 50, textvariable=self.v)
        self.new_tsl_filename_tf.grid(row=3, column=1, padx=3, pady=3)

        # Button
        button_start = ttk.Button(self.root, text = "Start...",
                                  command = lambda: self.handleButtonPress('__start__'))
        button_start.grid(row=4, columnspan=2, sticky='se', padx=5, pady=5)        
        self.root.mainloop()

    # input: TAB delimited file, exported from MS Excel.
    # output: Filename of new TSL game entries
    def genNewTSLEntries(self):
        outfilename = self.filename.rstrip(".txt") + "_TSL_FORMAT.tsl"
        try:
            outfile = open(outfilename, "w+")
            infile = open(self.filename, 'r')
            input_fieldnames = ['game_name', 'manufacturer', 'approval_status', 
                'approval_date', 'market','ssan','vid_type','binimage','bin_type']
            reader = csv.DictReader(infile, delimiter='\t', fieldnames=input_fieldnames)

            for row in reader:
                # Remove commas in game name
                # If you want to replace it with another symbol change the following 
                #   line to: .replace(",","[INSERT SYMBOL HERE]")
                cleaned_game_name = str(row['game_name']).replace(",", "")
            
                # Process Video Type & Append to game name
                if row['vid_type'].lower() == 'video':
                    cleaned_game_name += "-V"
                else :
                    cleaned_game_name += "-S"

                # Process Binimage type
                if row['bin_type'] == 'BIN LINK FILE':
                    my_bin_type = 'BLNK'
                elif row['bin_type'] == 'PSA 32':
                    my_bin_type = "PS32"
                elif row['bin_type'] == 'HMAC SHA1':
                    my_bin_type = "SHA1"
                else:
                    sys.exit('Unknown binimage type %s' % row['bin_type'])         

                # print ("%02d,%010d,%-60s,%-20s,%4s" % (int(row['manufacturer']), 
                #   int(row['ssan']), cleaned_game_name, row['binimage'], my_bin_type))
                outfile.writelines("%02d,%010d,%-60s,%-20s,%4s\n" % 
                    (int(row['manufacturer']), int(row['ssan']), 
                    cleaned_game_name, row['binimage'], my_bin_type))
            
            infile.close();
        except csv.Error as e: 
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
        
        self.filename = outfilename

	# input:    None
	# output:   Filename for Single TSL file concatenated created, 
	#           i.e. cat tslfile1 >> tslfile2
    def concatenateTSLfiles(self):
        filenames = [self.filename, self.filename2]
        outputfilename = self.filename.rstrip(".tsl") + "_&_new_games_&_concat.tsl"
    
        with open(outputfilename, 'w+') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())           
        self.filename = outputfilename

	# input: TSL file that includes duplicate entries
	# output: Filename for Single TSL file with no duplicate entries. 
    def dropDuplicates(self):
        lines_seen = set() # holds lines already seen
        #outfilename = self.filename.rstrip(".tsl")+ "_&_no_dups.tsl"
        outfilename = self.final_filename;
        
        outfile = open(outfilename, "w+")
        for line in open(self.filename, "r"):
            if line not in lines_seen: # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        self.filename = outfilename
        self.final_filename = outfilename

    # input: TSL file that is unordered
    # output: Filename for Single TSL file that is ordered.
    def sortFile(self):
        outfilename = self.filename.rstrip(".tsl") + "_&_sorted.tsl"
        try:
            outfile = open(outfilename, "w+")
            infile = open(self.filename, 'r')
            reader = csv.reader(infile, delimiter=",")

            # Sort column 0, 2, 1: SSAN, Game Name, Approval Number
            sortedlist = sorted(reader, key=operator.itemgetter(0,2,1))
  
            # To print a list
            for item in sortedlist:
                # Uncomment next line to print to screen. 
                # print (",".join(item))
                outfile.writelines([",".join(item), '\n'])

            outfile.close()

        except csv.Error as e: 
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
        self.filename = outfilename

def main():
    app = QCAS_TSL_Generator()    
    
if __name__ == "__main__": main()
