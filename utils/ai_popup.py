import streamlit.components.v1 as components


def render_ai_popup():
    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
    html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        overflow: hidden;
    }}

    #assistant-widget {{
        position: absolute;
        left: 0;
        bottom: 0;
        width: 330px;
        color: #eef2f7;
        background: #101827;
        border: 1px solid rgba(34, 211, 238, 0.34);
        border-radius: 10px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
        overflow: hidden;
    }}

    #assistant-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        padding: 10px 12px;
        background: #0b1220;
        border-bottom: 1px solid rgba(34, 211, 238, 0.28);
        cursor: move;
        user-select: none;
    }}

    #assistant-title {{
        font-size: 13px;
        font-weight: 750;
        color: #f8fafc;
    }}

    #assistant-actions {{
        display: flex;
        gap: 6px;
    }}

    .icon-button {{
        width: 26px;
        height: 26px;
        border: 1px solid #334155;
        border-radius: 6px;
        color: #cbd5e1;
        background: #151f31;
        cursor: pointer;
        font-weight: 800;
        line-height: 1;
    }}

    .icon-button:hover {{
        background: #1e2b42;
        color: #ffffff;
    }}

    #assistant-body {{
        padding: 12px;
    }}

    #assistant-body.collapsed {{
        display: none;
    }}

    label {{
        display: block;
        margin-bottom: 6px;
        font-size: 12px;
        color: #98a5b8;
    }}

    textarea {{
        width: 100%;
        min-height: 92px;
        resize: vertical;
        box-sizing: border-box;
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        background: #0b1220;
        color: #e5e7eb;
        padding: 10px;
        outline: none;
        font-size: 13px;
    }}

    textarea:focus {{
        border-color: #22d3ee;
    }}

    .hint {{
        margin: 8px 0 10px;
        color: #98a5b8;
        font-size: 12px;
        line-height: 1.4;
    }}

    #open-assistant {{
        width: 100%;
        min-height: 38px;
        border: 1px solid #22d3ee;
        border-radius: 8px;
        background: linear-gradient(135deg, #22d3ee, #3b82f6);
        color: #03121f;
        font-size: 13px;
        font-weight: 800;
        cursor: pointer;
    }}

    #open-assistant:hover {{
        filter: brightness(1.06);
        border-color: #f59e0b;
    }}
</style>
</head>
<body>
<div id="assistant-widget">
    <div id="assistant-header">
        <div id="assistant-title">AI Assistant</div>
        <div id="assistant-actions">
            <button class="icon-button" id="toggle" title="Minimize or expand">-</button>
        </div>
    </div>
    <div id="assistant-body">
        <label for="assistant-question">Quick question</label>
        <textarea id="assistant-question" placeholder="Ask about threats, logs, phishing, IP risk..."></textarea>
        <div class="hint">Drag this popup from the top bar. It opens the full assistant with your question ready.</div>
        <button id="open-assistant">Open Assistant</button>
    </div>
</div>

<script>
    const frame = window.frameElement;
    if (frame) {{
        const savedLeft = localStorage.getItem("aiPopupLeft");
        const savedTop = localStorage.getItem("aiPopupTop");
        if (savedLeft && parseInt(savedLeft, 10) < 380) {{
            localStorage.removeItem("aiPopupLeft");
            localStorage.removeItem("aiPopupTop");
        }}
        frame.style.position = "fixed";
        frame.style.left = localStorage.getItem("aiPopupLeft") || "";
        frame.style.right = localStorage.getItem("aiPopupLeft") ? "" : "16px";
        frame.style.top = localStorage.getItem("aiPopupTop") || "";
        frame.style.bottom = localStorage.getItem("aiPopupTop") ? "" : "16px";
        frame.style.width = "340px";
        frame.style.height = localStorage.getItem("aiPopupCollapsed") === "true" ? "50px" : "275px";
        frame.style.zIndex = "2147483647";
        frame.style.border = "0";
        frame.style.background = "transparent";
        frame.style.pointerEvents = "auto";
    }}

    const header = document.getElementById("assistant-header");
    const body = document.getElementById("assistant-body");
    const toggle = document.getElementById("toggle");
    const openButton = document.getElementById("open-assistant");

    if (localStorage.getItem("aiPopupCollapsed") === "true") {{
        body.classList.add("collapsed");
        toggle.textContent = "+";
    }}

    let dragging = false;
    let startX = 0;
    let startY = 0;
    let startLeft = 0;
    let startTop = 0;

    header.addEventListener("mousedown", (event) => {{
        if (event.target.tagName === "BUTTON") return;
        dragging = true;
        startX = event.clientX;
        startY = event.clientY;
        const rect = frame.getBoundingClientRect();
        startLeft = rect.left;
        startTop = rect.top;
        document.body.style.cursor = "move";
    }});

    window.addEventListener("mousemove", (event) => {{
        if (!dragging || !frame) return;
        const nextLeft = Math.max(8, Math.min(window.parent.innerWidth - 350, startLeft + event.clientX - startX));
        const nextTop = Math.max(8, Math.min(window.parent.innerHeight - 60, startTop + event.clientY - startY));
        frame.style.left = `${{nextLeft}}px`;
        frame.style.top = `${{nextTop}}px`;
        frame.style.bottom = "";
        localStorage.setItem("aiPopupLeft", `${{nextLeft}}px`);
        localStorage.setItem("aiPopupTop", `${{nextTop}}px`);
    }});

    window.addEventListener("mouseup", () => {{
        dragging = false;
        document.body.style.cursor = "default";
    }});

    toggle.addEventListener("click", () => {{
        const collapsed = body.classList.toggle("collapsed");
        toggle.textContent = collapsed ? "+" : "-";
        localStorage.setItem("aiPopupCollapsed", collapsed ? "true" : "false");
        if (frame) frame.style.height = collapsed ? "50px" : "275px";
    }});

    openButton.addEventListener("click", () => {{
        const question = document.getElementById("assistant-question").value.trim();
        const params = new URLSearchParams();
        params.set("page", "AI Assistant");
        if (question) params.set("assistant_question", question);
        window.parent.location.href = `${{window.parent.location.pathname}}?${{params.toString()}}`;
    }});
</script>
</body>
</html>
"""
    components.html(html, height=0, width=0)
