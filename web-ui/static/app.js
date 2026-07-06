const state = {
  summary: null,
  session: null,
  docs: null,
  activeDoc: null,
  preview: null,
  handoff: null,
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
        <a href="#" data-doc-path="${doc.path}" title="${doc.path}">
          <strong>${doc.title || doc.path}</strong>
          <span>${doc.path}</span>
        </a>
      `,
    )
    .join("");
  document.querySelectorAll("[data-doc-path]").forEach((item) => {
    item.addEventListener("click", (event) => {
      event.preventDefault();
      loadDoc(item.dataset.docPath);
    });
  });
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

function renderParadigm(session) {
  if (!session || !session.paradigm) {
    $("#paradigmBadge").textContent = "";
    $("#paradigmPanel").innerHTML = "";
    return;
  }
  const p = session.paradigm;
  $("#paradigmBadge").textContent = p.recommended_paradigm.id;
  const evidence = p.evidence_track;
  $("#paradigmPanel").innerHTML = `
    <article class="trunk">
      <h3>${p.recommended_paradigm.title}</h3>
      <p>${p.recommended_paradigm.why}</p>
      <div class="chips">
        <span class="chip">${p.trunk.title}</span>
        <span class="chip">${p.question_type}</span>
        <span class="chip">${p.execution_boundary.automation_mode}</span>
      </div>
    </article>
    <article class="trunk">
      <h3>证据轨道</h3>
      <div class="chips">
        <span class="chip">科学/实用 ${evidence.scientific_or_practical_validation ? "是" : "否"}</span>
        <span class="chip">溯源 ${evidence.provenance_audit ? "是" : "否"}</span>
        <span class="chip">神秘边界 ${evidence.mystical_boundary_priority ? "优先" : "常规"}</span>
      </div>
    </article>
  `;
}

function renderPacket(session) {
  if (!session || !session.packet) {
    $("#packetBadge").textContent = "";
    $("#packetPanel").innerHTML = "";
    return;
  }
  const packet = session.packet;
  $("#packetBadge").textContent = packet.agent_brief.handoff_summary;
  const runnable = packet.tool_chain.filter((item) => item.execution_status === "runnable_now").length;
  const structured = packet.tool_chain.filter((item) => item.execution_status === "requires_structured_input").length;
  $("#packetPanel").innerHTML = `
    <article class="packet-card">
      <h3>执行状态</h3>
      <div class="chips">
        <span class="chip">可直接运行 ${runnable}</span>
        <span class="chip">需补字段 ${structured}</span>
        <span class="chip">${packet.session.route_status}</span>
      </div>
    </article>
    <article class="packet-card">
      <h3>复核清单</h3>
      <ul>
        ${packet.agent_brief.review_checklist.map((item) => `<li>${item}</li>`).join("")}
      </ul>
    </article>
  `;
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

function renderDocIndex() {
  if (!state.docs) return;
  $("#docBadge").textContent = `${state.docs.count} 篇`;
  const selected = state.activeDoc?.path;
  $("#docIndex").innerHTML = state.docs.docs
    .map(
      (doc) => `
        <button class="doc-button ${selected === doc.path ? "active" : ""}" data-read-doc="${doc.path}" type="button">
          <strong>${doc.title || doc.path}</strong>
          <span>${doc.section} · ${doc.path}</span>
        </button>
      `,
    )
    .join("");
  document.querySelectorAll("[data-read-doc]").forEach((button) => {
    button.addEventListener("click", () => loadDoc(button.dataset.readDoc));
  });
  if (state.activeDoc) {
    $("#docContent").textContent = state.activeDoc.content;
  }
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

function renderPreview() {
  $("#previewBadge").textContent = state.preview ? state.preview.tool_name : "待生成";
  $("#previewOutput").textContent = JSON.stringify(state.preview || {}, null, 2);
}

function renderHandoff() {
  $("#handoffBadge").textContent = state.handoff ? state.handoff.handoff_status : "待生成";
  $("#handoffOutput").textContent = JSON.stringify(state.handoff || {}, null, 2);
}

function renderAll() {
  if (state.summary) {
    renderMetrics(state.summary.metrics);
    renderDocs(state.summary.entry_docs);
    renderTrunks(state.summary.trunks);
  }
  renderStatus(state.session);
  renderWorkflow(state.session);
  renderParadigm(state.session);
  renderPacket(state.session);
  renderContext(state.session);
  renderCommands(state.session);
  renderDocIndex();
  renderPreview();
  renderHandoff();
  setJson(state.session || state.summary || {});
}

async function loadSummary() {
  const response = await fetch("/api/summary");
  if (!response.ok) throw new Error(`summary failed: ${response.status}`);
  state.summary = await response.json();
  renderAll();
}

async function loadDocs() {
  const response = await fetch("/api/docs");
  if (!response.ok) throw new Error(`docs failed: ${response.status}`);
  state.docs = await response.json();
  renderAll();
}

async function loadDoc(path) {
  const response = await fetch(`/api/docs?path=${encodeURIComponent(path)}`);
  if (!response.ok) throw new Error(`doc failed: ${response.status}`);
  state.activeDoc = await response.json();
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
      paradigm: null,
      packet: null,
      context: {skill: {}, sop: [], knowledge: []},
      initial_tool_commands: [],
    };
    renderAll();
  } finally {
    button.disabled = false;
    button.textContent = "运行路由";
  }
}

function tarotPayload() {
  const positionsBySpread = {
    three_card_situation: ["现状", "阻碍", "建议"],
    past_present_tendency: ["过去影响", "当前状态", "趋势提醒"],
  };
  const spreadId = $("#tarotSpread").value;
  const cards = [1, 2, 3].map((index) => ({
    position: positionsBySpread[spreadId][index - 1],
    card: $(`#tarotCard${index}`).value.trim(),
    orientation: $(`#tarotOrientation${index}`).value,
  }));
  return {
    question_text: $("#tarotQuestion").value.trim(),
    spread_id: spreadId,
    cards,
  };
}

function fengshuiPayload() {
  const concerns = $("#fengshuiConcerns").value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
  return {
    request_text: $("#requestText").value.trim(),
    space_type: $("#fengshuiSpaceType").value,
    space_description: $("#fengshuiDescription").value.trim(),
    observation_text: $("#fengshuiDescription").value.trim(),
    concerns,
  };
}

async function runPreview() {
  const button = $("#previewButton");
  button.disabled = true;
  button.textContent = "生成中";
  try {
    const mode = $("#previewMode").value;
    const payload = mode === "tarot" ? tarotPayload() : fengshuiPayload();
    const response = await fetch("/api/tool-preview", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({mode, payload}),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `preview failed: ${response.status}`);
    state.preview = data;
  } catch (error) {
    state.preview = {tool: "web_ui_tool_preview", is_valid: false, error: error.message};
  } finally {
    button.disabled = false;
    button.textContent = "生成预览";
    renderAll();
  }
}

async function runHandoff() {
  const button = $("#handoffButton");
  button.disabled = true;
  button.textContent = "生成中";
  try {
    const payload = {
      request_text: $("#requestText").value.trim(),
      requested_domain: $("#domainSelect").value || undefined,
      preview_result: state.preview || undefined,
      draft_output: $("#draftOutput").value.trim(),
    };
    const response = await fetch("/api/handoff", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `handoff failed: ${response.status}`);
    state.handoff = data;
  } catch (error) {
    state.handoff = {tool: "consultation_handoff_builder", is_valid: false, error: error.message};
  } finally {
    button.disabled = false;
    button.textContent = "生成交接包";
    renderAll();
  }
}

function syncPreviewMode() {
  const mode = $("#previewMode").value;
  $("#tarotFields").hidden = mode !== "tarot";
  $("#fengshuiFields").hidden = mode !== "fengshui";
}

$("#runButton").addEventListener("click", runSession);
$("#previewButton").addEventListener("click", runPreview);
$("#handoffButton").addEventListener("click", runHandoff);
$("#previewMode").addEventListener("change", syncPreviewMode);

$("#toggleJson").addEventListener("click", () => {
  state.jsonOpen = !state.jsonOpen;
  $("#jsonOutput").hidden = !state.jsonOpen;
  $("#toggleJson").textContent = state.jsonOpen ? "收起" : "展开";
});

Promise.all([loadSummary(), loadDocs()])
  .then(() => {
    const first = state.summary?.entry_docs?.[0]?.path;
    if (first) return loadDoc(first);
    return null;
  })
  .then(renderAll)
  .catch((error) => {
    setJson({error: error.message});
  });

syncPreviewMode();
