"""Generate complete manuscript Figure 4; write only figures/fig4_quintic.pdf."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.plotting import BLUE, RED, GRAY, configure_style, save_figure, plt
from src.numerics import np, Search, predictions, branch_data, nonlinear_example


def main():
    configure_style()
    output = ROOT / 'figures' / 'fig4_quintic.pdf'
    curve_eps,quintic_curve,eps,quintic_points = branch_data(2)

    fig,ax=plt.subplots(figsize=(3.35,2.45),layout='constrained')
    ax.plot(curve_eps,quintic_curve[0],color='black',label=r'Analytic $\sigma=2$')
    for i,(N,vals) in enumerate(quintic_points.items()):
        ax.plot(eps,vals[0],ls='none',marker=['o','s'][i],ms=5,mfc='none',
                color=[BLUE,RED][i],label=rf'$N=10^{{{int(np.log10(N))}}}$')
    ax.set(xlabel=r'$\epsilon$',ylabel=r'$\kappa_{2,-}(\epsilon)$',xlim=(.035,.355))
    ax.legend(frameon=False,fontsize=8)
    ax.grid(alpha=.15)
    save_figure(fig, output)


if __name__ == "__main__":
    main()
