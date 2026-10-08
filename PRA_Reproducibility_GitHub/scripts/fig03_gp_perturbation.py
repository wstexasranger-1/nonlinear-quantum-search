"""Generate complete manuscript Figure 3; write only figures/fig3_nonlinear_example.pdf."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.plotting import BLUE, RED, GRAY, configure_style, save_figure, plt
from src.numerics import np, Search, predictions, branch_data, nonlinear_example


def main():
    configure_style()
    output = ROOT / 'figures' / 'fig3_nonlinear_example.pdf'
    nonlinear,report = nonlinear_example()

    fig,axs=plt.subplots(1,3,figsize=(7.05,2.35),layout='constrained',
                         gridspec_kw={'width_ratios':[1.05,1.15,.8]})
    model=Search(256)
    tstar=model.gp_time(np.pi/2)
    time=nonlinear['time']-tstar
    boundaries=np.asarray(report['boundary_times'])-tstar
    axs[0].plot(time,nonlinear['p0'],color='black',label=r'$p_0$')
    axs[0].plot(time,nonlinear['p_delta'],color=BLUE,ls='--',label=r'$p_\eta$')
    axs[0].set(xlabel=r'$t-t_*$',ylabel='Marked population',ylim=(-.02,1.05))
    axs[0].legend(frameon=False,loc='upper left')
    axs[1].plot(time,np.sqrt(nonlinear['infidelity']),color=RED,label=r'$D_{\rm tr}$')
    axs[1].plot(time,abs(nonlinear['delta_p']),color=BLUE,label=r'$|\Delta p|$')
    # Sparse circles expose the independent tangent prediction without a second curve.
    sel=np.arange(0,len(time),85)
    axs[1].plot(time[sel],np.sqrt(nonlinear['state_linear'][sel]),ls='none',marker='o',
                ms=3.2,mfc='none',color=RED)
    axs[1].plot(time[sel],abs(nonlinear['dp_linear'][sel]),ls='none',marker='o',
                ms=3.2,mfc='none',color=BLUE)
    axs[1].set(xlabel=r'$t-t_*$',ylabel='Distance')
    axs[1].ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
    axs[1].legend(frameon=False,loc='upper left')
    for ax in axs[:2]:
        for t,label,align in zip(boundaries,[r'$t_-$',r'$t_+$'],['right','left']):
            ax.axvline(t,color=GRAY,ls=':',lw=.8)
            ax.text(t,1.015,label,transform=ax.get_xaxis_transform(),ha=align,va='bottom')
    xx=np.arange(2)
    axs[2].plot(xx,report['boundary_nonlinear'],'o',ms=5,color=BLUE,label='Nonlinear')
    axs[2].plot(xx,report['boundary_tangent'],'s',ms=6,mfc='none',color=RED,label='Tangent')
    axs[2].plot(xx,predictions(.1)[:2],'_',ms=17,color='black',label=r'$N\to\infty$')
    axs[2].set(xticks=xx,xticklabels=[r'$t_-$',r'$t_+$'],
               ylabel=r'$D_{\rm tr}^{\,2}/[N(\Delta p)^2]$',xlim=(-.5,1.5))
    axs[2].legend(frameon=False,loc='best',fontsize=7)
    for j,ax in enumerate(axs):
        ax.set_title(f'({chr(97+j)})',loc='left',fontsize=9)
        ax.grid(alpha=.12)
    save_figure(fig, output)


if __name__ == "__main__":
    main()
