const BASE_URL = "http://tools.spamuraiwarrior.com";

function showSuccess(el, labelText, rows) {
    const rowsHtml = rows.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("");
    el.innerHTML = `
        <div class="result-box success">
            <div class="result-label">${labelText}</div>
            <table>${rowsHtml}</table>
        </div>`;
}

function showSimpleSuccess(el, labelText, valueText) {
    el.innerHTML = `
        <div class="result-box success">
            <div class="result-label">${labelText}</div>
            <strong>${valueText}</strong>
        </div>`;
}

function showError(el, msg) {
    el.innerHTML = `<div class="result-box error">${msg}</div>`;
}

function setLoading(btn, el, loading) {
    btn.disabled = loading;
    btn.textContent = loading ? "..." : "Lookup";
    if (loading) el.innerHTML = "";
}

async function doLookup(action, body, resultEl, btn) {
    setLoading(btn, resultEl, true);
    try {
        const params = new URLSearchParams({ action, ...body });
        const resp = await fetch(BASE_URL + "/api", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: params.toString(),
        });
        if (!resp.ok) throw new Error("Server error");
        const data = await resp.json();

        if (data.error) {
            showError(resultEl, data.error);
        } else if (action === "areacode") {
            showSimpleSuccess(resultEl, body.area_code, data.result);
        } else if (action === "domain") {
            showSuccess(resultEl, data.domain, [
                ["Registrar", data.registrar],
                ["Registered", data.created],
            ]);
        } else if (action === "ip") {
            showSuccess(resultEl, data.ip, [
                ["City", data.city],
                ["Region", data.region],
                ["Country", data.country],
                ["ISP", data.isp],
                ["Organization", data.org],
                ["Coordinates", `${data.lat}, ${data.lon}`],
            ]);
        }
    } catch (e) {
        showError(resultEl, "Could not reach tools.spamuraiwarrior.com. Is the server running?");
    }
    setLoading(btn, resultEl, false);
}

// Area code
document.getElementById("acBtn").addEventListener("click", () => {
    const val = document.getElementById("acInput").value.trim();
    doLookup("areacode", { area_code: val }, document.getElementById("acResult"), document.getElementById("acBtn"));
});

// Domain
document.getElementById("domainBtn").addEventListener("click", () => {
    const val = document.getElementById("domainInput").value.trim();
    doLookup("domain", { domain_query: val }, document.getElementById("domainResult"), document.getElementById("domainBtn"));
});

// IP
document.getElementById("ipBtn").addEventListener("click", () => {
    const val = document.getElementById("ipInput").value.trim();
    doLookup("ip", { ip_query: val }, document.getElementById("ipResult"), document.getElementById("ipBtn"));
});

// Enter key support
document.getElementById("acInput").addEventListener("keydown", e => { if (e.key === "Enter") document.getElementById("acBtn").click(); });
document.getElementById("domainInput").addEventListener("keydown", e => { if (e.key === "Enter") document.getElementById("domainBtn").click(); });
document.getElementById("ipInput").addEventListener("keydown", e => { if (e.key === "Enter") document.getElementById("ipBtn").click(); });

// Clear all
document.getElementById("clearBtn").addEventListener("click", () => {
    ["acInput", "domainInput", "ipInput"].forEach(id => document.getElementById(id).value = "");
    ["acResult", "domainResult", "ipResult"].forEach(id => document.getElementById(id).innerHTML = "");
});
