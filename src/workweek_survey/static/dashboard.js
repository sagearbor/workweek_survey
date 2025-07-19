async function loadData() {
    const res = await fetch('/export');
    if (!res.ok) return;
    const data = await res.json();
    const responses = data.responses || [];
    const branches = new Set();
    responses.forEach(r => {
        if (r.org_branch) {
            branches.add(r.org_branch);
        }
    });
    const select = document.getElementById('branch-select');
    select.innerHTML = '<option value="">All</option>' +
        Array.from(branches).map(b => `<option value="${b}">${b}</option>`).join('');
    select.addEventListener('change', () => render(select.value, responses));
    render('', responses);
}

function render(branch, responses) {
    const filtered = branch ? responses.filter(r => r.org_branch === branch) : responses;
    const totals = {};
    filtered.forEach(r => {
        r.tasks.forEach(t => {
            totals[t.name] = (totals[t.name] || 0) + t.duration_hours;
        });
    });
    const sum = Object.values(totals).reduce((a, b) => a + b, 0);
    const chart = document.getElementById('chart');
    chart.innerHTML = Object.entries(totals).map(([name, hours]) => {
        const pct = sum ? ((hours / sum) * 100).toFixed(1) : 0;
        return `<div>${name}: ${pct}%</div>`;
    }).join('');
}

window.addEventListener('load', loadData);
