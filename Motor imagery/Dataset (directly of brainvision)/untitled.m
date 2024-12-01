eeglab;
EEG = pop_loadset('filename', 'right_wrist.set', 'filepath', 'D:\Study-Work\Study\EEG BCI project\EEG-project\Motor imagery\Dataset (directly of brainvision)\');
channel = 'FC5'; % Replace with your desired channel
channelIndex = find(strcmp({EEG.chanlocs.labels}, channel));

times = [0 25000]; % Time window in milliseconds
cycles = [3 0.5]; % Wavelet cycles
%baseline = [0 500]; % Baseline period in milliseconds

[ersp, itc, powbase, times, freqs, erspboot, itcboot] = ...
    newtimef(EEG.data(channelIndex, :, :), EEG.pnts, times, EEG.srate, cycles, 'baseline', NaN);
% Find the indices of frequencies between 6 Hz and 18 Hz
bandPassFreqIndex = find(freqs >= 6 & freqs <= 18);

% Select the part of the ersp and freqs that correspond to these frequencies
filtered_ersp = ersp(bandPassFreqIndex, :);
filtered_freqs = freqs(bandPassFreqIndex);

% Plot the filtered results
figure;
imagesc(times, filtered_freqs, 10*log10(abs(filtered_ersp)));
set(gca, 'YDir', 'normal');
xlabel('Time (ms)');
ylabel('Frequency (Hz)');
title(['Time-Frequency Analysis of Channel ' channel ' (Band-pass 6-18 Hz)']);
colorbar;

% Overlay event markers
hold on;
for i = 1:length(EEG.event)
    eventLat = (EEG.event(i).latency - EEG.xmin * EEG.srate) / EEG.srate * 1000; % Convert latency to milliseconds
    line([eventLat eventLat], get(gca, 'YLim'), 'Color', 'r', 'LineWidth', 2);
end
hold off;
