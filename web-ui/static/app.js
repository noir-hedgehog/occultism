const state = {
  summary: null,
  evidence: null,
  backlog: null,
  validationTemplate: null,
  interactionMatrix: null,
  runtimeHandoff: null,
  examples: null,
  session: null,
  docs: null,
  docQuery: "",
  activeDoc: null,
  preview: null,
  execution: null,
  handoff: null,
  caseRecord: null,
  jsonOpen: false,
};

const $ = (selector) => document.querySelector(selector);

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function inlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, href) => {
      const safeHref = href.trim();
      const allowed = /^(https?:\/\/|#|\/|[A-Za-z0-9_.%/?=&:-]+$)/.test(safeHref);
      if (!allowed || /^javascript:/i.test(safeHref)) return label;
      return `<a href="${safeHref}" target="_blank" rel="noreferrer">${label}</a>`;
    });
}

function tableCells(line) {
  return line
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function renderMarkdownTable(lines, startIndex) {
  const header = tableCells(lines[startIndex]);
  const rows = [];
  let index = startIndex + 2;
  while (index < lines.length && lines[index].includes("|") && lines[index].trim()) {
    rows.push(tableCells(lines[index]));
    index += 1;
  }
  const html = `
    <table>
      <thead><tr>${header.map((cell) => `<th>${inlineMarkdown(cell)}</th>`).join("")}</tr></thead>
      <tbody>
        ${rows
          .map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join("")}</tr>`)
          .join("")}
      </tbody>
    </table>
  `;
  return {html, nextIndex: index};
}

function markdownToHtml(markdown) {
  const lines = String(markdown || "").replace(/\r\n/g, "\n").split("\n");
  const blocks = [];
  let listItems = [];
  let codeLines = [];
  let inCode = false;

  function flushList() {
    if (!listItems.length) return;
    blocks.push(`<ul>${listItems.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("")}</ul>`);
    listItems = [];
  }

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const trimmed = line.trim();

    if (trimmed.startsWith("```")) {
      if (inCode) {
        blocks.push(`<pre class="doc-code"><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
        codeLines = [];
        inCode = false;
      } else {
        flushList();
        inCode = true;
      }
      continue;
    }

    if (inCode) {
      codeLines.push(line);
      continue;
    }

    if (!trimmed) {
      flushList();
      continue;
    }

    if (/^\|.+\|$/.test(trimmed) && index + 1 < lines.length && /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(lines[index + 1].trim())) {
      flushList();
      const table = renderMarkdownTable(lines, index);
      blocks.push(table.html);
      index = table.nextIndex - 1;
      continue;
    }

    const heading = /^(#{1,4})\s+(.+)$/.exec(trimmed);
    if (heading) {
      flushList();
      const level = heading[1].length;
      blocks.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }

    const list = /^[-*]\s+(.+)$/.exec(trimmed);
    if (list) {
      listItems.push(list[1]);
      continue;
    }

    flushList();
    blocks.push(`<p>${inlineMarkdown(trimmed)}</p>`);
  }

  flushList();
  if (inCode) blocks.push(`<pre class="doc-code"><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
  return blocks.join("");
}

function docButton(doc, label = "") {
  const title = doc.title || doc.path;
  const prefix = label ? `<strong>${escapeHtml(label)}：${escapeHtml(title)}</strong>` : `<strong>${escapeHtml(title)}</strong>`;
  return `
    <button class="doc-link" data-read-doc="${escapeHtml(doc.path)}" type="button">
      ${prefix}
      <span>${escapeHtml(doc.path)}</span>
    </button>
  `;
}

function commandRow(item) {
  const encodedCommand = encodeURIComponent(item.command || "");
  return `
    <div class="command-row" data-status="${escapeHtml(item.execution_status || "")}" data-runs="${item.runs_now === true}">
      <div>
        <strong>${escapeHtml(item.tool)}</strong>
        <code>${escapeHtml(item.command)}</code>
      </div>
      <button class="command-copy" type="button" data-copy-command="${encodedCommand}">复制</button>
    </div>
  `;
}

async function copyTextWithFallback(text, button, fallbackKey = "copy_command") {
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = "已复制";
  } catch {
    $("#jsonOutput").hidden = false;
    $("#toggleJson").textContent = "收起";
    state.jsonOpen = true;
    setJson({[fallbackKey]: text});
    button.textContent = "已显示";
  }
  window.setTimeout(() => {
    button.textContent = button.dataset.defaultLabel || "复制";
  }, 1200);
}

function bindCommandCopyButtons() {
  document.querySelectorAll("[data-copy-command]").forEach((button) => {
    button.dataset.defaultLabel = button.textContent;
    button.addEventListener("click", () => copyTextWithFallback(decodeURIComponent(button.dataset.copyCommand || ""), button));
  });
  document.querySelectorAll("[data-copy-group]").forEach((button) => {
    button.dataset.defaultLabel = button.textContent;
    button.addEventListener("click", () =>
      copyTextWithFallback(decodeURIComponent(button.dataset.copyGroup || ""), button, "copy_command_group"),
    );
  });
}

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

function renderExamples() {
  if (!state.examples) {
    $("#examplePresets").innerHTML = "";
    return;
  }
  $("#examplePresets").innerHTML = `
    <div class="example-heading">
      <strong>示例请求</strong>
      <span>${state.examples.trunk_count} 条主干</span>
    </div>
    <div class="example-grid">
      ${state.examples.examples
        .map(
          (example) => `
            <button class="example-card" type="button" data-example-id="${example.id}" data-valid="${example.expected_matches}">
              <strong>${example.title}</strong>
              <span>${example.trunk_title} · ${example.domain_display_name}</span>
              <small>${example.actual_paradigm}</small>
            </button>
          `,
        )
        .join("")}
    </div>
  `;
  document.querySelectorAll("[data-example-id]").forEach((button) => {
    button.addEventListener("click", () => applyExample(button.dataset.exampleId));
  });
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

function workbenchActionState(session, action) {
  const manifest = session?.ui_actions?.[action];
  if (manifest) {
    return {
      label: manifest.label,
      disabled: manifest.enabled !== true,
      reason: manifest.reason,
      endpoint: manifest.endpoint,
      surface_id: manifest.surface_id,
    };
  }
  const canContinue = session?.can_continue_mystic_workflow === true;
  const states = {
    execute: {
      label: "安全执行",
      disabled: false,
      reason: "仅运行路由、范式和 intake 等安全白名单工具",
    },
    preview: {
      label: "结构化预览",
      disabled: !canContinue,
      reason: canContinue ? "补齐结构化输入后运行白名单领域工具" : "风险暂停时不继续领域工具预览",
    },
    handoff: {
      label: "Agent 交接",
      disabled: false,
      reason: canContinue ? "生成 Agent 综合和审校交接包" : "生成安全/专业边界交接包",
    },
    case: {
      label: "案例候选",
      disabled: !canContinue,
      reason: canContinue ? "记录回访和审校状态作为候选案例" : "风险暂停时不采集为普通案例",
    },
  };
  return states[action];
}

function workbenchActionButton(session, action) {
  const state = workbenchActionState(session, action);
  return `
    <button
      type="button"
      data-workbench-action="${action}"
      data-disabled-reason="${escapeHtml(state.reason)}"
      ${state.disabled ? "disabled" : ""}
      title="${escapeHtml(state.reason)}"
    >
      ${state.label}
    </button>
  `;
}

function renderWorkbenchOverview(session) {
  if (!session || !session.workbench_overview) {
    $("#workbenchOverview").innerHTML = `
      <div class="overview-intro">
        <strong>工作台总览</strong>
        <p>输入一个具体问题后，这里会汇总主干、范式、自动化步骤、Agent 接管点和必读文档。</p>
      </div>
    `;
    return;
  }
  const overview = session.workbench_overview;
  const counts = overview.counts;
  const docs = overview.required_docs
    .map((doc) => `<li>${docButton(doc, doc.role)}</li>`)
    .join("");
  const nextActions = overview.next_actions.map((item) => `<li>${item}</li>`).join("");
  $("#workbenchOverview").innerHTML = `
    <div class="overview-header">
      <div>
        <strong>${overview.title}</strong>
        <p>${overview.trunk.title} · ${overview.question_type} · ${overview.automation_mode}</p>
      </div>
      <span class="overview-risk risk-${overview.risk_level}">${overview.risk_level}</span>
    </div>
    <div class="overview-grid">
      <div class="overview-metric"><strong>${counts.runnable_tools}</strong><span>可直接运行</span></div>
      <div class="overview-metric"><strong>${counts.structured_input_tools}</strong><span>需结构化输入</span></div>
      <div class="overview-metric"><strong>${counts.agent_or_review_steps}</strong><span>Agent/审校步骤</span></div>
      <div class="overview-metric"><strong>${counts.context_docs}</strong><span>上下文文档</span></div>
    </div>
    <div class="overview-columns">
      <section>
        <h3>下一步</h3>
        <ol>${nextActions}</ol>
        <div class="overview-actions">
          ${["execute", "preview", "handoff", "case"].map((action) => workbenchActionButton(session, action)).join("")}
        </div>
        <p class="overview-action-note">${session.can_continue_mystic_workflow ? "当前请求可继续领域流程。" : "当前请求已暂停领域流程，只保留安全执行和边界交接。"}</p>
      </section>
      <section>
        <h3>必读文档</h3>
        <ul>${docs}</ul>
      </section>
    </div>
  `;
  bindWorkbenchActionButtons();
}

function bindWorkbenchActionButtons() {
  document.querySelectorAll("[data-workbench-action]").forEach((button) => {
    button.addEventListener("click", () => {
      if (button.disabled) return;
      const action = button.dataset.workbenchAction;
      if (action === "execute") runExecution();
      if (action === "preview") runPreview();
      if (action === "handoff") runHandoff();
      if (action === "case") runCaseRecord();
    });
  });
}

function applyPanelActionGuard(buttonSelector, noteSelector, action) {
  const button = $(buttonSelector);
  const note = $(noteSelector);
  if (!button || !note) return;
  const hasSession = Boolean(state.session);
  const actionState = workbenchActionState(state.session, action);
  const disabled = hasSession && actionState.disabled;
  button.disabled = disabled;
  button.title = hasSession ? actionState.reason : "";
  button.dataset.panelGuardReason = hasSession ? actionState.reason : "";
  note.hidden = !disabled;
  note.textContent = disabled ? actionState.reason : "";
}

function syncPanelActionGuards() {
  applyPanelActionGuard("#previewButton", "#previewGuardNote", "preview");
  applyPanelActionGuard("#caseButton", "#caseGuardNote", "case");
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
  const boundary = p.execution_boundary;
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
    <article class="trunk paradigm-boundary">
      <h3>执行分工</h3>
      <div class="boundary-grid">
        <section>
          <strong>程序化</strong>
          <ul>${boundary.automated_parts.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
        </section>
        <section>
          <strong>Agent</strong>
          <ul>${boundary.agent_required_parts.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
        </section>
      </div>
      <p class="review-note">${boundary.human_review_recommended ? "建议人工审校" : "常规记录即可"}</p>
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

function renderEvidence() {
  if (!state.evidence) {
    $("#evidenceBadge").textContent = "";
    $("#evidencePanel").innerHTML = "";
    return;
  }
  $("#evidenceBadge").textContent = `${state.evidence.domain_count} 个领域`;
  const priorities = Object.entries(state.evidence.priority_counts)
    .map(([key, value]) => `<span class="chip">${key} ${value}</span>`)
    .join("");
  const modes = Object.entries(state.evidence.evidence_mode_counts)
    .map(([key, value]) => `<span class="chip">${key} ${value}</span>`)
    .join("");
  $("#evidencePanel").innerHTML = `
    <article class="packet-card">
      <h3>优先级</h3>
      <div class="chips">${priorities}</div>
    </article>
    <article class="packet-card">
      <h3>证据模式</h3>
      <div class="chips">${modes}</div>
    </article>
    ${state.evidence.workstreams
      .map(
        (stream) => `
          <article class="evidence-stream">
            <strong>${stream.id}</strong>
            <p>${stream.description}</p>
            <span>${stream.domain_count} 个领域</span>
          </article>
        `,
      )
      .join("")}
  `;
}

function renderBacklog() {
  if (!state.backlog) {
    $("#backlogBadge").textContent = "";
    $("#backlogPanel").innerHTML = "";
    return;
  }
  $("#backlogBadge").textContent = `${state.backlog.backlog_count} 项`;
  const priorities = Object.entries(state.backlog.priority_counts)
    .map(([key, value]) => `<span class="chip">${key} ${value}</span>`)
    .join("");
  const artifacts = Object.entries(state.backlog.target_artifact_counts)
    .map(([key, value]) => `<span class="chip">${key} ${value}</span>`)
    .join("");
  $("#backlogPanel").innerHTML = `
    <article class="packet-card">
      <h3>优先级</h3>
      <div class="chips">${priorities}</div>
    </article>
    <article class="packet-card">
      <h3>目标产物</h3>
      <div class="chips">${artifacts}</div>
    </article>
    ${state.backlog.workstreams
      .map(
        (stream) => `
          <article class="evidence-stream">
            <strong>${stream.id}</strong>
            <p>${stream.description}</p>
            <span>${stream.recommended_tool}</span>
          </article>
        `,
      )
      .join("")}
  `;
}

function renderValidationTemplate() {
  $("#templateBadge").textContent = state.validationTemplate ? `${state.validationTemplate.template_count} 个模板` : "待生成";
  if (!state.validationTemplate || !state.validationTemplate.templates.length) {
    $("#templatePanel").innerHTML = "";
    $("#templateOutput").textContent = "{}";
    return;
  }
  const template = state.validationTemplate.templates[0];
  const fields = template.collection_template.fields
    .map((field) => `<span class="chip" title="${field.prompt}">${field.field}</span>`)
    .join("");
  const flow = template.recommended_tool_flow
    .map(
      (step) => `
        <article class="evidence-stream">
          <strong>${step.tool}</strong>
          <p>${step.purpose}</p>
          <span>${step.input_from_fields.join(", ")}</span>
        </article>
      `,
    )
    .join("");
  $("#templatePanel").innerHTML = `
    <article class="packet-card">
      <h3>${template.display_name} · ${template.priority}</h3>
      <div class="chips">
        <span class="chip">${template.target_artifact}</span>
        <span class="chip">${template.evidence_mode}</span>
        <span class="chip">${template.source_backlog_id}</span>
      </div>
    </article>
    <article class="packet-card">
      <h3>采集字段</h3>
      <div class="chips">${fields}</div>
    </article>
    ${flow}
  `;
  $("#templateOutput").textContent = JSON.stringify(
    {
      template_id: template.template_id,
      example_payload: template.collection_template.example_payload,
      review_checklist: template.collection_template.review_checklist,
      acceptance_criteria: template.collection_template.acceptance_criteria,
    },
    null,
    2,
  );
}

function renderInteractionMatrix() {
  if (!state.interactionMatrix) {
    $("#interactionBadge").textContent = "";
    $("#interactionPanel").innerHTML = "";
    return;
  }
  $("#interactionBadge").textContent = `${state.interactionMatrix.surface_count} 个入口`;
  const groups = state.interactionMatrix.automation_groups
    .map((group) => `<span class="chip" title="${group.description}">${group.automation_level} ${group.surface_count}</span>`)
    .join("");
  const surfaces = state.interactionMatrix.surfaces
    .map(
      (surface) => `
        <article class="evidence-stream">
          <strong>${surface.display_name}</strong>
          <p>${surface.user_surface} · ${surface.agent_boundary}</p>
          <span>${surface.api_endpoint} · ${surface.primary_tool} · ${surface.automation_level}</span>
        </article>
      `,
    )
    .join("");
  $("#interactionPanel").innerHTML = `
    <article class="packet-card">
      <h3>自动化等级</h3>
      <div class="chips">${groups}</div>
    </article>
    ${surfaces}
  `;
}

function renderRuntimeHandoff() {
  if (!state.runtimeHandoff) {
    $("#runtimeBadge").textContent = "待加载";
    $("#runtimePanel").innerHTML = "";
    $("#runtimeOutput").textContent = "{}";
    return;
  }
  const runtime = state.runtimeHandoff;
  $("#runtimeBadge").textContent = runtime.handoff_status;
  const actionRows = Object.entries(runtime.ui_action_manifests || {})
    .flatMap(([status, actions]) =>
      Object.values(actions).map(
        (action) => `
          <article class="runtime-action" data-enabled="${action.enabled}">
            <strong>${status} · ${action.label}</strong>
            <p>${action.reason}</p>
            <span>${action.enabled ? "enabled" : "disabled"} · ${action.endpoint} · ${action.surface_id}</span>
          </article>
        `,
      ),
    )
    .join("");
  const checks = (runtime.readiness_checks || [])
    .slice(0, 6)
    .map(
      (check) => `
        <span class="chip" title="${escapeHtml(check.summary)}">${check.check} ${check.passed ? "OK" : "FAIL"}</span>
      `,
    )
    .join("");
  const openItems = (runtime.open_external_items || []).map((item) => `<span class="chip">${item}</span>`).join("");
  $("#runtimePanel").innerHTML = `
    <article class="packet-card">
      <h3>运行时状态</h3>
      <div class="chips">
        <span class="chip">${runtime.skill_count} Skills</span>
        <span class="chip">${runtime.tool_count} Tools</span>
        <span class="chip">${runtime.handoff_status}</span>
      </div>
    </article>
    <article class="packet-card">
      <h3>准备度</h3>
      <div class="chips">${checks}</div>
    </article>
    <article class="packet-card">
      <h3>外部开放项</h3>
      <div class="chips">${openItems}</div>
    </article>
    <div class="runtime-actions">${actionRows}</div>
  `;
  $("#runtimeOutput").textContent = JSON.stringify(
    {
      handoff_status: runtime.handoff_status,
      ui_action_manifests: runtime.ui_action_manifests,
      integration_contract: runtime.integration_contract,
      limits: runtime.limits,
    },
    null,
    2,
  );
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
        <div class="doc-row">${docButton(doc, kind)}</div>
      `,
    )
    .join("");
}

function renderDocIndex() {
  if (!state.docs) return;
  const total = state.docs.total_count || state.docs.count;
  const query = state.docs.query || "";
  $("#docSearch").value = query;
  $("#docBadge").textContent = query ? `${state.docs.count}/${total} 篇` : `${state.docs.count} 篇`;
  $("#docSearchMeta").textContent = query ? `筛选：${query}` : "全部文档";
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
    $("#docContent").innerHTML = markdownToHtml(state.activeDoc.content);
  }
}

function renderCommands(session) {
  if (!session) {
    $("#toolCommands").innerHTML = "";
    $("#toolBadge").textContent = "";
    return;
  }
  const chain = session.packet?.tool_chain || session.initial_tool_commands || [];
  const groups = [
    ["runnable_now", "可直接运行"],
    ["requires_structured_input", "需结构化输入"],
    ["requires_draft_output", "需草稿/Agent"],
  ];
  const grouped = groups
    .map(([status, label]) => [status, label, chain.filter((item) => item.execution_status === status)])
    .filter(([, , items]) => items.length);
  const fallback = chain.filter((item) => !item.execution_status);
  const count = chain.length;
  $("#toolBadge").textContent = `${count} 个工具`;
  $("#toolCommands").innerHTML = `
    ${grouped
      .map(
        ([status, label, items]) => `
          <section class="tool-chain-group" data-status="${status}">
            <h3>
              <span>${label}<small>${items.length}</small></span>
              ${
                status === "runnable_now"
                  ? `<button class="command-copy group-copy" type="button" data-copy-group="${encodeURIComponent(
                      items.map((item) => item.command).join("\n"),
                    )}">复制本组</button>`
                  : ""
              }
            </h3>
            ${items
              .map((item) => commandRow(item))
              .join("")}
          </section>
        `,
      )
      .join("")}
    ${fallback
      .map((item) => commandRow(item))
      .join("")}
  `;
  bindCommandCopyButtons();
}

function renderExecution() {
  $("#executionBadge").textContent = state.execution ? state.execution.run_status : "待运行";
  if (!state.execution) {
    $("#executionPanel").innerHTML = "";
    $("#executionOutput").textContent = "{}";
    return;
  }
  const summary = state.execution.execution_summary;
  $("#executionPanel").innerHTML = `
    <article class="packet-card">
      <h3>已执行</h3>
      <div class="chips">
        <span class="chip">${summary.executed_count} 个工具</span>
        <span class="chip">跳过 ${summary.skipped_count}</span>
        <span class="chip">错误 ${summary.error_count}</span>
      </div>
    </article>
    <article class="packet-card">
      <h3>接管需求</h3>
      <div class="chips">
        <span class="chip">结构化输入 ${summary.structured_input_count}</span>
        <span class="chip">草稿检查 ${summary.draft_required_count}</span>
        <span class="chip">${state.execution.agent_handoff.required ? "需要 Agent" : "可继续自动"}</span>
      </div>
    </article>
  `;
  $("#executionOutput").textContent = JSON.stringify(
    {
      run_status: state.execution.run_status,
      executed_tools: state.execution.executed_tools.map((item) => item.summary),
      skipped_tools: state.execution.skipped_tools.map((item) => ({
        tool: item.tool,
        reason: item.reason,
      })),
      next_ui_steps: state.execution.agent_handoff.next_ui_steps,
    },
    null,
    2,
  );
}

function renderPreview() {
  $("#previewBadge").textContent = state.preview ? state.preview.tool_name : "待生成";
  $("#previewOutput").textContent = JSON.stringify(state.preview || {}, null, 2);
}

function renderHandoff() {
  $("#handoffBadge").textContent = state.handoff ? state.handoff.handoff_status : "待生成";
  $("#handoffOutput").textContent = JSON.stringify(state.handoff || {}, null, 2);
}

function renderCaseRecord() {
  $("#caseBadge").textContent = state.caseRecord ? state.caseRecord.case_status : "待生成";
  $("#caseOutput").textContent = JSON.stringify(state.caseRecord || {}, null, 2);
}

function renderAll() {
  if (state.summary) {
    renderMetrics(state.summary.metrics);
    renderDocs(state.summary.entry_docs);
    renderTrunks(state.summary.trunks);
  }
  renderExamples();
  renderStatus(state.session);
  renderWorkbenchOverview(state.session);
  renderWorkflow(state.session);
  renderParadigm(state.session);
  renderPacket(state.session);
  renderEvidence();
  renderBacklog();
  renderValidationTemplate();
  renderInteractionMatrix();
  renderRuntimeHandoff();
  renderContext(state.session);
  renderCommands(state.session);
  renderDocIndex();
  renderExecution();
  renderPreview();
  renderHandoff();
  renderCaseRecord();
  syncPanelActionGuards();
  setJson(state.session || state.summary || {});
}

async function loadSummary() {
  const response = await fetch("/api/summary");
  if (!response.ok) throw new Error(`summary failed: ${response.status}`);
  state.summary = await response.json();
  renderAll();
}

async function loadDocs(query = state.docQuery || "") {
  state.docQuery = query;
  const url = query ? `/api/docs?q=${encodeURIComponent(query)}` : "/api/docs";
  const response = await fetch(url);
  if (!response.ok) throw new Error(`docs failed: ${response.status}`);
  state.docs = await response.json();
  renderAll();
}

async function loadEvidence() {
  const response = await fetch("/api/evidence-matrix");
  if (!response.ok) throw new Error(`evidence matrix failed: ${response.status}`);
  state.evidence = await response.json();
  renderAll();
}

async function loadBacklog() {
  const response = await fetch("/api/validation-backlog");
  if (!response.ok) throw new Error(`validation backlog failed: ${response.status}`);
  state.backlog = await response.json();
  renderAll();
}

async function loadValidationTemplate(domain = "fengshui") {
  const response = await fetch(`/api/validation-template?domain=${encodeURIComponent(domain)}`);
  if (!response.ok) throw new Error(`validation template failed: ${response.status}`);
  state.validationTemplate = await response.json();
  renderAll();
}

async function loadInteractionMatrix() {
  const response = await fetch("/api/interaction-surface-matrix");
  if (!response.ok) throw new Error(`interaction surface matrix failed: ${response.status}`);
  state.interactionMatrix = await response.json();
  renderAll();
}

async function loadRuntimeHandoff() {
  const response = await fetch("/api/runtime-handoff");
  if (!response.ok) throw new Error(`runtime handoff failed: ${response.status}`);
  state.runtimeHandoff = await response.json();
  renderAll();
}

async function loadExamples() {
  const response = await fetch("/api/examples");
  if (!response.ok) throw new Error(`examples failed: ${response.status}`);
  state.examples = await response.json();
  renderAll();
}

async function loadDoc(path) {
  const response = await fetch(`/api/docs?path=${encodeURIComponent(path)}`);
  if (!response.ok) throw new Error(`doc failed: ${response.status}`);
  state.activeDoc = await response.json();
  renderAll();
}

function applyExample(exampleId) {
  const example = state.examples?.examples?.find((item) => item.id === exampleId);
  if (!example) return;
  $("#requestText").value = example.request_text;
  $("#domainSelect").value = example.requested_domain || "";
  if (example.requested_domain === "tarot") {
    $("#previewMode").value = "tarot";
  } else if (example.requested_domain === "fengshui") {
    $("#previewMode").value = "fengshui";
  }
  syncPreviewMode();
  runSession();
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
  if (button.disabled) return;
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

async function runExecution() {
  const button = $("#executionButton");
  button.disabled = true;
  button.textContent = "运行中";
  try {
    const payload = {
      request_text: $("#requestText").value.trim(),
      requested_domain: $("#domainSelect").value || undefined,
    };
    const response = await fetch("/api/execute-safe", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `execute failed: ${response.status}`);
    state.execution = data;
  } catch (error) {
    state.execution = {tool: "consultation_execution_runner", run_status: "error", execution_summary: {executed_count: 0, skipped_count: 0, error_count: 1, structured_input_count: 0, draft_required_count: 0}, agent_handoff: {required: true, next_ui_steps: []}, executed_tools: [], skipped_tools: [], error: error.message};
  } finally {
    button.disabled = false;
    button.textContent = "运行安全子集";
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

async function runCaseRecord() {
  const button = $("#caseButton");
  if (button.disabled) return;
  button.disabled = true;
  button.textContent = "生成中";
  try {
    const payload = {
      request_text: $("#requestText").value.trim(),
      requested_domain: $("#domainSelect").value || undefined,
      preview_result: state.preview || undefined,
      handoff_result: state.handoff || undefined,
      draft_output: $("#draftOutput").value.trim(),
      source_label: $("#caseSourceLabel").value.trim() || "web-ui-candidate",
      follow_up_text: $("#caseFollowUp").value.trim(),
      validation_result: $("#caseValidation").value,
      reviewer: $("#caseReviewer").value.trim(),
      review_approved: $("#caseApproved").checked,
    };
    const response = await fetch("/api/case-record", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `case record failed: ${response.status}`);
    state.caseRecord = data;
  } catch (error) {
    state.caseRecord = {tool: "consultation_case_recorder", is_valid: false, error: error.message};
  } finally {
    button.disabled = false;
    button.textContent = "生成案例候选";
    renderAll();
  }
}

async function runValidationTemplate() {
  const button = $("#templateButton");
  button.disabled = true;
  button.textContent = "生成中";
  try {
    await loadValidationTemplate($("#templateDomain").value);
  } catch (error) {
    state.validationTemplate = {tool: "case_validation_template_builder", is_valid: false, template_count: 0, templates: [], error: error.message};
  } finally {
    button.disabled = false;
    button.textContent = "生成模板";
    renderAll();
  }
}

function syncPreviewMode() {
  const mode = $("#previewMode").value;
  $("#tarotFields").hidden = mode !== "tarot";
  $("#fengshuiFields").hidden = mode !== "fengshui";
}

$("#runButton").addEventListener("click", runSession);
$("#executionButton").addEventListener("click", runExecution);
$("#previewButton").addEventListener("click", runPreview);
$("#handoffButton").addEventListener("click", runHandoff);
$("#caseButton").addEventListener("click", runCaseRecord);
$("#templateButton").addEventListener("click", runValidationTemplate);
$("#previewMode").addEventListener("change", syncPreviewMode);
$("#docSearch").addEventListener("input", (event) => {
  loadDocs(event.target.value.trim()).catch((error) => setJson({error: error.message}));
});

$("#toggleJson").addEventListener("click", () => {
  state.jsonOpen = !state.jsonOpen;
  $("#jsonOutput").hidden = !state.jsonOpen;
  $("#toggleJson").textContent = state.jsonOpen ? "收起" : "展开";
});

Promise.all([
  loadSummary(),
  loadDocs(),
  loadExamples(),
  loadEvidence(),
  loadBacklog(),
  loadValidationTemplate(),
  loadInteractionMatrix(),
  loadRuntimeHandoff(),
])
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
