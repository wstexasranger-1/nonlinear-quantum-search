"""Generate complete manuscript Figure 2; write only figures/fig2_branch_functions.pdf."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.plotting import BLUE, RED, GRAY, configure_style, save_figure, plt
from src.numerics import np, Search, predictions, branch_data, nonlinear_example


def main():
    configure_style()
    output = ROOT / 'figures' / 'fig2_branch_functions.pdf'
    curve_eps,gp_curve,eps,gp_points = branch_data(1)

    fig,axs=plt.subplots(1,3,figsize=(6.9,2.35),layout='constrained')
    names=[r'$\kappa_-(\epsilon)$',r'$\kappa_+(\epsilon)$',r'$\mathcal{R}_X(\epsilon)$']
    for j,ax in enumerate(axs.flat):
        ax.plot(curve_eps,gp_curve[j],color='black',label='Analytic limit')
        for i,(N,vals) in enumerate(gp_points.items()):
            ax.plot(eps,vals[j],ls='none',marker=['o','s'][i],ms=5.5,
                    markerfacecolor='none',color=[BLUE,RED][i],label=rf'$N=10^{{{int(np.log10(N))}}}$')
        ax.set(xlabel=r'$\epsilon$',ylabel=names[j],xlim=(.035,.355))
        ax.set_title(f'({chr(97+j)})',loc='left',fontsize=9)
        ax.grid(alpha=.15)
    axs[0].legend(loc='upper right',frameon=False)
    save_figure(fig, output)


if __name__ == "__main__":
    main()
