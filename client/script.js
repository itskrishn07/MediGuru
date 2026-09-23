// MediGuru Vanilla JS Client - Binds directly to index.html UI
const API_BASE = (window.ENV && window.ENV.API_BASE_URL && window.ENV.API_BASE_URL !== "http://localhost:8000")
    ? window.ENV.API_BASE_URL
    : ((window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
        ? "http://localhost:8000"
        : "https://mediguru-backend.onrender.com");

let selectedFile = null;
let currentReportData = null;
let fileInputEl = null;

document.addEventListener("DOMContentLoaded", () => {
    initUploadSystem();
    bindAnalyzeButton();
    bindChatInterface();
    checkBackendHealth();
    initSessionClearControls();
});

// Automatic Session Cleanup on Page Refresh or Tab Close
window.addEventListener("beforeunload", () => {
    if (navigator.sendBeacon) {
        navigator.sendBeacon(`${API_BASE}/clear-session`);
    }
});

// 1. Backend Connectivity Check
async function checkBackendHealth() {
    const statusEl = document.getElementById("backend-status");
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            console.log("MediGuru FastAPI Backend Connected.");
            if (statusEl) {
                statusEl.className = "flex items-center gap-xs px-sm py-xs rounded-full bg-emerald-50 text-emerald-600 border border-emerald-200 text-label-sm font-semibold";
                statusEl.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span><span>Backend Online</span>`;
            }
        } else {
            setOfflineStatus(statusEl);
        }
    } catch (err) {
        setOfflineStatus(statusEl);
    }
}

function setOfflineStatus(el) {
    if (!el) return;
    el.className = "flex items-center gap-xs px-sm py-xs rounded-full bg-amber-50 text-amber-600 border border-amber-200 text-label-sm font-semibold";
    el.innerHTML = `<span class="w-2 h-2 rounded-full bg-amber-500"></span><span>Backend Offline (:8000)</span>`;
}

// 2. File Upload & Drag & Drop Handling
function initUploadSystem() {
    const uploadDashed = document.querySelector(".upload-dashed");
    fileInputEl = document.getElementById("file-input");

    // Ensure hidden file input exists
    if (!fileInputEl) {
        fileInputEl = document.createElement("input");
        fileInputEl.id = "file-input";
        fileInputEl.type = "file";
        fileInputEl.accept = ".pdf,.jpg,.jpeg,.png";
        fileInputEl.style.display = "none";
        document.body.appendChild(fileInputEl);
    }

    if (uploadDashed) {
        // Trigger file input click safely without preventing default browser action
        uploadDashed.addEventListener("click", (e) => {
            if (e.target !== fileInputEl) {
                fileInputEl.click();
            }
        });

        // Drag & drop listeners
        uploadDashed.addEventListener("dragover", (e) => {
            e.preventDefault();
            uploadDashed.style.borderColor = "#2563eb";
            uploadDashed.style.backgroundColor = "#eff4ff";
        });

        uploadDashed.addEventListener("dragleave", (e) => {
            e.preventDefault();
            uploadDashed.style.borderColor = "";
            uploadDashed.style.backgroundColor = "";
        });

        uploadDashed.addEventListener("drop", (e) => {
            e.preventDefault();
            uploadDashed.style.borderColor = "";
            uploadDashed.style.backgroundColor = "";

            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                handleFileSelection(e.dataTransfer.files[0]);
            }
        });
    }

    // Direct change event on file input
    fileInputEl.addEventListener("change", (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

function handleFileSelection(file) {
    selectedFile = file;
    const dragParagraph = document.querySelector(".upload-dashed p.text-body-lg");
    const subtextParagraph = document.querySelector(".upload-dashed p.text-body-sm");
    
    if (dragParagraph) {
        dragParagraph.textContent = `📄 ${file.name}`;
        dragParagraph.className = "text-body-lg font-body-lg font-bold text-primary";
    }
    if (subtextParagraph) {
        subtextParagraph.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB • Ready to analyze`;
        subtextParagraph.className = "text-body-sm font-body-sm text-emerald-600 font-semibold mt-xs";
    }

    updateTimelineSteps(1); // Step 1: Upload Complete
}

// 3. Bind Analyze Button Action
function bindAnalyzeButton() {
    const uploadCard = document.querySelector(".upload-dashed")?.closest(".bg-surface-container-lowest");
    if (!uploadCard) return;

    const analyzeBtn = Array.from(uploadCard.querySelectorAll("button")).find(b => b.textContent.includes("Analyze Document"));
    if (!analyzeBtn) return;

    analyzeBtn.addEventListener("click", (e) => {
        e.preventDefault();
        if (!selectedFile) {
            if (fileInputEl) fileInputEl.click();
            return;
        }
        processDocumentUpload(selectedFile, analyzeBtn);
    });
}

async function processDocumentUpload(file, analyzeBtn) {
    const originalText = analyzeBtn.innerHTML;
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `<span class="material-symbols-outlined text-[20px] animate-spin">sync</span> Analyzing...`;

    updateTimelineSteps(2); // Step 2: Extracting Text

    const formData = new FormData();
    formData.append("file", file);

    try {
        setTimeout(() => updateTimelineSteps(3), 600); // Step 3: Running Vision / AI

        const response = await fetch(`${API_BASE}/process`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Analysis request failed");
        }

        const data = await response.json();
        currentReportData = data;

        updateTimelineSteps(4); // Step 4: AI Understanding Complete

        renderSummaryCardResults(data);

    } catch (error) {
        alert(`Analysis Error: ${error.message}`);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = originalText;
    }
}

// 4. Update Timeline Steps Dynamically
function updateTimelineSteps(activeStepNum) {
    const timelineContainer = document.querySelector(".upload-dashed")?.closest(".lg\\:col-span-5")?.querySelectorAll(".bg-surface-container-lowest")[1];
    if (!timelineContainer) return;

    const stepItems = timelineContainer.querySelectorAll(".flex.items-start.gap-md");
    
    stepItems.forEach((item, index) => {
        const stepNum = index + 1;
        const iconContainer = item.querySelector("div");
        const titleText = item.querySelector("p.text-body-md");

        if (stepNum < activeStepNum) {
            // Completed
            if (iconContainer) {
                iconContainer.className = "w-6 h-6 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center mt-1 shrink-0";
                iconContainer.innerHTML = `<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">check</span>`;
            }
            if (titleText) titleText.className = "text-body-md font-body-md font-medium text-on-surface";
        } else if (stepNum === activeStepNum) {
            // Active Pulse
            if (iconContainer) {
                iconContainer.className = "w-6 h-6 rounded-full bg-surface-container-lowest border-2 border-secondary-container pulse-cyan flex items-center justify-center mt-1 shrink-0";
                iconContainer.innerHTML = `<div class="w-2 h-2 rounded-full bg-secondary-container"></div>`;
            }
            if (titleText) titleText.className = "text-body-md font-body-md font-bold text-primary";
        } else {
            // Pending
            if (iconContainer) {
                iconContainer.className = "w-6 h-6 rounded-full bg-surface-container-lowest border-2 border-outline-variant flex items-center justify-center mt-1 shrink-0";
                iconContainer.innerHTML = `<span class="material-symbols-outlined text-[14px] text-outline-variant">hourglass_empty</span>`;
            }
            if (titleText) titleText.className = "text-body-md font-body-md text-outline";
        }
    });
}

// 5. Render Results in Summary Card
function renderSummaryCardResults(data) {
    const summaryCard = document.querySelector(".bg-surface-container-lowest.border-primary-fixed");
    if (!summaryCard) return;

    const ext = data.extracted_data || {};
    const isMedical = ext.is_medical_document !== false;

    // Update Draft Badge
    const badge = summaryCard.querySelector("span.bg-surface-container, span.bg-emerald-50, span.bg-amber-50");
    if (badge) {
        if (isMedical) {
            badge.className = "bg-emerald-50 text-emerald-600 px-sm py-xs rounded-full text-label-sm font-label-sm font-semibold border border-emerald-200";
            badge.textContent = "Processed";
        } else {
            badge.className = "bg-amber-50 text-amber-700 px-sm py-xs rounded-full text-label-sm font-label-sm font-semibold border border-amber-200";
            badge.textContent = "Invalid Document";
        }
    }

    // Replace empty state with results content
    const emptyState = summaryCard.querySelector(".flex-grow.flex.flex-col");
    if (emptyState) {
        if (!isMedical) {
            emptyState.className = "flex-grow flex flex-col gap-md p-md text-left overflow-y-auto";
            emptyState.innerHTML = `
                <div class="bg-amber-50 border border-amber-200 text-amber-900 p-md rounded-xl flex items-start gap-md shadow-sm">
                    <span class="material-symbols-outlined text-amber-600 text-[28px] shrink-0 mt-0.5">warning</span>
                    <div>
                        <h5 class="text-body-lg font-bold text-amber-900 mb-xs">Non-Medical Document Detected</h5>
                        <p class="text-body-md text-amber-800 leading-relaxed">${escapeHtml(data.summary)}</p>
                    </div>
                </div>
                <div class="p-md bg-surface-bright border border-outline-variant rounded-xl text-center text-on-surface-variant text-body-sm">
                    <p>MediGuru only processes clinical documents (prescriptions, lab reports, discharge summaries, etc.).</p>
                    <p class="mt-xs text-primary font-semibold">Please upload a valid medical report or prescription image.</p>
                </div>
            `;
            return;
        }

        const summaryText = data.summary || "Medical summary extracted successfully.";
        let medicinesHtml = "";
        if (ext.medicines && ext.medicines.length > 0) {
            medicinesHtml = ext.medicines.map(m => `
                <tr class="border-b border-surface-container-highest">
                    <td class="p-sm font-medium text-on-surface">${escapeHtml(m.medicine_name || '-')}</td>
                    <td class="p-sm text-on-surface-variant">${escapeHtml(m.strength || '-')}</td>
                    <td class="p-sm text-on-surface-variant">${escapeHtml(m.dosage || '-')}</td>
                    <td class="p-sm text-on-surface-variant">${escapeHtml(m.frequency || '-')}</td>
                    <td class="p-sm text-on-surface-variant">${escapeHtml(m.food_instruction || '-')}</td>
                </tr>
            `).join("");
        } else {
            medicinesHtml = `<tr><td colspan="5" class="p-md text-center text-outline">No prescription medicines detected.</td></tr>`;
        }

        emptyState.className = "flex-grow flex flex-col gap-md p-sm text-left overflow-y-auto";
        emptyState.innerHTML = `
            <div class="bg-surface-container-low p-md rounded-xl border border-surface-container-high text-body-md text-on-surface leading-relaxed flex flex-col gap-xs">
                ${formatStructuredSummary(summaryText)}
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-sm">
                <div class="bg-surface-bright p-sm rounded-lg border border-outline-variant">
                    <p class="text-label-sm text-outline uppercase tracking-wider mb-xs">Patient Name</p>
                    <p class="text-body-md font-semibold text-on-surface">${escapeHtml(ext.patient_name || "Not Specified")}</p>
                </div>
                <div class="bg-surface-bright p-sm rounded-lg border border-outline-variant">
                    <p class="text-label-sm text-outline uppercase tracking-wider mb-xs">Attending Doctor</p>
                    <p class="text-body-md font-semibold text-on-surface">${escapeHtml(ext.doctor_name || "Not Specified")}</p>
                </div>
            </div>

            <div class="bg-surface-bright p-sm rounded-lg border border-outline-variant">
                <p class="text-label-sm text-primary font-semibold mb-xs">Prescribed Medicines:</p>
                <div class="overflow-x-auto -mx-1 px-1">
                    <table class="w-full text-left text-body-sm min-w-[500px]">
                        <thead class="bg-surface-container text-on-surface font-semibold">
                            <tr>
                                <th class="p-sm">Medicine</th>
                                <th class="p-sm">Strength</th>
                                <th class="p-sm">Dosage</th>
                                <th class="p-sm">Frequency</th>
                                <th class="p-sm">Food Instruction</th>
                            </tr>
                        </thead>
                        <tbody>${medicinesHtml}</tbody>
                    </table>
                </div>
            </div>

            <div class="bg-surface-bright p-sm rounded-lg border border-outline-variant">
                <p class="text-label-sm text-primary font-semibold mb-xs">Diagnosis / Condition:</p>
                <p class="text-body-sm text-on-surface">${escapeHtml(ext.diagnosis || "No specific diagnosis detected.")}</p>
            </div>
        `;
    }
}

// Format raw LLM text into clean structured HTML blocks without raw asterisks
function formatStructuredSummary(rawText) {
    if (!rawText) return "";

    // 1. Remove raw markdown asterisks and convert bold text to strong elements
    let cleaned = rawText
        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-primary font-bold">$1</strong>')
        .replace(/\*(.*?)\*/g, '$1');

    // 2. Split into sentences or key-value section headers
    const sectionKeywords = [
        "Patient:", "Condition/Diagnoses:", "Condition & Diagnosis:", "Diagnosis:",
        "Lab Results:", "Key Lab Results:", "Active Prescriptions:", "Prescribed Medications:",
        "Follow-up Instructions:", "Follow-up Plan:"
    ];

    sectionKeywords.forEach(kw => {
        const regex = new RegExp(kw.replace("/", "\\/"), "g");
        cleaned = cleaned.replace(regex, `<br/><strong class="text-primary font-bold mt-xs inline-block">${kw}</strong> `);
    });

    // 3. Handle bullet points
    let lines = cleaned.split("<br/>");
    let formattedHtml = lines.map(line => {
        let trimmed = line.trim();
        if (!trimmed) return "";

        if (trimmed.startsWith("* ") || trimmed.startsWith("• ") || trimmed.startsWith("- ")) {
            let item = trimmed.substring(2).trim();
            return `<div class="flex items-start gap-xs pl-xs py-[1px]"><span class="text-primary font-bold">•</span><span>${item}</span></div>`;
        }

        trimmed = trimmed.replace(/\s\*\s/g, '<br/>• ');
        return `<div>${trimmed}</div>`;
    }).join("");

    return formattedHtml || cleaned;
}

// 6. Bind AI Chat Assistant & Suggestion Chips
function bindChatInterface() {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("btn-send-chat");
    const suggestionChips = document.querySelectorAll(".suggestion-chip");

    if (chatForm && chatInput) {
        chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            submitChat(chatInput);
        });
    }

    if (sendBtn && chatInput) {
        sendBtn.addEventListener("click", (e) => {
            e.preventDefault();
            submitChat(chatInput);
        });
    }

    if (suggestionChips && chatInput) {
        suggestionChips.forEach(chip => {
            chip.addEventListener("click", (e) => {
                e.preventDefault();
                chatInput.value = chip.textContent.trim();
                submitChat(chatInput);
            });
        });
    }
}

async function submitChat(inputEl) {
    const query = inputEl.value.trim();
    if (!query) return;

    inputEl.value = "";
    appendUserBubble(query);

    const loadingId = appendLoadingBubble();

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: query })
        });

        removeLoadingBubble(loadingId);

        if (!response.ok) {
            const errJson = await response.json().catch(() => ({}));
            throw new Error(errJson.detail || "Assistant request failed");
        }

        const data = await response.json();
        let formattedAnswer = formatStructuredSummary(data.answer || "No response received.");
        appendAssistantBubbleHtml(formattedAnswer);
    } catch (error) {
        removeLoadingBubble(loadingId);
        let msg = escapeHtml(error.message);
        if (msg.includes("429") || msg.includes("RESOURCE_EXHAUSTED") || msg.includes("Quota")) {
            msg = "Gemini API free tier rate limit reached. Please wait ~15-20 seconds before asking your next question.";
        }
        appendAssistantBubbleHtml(msg);
    }
}

function getChatMessagesArea() {
    return document.getElementById("chat-messages-list") || document.querySelector("#chat-scroll-area > div");
}

function appendUserBubble(text) {
    const area = getChatMessagesArea();
    if (!area) return;

    const msgDiv = document.createElement("div");
    msgDiv.className = "flex gap-sm justify-end";
    msgDiv.innerHTML = `
        <div class="bg-primary text-on-primary px-md py-sm rounded-lg rounded-tr-none max-w-[90%] sm:max-w-[85%] text-body-sm font-body-sm shadow-sm">
            ${escapeHtml(text)}
        </div>
    `;
    area.appendChild(msgDiv);
    scrollChatToBottom();
}

function appendAssistantBubbleHtml(htmlContent) {
    const area = getChatMessagesArea();
    if (!area) return;

    const msgDiv = document.createElement("div");
    msgDiv.className = "flex gap-sm";
    msgDiv.innerHTML = `
        <div class="w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center shrink-0 shadow-sm">
            <span class="material-symbols-outlined text-[18px]">smart_toy</span>
        </div>
        <div class="bg-surface-container-lowest border border-surface-container-high text-on-surface px-md py-sm rounded-2xl rounded-tl-xs max-w-[90%] sm:max-w-[85%] text-body-md shadow-sm space-y-xs">
            ${htmlContent}
        </div>
    `;
    area.appendChild(msgDiv);
    scrollChatToBottom();
}

function appendLoadingBubble() {
    const area = getChatMessagesArea();
    if (!area) return "";

    const id = "loading-" + Date.now();
    const msgDiv = document.createElement("div");
    msgDiv.id = id;
    msgDiv.className = "flex gap-sm";
    msgDiv.innerHTML = `
        <div class="w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center shrink-0 shadow-sm">
            <span class="material-symbols-outlined text-[18px] animate-spin">sync</span>
        </div>
        <div class="bg-surface-container-lowest border border-surface-container-high text-on-surface px-md py-sm rounded-2xl rounded-tl-xs max-w-[90%] sm:max-w-[85%] text-body-md shadow-sm">
            Searching document context...
        </div>
    `;
    area.appendChild(msgDiv);
    scrollChatToBottom();
    return id;
}

function removeLoadingBubble(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollChatToBottom() {
    const chatScrollBox = document.getElementById("chat-scroll-area") || document.querySelector(".overflow-y-auto");
    if (chatScrollBox) {
        setTimeout(() => {
            chatScrollBox.scrollTo({
                top: chatScrollBox.scrollHeight + 500,
                behavior: 'smooth'
            });
        }, 50);
    }
}

// 7. Manual & Automatic Session Clear Controls
function initSessionClearControls() {
    const btnClear = document.getElementById("btn-clear-session");
    if (!btnClear) return;

    btnClear.addEventListener("click", async () => {
        if (confirm("Are you sure you want to clear all uploaded data and chat session?")) {
            try {
                await fetch(`${API_BASE}/clear-session`, { method: "POST" });
            } catch (e) {}

            selectedFile = null;
            currentReportData = null;
            if (fileInputEl) fileInputEl.value = "";

            const dragParagraph = document.querySelector(".upload-dashed p.text-body-lg");
            const subtextParagraph = document.querySelector(".upload-dashed p.text-body-sm");
            if (dragParagraph) {
                dragParagraph.textContent = "Drag & Drop";
                dragParagraph.className = "text-body-lg font-body-lg font-medium text-on-surface";
            }
            if (subtextParagraph) {
                subtextParagraph.textContent = "PDF, JPG, PNG up to 10MB";
                subtextParagraph.className = "text-body-sm font-body-sm text-on-surface-variant mt-xs";
            }

            updateTimelineSteps(0);

            // Reset summary card
            const summaryCard = document.querySelector(".bg-surface-container-lowest.border-primary-fixed");
            if (summaryCard) {
                const badge = summaryCard.querySelector("span.bg-surface-container");
                if (badge) {
                    badge.className = "bg-surface-container px-sm py-xs rounded-full text-label-sm font-label-sm text-primary";
                    badge.textContent = "Draft";
                }
                const emptyState = summaryCard.querySelector(".flex-grow.flex.flex-col");
                if (emptyState) {
                    emptyState.className = "flex-grow flex flex-col justify-center items-center text-center p-6 sm:p-xl";
                    emptyState.innerHTML = `
                        <div class="w-16 h-16 sm:w-24 sm:h-24 rounded-full bg-surface-container-low flex items-center justify-center mb-md">
                            <span class="material-symbols-outlined text-[32px] sm:text-[48px] text-primary-fixed-dim">document_scanner</span>
                        </div>
                        <h4 class="text-body-lg font-body-lg font-medium text-on-surface mb-xs">No Document Analyzed Yet</h4>
                        <p class="text-body-sm font-body-sm text-on-surface-variant max-w-sm">
                            Upload a medical document to generate a patient-friendly summary, extract key entities, and ask questions.
                        </p>
                    `;
                }
            }

            // Reset Chat Messages
            const msgList = getChatMessagesArea();
            if (msgList) {
                msgList.innerHTML = `
                    <div class="flex gap-sm">
                        <div class="w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[18px]">smart_toy</span>
                        </div>
                        <div class="bg-surface-container-lowest border border-surface-container-high text-on-surface px-md py-sm rounded-2xl rounded-tl-xs max-w-[90%] sm:max-w-[85%] text-body-md shadow-sm">
                            Hello! Once you upload a document, I can help explain your diagnosis, summarize prescriptions, or answer any medical questions you have about the text.
                        </div>
                    </div>
                `;
            }
        }
    });
}

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}
