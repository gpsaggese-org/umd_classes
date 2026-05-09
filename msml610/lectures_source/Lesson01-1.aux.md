// #############################################################################
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

// #############################################################################
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

// #############################################################################
# Hotel Pricing Paradox

```svg
<?xml version="1.0" encnoding="UTF-8" standalone="no"?>
<svg
   viewBox="0 0 680 470"
   role="img"
   version="1.1"
   id="svg23"
   sodipodi:docname="input.svg"
   inkscape:version="1.4.3 (0d15f75, 2025-12-25)"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview23"
     pagecolor="#ffffff"
     bordercolor="#000000"
     borderopacity="0.25"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:zoom="1.2852941"
     inkscape:cx="340"
     inkscape:cy="235.35469"
     inkscape:window-width="1504"
     inkscape:window-height="1172"
     inkscape:window-x="0"
     inkscape:window-y="25"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg23"
     showgrid="false" />
  <title
     id="title1">Reality vs naive prediction in causal inference for hotel pricing</title>
  <desc
     id="desc1">Two side-by-side panels: the left &quot;Reality&quot; panel shows demand causing both price and occupancy to rise (a confounded correlation); the right &quot;Naive prediction&quot; panel shows that intervening on price will not increase occupancy. A summary bar at the bottom states correlation does not imply causation.</desc>
  <defs
     id="defs2">
    <marker
       id="arrow"
       viewBox="0 0 10 10"
       refX="8"
       refY="5"
       markerWidth="6"
       markerHeight="6"
       orient="auto-start-reverse">
      <path
         d="M2 1L8 5L2 9"
         fill="none"
         stroke="context-stroke"
         stroke-width="1.5"
         stroke-linecap="round"
         stroke-linejoin="round"
         id="path1" />
    </marker>
    <marker
       id="arrow-bold"
       viewBox="0 0 10 10"
       refX="8"
       refY="5"
       markerWidth="7"
       markerHeight="7"
       orient="auto-start-reverse">
      <path
         d="M2 1L8 5L2 9"
         fill="none"
         stroke="context-stroke"
         stroke-width="2"
         stroke-linecap="round"
         stroke-linejoin="round"
         id="path2" />
    </marker>
  </defs>
  <style
     id="style2">
    .t, .ts, .th { font-family: -apple-system, &quot;Segoe UI&quot;, system-ui, sans-serif; fill: #1f2937; }
    .th { font-size: 14px; font-weight: 500; }
    .ts { font-size: 12px; font-weight: 400; }

    .c-purple-fill { fill: #f5f3ff; }
    .c-purple-stroke { stroke: #7c3aed; }
    .c-purple-text { fill: #5b21b6; }

    .c-teal-fill { fill: #f0fdfa; }
    .c-teal-stroke { stroke: #0d9488; }
    .c-teal-text { fill: #115e59; }

    .c-coral-fill { fill: #fef2f2; }
    .c-coral-stroke { stroke: #dc2626; }
    .c-coral-text { fill: #991b1b; }

    .c-gray-fill { fill: #f9fafb; }
    .c-gray-stroke { stroke: #6b7280; }
    .c-gray-text { fill: #374151; }

    .arrow-purple { fill: none; stroke: #7c3aed; stroke-width: 1.5; }
    .arrow-coral-bold { fill: none; stroke: #dc2626; stroke-width: 2.5; }
    .dashed-corr { fill: none; stroke: #0d9488; stroke-width: 1; stroke-dasharray: 5 3; opacity: 0.7; }

    .axis-line { stroke: #9ca3af; stroke-width: 1.5; fill: none; }
    .chart-teal-solid { stroke: #0d9488; stroke-width: 1.8; fill: none; }
    .chart-purple-dashed { stroke: #7c3aed; stroke-width: 1.5; fill: none; stroke-dasharray: 4 3; }
    .chart-coral-solid { stroke: #dc2626; stroke-width: 1.8; fill: none; }
    .chart-teal-dashed { stroke: #0d9488; stroke-width: 1.5; fill: none; stroke-dasharray: 4 3; }

    .panel-divider { stroke: #e5e7eb; stroke-width: 1; }
  </style>
  <rect
     x="42.5"
     y="40"
     width="290"
     height="330"
     fill="none"
     stroke="#7c3aed"
     stroke-width="4"
     rx="8"
     id="rect12"
     style="stroke-width:3;stroke-dasharray:none" />
  <rect
     x="338.89023"
     y="40"
     width="290"
     height="330"
     fill="none"
     stroke="#dc2626"
     stroke-width="4"
     rx="8"
     id="rect13"
     style="stroke-width:3;stroke-dasharray:none" />
  <!-- ============ LEFT PANEL: Reality ============ -->
  <text
     class="th c-purple-text"
     x="182.33409"
     y="58.112122"
     text-anchor="middle"
     id="text2"><tspan
       style="font-weight:bold"
       id="tspan23">Reality</tspan></text>
  <!-- Demand box (purple, top of tree) -->
  <rect
     class="c-purple-fill c-purple-stroke"
     x="140"
     y="75"
     width="80"
     height="36"
     rx="4"
     stroke-width="1.5"
     id="rect2" />
  <text
     class="th c-purple-text"
     x="180"
     y="98"
     text-anchor="middle"
     id="text3">Demand ↑</text>
  <!-- Branching arrows down-left and down-right -->
  <path
     class="arrow-purple"
     d="M 165 111 L 110 158"
     marker-end="url(#arrow)"
     id="path3" />
  <path
     class="arrow-purple"
     d="M 195 111 L 250 158"
     marker-end="url(#arrow)"
     id="path4" />
  <!-- Price box (teal, lower-left) -->
  <rect
     class="c-teal-fill c-teal-stroke"
     x="60"
     y="160"
     width="80"
     height="36"
     rx="4"
     stroke-width="1.5"
     id="rect4" />
  <text
     class="th c-teal-text"
     x="100"
     y="183"
     text-anchor="middle"
     id="text4">Price ↑</text>
  <!-- Occupancy box (teal, lower-right) -->
  <rect
     class="c-teal-fill c-teal-stroke"
     x="220"
     y="160"
     width="100"
     height="36"
     rx="4"
     stroke-width="1.5"
     id="rect5" />
  <text
     class="th c-teal-text"
     x="270"
     y="183"
     text-anchor="middle"
     id="text5">Occupancy ↑</text>
  <!-- Dashed correlation line between Price and Occupancy -->
  <path
     class="dashed-corr"
     d="M 140 178 L 220 178"
     id="path5" />
  <text
     class="ts c-teal-text"
     x="180"
     y="216"
     text-anchor="middle"
     id="text6">Correlated</text>
  <text
     class="ts c-gray-text"
     x="180"
     y="232"
     text-anchor="middle"
     id="text7">(both caused by demand)</text>
  <!-- Mini line chart (Reality): both curves rise with demand -->
  <g
     transform="translate(60,262)"
     id="g12">
    <path
       class="axis-line"
       d="M 0,80 H 240"
       id="path7" />
    <path
       class="axis-line"
       d="M 0,0 V 80"
       id="path8" />
    <!-- price: solid teal, rising -->
    <path
       class="chart-teal-solid"
       d="M 5,70 Q 60,56 120,36 180,16 235,8"
       id="path9" />
    <!-- occupancy: dashed purple, rising in parallel -->
    <path
       class="chart-purple-dashed"
       d="M 5,73 Q 60,60 120,40 180,20 235,13"
       id="path10" />
    <text
       class="ts c-gray-text"
       x="120"
       y="95"
       text-anchor="middle"
       id="text10">Demand →</text>
    <!-- legend -->
    <line
       x1="10"
       y1="10"
       x2="30"
       y2="10"
       stroke="#0d9488"
       stroke-width="1.8"
       id="line10" />
    <text
       class="ts c-teal-text"
       x="35"
       y="13"
       id="text11">Price</text>
    <line
       x1="10"
       y1="26"
       x2="30"
       y2="26"
       stroke="#7c3aed"
       stroke-width="1.5"
       stroke-dasharray="4, 3"
       id="line11" />
    <text
       class="ts c-purple-text"
       x="35"
       y="29"
       id="text12">Occupancy</text>
  </g>
  <!-- Panel enclosing boxes -->
  <!-- Vertical divider -->
  <!-- ============ RIGHT PANEL: Naive prediction (wrong) ============ -->
  <text
     class="th c-coral-text"
     x="482.33414"
     y="58.112122"
     text-anchor="middle"
     id="text13"><tspan
       style="font-weight:bold"
       id="tspan24">Naive prediction (wrong)</tspan></text>
  <!-- Raise price box (coral, top of chain) -->
  <rect
     class="c-coral-fill c-coral-stroke"
     x="420"
     y="75"
     width="120"
     height="36"
     rx="4"
     stroke-width="1.5"
     id="rect14" />
  <text
     class="th c-coral-text"
     x="480"
     y="98"
     text-anchor="middle"
     id="text14">Raise price</text>
  <!-- Bold red downward arrow -->
  <path
     class="arrow-coral-bold"
     d="m 480,112 v 46"
     marker-end="url(#arrow-bold)"
     id="path14" />
  <!-- Sell more rooms? box (coral, bottom of chain) -->
  <rect
     class="c-coral-fill c-coral-stroke"
     x="400"
     y="160"
     width="160"
     height="36"
     rx="4"
     stroke-width="1.5"
     id="rect15" />
  <text
     class="th c-coral-text"
     x="480"
     y="183"
     text-anchor="middle"
     id="text15">Sell more rooms?</text>
  <!-- Big red ✕ -->
  <text
     x="401.85355"
     y="232"
     text-anchor="middle"
     font-family="'-apple-system', system-ui, sans-serif"
     font-size="32px"
     font-weight="700"
     fill="#dc2626"
     id="text16">✕</text>
  <!-- Caption beneath the X -->
  <text
     class="ts c-gray-text"
     x="495.49774"
     y="218.59375"
     text-anchor="middle"
     id="text17">Demand didn't change —</text>
  <text
     class="ts c-gray-text"
     x="491.60736"
     y="232.66812"
     text-anchor="middle"
     id="text18">Occupancy will fall</text>
  <!-- Mini line chart (Naive): price climbs, occupancy flattens then drops -->
  <g
     transform="translate(360,262.16591)"
     id="g23">
    <path
       class="axis-line"
       d="M 0,80 H 240"
       id="path18" />
    <path
       class="axis-line"
       d="M 0,0 V 80"
       id="path19" />
    <!-- price: solid coral, climbing -->
    <path
       class="chart-coral-solid"
       d="M 5,70 Q 60,55 120,38 180,21 235,25"
       id="path20" />
    <!-- occupancy: dashed teal, flat then falling -->
    <path
       class="chart-teal-dashed"
       d="m 5,48 75,2 q 60,3 100,14 40,11 55,12"
       id="path21" />
    <text
       class="ts c-gray-text"
       x="120"
       y="95"
       text-anchor="middle"
       id="text21">Time after price hike →</text>
    <!-- legend -->
    <line
       x1="10"
       y1="0"
       x2="30"
       y2="0"
       stroke="#dc2626"
       stroke-width="1.8"
       id="line21" />
    <text
       class="ts c-coral-text"
       x="35.553787"
       y="2.4560637"
       id="text22">Price</text>
    <line
       x1="10"
       y1="16"
       x2="30"
       y2="16"
       stroke="#0d9488"
       stroke-width="1.5"
       stroke-dasharray="4, 3"
       id="line22" />
    <text
       class="ts c-teal-text"
       x="35"
       y="19"
       id="text23">Occupancy</text>
  </g>
</svg>
```
