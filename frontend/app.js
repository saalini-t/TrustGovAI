/**
 * ═══════════════════════════════════════════════════════════════
 * TrustGov AI - Frontend Application
 * ═══════════════════════════════════════════════════════════════
 */

// API Configuration
const API_BASE_URL = "http://localhost:8000";

// DOM Elements
const elements = {
  chatMessages: document.getElementById("chatMessages"),
  messageInput: document.getElementById("messageInput"),
  sendButton: document.getElementById("sendButton"),
  micButton: document.getElementById("micButton"),
  recordingIndicator: document.getElementById("recordingIndicator"),
  stopRecording: document.getElementById("stopRecording"),
  welcomeContainer: document.getElementById("welcomeContainer"),
  languageBadge: document.getElementById("languageBadge"),
  detectedLanguage: document.getElementById("detectedLanguage"),
  sourcesPanel: document.getElementById("sourcesPanel"),
  closePanel: document.getElementById("closePanel"),
  confidenceBar: document.getElementById("confidenceBar"),
  confidenceValue: document.getElementById("confidenceValue"),
  verificationBadge: document.getElementById("verificationBadge"),
  sourcesList: document.getElementById("sourcesList"),
  contextPreview: document.getElementById("contextPreview"),
  menuToggle: document.getElementById("menuToggle"),
  sidebar: document.querySelector(".sidebar"),
  toast: document.getElementById("toast"),
  toastMessage: document.getElementById("toastMessage"),
};

// State
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];
let currentResponse = null;
let isServerOnline = false;
let currentAudio = null; // For TTS playback
let isSpeaking = false;

// Language display mapping
const languageNames = {
  en: "English",
  hi: "हिंदी (Hindi)",
  ta: "தமிழ் (Tamil)",
  te: "తెలుగు (Telugu)",
  mr: "मराठी (Marathi)",
  bn: "বাংলা (Bengali)",
  gu: "ગુજરાતી (Gujarati)",
  kn: "ಕನ್ನಡ (Kannada)",
  ml: "മലയാളം (Malayalam)",
  pa: "ਪੰਜਾਬੀ (Punjabi)",
  tl: "Tanglish/Mixed",
  id: "Mixed Language",
};

// ═══════════════════════════════════════════════════════════════
// Initialization
// ═══════════════════════════════════════════════════════════════

document.addEventListener("DOMContentLoaded", () => {
  initializeEventListeners();
  autoResizeTextarea();
  checkServerStatus();
  // Check server status every 10 seconds
  setInterval(checkServerStatus, 10000);
});

async function checkServerStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: "GET",
      timeout: 3000,
    });
    if (response.ok) {
      isServerOnline = true;
      updateServerStatus(true);
    } else {
      throw new Error("Server error");
    }
  } catch (error) {
    isServerOnline = false;
    updateServerStatus(false);
  }
}

function updateServerStatus(online) {
  const statusDot = document.querySelector(".status-dot");
  const statusText = document.querySelector(
    ".status-indicator span:last-child"
  );

  if (statusDot && statusText) {
    if (online) {
      statusDot.classList.add("online");
      statusText.textContent = "System Online";
    } else {
      statusDot.classList.remove("online");
      statusText.textContent = "Server Offline";
    }
  }
}

function initializeEventListeners() {
  // Send message
  elements.sendButton.addEventListener("click", sendMessage);
  elements.messageInput.addEventListener("keydown", handleKeyDown);

  // Voice recording
  elements.micButton.addEventListener("click", toggleRecording);
  elements.stopRecording.addEventListener("click", stopRecordingAudio);

  // Quick prompts
  document.querySelectorAll(".quick-prompt").forEach((btn) => {
    btn.addEventListener("click", () => {
      const prompt = btn.dataset.prompt;
      elements.messageInput.value = prompt;
      sendMessage();
    });
  });

  // Scheme tags
  document.querySelectorAll(".scheme-tag").forEach((tag) => {
    tag.addEventListener("click", () => {
      const scheme = tag.dataset.scheme;
      elements.messageInput.value = `Tell me about ${scheme}`;
      sendMessage();
    });
  });

  // Panel controls
  elements.closePanel.addEventListener("click", () => {
    elements.sourcesPanel.classList.add("hidden");
  });

  // Mobile menu toggle
  elements.menuToggle.addEventListener("click", () => {
    elements.sidebar.classList.toggle("open");
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener("click", (e) => {
    if (window.innerWidth <= 768) {
      if (
        !elements.sidebar.contains(e.target) &&
        !elements.menuToggle.contains(e.target)
      ) {
        elements.sidebar.classList.remove("open");
      }
    }
  });
}

function autoResizeTextarea() {
  elements.messageInput.addEventListener("input", () => {
    elements.messageInput.style.height = "auto";
    elements.messageInput.style.height =
      Math.min(elements.messageInput.scrollHeight, 150) + "px";
  });
}

// ═══════════════════════════════════════════════════════════════
// Chat Functions
// ═══════════════════════════════════════════════════════════════

function handleKeyDown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

async function sendMessage() {
  const message = elements.messageInput.value.trim();
  if (!message) return;

  // Check server status first
  if (!isServerOnline) {
    showToast("Server is offline. Please start the backend server.", "error");
    addMessage(
      "⚠️ Cannot connect to server. Please make sure the backend is running:\n\n1. Open terminal\n2. Run: cd TrustGovAI && source .venv/bin/activate\n3. Run: FAST_MODE=true uvicorn app.main:app --port 8000",
      "assistant",
      { verified: false, confidence_score: 0 }
    );
    return;
  }

  // Hide welcome screen
  hideWelcome();

  // Add user message
  addMessage(message, "user");

  // Clear input
  elements.messageInput.value = "";
  elements.messageInput.style.height = "auto";

  // Show typing indicator
  const typingId = showTypingIndicator();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();
    currentResponse = data;

    // Remove typing indicator
    removeTypingIndicator(typingId);

    // Add assistant message
    addMessage(data.answer, "assistant", data);

    // Update UI elements
    updateLanguageDisplay(data.language);
    updateSourcesPanel(data);
  } catch (error) {
    console.error("Error:", error);
    removeTypingIndicator(typingId);

    let errorMessage = "❌ ";
    if (error.name === "AbortError") {
      errorMessage +=
        "Request timed out. The server is taking too long to respond.";
    } else if (
      error.message.includes("Failed to fetch") ||
      error.message.includes("NetworkError")
    ) {
      errorMessage +=
        "Cannot connect to server. Please check if the backend is running on port 8000.";
      isServerOnline = false;
      updateServerStatus(false);
    } else {
      errorMessage += `Error: ${error.message}`;
    }

    addMessage(errorMessage, "assistant", {
      verified: false,
      confidence_score: 0,
    });
    showToast("Failed to get response", "error");
  }
}

function hideWelcome() {
  if (elements.welcomeContainer) {
    elements.welcomeContainer.style.display = "none";
  }
}

function addMessage(content, type, data = null) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}`;
  const messageId = "msg-" + Date.now();
  messageDiv.id = messageId;

  const time = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  let metaHTML = "";
  if (type === "assistant" && data) {
    const verifiedClass = data.verified ? "verified" : "unverified";
    const verifiedIcon = data.verified
      ? "fa-circle-check"
      : "fa-triangle-exclamation";
    const verifiedText = data.verified ? "Verified" : "Needs Review";
    const lang = data.language || "en";

    metaHTML = `
      <div class="message-meta">
        <span class="message-time">${time}</span>
        <span class="message-verification ${verifiedClass}">
          <i class="fas ${verifiedIcon}"></i> ${verifiedText}
        </span>
        <button class="speak-btn" onclick="speakText('${messageId}', '${lang}')" title="Listen to response">
          <i class="fas fa-volume-up"></i>
        </button>
        <button class="view-sources-btn" onclick="showSourcesPanel()">
          <i class="fas fa-book-open"></i> Sources
        </button>
      </div>
    `;
  } else {
    metaHTML = `
      <div class="message-meta">
        <span class="message-time">${time}</span>
      </div>
    `;
  }

  messageDiv.innerHTML = `
    <div class="message-avatar">
      <i class="fas ${type === "user" ? "fa-user" : "fa-robot"}"></i>
    </div>
    <div class="message-content">
      <div class="message-bubble" data-text="${encodeURIComponent(content)}">${formatMessage(content)}</div>
      ${metaHTML}
    </div>
  `;

  elements.chatMessages.appendChild(messageDiv);
  scrollToBottom();
}

function formatMessage(content) {
  // Basic markdown-like formatting
  return content
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br>");
}

function showTypingIndicator() {
  const id = "typing-" + Date.now();
  const typingDiv = document.createElement("div");
  typingDiv.className = "message assistant";
  typingDiv.id = id;
  typingDiv.innerHTML = `
    <div class="message-avatar"><i class="fas fa-robot"></i></div>
    <div class="message-content">
      <div class="typing-indicator"><span></span><span></span><span></span></div>
    </div>
  `;
  elements.chatMessages.appendChild(typingDiv);
  scrollToBottom();
  return id;
}

function removeTypingIndicator(id) {
  const typingEl = document.getElementById(id);
  if (typingEl) typingEl.remove();
}

function scrollToBottom() {
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

// ═══════════════════════════════════════════════════════════════
// Text-to-Speech Functions
// ═══════════════════════════════════════════════════════════════

async function speakText(messageId, language) {
  const messageEl = document.getElementById(messageId);
  if (!messageEl) return;

  const bubble = messageEl.querySelector(".message-bubble");
  const text = decodeURIComponent(bubble.dataset.text);
  const speakBtn = messageEl.querySelector(".speak-btn");

  // If already speaking, stop
  if (isSpeaking && currentAudio) {
    stopSpeaking();
    return;
  }

  try {
    // Update button to show loading
    speakBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    speakBtn.classList.add("loading");
    showToast("🔊 Generating audio...", "info");

    // Call backend TTS API
    const response = await fetch(`${API_BASE_URL}/tts/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, language }),
    });

    if (!response.ok) throw new Error("TTS request failed");

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);

    // Play audio
    currentAudio = new Audio(audioUrl);
    isSpeaking = true;

    // Update button to show playing
    speakBtn.innerHTML = '<i class="fas fa-stop"></i>';
    speakBtn.classList.remove("loading");
    speakBtn.classList.add("playing");

    currentAudio.play();
    showToast("🔊 Playing audio...", "success");

    currentAudio.onended = () => {
      stopSpeaking();
      speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
      speakBtn.classList.remove("playing");
    };

    currentAudio.onerror = () => {
      stopSpeaking();
      speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
      speakBtn.classList.remove("playing");
      showToast("Audio playback error", "error");
    };

  } catch (error) {
    console.error("TTS error:", error);
    speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
    speakBtn.classList.remove("loading");
    showToast("Failed to generate audio. Trying browser TTS...", "error");
    
    // Fallback to browser TTS
    speakWithBrowserTTS(text, language);
  }
}

function stopSpeaking() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
  }
  isSpeaking = false;
  
  // Reset all speak buttons
  document.querySelectorAll(".speak-btn.playing").forEach(btn => {
    btn.innerHTML = '<i class="fas fa-volume-up"></i>';
    btn.classList.remove("playing");
  });
}

function speakWithBrowserTTS(text, language) {
  // Fallback to browser's Web Speech API
  if (!("speechSynthesis" in window)) {
    showToast("Text-to-speech not supported in this browser", "error");
    return;
  }

  // Stop any ongoing speech
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  
  // Map language codes to browser TTS voices
  const langMap = {
    en: "en-US",
    hi: "hi-IN",
    ta: "ta-IN",
    te: "te-IN",
    kn: "kn-IN",
    ml: "ml-IN",
    bn: "bn-IN",
    mr: "mr-IN",
    gu: "gu-IN",
    pa: "pa-IN",
  };

  utterance.lang = langMap[language] || "en-US";
  utterance.rate = 0.9;
  utterance.pitch = 1;

  utterance.onstart = () => {
    isSpeaking = true;
    showToast("🔊 Speaking...", "success");
  };

  utterance.onend = () => {
    isSpeaking = false;
  };

  utterance.onerror = (e) => {
    isSpeaking = false;
    showToast("Speech error: " + e.error, "error");
  };

  window.speechSynthesis.speak(utterance);
}

// ═══════════════════════════════════════════════════════════════
// Voice Recording Functions
// ═══════════════════════════════════════════════════════════════

async function toggleRecording() {
  if (isRecording) {
    stopRecordingAudio();
  } else {
    startRecording();
  }
}

async function startRecording() {
  if (!isServerOnline) {
    showToast("Server is offline. Cannot process voice.", "error");
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (e) => {
      audioChunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      await sendVoiceMessage(audioBlob);

      // Stop all tracks
      stream.getTracks().forEach((track) => track.stop());
    };

    mediaRecorder.start();
    isRecording = true;

    // Update UI
    elements.micButton.classList.add("recording");
    elements.recordingIndicator.classList.add("active");
    showToast("🎤 Recording started...", "success");
  } catch (error) {
    console.error("Microphone error:", error);
    showToast(
      "Could not access microphone. Please allow microphone permissions.",
      "error"
    );
  }
}

function stopRecordingAudio() {
  if (mediaRecorder && isRecording) {
    mediaRecorder.stop();
    isRecording = false;

    // Update UI
    elements.micButton.classList.remove("recording");
    elements.recordingIndicator.classList.remove("active");
    showToast("Processing voice...", "info");
  }
}

async function sendVoiceMessage(audioBlob) {
  hideWelcome();

  // Show typing indicator
  const typingId = showTypingIndicator();

  try {
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.wav");

    const response = await fetch(`${API_BASE_URL}/voice/`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Voice API request failed");

    const data = await response.json();
    currentResponse = data;

    removeTypingIndicator(typingId);

    if (data.transcribed_text) {
      addMessage(data.transcribed_text, "user");
    }

    addMessage(data.answer, "assistant", {
      verified: data.verified,
      confidence_score: data.confidence,
      language: data.language,
    });

    updateLanguageDisplay(data.language);
    updateSourcesPanel({
      ...data,
      confidence_score: data.confidence,
    });

    showToast("✅ Voice processed successfully", "success");
  } catch (error) {
    console.error("Voice error:", error);
    removeTypingIndicator(typingId);
    addMessage(
      "❌ Could not process voice message. Please try again or type your question.",
      "assistant",
      { verified: false, confidence_score: 0 }
    );
    showToast("Voice processing failed", "error");
  }
}

// ═══════════════════════════════════════════════════════════════
// UI Update Functions
// ═══════════════════════════════════════════════════════════════

function updateLanguageDisplay(langCode) {
  const langName = languageNames[langCode] || langCode.toUpperCase();
  elements.detectedLanguage.textContent = langName;
  elements.languageBadge.classList.add("pulse");
  setTimeout(() => elements.languageBadge.classList.remove("pulse"), 500);
}

function updateSourcesPanel(data) {
  const confidence = Math.round((data.confidence_score || 0) * 100);
  elements.confidenceBar.style.width = confidence + "%";
  elements.confidenceValue.textContent = confidence + "%";

  elements.verificationBadge.className = "verification-badge " + (data.verified ? "verified" : "unverified");
  elements.verificationBadge.innerHTML = data.verified
    ? '<i class="fas fa-circle-check"></i> Verified'
    : '<i class="fas fa-triangle-exclamation"></i> Needs Review';

  if (data.sources && data.sources.length > 0) {
    elements.sourcesList.innerHTML = data.sources
      .map((source) => {
        // Handle different source formats
        let sourceName = "";
        if (typeof source === "string") {
          sourceName = source;
        } else if (source && source.source) {
          sourceName = source.source;
        } else if (source && source.doc_index !== undefined) {
          sourceName = `Document ${source.doc_index + 1}`;
        } else {
          sourceName = "Unknown Source";
        }
        
        return `
          <div class="source-item">
            <div class="source-icon"><i class="fas fa-file-lines"></i></div>
            <div class="source-info">
              <div class="source-name">${formatSourceName(sourceName)}</div>
              <div class="source-type">Government Document</div>
            </div>
          </div>
        `;
      })
      .join("");
  } else {
    elements.sourcesList.innerHTML = '<p class="no-sources">No specific sources referenced.</p>';
  }

  // Update context preview
  if (data.source) {
    elements.contextPreview.innerHTML = `<p>${data.source.substring(0, 500)}${
      data.source.length > 500 ? "..." : ""
    }</p>`;
  } else {
    elements.contextPreview.innerHTML =
      '<p class="no-context">No context available.</p>';
  }

  // Show panel on desktop
  if (window.innerWidth > 1200) {
    elements.sourcesPanel.classList.remove("hidden");
  }
}

function formatSourceName(source) {
  // Extract filename and make it readable
  const filename = source.split("/").pop().replace(".txt", "");
  return filename
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function showSourcesPanel() {
  elements.sourcesPanel.classList.remove("hidden");
}

// ═══════════════════════════════════════════════════════════════
// Toast Notifications
// ═══════════════════════════════════════════════════════════════

function showToast(message, type = "info") {
  elements.toastMessage.textContent = message;
  elements.toast.className = "toast " + type;
  elements.toast.classList.add("show");

  setTimeout(() => {
    elements.toast.classList.remove("show");
  }, 3000);
}

// ═══════════════════════════════════════════════════════════════
// Global Functions (for onclick handlers)
// ═══════════════════════════════════════════════════════════════

window.showSourcesPanel = showSourcesPanel;
window.speakText = speakText;
window.stopSpeaking = stopSpeaking;

