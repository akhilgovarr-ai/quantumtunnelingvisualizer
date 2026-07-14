const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const W = canvas.width;
const H = canvas.height;

function readParams() {
  return {
    V0: parseFloat(document.getElementById("v0").value),
    barrierWidth: parseFloat(document.getElementById("width").value),
    k0: parseFloat(document.getElementById("k0").value),
  };
}

let solver = new QuantumSolver(readParams());
let isRunning = false;
let lastFrameTime = performance.now();

const PRESETS = {
  sun: {
    V0: 25, barrierWidth: 0.5, k0: 3,
    caption: "Inside the Sun, hydrogen nuclei have to overcome their mutual repulsion to fuse. There's barely enough energy — so fusion in any single nucleus is extremely rare, but there are a lot of nuclei in a star."
  },
  flash: {
    V0: 15, barrierWidth: 0.3, k0: 5,
    caption: "In flash memory, electrons tunnel through a thin insulating layer to get written into a memory cell. The layer is made deliberately thin — that's the whole reason this works at all."
  },
  stm: {
    V0: 10, barrierWidth: 0.2, k0: 4,
    caption: "A scanning tunneling microscope brings a needle almost into contact with a surface. Electrons tunnel across the tiny gap between the tip and the atoms, and the strength of that tunneling current is enough to image individual atoms."
  },
  alpha: {
    V0: 20, barrierWidth: 2.5, k0: 2,
    caption: "In alpha decay, a particle inside a uranium nucleus is trapped behind a barrier from the nuclear force. The barrier is wide, so decay of any one nucleus is a rare event — one that can take thousands of years to happen."
  },
};

document.querySelectorAll(".preset").forEach((btn) => {
  btn.addEventListener("click", () => {
    const preset = PRESETS[btn.dataset.preset];
    document.getElementById("v0").value = preset.V0;
    document.getElementById("width").value = preset.barrierWidth;
    document.getElementById("k0").value = preset.k0;
    document.getElementById("v0-value").textContent = preset.V0;
    document.getElementById("width-value").textContent = preset.barrierWidth;
    document.getElementById("k0-value").textContent = preset.k0;
    document.getElementById("preset-caption").textContent = preset.caption;

    document.querySelectorAll(".preset").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    isRunning = false;
    document.getElementById("startBtn").textContent = "Run";
    solver.setParams(readParams());
    solver.reset();
    drawFrame();
  });
});

function computeTR() {
  const density = solver.getProbabilityDensity();
  const barrierEnd = solver.barrierStart + solver.barrierWidth;
  let transmitted = 0;
  let reflected = 0;
  for (let i = 0; i < solver.N; i++) {
    if (solver.x[i] > barrierEnd) transmitted += density[i];
    else if (solver.x[i] < solver.barrierStart) reflected += density[i];
  }
  transmitted *= solver.dx;
  reflected *= solver.dx;
  return { transmitted, reflected };
}

function drawFrame() {
  ctx.clearRect(0, 0, W, H);

  const density = solver.getProbabilityDensity();
  const maxDensity = Math.max(...density);
  const V = solver.V;
  const maxV = 30;

  function xToPixel(xVal) {
    return ((xVal - solver.xMin) / (solver.xMax - solver.xMin)) * W;
  }

  ctx.beginPath();
  ctx.strokeStyle = "rgba(255, 138, 102, 0.9)";
  ctx.lineWidth = 2;
  for (let i = 0; i < solver.N; i++) {
    const px = xToPixel(solver.x[i]);
    const py = H - (V[i] / maxV) * (H * 0.5);
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  ctx.beginPath();
  ctx.strokeStyle = "rgba(139, 127, 255, 1)";
  ctx.lineWidth = 2;
  for (let i = 0; i < solver.N; i++) {
    const px = xToPixel(solver.x[i]);
    const py = H - (density[i] / maxDensity) * (H * 0.85) - 10;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  document.getElementById("time-readout").textContent = `t = ${solver.time.toFixed(2)}`;
  document.getElementById("norm-readout").textContent = `probability = ${solver.getNorm().toFixed(4)}`;

  const { transmitted, reflected } = computeTR(); 
  const tPct = (transmitted / (transmitted + reflected + 1e-9)) * 100;

  document.getElementById("prob-fill-t").style.width = `${Math.min(tPct, 100)}%`;
  document.getElementById("prob-fill-r").style.width = `${Math.max(100 - tPct, 0)}%`;
  document.getElementById("prob-t").textContent = `${(transmitted * 100).toFixed(1)}%`;
  document.getElementById("prob-r").textContent = `${(reflected * 100).toFixed(1)}%`;

  const feedback = document.getElementById("task-feedback");
  if (feedback) {
    if (tPct > 50) {
      feedback.textContent = "✓ Challenge 1 complete — more than half got through";
    } else if (tPct < 2 && solver.time > 2) {
      feedback.textContent = "✓ Challenge 2 complete — almost nothing got through";
    } else {
      feedback.textContent = "";
    }
  }
} 
function animate() {
    if (!isRunning) return;
  
    const now = performance.now();
    const elapsed = now - lastFrameTime;
    lastFrameTime = now;
  
    const stepsThisFrame = Math.max(1, Math.round((elapsed / 1000) * 500));
    for (let i = 0; i < Math.min(stepsThisFrame, 30); i++) {
      solver.step();
    }
  
    drawFrame();
    requestAnimationFrame(animate);
  }
  
  document.getElementById("startBtn").addEventListener("click", () => {
    if (isRunning) {
      isRunning = false;
      document.getElementById("startBtn").textContent = "Run";
    } else {
      isRunning = true;
      document.getElementById("startBtn").textContent = "Pause";
      lastFrameTime = performance.now();
      animate();
    }
  });
  
  document.getElementById("resetBtn").addEventListener("click", () => {
    isRunning = false;
    document.getElementById("startBtn").textContent = "Run";
    solver.setParams(readParams());
    solver.reset();
    drawFrame();
  });
  
  ["v0", "width", "k0"].forEach((id) => {
    document.getElementById(id).addEventListener("input", () => {
      document.getElementById(id + "-value").textContent = document.getElementById(id).value;
      document.querySelectorAll(".preset").forEach((b) => b.classList.remove("active"));
      document.getElementById("preset-caption").textContent = "Pick a preset, or set the sliders yourself.";
      isRunning = false;
      document.getElementById("startBtn").textContent = "Run";
      solver.setParams(readParams());
      solver.reset();
      drawFrame();
    });
  });
  
  drawFrame();