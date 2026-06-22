\documentclass[border=12pt]{standalone}
\usepackage{tikz}
\usepackage{xcolor}
\usetikzlibrary{arrows.meta, calc}

\begin{document}

% ---------- Palette ----------
\definecolor{axisInk}{RGB}{45,45,45}          % axes, strong text
\definecolor{labelInk}{RGB}{110,110,108}      % axis titles, question labels
\definecolor{curveInk}{RGB}{40,90,150}        % the maturity curve, accent blue
\definecolor{dividerInk}{RGB}{170,170,165}    % dashed divider
\definecolor{tagBorder}{RGB}{60,60,58}        % historical/future view pill borders
\definecolor{histFill}{RGB}{246,247,248}      % light neutral box fill (left side)
\definecolor{histBorder}{RGB}{198,200,202}
\definecolor{futFill}{RGB}{224,237,246}       % light blue fill (right side)
\definecolor{futBorder}{RGB}{151,190,216}
\definecolor{futTextInk}{RGB}{30,70,110}

\begin{tikzpicture}[
  every node/.style={font=\sffamily},
  >=stealth
]

% ============ Canvas guides ============
% Plot area roughly x: 0 to 17.6, y: 0 to 11
\def\xmin{0}
\def\xmax{20.2}
\def\ymin{0}
\def\ymax{12.6}
\def\xaxisY{1.4}     % y position of x-axis
\def\yaxisX{1.0}      % x position of y-axis

% ============ Axes ============
\draw[axisInk, line width=0.45pt, ->] (\yaxisX, \ymax) -- (\yaxisX, \xaxisY);
\draw[axisInk, line width=0.45pt, ->] (\yaxisX, \xaxisY) -- (\xmax, \xaxisY);

% Axis titles
\node[labelInk, font=\sffamily\small, rotate=90, anchor=south] at (0.32, 7.0) {STRATEGIC VALUE};
\node[labelInk, font=\sffamily\small, anchor=north] at ({(\yaxisX+\xmax)/2}, \xaxisY-0.35) {ANALYTICAL SOPHISTICATION};

% ============ Dashed divider between Historical / Future ============
\def\dividerX{8.2}
\draw[dividerInk, line width=0.5pt, dash pattern=on 3pt off 2.4pt] (\dividerX, 12.1) -- (\dividerX, \xaxisY);

% ============ View tag pills ============
% Historical view pill (top-left)
\draw[tagBorder, line width=0.6pt, rounded corners=9pt, fill=white]
  (1.35, 11.9) rectangle (4.55, 12.6);
\node[axisInk, font=\sffamily\bfseries\small] at (2.95, 12.25) {HISTORICAL VIEW};

% Future view pill (top-right)
\draw[tagBorder, line width=0.6pt, rounded corners=9pt, fill=white]
  (14.6, 11.9) rectangle (17.5, 12.6);
\node[axisInk, font=\sffamily\bfseries\small] at (16.05, 12.25) {FUTURE VIEW};

% ============ Maturity curve ============
\draw[curveInk, line width=1.6pt]
  (1.55, 1.65)
  .. controls (3.1, 1.72) and (4.45, 1.85) .. (5.6, 2.15)
  .. controls (6.75, 2.45) and (7.55, 2.78) .. (8.35, 3.25)
  .. controls (9.15, 3.72) and (9.75, 4.2) .. (10.45, 4.75)
  .. controls (11.15, 5.3) and (11.85, 5.85) .. (12.65, 6.35)
  .. controls (13.45, 6.85) and (14.55, 7.4) .. (16.0, 7.95)
  .. controls (16.85, 8.27) and (17.7, 8.45) .. (18.6, 8.55);

% (dot markers removed — boxes already anchor each stage along the curve)

% ============ Stage 1: Raw data ============
\draw[histBorder, line width=0.7pt, rounded corners=4pt, fill=histFill]
  (1.75, 1.95) rectangle (3.75, 2.75);
\node[axisInk, font=\sffamily\small\bfseries] at (2.75, 2.35) {Raw data};

% ============ Stage 2: Descriptive statistics ============
\draw[histBorder, line width=0.7pt, rounded corners=4pt, fill=histFill]
  (4.85, 2.95) rectangle (6.85, 3.95);
\node[axisInk, font=\sffamily\small\bfseries] at (5.85, 3.62) {Descriptive};
\node[axisInk, font=\sffamily\small\bfseries] at (5.85, 3.32) {statistics};

% Question labels for historical side
\node[labelInk, font=\sffamily\itshape\small] at (2.75, 4.55) {What happened?};

% ============ Stage 3: Predictive models ============
\draw[futBorder, line width=0.7pt, rounded corners=4pt, fill=futFill]
  (7.95, 4.15) rectangle (9.95, 5.15);
\node[futTextInk, font=\sffamily\small\bfseries] at (8.95, 4.82) {Predictive};
\node[futTextInk, font=\sffamily\small\bfseries] at (8.95, 4.52) {models};
\node[labelInk, font=\sffamily\itshape\small] at (8.95, 5.75) {What will happen?};

% ============ Stage 4: Prescriptive model ============
\draw[futBorder, line width=0.7pt, rounded corners=4pt, fill=futFill]
  (11.05, 5.55) rectangle (13.05, 6.55);
\node[futTextInk, font=\sffamily\small\bfseries] at (12.05, 6.22) {Prescriptive};
\node[futTextInk, font=\sffamily\small\bfseries] at (12.05, 5.92) {model};
\node[labelInk, font=\sffamily\itshape\small] at (12.05, 7.15) {What should we do?};

% ============ Stage 5: Simulation & Optimization (grouped, top right) ============
\node[labelInk, font=\sffamily\itshape\small, align=center] at (15.55, 9.7) {What is the\\best we can do?};
\draw[futBorder, line width=0.7pt, rounded corners=4pt, fill=futFill]
  (14.55, 7.95) rectangle (16.55, 8.95);
\node[futTextInk, font=\sffamily\small\bfseries] at (15.55, 8.45) {Simulation};

\node[labelInk, font=\sffamily\itshape\small, align=center] at (18.05, 11.15) {What is the best\\course to take?};
\draw[futBorder, line width=0.7pt, rounded corners=4pt, fill=futFill]
  (17.05, 9.45) rectangle (19.05, 10.45);
\node[futTextInk, font=\sffamily\small\bfseries] at (18.05, 9.95) {Optimization};

\end{tikzpicture}

\end{document}
