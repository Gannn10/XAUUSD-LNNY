/* ============================================
   GANIQUANT PORTFOLIO — app.js
   ============================================ */

// ===== DATA =====
const features = [
  { name: 'ob', score: 1.0 },
  { name: 'm15_ob', score: 0.2118 },
  { name: 'ob_bottom', score: 0.2104 },
  { name: 'ob_top', score: 0.1951 },
  { name: 'consecutive_direction', score: 0.1631 },
  { name: 'ob_mitigated', score: 0.0779 },
  { name: 'atr_ratio', score: 0.0717 },
  { name: 'body_ratio', score: 0.0539 },
  { name: 'returns_1', score: 0.049 },
  { name: 'bb_percent_b', score: 0.0488 },
];

const monthlyData = [
  { y: 2025, m: 'Aug', v: 1.22 }, { y: 2025, m: 'Sep', v: 3.07 },
  { y: 2025, m: 'Oct', v: 6.22 }, { y: 2025, m: 'Nov', v: 1.77 },
  { y: 2025, m: 'Dec', v: 2.64 },
  { y: 2026, m: 'Jan', v: 12.98 }, { y: 2026, m: 'Feb', v: 12.38 },
  { y: 2026, m: 'Mar', v: 10.02 }, { y: 2026, m: 'Apr', v: 4.38 },
  { y: 2026, m: 'May', v: 7.91 }, { y: 2026, m: 'Jun', v: 7.60 },
  { y: 2026, m: 'Jul', v: 5.04 }, { y: 2026, m: 'Aug', v: 5.18 },
];

// Simulated equity data (monthly interpolated)
const equityLabels = [
  'Aug 25','Sep 25','Oct 25','Nov 25','Dec 25',
  'Jan 26','Feb 26','Mar 26','Apr 26','May 26',
  'Jun 26','Jul 26','Aug 26','Sep 26'
];
const equityValues = [10000, 10307, 10949, 11126, 11421, 12836, 14424, 15868, 16563, 17872, 19228, 20218, 21267, 21267];
const drawdownValues = [0.0, 0.3, 0.6, 1.0, 0.4, 0.6, 2.37, 0.5, 0.8, 0.5, 0.7, 0.6, 0.4, 0.3];

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  initHeatmapColors();
  initFeatureList();
  initEquityChart();
  initDonutCharts();
  initTabSystem();
  initFeatureBars();
  initBigHeatmap();
  initDistChart();
  initScrollAnimations();
});

// ===== HEATMAP COLORS =====
function initHeatmapColors() {
  document.querySelectorAll('.cell').forEach(cell => {
    const val = parseFloat(cell.getAttribute('data-val'));
    const intensity = val / 13;
    const L = 18 + intensity * 18;
    const S = 40 + intensity * 20;
    cell.style.backgroundColor = `hsl(130, ${S}%, ${L}%)`;
    cell.style.color = `hsl(130, 30%, ${60 + intensity * 20}%)`;
  });
}

// ===== FEATURE LIST =====
function initFeatureList() {
  const container = document.getElementById('featureList');
  if (!container) return;
  features.forEach(f => {
    const row = document.createElement('div');
    row.className = 'feat-row';
    row.innerHTML = `
      <div class="feat-name">${f.name}</div>
      <div class="feat-bar-wrap">
        <div class="feat-bar" data-width="${f.score * 100}"></div>
      </div>
      <div class="feat-score">${f.score.toFixed(4)}</div>
    `;
    container.appendChild(row);
  });
}

// ===== EQUITY CHART (Chart.js via CDN fallback — draw manually) =====
function initEquityChart() {
  const canvas = document.getElementById('equityChart');
  if (!canvas) return;

  // Load Chart.js dynamically
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
  script.onload = () => {
    const ctx = canvas.getContext('2d');

    const greenGrad = ctx.createLinearGradient(0, 0, 0, 300);
    greenGrad.addColorStop(0, 'rgba(78,204,163,0.3)');
    greenGrad.addColorStop(1, 'rgba(78,204,163,0.0)');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: equityLabels,
        datasets: [
          {
            label: 'Equity ($)',
            data: equityValues,
            borderColor: '#4ecca3',
            backgroundColor: greenGrad,
            borderWidth: 2.5,
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#4ecca3',
            pointRadius: 4,
            pointHoverRadius: 6,
            yAxisID: 'y',
          },
          {
            label: 'Max Drawdown (%)',
            data: drawdownValues,
            borderColor: '#63b3ed',
            backgroundColor: 'rgba(99,179,237,0.08)',
            borderWidth: 1.5,
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            yAxisID: 'y1',
            borderDash: [5,3],
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            labels: { color: '#8fa3c0', font: { family: 'Inter', size: 12 } }
          },
          tooltip: {
            backgroundColor: '#0d1a2e',
            borderColor: 'rgba(78,204,163,0.3)',
            borderWidth: 1,
            titleColor: '#e8f0fe',
            bodyColor: '#8fa3c0',
          }
        },
        scales: {
          x: {
            ticks: { color: '#8fa3c0', font: { size: 11 } },
            grid: { color: 'rgba(255,255,255,0.04)' }
          },
          y: {
            position: 'left',
            ticks: {
              color: '#4ecca3',
              callback: v => '$' + v.toLocaleString(),
              font: { size: 11 }
            },
            grid: { color: 'rgba(255,255,255,0.04)' }
          },
          y1: {
            position: 'right',
            ticks: {
              color: '#63b3ed',
              callback: v => v + '%',
              font: { size: 11 }
            },
            grid: { display: false }
          }
        }
      }
    });
  };
  document.head.appendChild(script);
}

// ===== DONUT CHARTS =====
function initDonutCharts() {
  const chartScript = document.querySelector('script[src*="chart.js"]');
  const doAfterChartJs = () => {
    if (typeof Chart === 'undefined') { setTimeout(doAfterChartJs, 200); return; }
    drawDonut('asianChart', 32.87, '#4ecca3', '#1a3a2a');
    drawDonut('londonChart', 38.14, '#63b3ed', '#0d1e33');
  };
  setTimeout(doAfterChartJs, 500);
}

function drawDonut(id, winRate, color, bgColor) {
  const canvas = document.getElementById(id);
  if (!canvas || typeof Chart === 'undefined') return;
  new Chart(canvas.getContext('2d'), {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [winRate, 100 - winRate],
        backgroundColor: [color, bgColor],
        borderWidth: 0,
        hoverOffset: 4,
      }]
    },
    options: {
      cutout: '72%',
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      animation: { animateRotate: true, duration: 1200 }
    }
  });
}

// ===== TABS =====
function initTabSystem() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tab = btn.getAttribute('data-tab');
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const panel = document.getElementById('tab-' + tab);
      if (panel) panel.classList.add('active');
    });
  });
}

// ===== FEATURE BARS (dashboard tab) =====
function initFeatureBars() {
  const container = document.getElementById('featureBars');
  if (!container) return;
  features.forEach(f => {
    const row = document.createElement('div');
    row.className = 'fb-row';
    row.innerHTML = `
      <div class="fb-name">${f.name}</div>
      <div class="fb-bar-wrap">
        <div class="fb-bar" style="width:${f.score * 100}%"></div>
      </div>
      <div class="fb-score">${f.score.toFixed(2)}</div>
    `;
    container.appendChild(row);
  });
}

// ===== BIG HEATMAP =====
function initBigHeatmap() {
  const container = document.getElementById('bigHeatmap');
  if (!container) return;
  const max = Math.max(...monthlyData.map(d => d.v));
  const html = monthlyData.map(d => {
    const intensity = d.v / max;
    const L = 18 + intensity * 20;
    const S = 40 + intensity * 20;
    const cL = 60 + intensity * 20;
    return `
      <div style="
        display:inline-block; margin:6px;
        background: hsl(130, ${S}%, ${L}%);
        color: hsl(130, 30%, ${cL}%);
        padding: 16px 20px; border-radius: 10px;
        font-size: 0.85rem; font-weight: 700; text-align:center;
        min-width: 90px;
      ">
        <div style="font-size:0.7rem;opacity:0.7;margin-bottom:4px">${d.m} ${d.y}</div>
        <div>+${d.v}%</div>
      </div>`;
  }).join('');
  container.innerHTML = html;
}

// ===== P&L DISTRIBUTION CHART =====
function initDistChart() {
  const canvas = document.getElementById('distChart');
  if (!canvas) return;
  const doAfterChartJs = () => {
    if (typeof Chart === 'undefined') { setTimeout(doAfterChartJs, 200); return; }
    const bins = ['-120','-100','-80','-60','-40','-30','-20','-10','0','10','20','30','40','50','60','70','80','100','120','150','200'];
    const losses = [2, 3, 5, 8, 15, 75, 430, 750, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    const wins =   [0, 0, 0, 0, 0, 0, 0, 0, 40, 155, 185, 110, 80, 45, 25, 15, 8, 5, 3, 2, 1];
    new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: bins,
        datasets: [
          { label: 'Loss Trades', data: losses, backgroundColor: 'rgba(252,129,129,0.7)', borderRadius: 4 },
          { label: 'Win Trades', data: wins, backgroundColor: 'rgba(78,204,163,0.7)', borderRadius: 4 },
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#8fa3c0', font: { family: 'Inter', size: 12 } } },
          tooltip: {
            backgroundColor: '#0d1a2e', borderColor: 'rgba(78,204,163,0.3)', borderWidth: 1,
            titleColor: '#e8f0fe', bodyColor: '#8fa3c0'
          }
        },
        scales: {
          x: { ticks: { color: '#8fa3c0', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.04)' } },
          y: { ticks: { color: '#8fa3c0', font: { size: 11 } }, grid: { color: 'rgba(255,255,255,0.04)' } }
        }
      }
    });
  };
  setTimeout(doAfterChartJs, 600);
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Animate bars
        entry.target.querySelectorAll('.feat-bar').forEach(bar => {
          bar.style.width = bar.getAttribute('data-width') + '%';
        });
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.kpi-card, .strategy-card, .tech-card, .skill-card, .feature-importance, .heatmap-container, .gallery-item, .gallery-featured').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });

  // Animate on visible
  document.addEventListener('animationframe', () => {});
  const styleTag = document.createElement('style');
  styleTag.textContent = `
    .visible { opacity: 1 !important; transform: translateY(0) !important; }
    .kpi-card.visible { transition-delay: calc(var(--i, 0) * 0.08s); }
  `;
  document.head.appendChild(styleTag);
}

// ===== LIGHTBOX =====
function openLightbox(src, caption) {
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lightboxImg');
  const cap = document.getElementById('lightboxCaption');
  if (!lb || !img) return;
  img.src = src;
  img.alt = caption || '';
  if (cap) cap.textContent = caption || '';
  lb.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  const lb = document.getElementById('lightbox');
  if (!lb) return;
  lb.classList.remove('open');
  document.body.style.overflow = '';
}

// Close on Escape key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeLightbox();
});

