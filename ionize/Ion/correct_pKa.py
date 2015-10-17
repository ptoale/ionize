import warnings
from math import log
from ..constants import gas_constant, kelvin


def pKa(self, ionic_strength=None, temperature=None):
    """Return the pKa corrected for temperature.

    If dCp for the ion is available, returns the Clark-Glew correction, which
    is most accurate. If only dH is available, returns the van't Hoff
    correction, which is less accurate. If neither is available, returns the
    original pKa, with a warning.
    """
    _, ionic_strength, temperature = \
        self._resolve_context(None, ionic_strength, temperature)

    if self.dH and self.dCp:
        return _clark_glew(self, temperature)
    elif self.dH and not self.dCp:
        return _vant_hoff(self, temperature)
    else:
        warnings.warn('No data available to correct pKa for temperature.')
        return self._pKa_ref


def _vant_hoff(self, temprature):
    temperature = kelvin(temperature)
    reference_temperature = kelvin(self.reference_temperature)

    if abs(temperature - reference_temperature) > 20:
        warnings.warn("Using the van't Hoff correction for dT > 20 deg.")

    if len(self.enthalpy) != len(self.reference_pKa):
        raise RuntimeError('Enthalpy must have an entry for each pKa.')

    pKa_ref = self._pKa_ref
    dH = self.dH
    pKa = [p - h/(2.303 * gas_constant)*(1/T_ref - 1/T)
           for p, h in zip(pKa_ref, dH)]
    return pKa

def _clark_glew(self):
    T = self.T + 273.15
    T_ref = self._T_ref + 273.15
    if abs(T-T_ref) > 100:
        warnings.warn('Using the Clark-Glew correction for dT > 100 deg.')
    pKa_ref = self._pKa_ref
    dH = self.dH
    dCp = self.dCp
    if dH and dCp and len(dH) == len(pKa_ref) == len(dCp):
        pKa = [p - h/(2.303 * gas_constant)*(1/T_ref - 1/T) -
               c/(2.303 * gas_constant) * (T_ref/T - 1 - log(T/T_ref))
               for p, h, c in zip(pKa_ref, dH, dCp)]
    else:
        warnings.warn('No dCp available. Returning uncorrected pKa.')
        pKa = pKa_ref
    return pKa
