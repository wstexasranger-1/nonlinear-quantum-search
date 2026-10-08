"""Generate complete manuscript Figure 1; write only figures/fig1_tangent_shear.pdf."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.plotting import BLUE, RED, GRAY, configure_style, save_figure, plt
from src.numerics import np, Search, predictions, branch_data, nonlinear_example


def main():
    configure_style()
    output = ROOT / 'figures' / 'fig1_tangent_shear.pdf'

    # Deterministic tangent patch: an area-preserving shear, not a covariance.
    fig,axs=plt.subplots(1,2,figsize=(3.35,2.4),layout='constrained')
    angle=np.linspace(0,2*np.pi,401)
    circle=.3*np.array([np.cos(angle),np.sin(angle)])
    shear=np.array([[1.,0.],[3.,1.]])
    for ax,patch,title in zip(axs,[circle,shear@circle],
                              ['Initial tangent patch','After phase shear']):
        ax.fill(*patch,color=BLUE,alpha=.16)
        ax.plot(*patch,color=BLUE)
        ax.annotate('',xy=(.65,0),xytext=(-.65,0),
                    arrowprops=dict(arrowstyle='->',lw=.7,color=GRAY))
        ax.annotate('',xy=(0,1.17),xytext=(0,-1.08),
                    arrowprops=dict(arrowstyle='->',lw=.7,color=GRAY))
        ax.text(.59,-.2,r'$X$')
        ax.text(.08,1.08,r'$Y$')
        ax.set(xlim=(-.7,.7),ylim=(-1.42,1.38),aspect='equal')
        ax.set_title(title,fontsize=8,pad=2)
        ax.axis('off')
    axs[1].plot([-.3,.3],[-1.12,-1.12],color=RED,lw=3)
    axs[1].plot([-.3,-.3],[-.9,-1.12],color=RED,ls=':',lw=.8)
    axs[1].plot([.3,.3],[.9,-1.12],color=RED,ls=':',lw=.8)
    axs[1].text(0,-1.39,r'$\delta p=-vX$',ha='center',color=RED,fontsize=9)
    fig.text(.49,.54,r'$\longrightarrow$',ha='center',fontsize=15)
    save_figure(fig, output)


if __name__ == "__main__":
    main()
