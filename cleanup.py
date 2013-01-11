import os
import shutil
def scandirs(path):
    for root, dirs, files in os.walk(path):
        for currentFile in files:
            #print "processing file: " + currentFile
            exts=('.pyc',)
            if any(currentFile.lower().endswith(ext) for ext in exts):
                rempath = os.path.join(root,currentFile)
                try:
                    os.remove(rempath)
                    print "removing file: " + rempath
                except:
                    print "removing file: " + rempath +  ' ---Failed'

if __name__ == '__main__':
    fullpath = os.path.realpath(__file__)
    dirname, filename = os.path.split(os.path.abspath(__file__))

    # Remove the build folder
    shutil.rmtree("build", ignore_errors=True)
    
    # do the same for dist folder
    shutil.rmtree("dist", ignore_errors=True)
    
    
    scandirs(dirname)