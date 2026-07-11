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
let animationId = null;

// ============================================================
// Рисование одного кадра
// ============================================================
function drawFrame() {
  ctx.clearRect(0, 0, W, H);

  const density = solver.getProbabilityDensity();
  const maxDensity = Math.max(...density);
  const V = solver.V;
  const maxV = Math.max(...V, 1); // избегаем деления на 0, если V0=0

  // --- координаты: переводим x из физических единиц в пиксели canvas ---
  function xToPixel(xVal) {
    return ((xVal - solver.xMin) / (solver.xMax - solver.xMin)) * W;
  }

  // --- рисуем барьер (красным, снизу вверх, полупрозрачным) ---
  ctx.beginPath();
  ctx.strokeStyle = "rgba(255, 90, 90, 0.9)";
  ctx.lineWidth = 2;
  for (let i = 0; i < solver.N; i++) {
    const px = xToPixel(solver.x[i]);
    const py = H - (V[i] / maxV) * (H * 0.5);
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // --- рисуем |psi|^2 (синим) ---
  ctx.beginPath();
  ctx.strokeStyle = "rgba(90, 160, 255, 1)";
  ctx.lineWidth = 2;
  for (let i = 0; i < solver.N; i++) {
    const px = xToPixel(solver.x[i]);
    const py = H - (density[i] / maxDensity) * (H * 0.85) - 10;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // --- подпись времени ---
  ctx.fillStyle = "#e6e6e6";
  ctx.font = "14px system-ui";
  ctx.fillText(`t = ${solver.time.toFixed(2)}`, 10, 20);
  ctx.fillText(`норма = ${solver.getNorm().toFixed(4)}`, 10, 40);
}

// ============================================================
// Цикл анимации
// ============================================================
function animate() {
  if (!isRunning) return;

  // несколько шагов за кадр, чтобы движение было заметным (иначе слишком медленно)
  for (let i = 0; i < 5; i++) {
    solver.step();
  }

  drawFrame();
  animationId = requestAnimationFrame(animate);
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

// ============================================================
// Обработчики слайдеров — обновляют подписи и пересоздают солвер
// ============================================================
["v0", "width", "k0"].forEach((id) => {
  document.getElementById(id).addEventListener("input", () => {
    document.getElementById(id + "-value").textContent = document.getElementById(id).value;
    isRunning = false;
    document.getElementById("startBtn").textContent = "Запустить";
    solver.setParams(readParams());
    solver.reset();
    drawFrame();
  });
});

// --- первая отрисовка при загрузке страницы ---
drawFrame();