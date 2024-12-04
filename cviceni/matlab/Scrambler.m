% Parameters
fs = 42000; % Sampling frequency
t = 0:1/fs:1-1/fs; % Time vector
f_carrier = 3000; % Carrier frequency

% Signal parameters
frequencies = [500, 1000, 1500]; % Example frequencies
amplitudes = [1, 0.5, 0.25]; % Example amplitudes

% Generate the original signal
original_signal = zeros(size(t));
for i = 1:length(frequencies)
    original_signal = original_signal + amplitudes(i)*sin(2*pi*frequencies(i)*t);
end

% Filtering
% Create a low-pass filter
Fpass = 3000; % Passband frequency 
Fstop = 3500; % Stopband frequency
Astop = 80;   % Stopband attenuation

[b, nb]=My_FIR(Fpass, Fstop, Astop);

% 2. Filter the signal
filtered_signal = filter(b, 1, original_signal);

% Scramble the signal
carrier_signal = sin(2*pi*f_carrier*t);
scrambled_signal = filtered_signal .* carrier_signal;

% filtering
G = 2; % gain
filtered_output = filter(b, 1/G, scrambled_signal);

% Compute and plot the spectrum before scrambling
figure;
% velikost grafu
set(gcf, 'Position', [100, 100, 800, 600]);

subplot(3,1,1);
original_spectrum = abs(fft(original_signal));
f = (0:length(original_spectrum)-1)*fs/length(original_spectrum);
plot(f, original_spectrum);
% omezeni na Fs/2
xlim([0, fs/2]);
title('Spectrum Before Scrambling');
xlabel('Frequency (Hz)');
ylabel('Magnitude');

% Compute and plot the spectrum after scrambling
subplot(3,1,2);
scrambled_spectrum = abs(fft(scrambled_signal));
plot(f, scrambled_spectrum);
xlim([0, fs/2]);
title('Spectrum After Scrambling');
xlabel('Frequency (Hz)');
ylabel('Magnitude');

% Compute and plot the spectrum
subplot(3,1,3);
descrambled_spectrum = abs(fft(filtered_output));
plot(f, descrambled_spectrum);
xlim([0, fs/2]);
title('Spectrum After Filtering');
xlabel('Frequency (Hz)');
ylabel('Magnitude');