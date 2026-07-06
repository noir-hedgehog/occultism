const state = {
  summary: null,
  session: null,
  jsonOpen: false,
};

const $ = (selector) => document.querySelector(selector);

function setJson(data) {
  $("#jsonOutput").textContent = JSON.stringify(data, null, 2);
}

function renderMetrics(metrics) {
  const items = [
    ["领域", `${metrics.complete_domains}/${metrics.domains}`],
    ["Skill", metrics.skills],
    ["工具", metrics.tools],
    ["Dry-run", `${metrics.ready_cases}+${metrics.paused_or_blocked_cases}`],
  ];
  $("#metrics").innerHTML = items
    .map(([label, value]) => `<div class="metric"><strong>${value}</strong><span>${label}</span></div>`)
    .join("");
}

function renderDocs(docs) {
  $("#docs").innerHTML = docs
    .map(
      (doc) => `
        <a href="#" title="${doc.path}">
          <strong>${doc.title || doc.path}</strong>
          <span>${doc.path}</span>
        </a>
      `,
    )
    .join("");
}

function renderTrunks(trunks) {
  $("#trunkCount").textContent = `${trunks.length} 条主干`;
  $("#trunks").innerHTML = trunks
    .map(
      (trunk) => `
        <article class="trunk">
          <h3>${trunk.title}</h3>
          <div class="chips">
            ${trunk.domains
              .map((domain) => `<span class="chip" title="${domain.domain}">${domain.display_name}</span>`)
              .join("")}
          </div>
        </article>
      `,
    )
    .join("");
}

function renderStatus(session) {
  if (!session) {
    $("#statusStrip").innerHTML = `
      <div class="status-item"><strong>状态</strong><p>等待请求</p></div>
      <div class="status-item"><strong>风险</strong><p>未评估</p></div>
      <div class="status-item"><strong>流派</strong><p>未选择</p></div>
      <div class="status-item"><strong>下一步</strong><p>运行路由</p></div>
    `;
    return;
  }
  const riskClass = `risk-${session.risk_level}`;
  $("#statusStrip").innerHTML = `
    <div class="status-item"><strong>状态</strong><p>${session.route_status}</p></div>
    <div class="status-item"><strong>风险</strong><p class="${riskClass}">${session.risk_level}</p></div>
    <div class="status-item"><strong>流派</strong><p>${session.domain_display_name}</p></div>
    <div class="status-item"><strong>可继续</strong><p>${session.can_continue_mystic_workflow ? "是" : "否"}</p></div>
  `;
}

function renderWorkflow(session) {
  if (!session) {
    $("#workflow").innerHTML = "";
    $("#routeBadge").textContent = "待运行";
    return;
  }
  $("#routeBadge").textContent = session.route_status;
  $("#workflow").innerHTML = session.workflow_steps
    .map(
      (step) => `
        <article class="workflow-step" data-status="${step.status}">
          <h3>${step.step}</h3>
          <p>${step.label}</p>
        </article>
      `,
    )
    .join("");
}

function renderContext(session) {
  if (!session) {
    $("#contextDocs").innerHTML = "";
    $("#contextBadge").textContent = "";
    return;
  }
  const docs = [];
  if (session.context.skill.path) docs.push(["Skill", session.context.skill]);
  session.context.sop.forEach((doc) => docs.push(["SOP", doc]));
  session.context.knowledge.forEach((doc) => docs.push(["知识卡", doc]));
  $("#contextBadge").textContent = `${docs.length} 个文件`;
  $("#contextDocs").innerHTML = docs
    .map(
      ([kind, doc]) => `
        <div class="doc-row">
          <strong>${kind}：${doc.title || doc.path}</strong>
          <span>${doc.path}</span>
        </div>
      `,
    )
    .join("");
}

function renderCommands(session) {
  if (!session) {
    $("#toolCommands").innerHTML = "";
    $("#toolBadge").textContent = "";
    return;
  }
  $("#toolBadge").textContent = `${session.initial_tool_commands.length} 个工具`;
  $("#toolCommands").innerHTML = session.initial_tool_commands
    .map(
      (item) => `
        <div class="command-row" data-runs="${item.runs_now}">
          <strong>${item.tool}</strong>
          <code>${item.command}</code>
        </div>
      `,
    )
    .join("");
}

function renderAll() {
  if (state.summary) {
    renderMetrics(state.summary.metrics);
    renderDocs(state.summary.entry_docs);
    renderTrunks(state.summary.trunks);
  }
  renderStatus(state.session);
  renderWorkflow(state.session);
  renderContext(state.session);
  renderCommands(state.session);
  setJson(state.session || state.summary || {});
}

async function loadSummary() {
  const response = await fetch("/api/summary");
  if (!response.ok) throw new Error(`summary failed: ${response.status}`);
  state.summary = await response.json();
  renderAll();
}

async function runSession() {
  const button = $("#runButton");
  button.disabled = true;
  button.textContent = "运行中";
  try {
    const requestText = $("#requestText").value.trim();
    const requestedDomain = $("#domainSelect").value;
    const response = await fetch("/api/session", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        request_text: requestText,
        requested_domain: requestedDomain || undefined,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `session failed: ${response.status}`);
    state.session = data;
    renderAll();
  } catch (error) {
    state.session = {
      route_status: "error",
      risk_level: "red",
      domain_display_name: "错误",
      can_continue_mystic_workflow: false,
      workflow_steps: [{step: "error", status: "next", label: error.message}],
      context: {skill: {}, sop: [], knowledge: []},
      initial_tool_commands: [],
    };
    renderAll();
  } finally {
    button.disabled = false;
    button.textContent = "运行路由";
  }
}

$("#runButton").addEventListener("click", runSession);

$("#toggleJson").addEventListener("click", () => {
  state.jsonOpen = !state.jsonOpen;
  $("#jsonOutput").hidden = !state.jsonOpen;
  $("#toggleJson").textContent = state.jsonOpen ? "收起" : "展开";
});

loadSummary().then(renderAll).catch((error) => {
  setJson({error: error.message});
});

