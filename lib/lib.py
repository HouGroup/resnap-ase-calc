from pathlib import Path
import shutil
import subprocess
import contextlib
import tempfile

import ase.io
import pymatgen.io.lammps.outputs

template = (Path(__file__).parent / "template.in").read_text()

def get_bispectrum_coefficients(atoms, config={'rcutfac': 1.0, 'rfac0': 0.94, 'twojmax': 10, 'R_1': 1.8}):
    with tempfile.TemporaryDirectory() as tempdir:
        with contextlib.chdir(tempdir):
            ase.io.write('1.data', atoms, format='lammps-data')
            Path('1.in').write_text(template.format(**config))
            subprocess.run(['lmp_serial', '-in', '1.in', '-log', "1.log"], check=True, stdout=subprocess.DEVNULL)
            return pymatgen.io.lammps.outputs.parse_lammps_log("1.log")[0]  # pd.DataFrame

template_atom = (Path(__file__).parent / "template.atomwise.in").read_text()

def get_bispectrum_coefficients_atomwise(atoms, config={'rcutfac': 1.0, 'rfac0': 0.94, 'twojmax': 10, 'R_1': 1.8}):
    with tempfile.TemporaryDirectory() as tempdir:
        with contextlib.chdir(tempdir):
            ase.io.write('1.data', atoms, format='lammps-data')
            Path('1.in').write_text(template_atom.format(**config))
            subprocess.run(['lmp_serial', '-in', '1.in', '-log', "1.log"], check=True, stdout=subprocess.DEVNULL)
            return pymatgen.io.lammps.outputs.LammpsDump.from_str(Path("1.dump").read_text()).data