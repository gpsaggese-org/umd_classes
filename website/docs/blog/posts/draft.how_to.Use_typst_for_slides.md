
Typst vs Latex


Typst is a great modern alternative to LaTeX for creating presentations, typically using the polylux or touying packages.

vs Beamer

Key differences:
- Touying: Structured slides with predefined components; good for formal presentations
- Polylux: Bare-bones building blocks; good for custom designs and developer presentations

Touying / Polylux vs Beamer (presentation slides)

Beamer is the classic LaTeX class for slides — mature, extremely customizable, with tons of themes, but inherits LaTeX's slow compile times, which is especially annoying when iterating on slide layout.
Polylux is a Typst package for presentations — aims to bring Beamer-like slide functionality to Typst, benefiting from Typst's fast compiles and simpler syntax; lighter-weight and a bit more minimal/manual than Beamer in terms of built-in themes.
Touying is a more feature-rich Typst presentation package — supports more advanced features like animations/reveals (similar to Beamer's \pause, overlays), more sophisticated themes, and is generally considered more actively developed and closer to matching Beamer's feature set than Polylux.
Iteration speed: both Touying and Polylux benefit hugely from Typst's near-instant compilation — a major practical advantage over Beamer when you're tweaking slide-by-slide content or layout repeatedly.
Themes/maturity: Beamer has the most mature theme ecosystem (Madrid, Berlin, metropolis, etc.) accumulated over many years; Touying and Polylux have fewer built-in themes but are catching up, and Touying in particular has a growing set of templates.
Syntax: Beamer slides are wrapped in \begin{frame}...\end{frame} with LaTeX commands; Touying/Polylux use Typst's lighter function/markup-based syntax, which many find faster to write and easier to customize programmatically.
Choosing between Touying and Polylux: Polylux is simpler and good for straightforward slides; Touying is the better pick if you want more advanced features (complex overlays/animations, fancier theming) closer to what Beamer power-users expect.

To compile either, save and run:
typst compile example_touying_slides.typ
typst compile example_polylux_slides.typ

Describe the slides in details

https://github.com/alexmodrono/typst-pandoc

https://typst.app/universe/package/bookly/

https://typst.app/universe/package/qooklet/

typstyle --inplace --wrap-text -l 80 msml610/book/Lesson06.2-Using_Bayesian_Networks.typ

typst compile --root . msml610/book/Lesson06.1-Bayesian_Networks.typ

https://typst.app/universe/package/touying/

https://typst.app/universe/package/polylux/

