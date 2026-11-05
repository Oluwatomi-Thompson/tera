// Progressive enhancement for /lessons/calculator: updates the numbers and
// bar chart live as the sliders move, via the JSON API blueprint, instead
// of a full page reload on every drag. Works without JS too (the <form>
// submits as a GET and the server renders the same numbers) — this file
// never introduces a feature the server-rendered page lacks.

(function () {
  const form = document.getElementById("calc-form");
  if (!form) return;

  const monthlyInput = document.getElementById("monthly_rwf");
  const monthsInput = document.getElementById("months");
  const monthlyLabel = document.getElementById("monthly_rwf-value");
  const monthsLabel = document.getElementById("months-value");
  const totalContributedEl = document.getElementById("total_contributed");
  const growthEl = document.getElementById("growth");
  const totalValueEl = document.getElementById("total_value");
  const chart = document.getElementById("chart");

  const rwf = (n) => "RWF " + Math.round(n).toLocaleString("en-US");

  let debounceTimer = null;

  function recalculate() {
    const monthly_rwf = Number(monthlyInput.value);
    const months = Number(monthsInput.value);

    monthlyLabel.textContent = rwf(monthly_rwf);
    monthsLabel.textContent = `${months} months (~${(months / 12).toFixed(1)} yrs)`;

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch("/api/v1/calculator", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ monthly_rwf, months }),
        });
        if (!res.ok) return; // fall back silently — the form still works via GET submit
        const data = await res.json();

        totalContributedEl.textContent = rwf(data.total_contributed);
        growthEl.textContent = "+" + rwf(data.growth);
        totalValueEl.textContent = rwf(data.total_value);

        renderChart(data.schedule);
      } catch (err) {
        // Network hiccup — the sliders still reflect the new values, and a
        // normal form submit (or next successful fetch) will catch up.
      }
    }, 150);
  }

  function renderChart(schedule) {
    if (!schedule.length) return;
    const maxBalance = schedule[schedule.length - 1].balance || 1;
    const step = Math.max(1, Math.floor(schedule.length / 24));

    chart.innerHTML = "";
    schedule.forEach((point, i) => {
      if (i % step !== 0 && i !== schedule.length - 1) return;
      const bar = document.createElement("div");
      bar.className = "flex-1 bg-navy-400 rounded-t";
      bar.style.height = `${Math.round((point.balance / maxBalance) * 1000) / 10}%`;
      bar.title = `Month ${point.month}: ${rwf(point.balance)}`;
      chart.appendChild(bar);
    });
  }

  monthlyInput.addEventListener("input", recalculate);
  monthsInput.addEventListener("input", recalculate);
})();
