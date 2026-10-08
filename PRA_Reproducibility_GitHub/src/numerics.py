"""Original manuscript analytical curves and first-order/nonlinear ODE routines.

Parameters, solver settings, and arithmetic are preserved from the established
calculation. No data files are written by this module.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import gamma, hyp2f1

def mode_parameters(sigma):
    r = (np.sqrt(1 + 8*sigma) - 1)/4
    return r, r+.5+.5*np.sqrt(1+2*sigma), r+.5-.5*np.sqrt(1+2*sigma), 2*r+1.5


def analytic_modes(p, sigma=1):
    """Return rising/falling X and dX/dp in the continuous tangent frame."""
    p = np.asarray(p)
    r, a, b, c = mode_parameters(sigma)
    F = hyp2f1(a,b,c,p)
    Fp = a*b/c*hyp2f1(a+1,b+1,c+1,p)
    xm = p**r*F
    dxm = r*p**(r-1)*F + p**r*Fp
    # c-a-b=1/2 for every sigma. The odd coefficient reverses at the peak.
    A, B = c-a, c-b
    c0 = gamma(c)*gamma(.5)/(gamma(A)*gamma(B))
    c1 = gamma(c)*gamma(-.5)/(gamma(a)*gamma(b))
    E = hyp2f1(a,b,.5,1-p)
    Ep = -2*a*b*hyp2f1(a+1,b+1,1.5,1-p)
    O = hyp2f1(A,B,1.5,1-p)
    Op = -A*B/1.5*hyp2f1(A+1,B+1,2.5,1-p)
    chi0 = p**r*E
    dchi0 = r*p**(r-1)*E + p**r*Ep
    chi1 = p**r*np.sqrt(1-p)*O
    dchi1 = (r/p-.5/(1-p))*chi1 + p**r*np.sqrt(1-p)*Op
    xp = c0*chi0-c1*chi1
    dxp = c0*dchi0-c1*dchi1
    return xm, dxm, xp, dxp


def predictions(epsilon, sigma=1):
    p = 1-np.asarray(epsilon)
    xm,dxm,xp,dxp = analytic_modes(p,sigma)
    return np.asarray([(p*dxm/xm)**2, (p*dxp/xp)**2,
                       (xp/xm)**2, (dxp/dxm)**2])


class Search:
    def __init__(self, N, sigma=1, k=1):
        self.N, self.k, self.sigma = float(N), k, sigma
        self.n, self.a = self.N-k, k/self.N
        self.g = (self.N-1)/np.sqrt(self.N)

    def geometry(self, tau):
        return (self.a+(1-self.a)*np.sin(tau)**2,
                (1-self.a)*np.cos(tau)**2)

    def coefficients(self, tau):
        p,Q = self.geometry(tau)
        D = (p/self.k)**self.sigma-(Q/self.n)**self.sigma
        F = 1+self.g*D
        Lam = self.sigma*((p/self.k)**(self.sigma-1)/self.k
                         +(Q/self.n)**(self.sigma-1)/self.n)
        return p,Q,F,Lam

    def clock(self, tau):
        return np.sqrt(self.N/self.k)/self.coefficients(tau)[2]

    def generator(self, tau):
        # Original time-domain Kcrit, multiplied by the ideal dt/dtau.
        p,Q,F,Lam = self.coefficients(tau)
        upper = self.k*F/(self.N*p)
        return self.clock(tau)*np.array([[0.,upper],
                    [2*self.g*p*Q*Lam-upper,0.]])

    def boundary_clock(self, epsilon):
        tm = np.arcsin(np.sqrt((1-epsilon-self.a)/(1-self.a)))
        return tm, np.pi-tm

    def gp_time(self, tau):
        assert self.sigma == 1 and self.k == 1
        return np.sqrt(self.N/(1+self.g))*np.arctan2(
            np.sqrt(1+self.g)*np.sin(tau), np.cos(tau))


def direct_tangent(model, epsilons, rtol=2e-10):
    """Phase-direction input z(0)=(0,1); no analytic-mode initialization."""
    epsilons = np.asarray(epsilons)
    tm,tp = model.boundary_clock(epsilons)
    sol = solve_ivp(lambda t,z: model.generator(t)@z, (0,float(max(tp))),
                    [0.,1.], method='DOP853', rtol=rtol, atol=rtol*1e-3,
                    dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    xm,ym = sol.sol(tm)
    xp,yp = sol.sol(tp)
    v2 = 2*(1-epsilons)*epsilons
    out = np.asarray([(.5*(xm*xm+ym*ym)/(v2*xm*xm))/model.N,
                      (.5*(xp*xp+yp*yp)/(v2*xp*xp))/model.N,
                      (xp/xm)**2, (yp/ym)**2])
    return out, np.asarray([xm,ym,xp,yp]), sol.nfev


def pulse(tau):
    """Smooth finite-support oracle pulse, prescribed in the ideal clock."""
    left,right = .12,.35
    if left < tau < right:
        return np.sin(np.pi*(tau-left)/(right-left))**4
    return 0.


def nonlinear_example(eta=5e-4, rtol=2e-12):
    model = Search(256)
    tm,tp = model.boundary_clock(.1)
    end = model.boundary_clock(.35)[1]
    tt = np.unique(np.r_[np.linspace(0,end,1401),tm,np.pi/2,tp])
    initial = np.array([np.sqrt(model.a),np.sqrt(1-model.a)],complex)

    def amplitude(delta):
        def rhs(tau,psi):
            _,_,F,_ = model.coefficients(tau)
            coupling = F/model.N
            alpha,beta = psi
            h0 = -1-delta*pulse(tau)-model.k*coupling-model.g*abs(alpha)**2/model.k
            h1 = -model.n*coupling-model.g*abs(beta)**2/model.n
            off = -coupling*np.sqrt(model.k*model.n)
            # Removing trace/2 changes only each trajectory's common phase.
            d = (h0-h1)/2
            return -1j*model.clock(tau)*np.array([d*alpha+off*beta,off*alpha-d*beta])
        sol = solve_ivp(rhs,(0,end),initial,method='DOP853',rtol=rtol,
                        atol=rtol*.01,max_step=.012,dense_output=True)
        if not sol.success:
            raise RuntimeError(sol.message)
        psi = sol.sol(tt)
        norms = np.sum(abs(psi)**2,axis=0)
        return psi/np.sqrt(norms), float(np.max(abs(norms-1)))

    ideal,norm0 = amplitude(0.)
    perturbed,norm1 = amplitude(eta)
    half,normhalf = amplitude(eta/2)
    p0,p1,phalf = abs(ideal[0])**2,abs(perturbed[0])**2,abs(half[0])**2
    infidelity = abs(ideal[0]*perturbed[1]-ideal[1]*perturbed[0])**2
    infidelity_half = abs(ideal[0]*half[1]-ideal[1]*half[0])**2

    def forced(tau,z):
        p,_ = model.geometry(tau)
        signed_v = np.sqrt(2*p*(1-model.a))*np.cos(tau)
        return model.generator(tau)@z + model.clock(tau)*np.array([0.,-signed_v])*pulse(tau)
    tangent = solve_ivp(forced,(0,end),[0.,0.],method='DOP853',rtol=rtol,
                        atol=rtol*.01,max_step=.012,dense_output=True)
    if not tangent.success:
        raise RuntimeError(tangent.message)
    x,y = tangent.sol(tt)
    p,Q = model.geometry(tt)
    dp_linear = -np.sqrt(2*p*(1-model.a))*np.cos(tt)*x*eta
    state_linear = .5*(x*x+y*y)*eta**2
    ids = [int(np.argmin(abs(tt-t))) for t in (tm,tp)]
    boundary_nonlinear = infidelity[ids]/((p1-p0)[ids]**2*model.N)
    boundary_tangent = state_linear[ids]/(dp_linear[ids]**2*model.N)
    scale = max(abs(dp_linear))
    report = dict(N=256,k=1,g=model.g,epsilon=.1,eta=eta,
                  pulse_clock_interval=[.12,.35],rtol=rtol,
                  norm_defect=max(norm0,norm1,normhalf),
                  ideal_population_error=float(max(abs(p0-p))),
                  population_linear_error=float(max(abs(p1-p0-dp_linear))/scale),
                  half_population_linear_error=float(max(abs(phalf-p0-dp_linear/2))/(scale/2)),
                  state_linear_error=float(max(abs(infidelity-state_linear))/max(state_linear)),
                  half_state_linear_error=float(max(abs(infidelity_half-state_linear/4))/(max(state_linear)/4)),
                  boundary_nonlinear=boundary_nonlinear.tolist(),
                  boundary_tangent=boundary_tangent.tolist(),
                  boundary_population_error=abs((p1-p0)[ids]).tolist(),
                  boundary_infidelity=infidelity[ids].tolist(),
                  boundary_times=model.gp_time(np.array([tm,tp])).tolist())
    arrays = dict(tau=tt,time=model.gp_time(tt),p0=p0,p_delta=p1,
                  delta_p=p1-p0,infidelity=infidelity,dp_linear=dp_linear,
                  state_linear=state_linear,ideal=ideal,perturbed=perturbed,
                  boundary_indices=np.asarray(ids))
    return arrays,report


def branch_data(sigma):
    """Recompute only the plotted points at the original settings, in memory."""
    epsilon = np.asarray([.05, .1, .2, .3])
    curve_epsilon = np.linspace(.04, .35, 401)
    sizes = {1: (1e4, 1e8), 2: (1e6, 1e10)}[sigma]
    points = {N: direct_tangent(Search(N, sigma), epsilon)[0] for N in sizes}
    return curve_epsilon, predictions(curve_epsilon, sigma), epsilon, points
