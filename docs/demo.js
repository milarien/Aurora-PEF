(() => {
  const WORKER_URL = "https://aurora-clarify.milamba.workers.dev";

  // One source of truth: scenario id -> prompt + context array
  const SCENARIOS = {
    bird_missing_v1: {
      prompt: `James has a bird.
Jenny has a bird.
The bird is missing.

Where is the bird?`,
      context: [
        "James has a bird.",
        "Jenny has a bird.",
        "The bird is missing."
      ]
    },
    telescope_v1: {
      prompt: `I saw the man with the telescope.`,
      context: [
        "I saw the man with the telescope."
      ]
    },
    trophy_v1: {
      prompt: `The trophy didn't fit in the suitcase because it was too small.`,
      context: [
        "The trophy didn't fit in the suitcase because it was too small."
      ]
    }
  };

  const el = (id) => document.getElementById(id);

  const scenarioSel = el("demoScenario");   // <select>
  const promptBox   = el("demoPrompt");     // <pre>
  const startBtn    = el("demoStart");
  const resetBtn    = el("demoReset");
  const statusBox   = el("demoStatus");
  const verdict     = el("demoVerdict");
  const msg         = el("demoMsg");
  const choices     = el("demoChoices");
  const out         = el("demoOutput");

  function currentScenarioId() {
    const v = scenarioSel?.value || "bird_missing_v1";
    return SCENARIOS[v] ? v : "bird_missing_v1";
  }

  function applyScenarioToUI() {
    const sid = currentScenarioId();
    promptBox.textContent = SCENARIOS[sid].prompt;
  }

  function setStatus(kind, title, text) {
    statusBox.style.display = "block";
    verdict.textContent = title;
    msg.textContent = text || "";
    statusBox.className = `status ${kind}`;
  }

  function clearUI() {
    statusBox.style.display = "none";
    choices.style.display = "none";
    choices.innerHTML = "";         // IMPORTANT: dynamic options now
    out.textContent = "";
    resetBtn.style.display = "none";
  }

  // Render choice buttons from Worker response options
  function renderChoices(options) {
    choices.innerHTML = "";

    (options || []).forEach((opt) => {
      // support either ["id","id2"] OR [{id,label}, ...]
      const id = typeof opt === "string" ? opt : opt.id;
      const label = typeof opt === "string" ? opt : (opt.label || opt.id);

      const b = document.createElement("button");
      b.className = "pill";
      b.dataset.choice = id;
      b.textContent = label;
      choices.appendChild(b);
    });

    choices.style.display = (options && options.length) ? "block" : "none";
  }

  async function callWorker(binding) {
    const sid = currentScenarioId();
    const ctx = SCENARIOS[sid].context;

    const res = await fetch(WORKER_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        context: ctx,
        binding: binding ?? null
      })
    });

    if (!res.ok) throw new Error(`Worker error: ${res.status}`);
    return res.json();
  }

  async function runInitial() {
    clearUI();
    applyScenarioToUI();

    out.textContent = "Calling gate…\n";

    const data = await callWorker(null);

    if (data.status === "STOP") {
      setStatus("warn", `Gate verdict: ${data.gate_verdict || "AMBIGUOUS_UNRESOLVED"}`, "Clarification required.");
      renderChoices(data.options);
      resetBtn.style.display = "inline-flex";
      out.textContent =
        "System: STOP\n" +
        `System: ${data.question}\n`;
      return;
    }

    if (data.status === "RESOLVED") {
      setStatus("ok", `Gate verdict: ${data.gate_verdict || "ADMISSIBLE"}`, "Resolution permitted.");
      resetBtn.style.display = "inline-flex";
      out.textContent += `System: ${data.statement}\n`;
      return;
    }

    // UNKNOWN / INVALID_BINDING / etc
    setStatus("bad", `Gate verdict: ${data.gate_verdict || "INADMISSIBLE_UNSUPPORTED"}`, data.message || "Unknown scenario.");
    resetBtn.style.display = "inline-flex";
    out.textContent += `System: ${data.status}\n`;
    if (data.message) out.textContent += `System: ${data.message}\n`;
  }

  async function choose(binding) {
    out.textContent += `User: ${binding}\n`;

    const data = await callWorker(binding);

    if (data.status === "RESOLVED") {
      setStatus("ok", `Gate verdict: ${data.gate_verdict || "ADMISSIBLE"}`, "Resolution permitted after binding.");
      choices.style.display = "none";
      resetBtn.style.display = "inline-flex";
      out.textContent += `System: ${data.statement}\n`;
      return;
    }

    setStatus("bad", `Gate verdict: ${data.gate_verdict || "INADMISSIBLE_UNSUPPORTED"}`, data.message || "Unexpected response.");
    resetBtn.style.display = "inline-flex";
    out.textContent += `Unexpected: ${JSON.stringify(data, null, 2)}\n`;
  }

  startBtn?.addEventListener("click", () => {
    runInitial().catch((e) => {
      setStatus("bad", "Gate verdict: INADMISSIBLE_UNSUPPORTED", "Demo unavailable.");
      resetBtn.style.display = "inline-flex";
      out.textContent += `${e.message}\n`;
    });
  });

  resetBtn?.addEventListener("click", () => {
    clearUI();
    applyScenarioToUI();
  });

  choices?.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-choice]");
    if (!btn) return;

    choose(btn.dataset.choice).catch((err) => {
      setStatus("bad", "Gate verdict: INADMISSIBLE_UNSUPPORTED", "Demo unavailable.");
      resetBtn.style.display = "inline-flex";
      out.textContent += `${err.message}\n`;
    });
  });

  scenarioSel?.addEventListener("change", () => {
    clearUI();
    applyScenarioToUI();
  });

  clearUI();
  applyScenarioToUI();
})();
