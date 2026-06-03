% render_matlab.m — produce the ground-truth MATLAB reference for openlab-style fidelity tuning
%
% Renders the EXACT same 4 plots as examples/before_after.py (same data, same
% layout, same figure size + DPI). Output is a single 2x2 grid PNG so we can
% put it side-by-side with examples/after.png and visually + pixel-diff.
%
% Usage in MATLAB:
%   cd /path/to/openlab-style/examples
%   render_matlab
%   % outputs: examples/matlab_reference.png
%
% After running, commit examples/matlab_reference.png to the repo so we have
% the ground truth checked in.

fig = figure('Color', 'white', 'Position', [100 100 1100 770]);

% ─── (1,1) Multi-line trig plot ──────────────────────────────────────────
subplot(2, 2, 1);
t = linspace(0, 2*pi, 200);
plot(t, sin(t), 'DisplayName', 'sin(t)'); hold on;
plot(t, cos(t), 'DisplayName', 'cos(t)');
plot(t, sin(2*t), 'DisplayName', 'sin(2t)');
hold off;
xlabel('t');
ylabel('amplitude');
title('Trig functions');
legend('show');
grid on;

% ─── (1,2) Histogram ─────────────────────────────────────────────────────
subplot(2, 2, 2);
rng(42);  % MATLAB equivalent of numpy.random.seed(42); not bit-identical but reproducible
data = randn(2000, 1);
histogram(data, 30);
xlabel('value');
ylabel('count');
title('Histogram of 2000 N(0,1) samples');
grid on;

% ─── (2,1) Peaks heatmap ─────────────────────────────────────────────────
subplot(2, 2, 3);
[X, Y] = meshgrid(linspace(-3, 3, 150), linspace(-3, 3, 150));
Z = 3*(1-X).^2 .* exp(-X.^2 - (Y+1).^2) ...
    - 10*(X/5 - X.^3 - Y.^5) .* exp(-X.^2 - Y.^2) ...
    - exp(-(X+1).^2 - Y.^2) / 3;
imagesc([-3 3], [-3 3], Z);
axis xy;             % flip y so origin is bottom-left (matches matplotlib origin='lower')
axis tight;
colorbar;
xlabel('X');
ylabel('Y');
title('peaks() — colormap test');

% ─── (2,2) Loglog frequency response ─────────────────────────────────────
subplot(2, 2, 4);
f = logspace(0, 4, 200);
H1 = 1 ./ (1 + 1j * f / 100);
H2 = 1 ./ (1 + 1j * f / 1000);
loglog(f, abs(H1), 'DisplayName', 'cutoff 100 Hz'); hold on;
loglog(f, abs(H2), 'DisplayName', 'cutoff 1 kHz');
hold off;
xlabel('frequency (Hz)');
ylabel('|H(f)|');
title('Two low-pass filters');
legend('show');
grid on;

% ─── Export ──────────────────────────────────────────────────────────────
% Match the Python output dimensions exactly: figsize=(10, 7) at dpi=110 = 1100x770 px
% MATLAB uses inches at 100 dpi by default; force 110 dpi via -r110
out_path = fullfile(fileparts(mfilename('fullpath')), 'matlab_reference.png');
exportgraphics(fig, out_path, 'Resolution', 110, 'BackgroundColor', 'white');
fprintf('Wrote %s\n', out_path);
fprintf('Now: commit it to the repo so the fidelity diff has a ground truth.\n');
