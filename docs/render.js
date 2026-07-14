// ============================================================
// Настройка canvas
// ============================================================
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const W = canvas.width;
const H = canvas.height;

// ============================================================
// Считываем текущие значения слайдеров
// ============================================================
function readParams() {
  return {
    V0: parseFloat(document.getElementById("v0").value),
    barrierWidth: parseFloat(document.getElementById("width").value),
    k0: parseFloat(document.getElementById("k0").value),
  };
}

// ============================================================
// Создаём солвер с начальными параметрами
// ============================================================
let solver = new QuantumSolver(readParams());
let isRunning = false;

// ============================================================
// Пресеты реальных систем (иллюстративные пропорции, не точные данные)
// ============================================================
const PRESETS = {
  sun: {
    V0: 25, barrierWidth: 0.5, k0: 3,
    caption: "Внутри Солнца ядра атомов водорода должны преодолеть взаимное отталкивание, чтобы слиться. Энергии почти не хватает — поэтому термоядерная реакция в одном конкретном ядре происходит крайне редко, но звёзд и ядер очень много."
  },
  flash: {
    V0: 15, barrierWidth: 0.3, k0: 5,
    caption: "Во флеш-памяти электроны туннелируют сквозь тонкий изолирующий слой, чтобы записаться в ячейку памяти. Слой специально делают тонким — именно поэтому это вообще возможно."
  },
  stm: {
    V0: 10, barrierWidth: 0.2, k0: 4,
    caption: "Сканирующий туннельный микроскоп подводит иглу почти вплотную к поверхности. Электроны туннелируют через промежуток между иглой и атомами — и по силе туннельного тока можно увидеть отдельные атомы."
  },
  alpha: {
    V0: 20, barrierWidth: 2.5, k0: 2,
    caption: "При альфа-распаде частица внутри ядра урана заперта барьером ядерных сил. Барьер широкий, поэтому распад одного конкретного ядра — редкое событие, которое может ждать своего часа тысячи лет."
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
    document.getElementById("startBtn").textContent = "Запустить";
    solver.setParams(readParams());
    solver.reset();
    drawFrame();
  });
});

// ============================================================
// Живая вероятность прохождения/отражения
// ============================================================
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

// ============================================================
// Рисование одного кадра
// ============================================================
function drawFrame() {
  ctx.clearRect(0, 0, W, H);

  const density = solver.getProbabilityDensity();
  const maxDensity = Math.max(...density);
  const V = solver.V;
  const maxV = 30; // фиксированный максимум = верхняя граница слайдера, чтобы высота барьера реально менялась с V0

  function xToPixel(xVal) {
    return ((xVal - solver.xMin) / (solver.xMax - solver.xMin)) * W;
  }

 // --- барьер: заливка + линия ---
 const barrierGradient = ctx.createLinearGradient(0, H, 0, 0);
 barrierGradient.addColorStop(0, "rgba(255, 138, 102, 0.25)");
 barrierGradient.addColorStop(1, "rgba(255, 138, 102, 0.02)");

 ctx.beginPath();
 ctx.moveTo(xToPixel(solver.x[0]), H);
 for (let i = 0; i < solver.N; i++) {
   const px = xToPixel(solver.x[i]);
   const py = H - (V[i] / maxV) * (H * 0.5);
   ctx.lineTo(px, py);
 }
 ctx.lineTo(xToPixel(solver.x[solver.N - 1]), H);
 ctx.closePath();
 ctx.fillStyle = barrierGradient;
 ctx.fill();

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

 // --- волна: заливка с градиентом + свечение на линии ---
 const waveGradient = ctx.createLinearGradient(0, H, 0, 0);
 waveGradient.addColorStop(0, "rgba(139, 127, 255, 0.35)");
 waveGradient.addColorStop(1, "rgba(139, 127, 255, 0.03)");

 function waveY(i) {
   return H - (density[i] / maxDensity) * (H * 0.85) - 10;
 }

 ctx.beginPath();
 ctx.moveTo(xToPixel(solver.x[0]), H);
 for (let i = 0; i < solver.N; i++) {
   ctx.lineTo(xToPixel(solver.x[i]), waveY(i));
 }
 ctx.lineTo(xToPixel(solver.x[solver.N - 1]), H);
 ctx.closePath();
 ctx.fillStyle = waveGradient;
 ctx.fill();

 ctx.beginPath();
 ctx.shadowColor = "rgba(139, 127, 255, 0.6)";
 ctx.shadowBlur = 8;
 ctx.strokeStyle = "rgba(139, 127, 255, 1)";
 ctx.lineWidth = 2;
 for (let i = 0; i < solver.N; i++) {
   const px = xToPixel(solver.x[i]);
   const py = waveY(i);
   if (i === 0) ctx.moveTo(px, py);
   else ctx.lineTo(px, py);
 }
 ctx.stroke();
 ctx.shadowBlur = 0;

 // --- точка: самое вероятное место частицы ---
 let maxIdx = 0;
 for (let i = 1; i < solver.N; i++) {
   if (density[i] > density[maxIdx]) maxIdx = i;
 }
 const dotX = xToPixel(solver.x[maxIdx]);
 const dotY = waveY(maxIdx);
 ctx.beginPath();
 ctx.arc(dotX, dotY - 6, 4, 0, Math.PI * 2);
 ctx.fillStyle = "#ffffff";
 ctx.shadowColor = "rgba(255, 255, 255, 0.8)";
 ctx.shadowBlur = 6;
 ctx.fill();
 ctx.shadowBlur = 0;

 // --- подписи прямо на графике ---
 ctx.font = "12px 'IBM Plex Mono', monospace";
 ctx.fillStyle = "rgba(255, 138, 102, 0.9)";
 ctx.fillText("стена", xToPixel(solver.barrierStart + solver.barrierWidth) + 8, 20);
 ctx.fillStyle = "rgba(200, 195, 255, 0.7)";
 ctx.fillText("вероятнее всего частица здесь", dotX + 10, dotY - 6);

  document.getElementById("time-readout").textContent = `t = ${solver.time.toFixed(2)}`;
  document.getElementById("norm-readout").textContent = `вероятность = ${solver.getNorm().toFixed(4)}`;

  const { transmitted, reflected } = computeTR();
  const total = transmitted + reflected;
  const tPct = total > 0 ? (transmitted / (transmitted + reflected + 1e-9)) * 100 : 0;

  document.getElementById("prob-fill-t").style.width = `${Math.min(tPct, 100)}%`;
  document.getElementById("prob-fill-r").style.width = `${Math.max(100 - tPct, 0)}%`;
  document.getElementById("prob-t").textContent = `${(transmitted * 100).toFixed(1)}%`;
  document.getElementById("prob-r").textContent = `${(reflected * 100).toFixed(1)}%`;
  
  const feedback = document.getElementById("task-feedback");
if (feedback) {
  if (tPct > 50) {
    feedback.textContent = "✓ Задача 1 выполнена — больше половины прошло сквозь барьер";
  } else if (tPct < 2 && solver.time > 2) {
    feedback.textContent = "✓ Задача 2 выполнена — почти ничего не прошло";
  } else {
    feedback.textContent = "";
  }
}
}

// ============================================================
// Цикл анимации
// ============================================================
let lastFrameTime = performance.now();

function animate() {
  if (!isRunning) return;

  const now = performance.now();
  const elapsed = now - lastFrameTime;
  lastFrameTime = now;

  // на медленном устройстве кадры реже, но шагов больше за раз — скорость эволюции одинаковая для всех
  const stepsThisFrame = Math.max(1, Math.round((elapsed / 1000) * 500));
  for (let i = 0; i < Math.min(stepsThisFrame, 30); i++) {
    solver.step();
  }

  drawFrame();
  requestAnimationFrame(animate);
}

// ============================================================
// Обработчики кнопок
// ============================================================
document.getElementById("startBtn").addEventListener("click", () => {
  if (isRunning) {
    isRunning = false;
    document.getElementById("startBtn").textContent = "Запустить";
  } else {
    isRunning = true;
    document.getElementById("startBtn").textContent = "Пауза";
    animate();
  }
});

document.getElementById("resetBtn").addEventListener("click", () => {
  isRunning = false;
  document.getElementById("startBtn").textContent = "Запустить";
  solver.setParams(readParams());
  solver.reset();
  drawFrame();
});

["v0", "width", "k0"].forEach((id) => {
  document.getElementById(id).addEventListener("input", () => {
    document.getElementById(id + "-value").textContent = document.getElementById(id).value;
    document.querySelectorAll(".preset").forEach((b) => b.classList.remove("active"));
    document.getElementById("preset-caption").textContent = "Настрой параметры вручную ползунками или выбери готовый сценарий — пропорции энергии к барьеру подобраны для наглядности, не для точности.";
    isRunning = false;
    document.getElementById("startBtn").textContent = "Запустить";
    solver.setParams(readParams());
    solver.reset();
    drawFrame();
  });
});

drawFrame();