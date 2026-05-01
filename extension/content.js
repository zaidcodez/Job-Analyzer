function extractExperience(text) {
    const match = text.match(/(\d+\+?\s*(years|yrs))/i);
    return match ? match[0] : "Not specified";
}

function detectSource() {
    const host = window.location.hostname;

    if (host.includes("rozee.pk")) return "rozee";
    if (host.includes("indeed.com")) return "indeed";
    if (host.includes("mustakbil.com")) return "mustakbil";

    return "generic";
}

function scrapeJobs() {
    const source = detectSource();
    const jobs = [];

    let selectors = [];

    // STRICT SELECTORS ONLY (THIS FIXES YOUR PROBLEM)
    if (source === "indeed") {
        selectors = ["li.css-5lfssm", "li"];
    } 
    else if (source === "rozee") {
        selectors = ["div.job-box", "div.job", "li.job", "article"];
    } 
    else {
        selectors = ["article", "li.job", "div.job"];
    }

    selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {

            const text = el.innerText?.trim();
            if (!text || text.length < 80) return;

            const link = el.querySelector("a")?.href || "";

            // SKIP LOGIN / NAV / JUNK PAGES (CRITICAL FIX)
            if (
                text.toLowerCase().includes("login") ||
                text.toLowerCase().includes("sign in") ||
                text.toLowerCase().includes("register") ||
                text.toLowerCase().includes("forgot password")
            ) return;

            if (!link) return;

            jobs.push({
                source: source,
                title: text.split("\n")[0],
                company: "not extracted",
                location: "not extracted",
                experience: "not extracted",
                link: link,
                description: text,
                scraped_at: new Date().toISOString()
            });
        });
    });

    return jobs.slice(0, 30);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    if (request.action === "collect_jobs") {
        const jobs = scrapeJobs();
        sendResponse({ jobs });
    }

    return true;
});