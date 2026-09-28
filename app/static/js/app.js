function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[ch]));
}

async function submitPlanner(url, body, form, isFormData=false) {
  const error = form.querySelector(".error");
  if (error) error.textContent = "";
  const button = form.querySelector("button[type=submit]");
  if (button) { button.disabled = true; button.textContent = "Generating..."; }

  try {
    const options = {
      method: "POST",
      headers: isFormData ? {} : {"Content-Type":"application/json"},
      body: isFormData ? body : JSON.stringify(body)
    };
    const res = await fetch(url, options);
    const data = await res.json();
    if (res.status === 401) { location.href="/login"; return; }
    if (!res.ok) throw new Error(data.detail || "Unable to generate recommendation.");
    sessionStorage.setItem("lastRecommendation", JSON.stringify(data));
    location.href = "/recommendations?latest=1";
  } catch (err) {
    if (error) error.textContent = err.message;
  } finally {
    if (button) { button.disabled = false; button.textContent = "Generate Plan"; }
  }
}

function renderRecommendation(data, container) {
  const allocations = (data.allocations || []).map(a => `
    <div class="allocation">
      <span class="muted">${escapeHtml(a.category)}</span>
      <strong>₹${Number(a.amount).toLocaleString("en-IN")}</strong>
      <small>${Number(a.percentage).toFixed(1)}% · ${escapeHtml(a.notes)}</small>
    </div>`).join("");

  const recommendations = (data.recommendations || []).map(r => `
    <article class="recommendation">
      <span class="platform">${escapeHtml(r.platform)} · ${escapeHtml(r.category)}</span>
      <h3>${escapeHtml(r.name)}</h3>
      <div class="price">₹${Number(r.price).toLocaleString("en-IN")}</div>
      <p class="muted">${escapeHtml(r.rationale)}</p>
      <a href="${escapeHtml(r.search_url)}" target="_blank" rel="noopener noreferrer">Open platform search ↗</a>
    </article>`).join("");

  const tips = (data.tips || []).map(t => `<li>${escapeHtml(t)}</li>`).join("");

  container.innerHTML = `
    <div class="result-header">
      <div><span class="eyebrow">${escapeHtml(data.planner)} planner · ${data.ai_generated ? "AI generated" : "fallback mode"}</span>
      <h1>${escapeHtml(data.title)}</h1><p class="result-summary">${escapeHtml(data.summary)}</p></div>
      <div class="budget-box"><span>Estimated spend</span><strong>₹${Number(data.estimated_spend).toLocaleString("en-IN")}</strong><span>Remaining ₹${Number(data.remaining_budget).toLocaleString("en-IN")}</span></div>
    </div>
    <h2>Budget allocation</h2>
    <div class="allocation-grid">${allocations}</div>
    <h2>Recommendations</h2>
    <div class="recommendation-list">${recommendations || "<p class='muted'>No catalog matches were available.</p>"}</div>
    <div class="section-heading small" style="margin-top:50px"><h2>Planning tips</h2></div>
    <ul>${tips}</ul>`;
}

window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(location.search);
  if (params.get("latest") === "1") {
    const saved = sessionStorage.getItem("lastRecommendation");
    const el = document.querySelector("#recommendations");
    if (saved && el) renderRecommendation(JSON.parse(saved), el);
  }
});
