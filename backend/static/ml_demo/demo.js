function getCodeText(targetId) {
  const el = targetId ? document.getElementById(targetId) : null;
  if (!el) return "";
  const code = el.querySelector("code");
  return (code || el).innerText || (code || el).textContent || "";
}

function flashButtonLabel(btn, temporaryLabel) {
  const label = btn.textContent;
  btn.textContent = temporaryLabel;
  setTimeout(() => {
    btn.textContent = label;
  }, 1500);
}

document.querySelectorAll("[data-copy-target]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const id = btn.getAttribute("data-copy-target");
    const text = getCodeText(id);
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      flashButtonLabel(btn, "Copied");
    });
  });
});

function openCodeFullScreen(btn) {
  const tab = btn.getAttribute("data-ml-tab") || "model1";
  const file = btn.getAttribute("data-code-file") || "1";
  const url = `/ml-demo/code-file?tab=${encodeURIComponent(tab)}&file=${encodeURIComponent(file)}`;
  const popup = window.open(url, "_blank", "noopener,noreferrer");
  if (!popup) {
    window.location.assign(url);
  }
}

document.querySelectorAll("[data-open-code-full]").forEach((btn) => {
  btn.addEventListener("click", (event) => {
    event.preventDefault();
    openCodeFullScreen(btn);
  });
});
