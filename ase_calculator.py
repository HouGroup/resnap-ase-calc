from ase.calculators.calculator import Calculator
import joblib

from lib.lib import get_bispectrum_coefficients

class SnapCalculator(Calculator):

    implemented_properties = ['energy']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rf = joblib.load('rf.joblib')

    def calculate(self, *args, **kwargs):
        super().calculate(*args, **kwargs)

        # calculate bispectrum coefficients
        N = len(self.atoms)
        c = get_bispectrum_coefficients(self.atoms).loc[0].values.tolist()
        c_N = [_/N for _ in c]

        # predict E
        E_N = self._rf.predict([c_N])[0]
        E = E_N * N
        
        # set results
        self.results['energy'] = E