const statusBox = document.getElementById("status");

function setStatus(message) {
    statusBox.innerText = message;
}

async function getActiveTab() {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

async function saveJobsLocally(newJobs) {
    chrome.storage.local.get(["savedJobs"], function(result) {
        let existingJobs = result.savedJobs || [];

        const existingLinks = new Set(existingJobs.map(job => job.link));
        const filteredNew = newJobs.filter(job => !existingLinks.has(job.link));

        const merged = existingJobs.concat(filteredNew);

        chrome.storage.local.set({ savedJobs: merged }, function() {
            setStatus(`${filteredNew.length} new jobs saved. Total: ${merged.length}`);
        });
    });
}

/* =========================
   COLLECT VISIBLE JOBS
========================= */
document.getElementById("collectVisible").addEventListener("click", async () => {
    const tab = await getActiveTab();

    setStatus("Collecting jobs...");

    chrome.tabs.sendMessage(
        tab.id,
        { action: "collect_jobs" },   // FIXED HERE
        function(response) {

            if (chrome.runtime.lastError) {
                setStatus("❌ Content script not running. Refresh page.");
                return;
            }

            if (!response) {
                setStatus("❌ No response from page.");
                return;
            }

            if (response.jobs && response.jobs.length > 0) {
                saveJobsLocally(response.jobs);
            } else {
                setStatus("⚠️ No jobs detected on this page.");
            }
        }
    );
});

/* =========================
   COLLECT SINGLE JOB (SAFE FALLBACK)
========================= */
document.getElementById("collectSingle").addEventListener("click", async () => {
    const tab = await getActiveTab();

    setStatus("Collecting single job...");

    chrome.tabs.sendMessage(
        tab.id,
        { action: "collect_current_job" },
        function(response) {

            if (chrome.runtime.lastError) {
                setStatus("❌ Content script not running. Refresh page.");
                return;
            }

            if (response && response.job) {
                saveJobsLocally([response.job]);
            } else {
                setStatus("⚠️ No job details found on this page.");
            }
        }
    );
});

/* =========================
   SYNC TO BACKEND
========================= */
document.getElementById("syncBackend").addEventListener("click", () => {

    setStatus("Syncing to backend...");

    chrome.storage.local.get(["savedJobs"], async function(result) {
        const jobs = result.savedJobs || [];

        if (jobs.length === 0) {
            setStatus("No jobs stored to send.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/save-jobs", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(jobs.map(job => ({
                    source: job.source || "unknown",
                    title: job.title || "",
                    company: job.company || "",
                    location: job.location || "",
                    posted: job.posted || "",
                    salary: job.salary || "",
                    link: job.link || "",
                    description: job.description || "",
                    easy_apply: Boolean(job.easy_apply),
                    scraped_at: job.scraped_at || new Date().toISOString(),
                    market_priority: job.market_priority || 50
                })))
            });

            const data = await response.json();

            if (data.status === "success") {
                setStatus(`✅ Synced ${jobs.length} jobs to backend.`);
                chrome.storage.local.set({ savedJobs: [] });
            } else {
                setStatus("❌ Backend rejected data.");
            }

        } catch (error) {
            setStatus("❌ Backend offline or unreachable.");
        }
    });
});