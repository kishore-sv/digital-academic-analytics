function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const PY_STRING_RE =
  /("""[\s\S]*?"""|'''[\s\S]*?'''|"[^"\\]*(?:\\.[^"\\]*)*"|'[^'\\]*(?:\\.[^'\\]*)*')/g;

const PY_KEYWORDS =
  /\b(and|as|assert|break|class|continue|def|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|not|or|pass|raise|return|True|try|while|with|yield)\b/g;

const JSON_STRING_RE = /"([^"\\]|\\.)*"/g;

function createPlaceholderStore() {
  const tokens = [];
  return {
    stash(html) {
      const id = tokens.length;
      tokens.push(html);
      return `\uE000${id}\uE001`;
    },
    restore(text) {
      let s = text;
      for (let i = 0; i < tokens.length; i += 1) {
        s = s.replace(`\uE000${i}\uE001`, tokens[i]);
      }
      return s;
    },
  };
}

function highlightPython(text) {
  const ph = createPlaceholderStore();
  let s = escapeHtml(text);

  s = s.replace(PY_STRING_RE, (m) => ph.stash(`<span class="hl-str">${m}</span>`));

  s = s.replace(/(^|[\n])(\s*#[^\n]*)/g, (_, lead, comment) => {
    return `${lead}${ph.stash(`<span class="hl-cmt">${comment}</span>`)}`;
  });

  s = s.replace(PY_KEYWORDS, '<span class="hl-kw">$&</span>');
  s = s.replace(/\b(\d+\.?\d*)\b/g, '<span class="hl-num">$1</span>');

  return ph.restore(s);
}

function highlightJson(text) {
  const ph = createPlaceholderStore();
  let s = escapeHtml(text);

  s = s.replace(/"([^"\\]|\\.)*"(?=\s*:)/g, (m) => ph.stash(`<span class="hl-key">${m}</span>`));
  s = s.replace(JSON_STRING_RE, (m) => ph.stash(`<span class="hl-str">${m}</span>`));

  s = s.replace(/\b(true|false|null)\b/g, '<span class="hl-kw">$1</span>');
  s = s.replace(/\b(-?\d+\.?\d*)\b/g, '<span class="hl-num">$1</span>');

  return ph.restore(s);
}

function applyCodeHighlight() {
  document.querySelectorAll("pre code[data-lang]:not([data-highlighted])").forEach((block) => {
    const lang = block.getAttribute("data-lang");
    const source = block.textContent || "";
    block.innerHTML = lang === "json" ? highlightJson(source) : highlightPython(source);
    block.setAttribute("data-highlighted", "true");
  });
}

applyCodeHighlight();
