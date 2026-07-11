function complex(re, im) {
    return { re: re, im: im };
  }
  function cAdd(a, b) { return complex(a.re + b.re, a.im + b.im); }
  function cSub(a, b) { return complex(a.re - b.re, a.im - b.im); }
  function cMul(a, b) {
    return complex(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
  }
  function cDiv(a, b) {
    const denom = b.re * b.re + b.im * b.im;
    return complex(
      (a.re * b.re + a.im * b.im) / denom,
      (a.im * b.re - a.re * b.im) / denom
    );
  }
  function cAbs2(a) { return a.re * a.re + a.im * a.im; }
  
  class QuantumSolver {
    constructor(params) {
      this.xMin = -20.0;
      this.xMax = 20.0;
      this.N = 400;
      this.dx = (this.xMax - this.xMin) / (this.N - 1);
      this.dt = 0.01;
  
      this.x = new Float64Array(this.N);
      for (let i = 0; i < this.N; i++) {
        this.x[i] = this.xMin + i * this.dx;
      }
  
      this.setParams(params);
      this.reset();
    }
  
    setParams(params) {
      this.V0 = params.V0;
      this.barrierStart = 0.0;
      this.barrierWidth = params.barrierWidth;
      this.k0 = params.k0;
      this.x0 = -10.0;
      this.sigma = 1.0;
  
      this.V = new Float64Array(this.N);
      for (let i = 0; i < this.N; i++) {
        if (this.x[i] >= this.barrierStart && this.x[i] <= this.barrierStart + this.barrierWidth) {
          this.V[i] = this.V0;
        }
      }
    }
  
    reset() {
      this.psi = [];
      let normSum = 0;
      for (let i = 0; i < this.N; i++) {
        const envelope = Math.exp(-((this.x[i] - this.x0) ** 2) / (4 * this.sigma * this.sigma));
        const phase = this.k0 * this.x[i];
        const val = complex(envelope * Math.cos(phase), envelope * Math.sin(phase));
        this.psi.push(val);
        normSum += cAbs2(val);
      }
      const norm = Math.sqrt(normSum * this.dx);
      for (let i = 0; i < this.N; i++) {
        this.psi[i] = complex(this.psi[i].re / norm, this.psi[i].im / norm);
      }
      this.time = 0;
    }
  
    step() {
      const N = this.N;
      const dx2 = this.dx * this.dx;
      const dtHalf = this.dt / 2;
      const kinetic = 1.0 / dx2;
      const offDiag = -0.5 / dx2;
  
      const aLower = new Array(N);
      const aDiag = new Array(N);
      const aUpper = new Array(N);
      const d = new Array(N);
  
      for (let i = 0; i < N; i++) {
        const Hii = this.V[i] + kinetic;
        aDiag[i] = complex(1, dtHalf * Hii);
        aLower[i] = complex(0, dtHalf * offDiag);
        aUpper[i] = complex(0, dtHalf * offDiag);
      }
  
      for (let i = 0; i < N; i++) {
        const Hii = this.V[i] + kinetic;
        let val = cMul(complex(1, -dtHalf * Hii), this.psi[i]);
        if (i > 0) {
          val = cSub(val, cMul(complex(0, dtHalf * offDiag), this.psi[i - 1]));
        }
        if (i < N - 1) {
          val = cSub(val, cMul(complex(0, dtHalf * offDiag), this.psi[i + 1]));
        }
        d[i] = val;
      }
  
      const cPrime = new Array(N);
      const dPrime = new Array(N);
  
      cPrime[0] = cDiv(aUpper[0], aDiag[0]);
      dPrime[0] = cDiv(d[0], aDiag[0]);
  
      for (let i = 1; i < N; i++) {
        const denom = cSub(aDiag[i], cMul(aLower[i], cPrime[i - 1]));
        if (i < N - 1) {
          cPrime[i] = cDiv(aUpper[i], denom);
        }
        dPrime[i] = cDiv(cSub(d[i], cMul(aLower[i], dPrime[i - 1])), denom);
      }
  
      const newPsi = new Array(N);
      newPsi[N - 1] = dPrime[N - 1];
      for (let i = N - 2; i >= 0; i--) {
        newPsi[i] = cSub(dPrime[i], cMul(cPrime[i], newPsi[i + 1]));
      }
  
      this.psi = newPsi;
      this.time += this.dt;
    }
  
    getProbabilityDensity() {
      const density = new Float64Array(this.N);
      for (let i = 0; i < this.N; i++) {
        density[i] = cAbs2(this.psi[i]);
      }
      return density;
    }
  
    getNorm() {
      let sum = 0;
      for (let i = 0; i < this.N; i++) {
        sum += cAbs2(this.psi[i]);
      }
      return sum * this.dx;
    }
  }