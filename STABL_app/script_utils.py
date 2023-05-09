
import os
from pathlib import Path

def test_script(foldername):
    os.makedirs(foldername)
    with open(Path(foldername, foldername + '.py'), 'w') as fpy:
        # TO DO write the python file to run STABL the way it is asked
        pass
    with open(Path(foldername, foldername + '.sbatch'), 'w') as fsbatch:
        # TO DO write the sbatch file to run the python script
        pass