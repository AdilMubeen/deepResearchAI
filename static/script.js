// Load preset reports on page load
window.addEventListener('DOMContentLoaded', () => {
    loadPreset('elizabeth-holmes');
    loadPreset('sam-bankman');
    loadPreset('martin-shkreli');
});

// Load a preset report
function loadPreset(presetId) {
    fetch('/get_preset/' + presetId)
        .then(res => res.json())
        .then(data => {
            const resultsContainerId = 'results-' + presetId;
            displayResults(data, document.getElementById(resultsContainerId));
            document.getElementById(resultsContainerId).style.display = 'block';
        })
        .catch(err => console.error('Failed to load preset:', err));
}

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-target');
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(target).classList.add('active');
    });
});

// Run preset research
function runPreset(name, context, focus, time_period, industry, location) {
    const tabId = name.toLowerCase().replace(/ /g, '-').replace(/[^a-z-]/g, '');
    runResearch({
        target: name,
        context,
        focus,
        time_period,
        industry,
        location
    }, `results-${tabId}`);
}

// Run research for new form
document.getElementById('researchForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    runResearch({
        target: formData.get('target'),
        context: formData.get('context'),
        focus: formData.get('focus'),
        time_period: formData.get('time_period'),
        industry: formData.get('industry'),
        location: formData.get('location')
    }, 'results-new-research');
});

function runResearch(data, resultsContainerId) {
    const resultsContainer = document.getElementById(resultsContainerId);
    const submitBtn = event.target.querySelector('.submit-btn') || document.getElementById('submitBtn');
    
    submitBtn.querySelector('.btn-text').style.display = 'none';
    submitBtn.querySelector('.btn-loader').style.display = 'inline-flex';
    submitBtn.disabled = true;
    
    fetch('/research', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams(data)
    })
    .then(res => res.json())
    .then(result => {
        if (result.error) {
            alert('Error: ' + result.error);
            return;
        }
        
        displayResults(result, resultsContainer);
        resultsContainer.style.display = 'block';
    })
    .catch(err => {
        console.error(err);
        alert('Research failed: ' + err.message);
    })
    .finally(() => {
        submitBtn.querySelector('.btn-text').style.display = 'inline';
        submitBtn.querySelector('.btn-loader').style.display = 'none';
        submitBtn.disabled = false;
    });
}

function displayResults(data, container) {
    const template = document.getElementById('resultsTemplate').innerHTML;
    container.innerHTML = template;
    
    container.querySelector('.result-target').textContent = data.target;
    container.querySelector('.report-content').innerHTML = marked.parse(data.full_report_markdown || 'No report generated');
    
    container.querySelector('.score-financial').textContent = data.risk_breakdown.financial || '--';
    container.querySelector('.score-legal').textContent = data.risk_breakdown.legal || '--';
    container.querySelector('.score-reputational').textContent = data.risk_breakdown.reputational || '--';
    container.querySelector('.score-association').textContent = data.risk_breakdown.association || '--';
    container.querySelector('.score-integrity').textContent = data.risk_breakdown.integrity || '--';
    container.querySelector('.score-operational').textContent = data.risk_breakdown.operational || '--';
    
    container.querySelector('.count-sources').textContent = data.stats.sources || 0;
    container.querySelector('.count-people').textContent = data.stats.people || 0;
    container.querySelector('.count-orgs').textContent = data.stats.organizations || 0;
    container.querySelector('.count-events').textContent = data.stats.events || 0;
    
    // Store report_id for download
    const reportId = data.report_id;
    container.querySelector('.download-pdf').addEventListener('click', () => {
        if (reportId) {
            window.location.href = '/download_pdf/' + reportId;
        } else {
            alert('Report ID not found. Please regenerate the report.');
        }
    });
}
