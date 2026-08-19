import React, { useState, useRef, useEffect, useCallback } from 'react';
import { sendMessage, exportDiagram, resetSession, getConfig } from './api.js';

/* ─── Small utilities ─── */

// Convert a base64 string into a Blob of a given MIME type. Used when the
// user exports a past revision: the image is already in memory as base64,
// so we don't need to round-trip through the backend.
function base64ToBlob(b64, mime) {
  const byteChars = atob(b64);
  const byteNumbers = new Array(byteChars.length);
  for (let i = 0; i < byteChars.length; i++) {
    byteNumbers[i] = byteChars.charCodeAt(i);
  }
  return new Blob([new Uint8Array(byteNumbers)], { type: mime });
}

// Trigger a browser download for a given Blob with the requested filename.
// Cleans up the object URL afterwards so we don't leak.
function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

/* ─── Zoom-and-pan image viewer with zoom % indicator ─── */

function ZoomImage({ src }) {
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [drag, setDrag] = useState(null);

  const onWheel = (e) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setZoom(z => Math.max(0.2, Math.min(5, z * delta)));
  };

  const onDown = (e) => setDrag({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  const onMove = (e) => {
    if (!drag) return;
    setPan({ x: e.clientX - drag.x, y: e.clientY - drag.y });
  };
  const onUp = () => setDrag(null);
  const reset = () => { setZoom(1); setPan({ x: 0, y: 0 }); };

  return (
    <div
      onWheel={onWheel}
      onMouseDown={onDown}
      onMouseMove={onMove}
      onMouseUp={onUp}
      onMouseLeave={onUp}
      style={{
        width: '100%', height: '100%', overflow: 'hidden',
        cursor: drag ? 'grabbing' : 'grab', position: 'relative',
        userSelect: 'none', minHeight: 200,
      }}
    >
      <img
        src={src}
        alt="diagram"
        draggable={false}
        style={{
          maxWidth: '100%', maxHeight: '100%', objectFit: 'contain',
          transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
          transformOrigin: 'center center',
          transition: drag ? 'none' : 'transform 0.1s',
          display: 'block', margin: 'auto',
        }}
      />
      <div style={{
        position: 'absolute', top: 8, right: 8, display: 'flex', gap: 4,
        alignItems: 'center',
        background: 'rgba(0,0,0,0.55)', padding: 4, borderRadius: 6,
      }}>
        <span style={{
          color: 'rgba(255,255,255,0.85)', fontSize: 11,
          fontFamily: "'JetBrains Mono', monospace",
          padding: '0 6px', minWidth: 38, textAlign: 'center',
        }}>{Math.round(zoom * 100)}%</span>
        <button onClick={() => setZoom(z => Math.min(5, z * 1.2))}
                title="Zoom in" style={zoomBtn}>+</button>
        <button onClick={() => setZoom(z => Math.max(0.2, z * 0.8))}
                title="Zoom out" style={zoomBtn}>−</button>
        <button onClick={reset} title="Reset zoom" style={zoomBtn}>⟲</button>
      </div>
    </div>
  );
}

const zoomBtn = {
  background: 'rgba(255,255,255,0.1)',
  color: 'white', border: '1px solid rgba(255,255,255,0.2)',
  borderRadius: 4, width: 26, height: 26,
  cursor: 'pointer', fontSize: 14,
  display: 'flex', alignItems: 'center', justifyContent: 'center',
};

/* ─── Style tokens ─── */

const palette = {
  bg: '#0d0f11',
  surface: '#161a1e',
  surfaceHover: '#1c2127',
  border: '#2a2f36',
  borderFocus: '#4f8eff',
  text: '#e2e5e9',
  textMuted: '#7a8290',
  textDim: '#4e5562',
  accent: '#4f8eff',
  accentSoft: 'rgba(79,142,255,0.12)',
  green: '#34d399',
  red: '#f87171',
  userBubble: '#1e293b',
  aiBubble: '#111418',
};

const font = {
  sans: "'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif",
  mono: "'JetBrains Mono', 'Fira Code', monospace",
};

/* ─── Chat bubble ─── */

function ChatBubble({ role, content, meta, isError, kind, onSuggestionClick }) {
  const isUser = role === 'user';
  const isDescription = kind === 'description';
  const isSuggestions = kind === 'suggestions';

  // Pick the label that goes on the top of an assistant bubble.
  let label = 'CDD';
  if (isError) label = 'Error';
  else if (isDescription) label = 'Description';
  else if (isSuggestions) label = 'Suggestions';

  // Tweak colors slightly for the description / suggestions bubbles so they
  // stand out from the regular "Diagram ready" bubble.
  const accentColor = isError
    ? palette.red
    : isDescription
      ? palette.green
      : isSuggestions
        ? '#a855f7'
        : palette.accent;

  return (
    <div style={{
      display: 'flex',
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: 12,
      animation: 'fadeSlide 0.25s ease-out',
    }}>
      <div style={{
        maxWidth: '85%',
        padding: '10px 14px',
        borderRadius: isUser ? '14px 14px 4px 14px' : '14px 14px 14px 4px',
        background: isError ? 'rgba(248,113,113,0.1)' : isUser ? palette.userBubble : palette.aiBubble,
        border: `1px solid ${isError ? palette.red : palette.border}`,
        color: isError ? palette.red : palette.text,
        fontSize: 14,
        lineHeight: 1.55,
        fontFamily: font.sans,
      }}>
        {!isUser && (
          <span style={{
            display: 'block',
            fontSize: 10,
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: accentColor,
            marginBottom: 4,
          }}>
            {label}
          </span>
        )}
        {/* Suggestions render as a clickable list — one click sends the
            suggestion straight back as a new user message. We use a flex
            row per suggestion (bullet column + text column) instead of a
            <ul> so the bullet always sits in line with the FIRST line of
            text, even when the text wraps to multiple lines. */}
        {isSuggestions && Array.isArray(content) ? (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 8,
          }}>
            {content.map((s, i) => (
              <div key={i} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 10,
              }}>
                <span style={{
                  flexShrink: 0,
                  // Match the line height of the text so the bullet sits
                  // visually on the first line.
                  lineHeight: '1.5',
                  fontSize: 14,
                  color: '#a855f7',
                  // Tiny vertical nudge so the round dot lines up optically
                  // with the cap-height of the first line of text.
                  marginTop: 1,
                }}>
                  •
                </span>
                <button
                  onClick={() => onSuggestionClick && onSuggestionClick(s)}
                  title="Click to apply this suggestion"
                  style={{
                    flex: 1,
                    background: 'transparent',
                    border: 'none',
                    color: palette.text,
                    padding: 0,
                    margin: 0,
                    cursor: onSuggestionClick ? 'pointer' : 'default',
                    fontSize: 14,
                    fontFamily: font.sans,
                    textAlign: 'left',
                    lineHeight: 1.5,
                    transition: 'color 0.15s',
                  }}
                  onMouseOver={e => { e.currentTarget.style.color = '#a855f7'; }}
                  onMouseOut={e => { e.currentTarget.style.color = palette.text; }}
                >
                  {s}
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div>{content}</div>
        )}
        {meta && (
          <div style={{
            marginTop: 6,
            fontSize: 11,
            color: palette.textDim,
            fontFamily: font.mono,
            display: 'flex', gap: 10, flexWrap: 'wrap',
          }}>
            {meta.format && <span>format: {meta.format}</span>}
            {meta.iterations !== undefined && (
              <span>iterations: {meta.iterations}</span>
            )}
            {meta.elapsed !== undefined && (
              <span>{meta.elapsed.toFixed(1)}s</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/* ─── Code block with copy button ─── */

function DotCodeBlock({ code, height }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };
  return (
    <div style={{
      position: 'relative',
      background: '#0a0c0e',
      border: `1px solid ${palette.border}`,
      borderRadius: 8,
      padding: '12px 14px',
      fontFamily: font.mono,
      fontSize: 12,
      lineHeight: 1.6,
      color: palette.textMuted,
      overflow: 'auto',
      height: height || '100%',
    }}>
      <button onClick={copy} style={{
        position: 'absolute', top: 6, right: 6,
        background: palette.surface, border: `1px solid ${palette.border}`,
        color: copied ? palette.green : palette.textMuted,
        borderRadius: 6, padding: '3px 8px', cursor: 'pointer',
        fontSize: 11, fontFamily: font.mono,
        zIndex: 2,
      }}>
        {copied ? '✓ copied' : 'copy'}
      </button>
      <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{code}</pre>
    </div>
  );
}

function ExampleChip({ text, onClick }) {
  return (
    <button onClick={() => onClick(text)} style={{
      background: palette.accentSoft,
      border: `1px solid ${palette.border}`,
      color: palette.accent,
      borderRadius: 20,
      padding: '6px 14px',
      fontSize: 12,
      fontFamily: font.sans,
      cursor: 'pointer',
      transition: 'all 0.15s',
      whiteSpace: 'nowrap',
    }}
    onMouseOver={e => e.currentTarget.style.borderColor = palette.accent}
    onMouseOut={e => e.currentTarget.style.borderColor = palette.border}
    >
      {text}
    </button>
  );
}

function LoadingDots() {
  return (
    <div style={{ display: 'flex', gap: 5, padding: '10px 14px' }}>
      {[0, 1, 2].map(i => (
        <div key={i} style={{
          width: 7, height: 7, borderRadius: '50%',
          background: palette.accent, opacity: 0.5,
          animation: `pulse 1.2s ease-in-out ${i * 0.15}s infinite`,
        }} />
      ))}
    </div>
  );
}

/* ─── Resizable vertical split bar ─── */

function SplitBar({ onDrag }) {
  const onMouseDown = (e) => {
    e.preventDefault();
    const startY = e.clientY;
    const move = (ev) => onDrag(ev.clientY - startY, ev.clientY);
    const up = () => {
      window.removeEventListener('mousemove', move);
      window.removeEventListener('mouseup', up);
    };
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', up);
  };
  return (
    <div onMouseDown={onMouseDown}
      style={{
        height: 6, cursor: 'ns-resize',
        background: palette.border,
        flexShrink: 0,
        position: 'relative',
      }}
      onMouseEnter={e => e.currentTarget.style.background = palette.accent}
      onMouseLeave={e => e.currentTarget.style.background = palette.border}
    >
      <div style={{
        position: 'absolute', left: '50%', top: '50%',
        transform: 'translate(-50%, -50%)',
        width: 32, height: 2,
        background: 'rgba(255,255,255,0.3)',
        borderRadius: 1,
      }} />
    </div>
  );
}

/* ─── Revision history strip ─── */

// Horizontal scroll of revision thumbnails. Clicking one pins the preview
// to that older revision; clicking the "live" badge unpins it. Each
// thumbnail shows the revision number and a snippet of the user message
// that produced it, so users can recognise the one they want.
function HistoryStrip({ history, viewingRevision, latestRevision, onSelect, onSelectLatest }) {
  if (!history || history.length === 0) return null;

  // Show newest first so the user doesn't have to scroll past old ones to
  // get to recent context. The "live" tile sits at the very left.
  const items = [...history].reverse();

  return (
    <div style={{
      borderTop: `1px solid ${palette.border}`,
      background: palette.surface,
      padding: '10px 16px',
      flexShrink: 0,
    }}>
      <div style={{
        display: 'flex', alignItems: 'center',
        justifyContent: 'space-between', marginBottom: 8,
      }}>
        <span style={{
          fontSize: 11, color: palette.textMuted,
          fontFamily: font.mono, letterSpacing: '0.05em',
          textTransform: 'uppercase',
        }}>
          Revisions ({history.length})
        </span>
        <span style={{
          fontSize: 10, color: palette.textDim, fontFamily: font.mono,
        }}>
          click a thumbnail to view it
        </span>
      </div>
      <div style={{
        display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 4,
      }}>
        {/* Live tile — selecting it returns to "latest" mode */}
        <button
          onClick={onSelectLatest}
          title="Show latest revision"
          style={{
            flex: '0 0 auto',
            width: 90, height: 90,
            borderRadius: 8,
            border: `2px solid ${viewingRevision === null ? palette.accent : palette.border}`,
            background: viewingRevision === null ? palette.accentSoft : palette.bg,
            color: viewingRevision === null ? palette.accent : palette.textMuted,
            cursor: 'pointer',
            display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center',
            fontFamily: font.mono, fontSize: 11,
            transition: 'all 0.15s',
          }}
        >
          <div style={{ fontSize: 20, marginBottom: 4 }}>●</div>
          <div>live</div>
          <div style={{ fontSize: 9, opacity: 0.7 }}>rev {latestRevision}</div>
        </button>

        {items.map(entry => {
          const isSelected = viewingRevision === entry.revision;
          const truncated = entry.userMessage.length > 32
            ? entry.userMessage.slice(0, 30) + '…'
            : entry.userMessage;
          return (
            <button
              key={entry.revision}
              onClick={() => onSelect(entry.revision)}
              title={entry.userMessage}
              style={{
                flex: '0 0 auto',
                width: 90, height: 90,
                borderRadius: 8,
                border: `2px solid ${isSelected ? palette.accent : palette.border}`,
                background: '#fff',
                cursor: 'pointer',
                padding: 0,
                position: 'relative',
                overflow: 'hidden',
                transition: 'all 0.15s',
              }}
            >
              <img
                src={`data:image/png;base64,${entry.imageB64}`}
                alt={`revision ${entry.revision}`}
                style={{
                  width: '100%', height: '100%',
                  objectFit: 'contain', background: '#fff',
                }}
              />
              <div style={{
                position: 'absolute', bottom: 0, left: 0, right: 0,
                background: 'rgba(0,0,0,0.7)',
                color: 'white', fontSize: 9,
                fontFamily: font.mono,
                padding: '2px 4px',
                textAlign: 'left',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}>
                rev {entry.revision} · {truncated}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

/* ─── Main App ─── */

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [dotSource, setDotSource] = useState('');
  const [imageB64, setImageB64] = useState('');
  const [revision, setRevision] = useState(0);
  const [loading, setLoading] = useState(false);
  const [provider, setProvider] = useState('gemini');
  const [providers, setProviders] = useState([]);
  const [format, setFormat] = useState('graphviz');
  const [formats, setFormats] = useState(['graphviz', 'mermaid', 'plantuml']);
  const [visionFeedback, setVisionFeedback] = useState(true);
  const [showDot, setShowDot] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Revision history: every successful turn pushes a snapshot here so the
  // user can compare the latest image to previous ones. We keep this in
  // memory only — the brief lists persistence as a non-goal — so resetting
  // the session or refreshing the tab clears it.
  // Each entry: { revision, imageB64, dotSource, format, userMessage,
  //               description, suggestions, timestamp }
  const [history, setHistory] = useState([]);
  // Which revision is currently displayed in the preview pane.
  // null means "show the latest" (the live imageB64).
  const [viewingRevision, setViewingRevision] = useState(null);
  // Toggle the history strip on/off.
  const [showHistory, setShowHistory] = useState(false);

  // Resizable split: ratio of diagram area (0..1). Code area gets the rest.
  const [splitRatio, setSplitRatio] = useState(0.65);
  const rightPaneRef = useRef(null);

  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    getConfig().then(cfg => {
      setProviders(cfg.providers || []);
      setProvider(cfg.default_provider || 'gemini');
      setFormats(cfg.formats || ['graphviz', 'mermaid', 'plantuml']);
      setFormat(cfg.default_format || 'graphviz');
    }).catch(() => {});
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Auto-grow the textarea up to ~5 rows.
  useEffect(() => {
    if (!inputRef.current) return;
    inputRef.current.style.height = 'auto';
    const h = Math.min(inputRef.current.scrollHeight, 140);
    inputRef.current.style.height = h + 'px';
  }, [input]);

  const handleDrag = useCallback((_dy, clientY) => {
    if (!rightPaneRef.current) return;
    const rect = rightPaneRef.current.getBoundingClientRect();
    const offset = clientY - rect.top;
    // Account for the toolbar (~50px). Keep both panes at least 80px tall.
    const ratio = Math.max(0.15, Math.min(0.9, (offset - 50) / (rect.height - 50)));
    setSplitRatio(ratio);
  }, []);

  // Resolve which image and source code the right pane should show. If the
  // user has pinned a previous revision, render that one; otherwise render
  // the live (latest) values. Falling back to the live values if the pinned
  // revision isn't in history (shouldn't happen, but safe).
  const pinnedEntry = viewingRevision !== null
    ? history.find(h => h.revision === viewingRevision)
    : null;
  const displayedImage = pinnedEntry ? pinnedEntry.imageB64 : imageB64;
  const displayedSource = pinnedEntry ? pinnedEntry.dotSource : dotSource;
  const displayedFormat = pinnedEntry ? pinnedEntry.format : format;
  const isViewingPast = pinnedEntry !== null;

  const send = async (text) => {
    if (!text.trim() || loading) return;
    const userMsg = text.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);
    const t0 = performance.now();

    try {
      const res = await sendMessage(userMsg, sessionId, provider, format, visionFeedback);
      const elapsed = (performance.now() - t0) / 1000;
      setSessionId(res.session_id);
      setDotSource(res.diagram_source || res.dot_source || '');
      setImageB64(res.image_base64);
      setRevision(res.revision);
      // New revision becomes the active view, so unpin any older one
      // the user might have been looking at.
      setViewingRevision(null);

      // Push this turn into the revision history so previous images stay
      // viewable. Newest is appended at the end.
      const historyEntry = {
        revision: res.revision,
        imageB64: res.image_base64,
        dotSource: res.diagram_source || res.dot_source || '',
        format: res.format || format,
        userMessage: userMsg,
        description: res.description || '',
        suggestions: res.suggestions || [],
        timestamp: Date.now(),
      };
      setHistory(prev => [...prev, historyEntry]);

      // Build the assistant chat messages. We split into up to three bubbles:
      //  1. "Diagram ready (rev N)"  — always shown.
      //  2. The plain-English description, if the model produced one.
      //  3. A bulleted list of suggestions for further changes, if any.
      // Splitting them keeps each bubble focused and skim-able rather than
      // burying the description inside a meta line.
      const newMessages = [{
        role: 'assistant',
        content: `Diagram ready (revision ${res.revision}).`,
        meta: {
          format: res.format || format,
          iterations: res.iterations,
          elapsed,
        },
      }];

      if (res.description) {
        newMessages.push({
          role: 'assistant',
          kind: 'description',
          content: res.description,
        });
      }

      if (Array.isArray(res.suggestions) && res.suggestions.length > 0) {
        newMessages.push({
          role: 'assistant',
          kind: 'suggestions',
          content: res.suggestions,
        });
      }

      setMessages(prev => [...prev, ...newMessages]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'error', content: err.message }]);
    }
    setLoading(false);
    inputRef.current?.focus();
  };

  const handleReset = async () => {
    if (sessionId) await resetSession(sessionId).catch(() => {});
    setMessages([]);
    setSessionId(null);
    setDotSource('');
    setImageB64('');
    setRevision(0);
    setShowDot(false);
    // Clear the in-memory revision history too, since it belongs to this
    // session only.
    setHistory([]);
    setViewingRevision(null);
    setShowHistory(false);
  };

  const handleExport = async (fmt) => {
    if (!sessionId) return;

    // If the user is viewing a pinned past revision, export from the
    // client-side cache rather than asking the backend (which only knows
    // the current revision). PNG is exported directly from the cached
    // base64 image; .dot/.txt source uses the cached source. For .svg of
    // a past revision we fall back to .png since we didn't cache the SVG.
    if (isViewingPast) {
      const filename = `diagram.rev${pinnedEntry.revision}.${fmt}`;
      if (fmt === 'png') {
        const blob = base64ToBlob(pinnedEntry.imageB64, 'image/png');
        triggerDownload(blob, filename);
        return;
      }
      if (fmt === 'dot' || fmt === 'source' || fmt === 'txt') {
        const blob = new Blob([pinnedEntry.dotSource], { type: 'text/plain' });
        triggerDownload(blob, filename);
        return;
      }
      // svg of a past revision isn't cached; fall through to live export
      // and warn in the console so the user understands.
      console.warn('SVG export of a past revision is not cached; exporting live diagram instead.');
    }

    try {
      const blob = await exportDiagram(sessionId, fmt);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `diagram.${fmt}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Export error:', e);
    }
  };

  const examples = [
    'Flowchart for user authentication',
    'Class diagram for e-commerce',
    'State machine for order lifecycle',
    'ER diagram for a blog platform',
    'Mind map of ML algorithms',
  ];

  return (
    <>
      <style>{`
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: ${palette.bg}; color: ${palette.text}; font-family: ${font.sans}; }
        @keyframes fadeSlide {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 0.3; transform: scale(0.85); }
          50% { opacity: 1; transform: scale(1.1); }
        }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: ${palette.border}; border-radius: 3px; }
        ::selection { background: ${palette.accentSoft}; }
        textarea { resize: none; }
      `}</style>

      <div style={{
        display: 'flex',
        height: '100vh',
        overflow: 'hidden',
      }}>

        {/* ─── LEFT: Chat Panel ─── */}
        <div style={{
          flex: sidebarOpen ? '0 0 460px' : '1 1 auto',
          display: 'flex',
          flexDirection: 'column',
          borderRight: sidebarOpen ? `1px solid ${palette.border}` : 'none',
          minWidth: 0,
          transition: 'flex 0.3s ease',
        }}>

          {/* Header */}
          <div style={{
            padding: '16px 20px',
            borderBottom: `1px solid ${palette.border}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexShrink: 0,
          }}>
            <div>
              <h1 style={{
                fontSize: 18, fontWeight: 700,
                letterSpacing: '-0.02em',
                display: 'flex', alignItems: 'center', gap: 8,
              }}>
                <span style={{
                  width: 28, height: 28, borderRadius: 8,
                  background: `linear-gradient(135deg, ${palette.accent}, #a855f7)`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 14,
                }}>◇</span>
                CDD
              </h1>
              <p style={{ fontSize: 11, color: palette.textDim, marginTop: 2 }}>
                Conversational Diagram Designer
              </p>
            </div>
            <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
              <select
                value={format}
                onChange={e => setFormat(e.target.value)}
                title="Diagram format"
                style={{
                  background: palette.surface, border: `1px solid ${palette.border}`,
                  color: palette.textMuted, borderRadius: 6,
                  padding: '4px 8px', fontSize: 11, fontFamily: font.mono,
                  cursor: 'pointer', outline: 'none',
                }}
              >
                {formats.map(f => <option key={f} value={f}>{f}</option>)}
              </select>
              <label
                title="Vision feedback loop (multimodal critique)"
                style={{
                  display: 'flex', alignItems: 'center', gap: 4,
                  fontSize: 11, color: palette.textMuted,
                  fontFamily: font.mono, cursor: 'pointer',
                  padding: '4px 8px',
                  border: `1px solid ${palette.border}`, borderRadius: 6,
                }}
              >
                <input
                  type="checkbox"
                  checked={visionFeedback}
                  onChange={e => setVisionFeedback(e.target.checked)}
                  style={{ margin: 0 }}
                />
                vision
              </label>
              {providers.length > 1 && (
                <select
                  value={provider}
                  onChange={e => setProvider(e.target.value)}
                  style={{
                    background: palette.surface, border: `1px solid ${palette.border}`,
                    color: palette.textMuted, borderRadius: 6,
                    padding: '4px 8px', fontSize: 11, fontFamily: font.mono,
                    cursor: 'pointer', outline: 'none',
                  }}
                >
                  {providers.map(p => <option key={p} value={p}>{p}</option>)}
                </select>
              )}
              <button onClick={handleReset} title="Reset" style={{
                background: 'transparent', border: `1px solid ${palette.border}`,
                color: palette.textMuted, borderRadius: 6,
                width: 32, height: 32, cursor: 'pointer',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 14, transition: 'all 0.15s',
              }}
              onMouseOver={e => { e.currentTarget.style.borderColor = palette.red; e.currentTarget.style.color = palette.red; }}
              onMouseOut={e => { e.currentTarget.style.borderColor = palette.border; e.currentTarget.style.color = palette.textMuted; }}
              >↺</button>
              <button onClick={() => setSidebarOpen(!sidebarOpen)} title="Toggle diagram pane" style={{
                background: 'transparent', border: `1px solid ${palette.border}`,
                color: palette.textMuted, borderRadius: 6,
                width: 32, height: 32, cursor: 'pointer',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 14,
              }}>⊞</button>
            </div>
          </div>

          {/* Messages: flex-grow:1 so input always sits at the bottom even when empty */}
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '20px 20px 10px',
            display: 'flex',
            flexDirection: 'column',
          }}>
            {messages.length === 0 && !loading ? (
              <div style={{
                display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center',
                flex: 1, gap: 20, opacity: 0.85,
              }}>
                <div style={{ fontSize: 42, opacity: 0.2 }}>◇</div>
                <p style={{
                  fontSize: 14, color: palette.textDim,
                  textAlign: 'center', maxWidth: 280,
                  lineHeight: 1.6,
                }}>
                  Describe a diagram in plain English.
                  <br />Refine it through conversation.
                </p>
                <div style={{
                  display: 'flex', flexWrap: 'wrap', gap: 8,
                  justifyContent: 'center', maxWidth: 380,
                }}>
                  {examples.map(ex => (
                    <ExampleChip key={ex} text={ex} onClick={send} />
                  ))}
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg, i) => (
                  <ChatBubble
                    key={i}
                    role={msg.role === 'error' ? 'assistant' : msg.role}
                    content={msg.content}
                    meta={msg.meta}
                    isError={msg.role === 'error'}
                    kind={msg.kind}
                    onSuggestionClick={send}
                  />
                ))}
                {loading && (
                  <div style={{
                    display: 'flex', justifyContent: 'flex-start',
                    marginBottom: 12, alignItems: 'center', gap: 8,
                  }}>
                    <div style={{
                      background: palette.aiBubble,
                      border: `1px solid ${palette.border}`,
                      borderRadius: '14px 14px 14px 4px',
                    }}>
                      <LoadingDots />
                    </div>
                    <span style={{
                      color: palette.textDim, fontSize: 11,
                      fontFamily: font.mono,
                    }}>
                      generating{visionFeedback ? ' (vision loop active)' : ''}…
                    </span>
                  </div>
                )}
                <div ref={chatEndRef} />
              </>
            )}
          </div>

          {/* Input — multi-line auto-grow */}
          <div style={{
            padding: '12px 20px 16px',
            borderTop: `1px solid ${palette.border}`,
            flexShrink: 0,
          }}>
            <div style={{
              display: 'flex', gap: 8, alignItems: 'flex-end',
              background: palette.surface,
              border: `1px solid ${palette.border}`,
              borderRadius: 12,
              padding: '8px 8px 8px 14px',
              transition: 'border-color 0.15s',
            }}>
              <textarea
                ref={inputRef}
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    send(input);
                  }
                }}
                placeholder="Describe a diagram… (Shift+Enter for new line)"
                disabled={loading}
                rows={1}
                style={{
                  flex: 1, background: 'transparent', border: 'none',
                  outline: 'none', color: palette.text,
                  fontSize: 14, fontFamily: font.sans,
                  lineHeight: 1.5, padding: '4px 0',
                  maxHeight: 140, overflow: 'auto',
                }}
              />
              <button
                onClick={() => send(input)}
                disabled={loading || !input.trim()}
                style={{
                  background: input.trim() && !loading ? palette.accent : palette.border,
                  border: 'none', borderRadius: 8,
                  width: 36, height: 36, cursor: input.trim() && !loading ? 'pointer' : 'default',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  color: '#fff', fontSize: 16, flexShrink: 0,
                  transition: 'background 0.15s',
                }}
              >↑</button>
            </div>
          </div>
        </div>

        {/* ─── RIGHT: Diagram + Code Panel (resizable) ─── */}
        {sidebarOpen && (
          <div ref={rightPaneRef} style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            minWidth: 0,
            background: palette.bg,
            overflow: 'hidden',
          }}>

            {/* Toolbar */}
            <div style={{
              padding: '12px 20px',
              borderBottom: `1px solid ${palette.border}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexShrink: 0,
              height: 50,
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: palette.text }}>
                  Preview
                </span>
                {revision > 0 && (
                  <span style={{
                    fontSize: 11,
                    // Pinned past revisions get a clearly different colour so
                    // the user is reminded they aren't looking at the latest.
                    color: isViewingPast ? '#a855f7' : palette.textDim,
                    fontFamily: font.mono,
                    background: isViewingPast ? 'rgba(168,85,247,0.15)' : palette.accentSoft,
                    padding: '2px 8px', borderRadius: 10,
                  }}>
                    {isViewingPast
                      ? `viewing rev ${pinnedEntry.revision} (latest: ${revision})`
                      : `rev ${revision}`}
                  </span>
                )}
              </div>
              {imageB64 && (
                <div style={{ display: 'flex', gap: 6 }}>
                  {/* History toggle — only useful once there are 2+ revisions
                      to compare. The button highlights when active. */}
                  {history.length > 1 && (
                    <button onClick={() => setShowHistory(!showHistory)}
                      title="Show / hide revision history"
                      style={{
                        background: showHistory ? palette.accentSoft : palette.surface,
                        border: `1px solid ${showHistory ? palette.accent : palette.border}`,
                        color: showHistory ? palette.accent : palette.textMuted,
                        borderRadius: 6, padding: '4px 10px',
                        fontSize: 11, fontFamily: font.mono,
                        cursor: 'pointer', transition: 'all 0.15s',
                        display: 'flex', alignItems: 'center', gap: 4,
                      }}
                    >
                      <span>⏱</span>
                      <span>history ({history.length})</span>
                    </button>
                  )}
                  {['png', 'svg', 'dot'].map(fmt => (
                    <button key={fmt} onClick={() => handleExport(fmt)}
                      title={`Download as .${fmt}`}
                      style={{
                        background: palette.surface,
                        border: `1px solid ${palette.border}`,
                        color: palette.textMuted,
                        borderRadius: 6, padding: '4px 10px',
                        fontSize: 11, fontFamily: font.mono,
                        cursor: 'pointer', transition: 'all 0.15s',
                      }}
                      onMouseOver={e => e.currentTarget.style.borderColor = palette.accent}
                      onMouseOut={e => e.currentTarget.style.borderColor = palette.border}
                    >
                      .{fmt}
                    </button>
                  ))}
                  <button onClick={() => setShowDot(!showDot)}
                    title="Show / hide source code"
                    style={{
                      background: showDot ? palette.accentSoft : palette.surface,
                      border: `1px solid ${showDot ? palette.accent : palette.border}`,
                      color: showDot ? palette.accent : palette.textMuted,
                      borderRadius: 6, padding: '4px 10px',
                      fontSize: 11, fontFamily: font.mono,
                      cursor: 'pointer',
                      display: 'flex', alignItems: 'center', gap: 4,
                    }}>
                    <span>{'</>'}</span>
                    <span>{showDot ? 'hide' : 'code'}</span>
                  </button>
                </div>
              )}
            </div>

            {/* Diagram area — uses displayedImage so we can show a pinned past
                revision when the user has selected one. */}
            <div style={{
              flex: imageB64 && showDot ? `0 0 calc(${splitRatio * 100}% - 25px)` : '1 1 auto',
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: imageB64 ? 'flex-start' : 'center',
              padding: 24,
              minHeight: 80,
            }}>
              {displayedImage ? (
                <ZoomImage
                  // Key on the revision so React fully remounts the zoom-image
                  // (resetting pan/zoom) when the user switches revisions.
                  key={isViewingPast ? `rev-${pinnedEntry.revision}` : 'live'}
                  src={`data:image/png;base64,${displayedImage}`}
                />
              ) : (
                <div style={{
                  textAlign: 'center',
                  color: palette.textDim,
                  fontSize: 13,
                }}>
                  <div style={{ fontSize: 48, opacity: 0.15, marginBottom: 12 }}>⬡</div>
                  <p>Your diagram will appear here</p>
                </div>
              )}
            </div>

            {/* Resizable split bar — only visible when code panel is open */}
            {imageB64 && showDot && (
              <>
                <SplitBar onDrag={handleDrag} />
                <div style={{
                  flex: '1 1 auto',
                  display: 'flex', flexDirection: 'column',
                  minHeight: 80,
                  overflow: 'hidden',
                }}>
                  <div style={{
                    padding: '8px 20px',
                    borderBottom: `1px solid ${palette.border}`,
                    display: 'flex', alignItems: 'center',
                    justifyContent: 'space-between',
                    flexShrink: 0,
                  }}>
                    <span style={{
                      fontSize: 11,
                      color: palette.textMuted,
                      fontFamily: font.mono,
                      letterSpacing: '0.05em',
                      textTransform: 'uppercase',
                    }}>
                      Source ({displayedFormat})
                      {isViewingPast && (
                        <span style={{ color: '#a855f7', marginLeft: 8 }}>
                          · rev {pinnedEntry.revision}
                        </span>
                      )}
                    </span>
                    <span style={{
                      fontSize: 10,
                      color: palette.textDim,
                      fontFamily: font.mono,
                    }}>
                      drag bar above to resize
                    </span>
                  </div>
                  <div style={{ flex: 1, overflow: 'hidden', padding: '12px 20px' }}>
                    <DotCodeBlock code={displayedSource} />
                  </div>
                </div>
              </>
            )}

            {/* Revision history strip — slides in at the bottom when toggled
                on. Lets the user view any previous diagram alongside the
                latest, addressing the "compare images" use case. */}
            {showHistory && imageB64 && (
              <HistoryStrip
                history={history}
                viewingRevision={viewingRevision}
                latestRevision={revision}
                onSelect={(rev) => setViewingRevision(rev)}
                onSelectLatest={() => setViewingRevision(null)}
              />
            )}
          </div>
        )}
      </div>
    </>
  );
}
