####################################
#Compatibility layer for Ramses-ism#
#                                  #
#-------Francesco Lovascio---------#
#--francesco.lovascio@ens-lyon.fr--#
####################################
import numpy as np
import pandas as pd
import shutil as sh

class hydroFileDescriptor:
    def __init__(self, infile, fname):
        self.infile=infile
        self.fname=fname
        self.get_legacy_hydro_descriptor()
        self.print_hydro_descriptor()

    def is_legacy(self):
        '''
        hydroFileDescriptor.is_legacy()
        Naively checks if the format matches the legacy ramses_ism format if so
        it returns True, returns False otherwise.
        '''
        with open(self.fname,'r') as f:
            if "nvar" in f.readline():
                return True
            return False

    def get_legacy_hydro_descriptor(self,check_if_legacy=True):
        '''
        hydroFileDescriptor.get_legacy_hydro_descriptor(check_if_legacy=True)
        Reads old style hydro descriptor into a dataframe compatible with the
        new format
        Setting check_if_legacy to <False> stops the code from first checking
        the style of the descriptor. This may lead to errors and is thus only
        recommended as a debug tool.
        '''
        if self.is_legacy():
            variables = pd.read_csv(self.fname,dtype=str,skiprows=1,names=["variable_name"])
            drop,variables["variable_name"]=zip(*variables["variable_name"].str.split(':'))
            mapping=[("B_left_x","B_x_left"),("B_left_y","B_y_left"),("B_left_z","B_z_left"),("B_right_x","B_x_right"),("B_right_y","B_y_right"),("B_right_z","B_z_right")]
            for a,b in mapping:
                variables["variable_name"]=variables["variable_name"].str.replace(a,b)
                variables["variable_type"]=["d"]*len(variables["variable_name"])
                variables["ivar"]=np.arange(start=1,stop=(len(variables["variable_name"])+1))
                self.variables=variables
        else:
            raise IOError('The file does not appear to be a ramses_ism hydro_file_descriptor')

    def print_hydro_descriptor(self,make_backup=True):
        '''
        hydroFileDescriptor.print_hydro_descriptor(make_backup=True)
        Prints new ramses hydro_file_descriptor.txt and if make_backup==True
        makes a copy of the old descriptor in
        <dir>/~legacy_hydro_file_descriptor.backup
        '''
        sh.copyfile(self.fname,self.infile+"/~legacy_hydro_file_descriptor.backup")
        with open(self.fname,'w') as f:
            f.write('# version:  1 \n# ivar, variable_name, variable_type\n')
            self.variables.to_csv(path_or_buf=f,header=False,index=False,columns=["ivar","variable_name","variable_type"])

