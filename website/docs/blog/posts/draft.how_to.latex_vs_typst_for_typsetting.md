# LaTeX vs Typst

- **LaTeX** is the long-established standard, with decades of packages, journal templates, and institutional support — but it has a steep learning curve, painfully slow compile times, and cryptic error messages that can take real effort to debug.
- **Typst** is a modern alternative built from scratch, designed to compile much faster (often near-instant) and give clearer, more helpful error messages.
- **Syntax**: LaTeX uses verbose commands (`\textbf{}`, `\begin{itemize}...\end{itemize}`); Typst uses lighter markup (`*bold*`, `- item`) closer to Markdown, with a more consistent and predictable underlying language for scripting/logic.
- **Ecosystem**: LaTeX has a vastly larger package ecosystem (CTAN) built up over 30+ years; Typst's package ecosystem is newer and smaller but growing quickly, with many essentials already covered.
- **Programmability**: Typst has a real, modern scripting language built in (functions, loops, conditionals feel natural); LaTeX's macro-based "programming" (via TeX primitives) is notoriously arcane.
- **Compatibility**: LaTeX is still required or expected by many academic journals/publishers; Typst is gaining adoption but isn't universally accepted yet, so check requirements before committing for formal submissions.
- **Learning curve**: Typst is generally easier to pick up, especially for people without a TeX background; LaTeX has more tutorials, Stack Exchange answers, and institutional muscle memory built up over time.

---

# Touying / Polylux vs Beamer (presentation slides)

- **Beamer** is the classic LaTeX class for slides — mature, extremely customizable, with tons of themes, but inherits LaTeX's slow compile times, which is especially annoying when iterating on slide layout.
- **Polylux** is a Typst package for presentations — aims to bring Beamer-like slide functionality to Typst, benefiting from Typst's fast compiles and simpler syntax; lighter-weight and a bit more minimal/manual than Beamer in terms of built-in themes.
- **Touying** is a more feature-rich Typst presentation package — supports more advanced features like animations/reveals (similar to Beamer's `\pause`, overlays), more sophisticated themes, and is generally considered more actively developed and closer to matching Beamer's feature set than Polylux.
- **Iteration speed**: both Touying and Polylux benefit hugely from Typst's near-instant compilation — a major practical advantage over Beamer when you're tweaking slide-by-slide content or layout repeatedly.
- **Themes/maturity**: Beamer has the most mature theme ecosystem (Madrid, Berlin, metropolis, etc.) accumulated over many years; Touying and Polylux have fewer built-in themes but are catching up, and Touying in particular has a growing set of templates.
- **Syntax**: Beamer slides are wrapped in `\begin{frame}...\end{frame}` with LaTeX commands; Touying/Polylux use Typst's lighter function/markup-based syntax, which many find faster to write and easier to customize programmatically.
- **Choosing between Touying and Polylux**: Polylux is simpler and good for straightforward slides; Touying is the better pick if you want more advanced features (complex overlays/animations, fancier theming) closer to what Beamer power-users expect.
