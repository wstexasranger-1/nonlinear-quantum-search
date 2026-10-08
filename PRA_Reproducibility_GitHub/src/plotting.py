"""Shared publication style and one-image output; caches are temporary."""
import os
from tempfile import TemporaryDirectory

# Keep font discovery/cache artifacts outside the repository and remove on exit.
_config = TemporaryDirectory(prefix='pra-matplotlib-')
os.environ['MPLCONFIGDIR'] = _config.name

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BLUE, RED, GRAY = '#17658b', '#b34b24', '#555555'


def configure_style():
    plt.rcParams.update({'font.family':'serif','font.serif':['cmr10'],
        'axes.formatter.use_mathtext':True,'axes.unicode_minus':False,
        'font.size':9,'axes.labelsize':10,
        'legend.fontsize':8,'xtick.labelsize':8,'ytick.labelsize':8,
        'mathtext.fontset':'cm','pdf.fonttype':42,'axes.linewidth':.7,
        'lines.linewidth':1.3,'savefig.bbox':'tight','savefig.pad_inches':.03})


def save_figure(fig, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, metadata={
        'Creator': 'Matplotlib', 'Author': '', 'CreationDate': None, 'ModDate': None})
    plt.close(fig)
