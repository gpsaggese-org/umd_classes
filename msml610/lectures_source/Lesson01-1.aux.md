# Analytical Sophistication 1

```tikz
% Color definitions
\definecolor{c2c2c2a}{RGB}{44,44,42}
\definecolor{c5f5e5a}{RGB}{95,94,90}
\definecolor{c888780}{RGB}{136,135,128}
\definecolor{cb4b2a9}{RGB}{180,178,169}
\definecolor{cf1efe8}{RGB}{241,239,232}
\definecolor{c444441}{RGB}{68,68,65}
\definecolor{cd3d1c7}{RGB}{211,209,199}

\def\globalscale{1.000000}

\begin{tikzpicture}[
  y=1cm, x=1cm,
  yscale=\globalscale, xscale=\globalscale,
  every node/.append style={scale=\globalscale},
  inner sep=0pt, outer sep=0pt
]

  % Axes
  \path[draw=c2c2c2a,fill,line width=0.0318cm,->] (1.27, 11.9063) -- (1.27, 2.1167);
  \path[draw=c2c2c2a,fill,line width=0.0318cm,->] (1.27, 2.1167) -- (17.4625, 2.1167);

  % Axis labels
  \node[text=c5f5e5a,anchor=south,rotate=90.0] (text2) at (0.8467, 6.8792){Strategic value};
  \node[text=c5f5e5a,anchor=south] (text3) at (9.6254, 1.3816){Analytical sophistication};

  % Maturity curve
  \path[draw=c2c2c2a,line width=0.0454cm]
    (1.7992, 2.4342).. controls (3.1221, 2.4925) and (4.3127, 2.6092) .. (5.371, 2.8134)..
    controls (6.4294, 3.0176) and (7.2231, 3.2802) .. (8.0169, 3.601)..
    controls (8.8106, 3.9219) and (9.3398, 4.272) .. (10.0013, 4.7096)..
    controls (10.6627, 5.1472) and (11.3242, 5.6139) .. (12.065, 6.0515)..
    controls (12.8058, 6.4891) and (13.7054, 6.8975) .. (14.896, 7.3059)..
    controls (15.4252, 7.4518) and (16.3513, 7.5684) .. (17.145, 7.6851);

  % Vertical divider line
  \path[draw=c888780,fill,line width=0.0265cm,dash pattern=on 0.1323cm off 0.1058cm]
    (7.0699, 11.8004) -- (7.0699, 2.1167);

  % Historical view label
  \begin{scope}[shift={(1.0583, -0.5292)}]
    \path[draw=c2c2c2a,line width=0.0318cm,rounded corners=0.1323cm]
      (1.4817, 11.6946) rectangle (5.08, 10.9008);
    \node[text=c2c2c2a,anchor=south] (text4) at (3.2808, 11.1654){Historical view};
  \end{scope}

  % Future view label
  \begin{scope}[shift={(-3.4332, 8.026)}]
    \path[draw=c2c2c2a,line width=0.0318cm,rounded corners=0.1323cm]
      (14.0229, 3.175) rectangle (17.1979, 2.3812);
    \node[text=c2c2c2a,anchor=south] (text5) at (15.6104, 2.6458){Future view};
  \end{scope}

  % Raw data box
  \begin{scope}[shift={(-0.6588, 0.0721)}]
    \path[draw=cb4b2a9,fill=cf1efe8,line width=0.0132cm,rounded corners=0.1058cm]
      (2.3367, 2.2429) rectangle (4.3367, 3.2429);
    \node[text=c444441,anchor=center] (text6) at (3.3367, 2.7429){Raw data};
  \end{scope}

  % Descriptive statistics box
  \begin{scope}[shift={(-0.926, -0.3351)}]
    \path[draw=cb4b2a9,fill=cf1efe8,line width=0.0132cm,rounded corners=0.1058cm]
      (5.2971, 2.8602) rectangle (7.2971, 3.8602);
    \node[text=c444441,anchor=center] (text7) at (6.2971, 3.4852){Descriptive};
    \node[text=c444441,anchor=center] (text8) at (6.2971, 3.2352){statistics};
  \end{scope}

  % Side labels
  \node[text=c5f5e5a,anchor=south] (text9) at (4.2981, 9.5955){What happened?};
  \node[text=c5f5e5a,anchor=south] (text9-9) at (12.2905, 9.7319){What will happen?};

  % Predictive models box
  \begin{scope}[shift={(-0.9855, -1.2198)}]
    \node[text=c5f5e5a,anchor=south] (text10) at (9.4192, 6.2442){What will};
    \node[text=c5f5e5a,anchor=south] (text11) at (9.525, 5.8738){happen?};
    \path[draw=c888780,fill=cd3d1c7,line width=0.0132cm,rounded corners=0.1058cm]
      (8.525, 4.5271) rectangle (10.525, 5.5271);
    \node[text=c2c2c2a,anchor=center] (text12) at (9.525, 5.1521){Predictive};
    \node[text=c2c2c2a,anchor=center] (text13) at (9.525, 4.9021){models};
  \end{scope}

  % Prescriptive model box
  \begin{scope}[shift={(-0.9525, -2.0108)}]
    \node[text=c5f5e5a,anchor=south] (text14) at (12.0798, 8.3078){What should};
    \node[text=c5f5e5a,anchor=south] (text15) at (12.0798, 7.9903){we do?};
    \path[draw=c888780,fill=cd3d1c7,line width=0.0132cm,rounded corners=0.1058cm]
      (11.0385, 6.7231) rectangle (13.0385, 7.7231);
    \node[text=c2c2c2a,anchor=center] (text16) at (12.0385, 7.3481){Prescriptive};
    \node[text=c2c2c2a,anchor=center] (text17) at (12.0385, 7.0981){model};
  \end{scope}

  % Simulation box
  \begin{scope}[shift={(0.2117, -3.7116)}]
    \node[text=c5f5e5a,anchor=south] (text18) at (12.9467, 11.1124){What is the best};
    \node[text=c5f5e5a,anchor=south] (text19) at (12.9467, 10.8213){we can do?};
    \path[draw=c888780,fill=cd3d1c7,line width=0.0132cm,rounded corners=0.1058cm]
      (11.9117, 9.6600) rectangle (13.9117, 10.6600);
    \node[text=c2c2c2a,anchor=center] (text20) at (12.9117, 10.1600){Simulation};
  \end{scope}

  % Optimization box
  \begin{scope}[shift={(0.3969, -2.0339)}]
    \begin{scope}[shift={(0.0, -2.1167)}]
      \node[text=c5f5e5a,anchor=south] (text21) at (15.7163, 12.3296){What is the best};
      \node[text=c5f5e5a,anchor=south] (text22) at (15.7163, 12.0385){course to take?};
      \path[draw=c888780,fill=cd3d1c7,line width=0.0132cm,rounded corners=0.1058cm]
        (14.6369, 10.9565) rectangle (16.6369, 11.9565);
      \node[text=c2c2c2a,anchor=center] (text23) at (15.6369, 11.4565){Optimization};
    \end{scope}
  \end{scope}

\end{tikzpicture}
```

# Analytical Sophistication 2

```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}

\begin{document}

\begin{tikzpicture}[
  >={Latex[scale=1.0]},
  box/.style={
    rectangle,
    rounded corners=4pt,
    draw=black,
    thick,
    fill=white,
    text centered,
    minimum width=2.4cm,
    minimum height=0.7cm,
    font=\footnotesize,
    inner sep=3pt
  },
  fbox/.style={
    rectangle,
    rounded corners=4pt,
    draw=black,
    thick,
    fill=white,
    text centered,
    minimum width=2.6cm,
    minimum height=0.95cm,
    font=\footnotesize,
    align=center,
    inner sep=3pt
  }
]

% Axes
\draw[->,thick] (0,0) -- (0,8) node[above,font=\small\bfseries] {Strategic Value};
\draw[->,thick] (0,0) -- (10,0) node[right,font=\small\bfseries] {Analytical Sophistication};

% Dashed vertical line separating past and future views
\draw[dashed,thick,gray] (4.5,-0.3) -- (4.5,7.7);

% Diagonal progression guide (all boxes lie on this line)
\draw[dotted,gray,thick] (0,0.04) -- (9.5,8.18);

% Past View boxes (diagonal: y = 0.857 x + 0.043)
\node[box] (raw)   at (1.0,0.9) {Raw Data};
\node[box] (clean) at (2.4,2.1) {Clean Data};
\node[box] (desc)  at (3.8,3.3) {Descriptive Stats};

% Future View boxes (continuing diagonal); each shows its question in italics
\node[fbox] (pred)  at (5.2,4.5)
  {Predictive Models\\[-1pt]{\scriptsize\itshape ``What will happen?''}};
\node[fbox] (presc) at (6.6,5.7)
  {Prescriptive Models\\[-1pt]{\scriptsize\itshape ``What should we do?''}};
\node[fbox] (sim)   at (8.0,6.9)
  {Simulation / Optimization\\[-1pt]{\scriptsize\itshape ``What's the best we can do?''}};

% Black arrows connecting sequential steps
\draw[->,thick] (raw)   -- (clean);
\draw[->,thick] (clean) -- (desc);
\draw[->,thick] (desc)  -- (pred);
\draw[->,thick] (pred)  -- (presc);
\draw[->,thick] (presc) -- (sim);

% Section labels (below x-axis)
\node[font=\small\bfseries] at (2.0,-0.7) {Past View};
\node[font=\footnotesize\itshape] at (2.0,-1.1) {``What happened?''};
\node[font=\small\bfseries] at (7.0,-0.7) {Future View};
\node[font=\footnotesize\itshape] at (7.0,-1.1) {``What will happen?''};

\end{tikzpicture}

\end{document}
```
