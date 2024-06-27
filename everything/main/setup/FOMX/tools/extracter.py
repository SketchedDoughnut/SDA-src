
# importing the zipfile module 
from zipfile import ZipFile 
def extract(zip_path, location):  
    # loading the temp.zip and creating a zip object 
    with ZipFile(zip_path, 'r') as zObject: 
    
        # Extracting all the members of the zip  
        # into a specific location. 
        zObject.extractall( 
            path=location) 