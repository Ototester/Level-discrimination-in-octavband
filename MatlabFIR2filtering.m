Fs = 44100;                     % Sampling rate of audiofile
Nyq = Fs/2;                     % Nyquist frequency
levelDiff = 92;                 % Scaling difference dB FS to dB SPL
% Converting scaling difference in dB to ratio
levelDiffLinear = 10^(levelDiff/20);

% The main filter
% Octave-band filter, with normalized frequencies
f1 = (4000/sqrt(2)-100)/Nyq;    % start of transition band
f2 = (4000/sqrt(2))/Nyq;        % lowest frequency
f3 = (4000/sqrt(2)+100)/Nyq;    % end of transition band
f4 = 4000/Nyq;                  % center frequency
f5 = (4000*sqrt(2)-100)/Nyq;    % start of transition band
f6 = (4000*sqrt(2))/Nyq;        % highest frequency
f7 = (4000*sqrt(2)+100)/Nyq;    % end of transition band
% Low pass filter part of the main filter
% Filters out sound information that is not needed
f8 = (10000-100)/Nyq;           % start of transition band
f9 = 10000/Nyq;                 % cut off frequency
f10 = (10000+100)/Nyq;          % end of transition band
% Sets the range of filtration for the main filter
% and converts it from dB to ratio
dB = -30:3:15;                  
ratio = 10.^(dB/20);            % Array with magnitude converted to ratio
n = 140;                        % order of samples for main filter
% Combining the frequencies to an array for the FIR2 filter
f = [0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, 1];

% Validating filter
% Half octave-bandpass filter, with normalized frequencies
% Used to validate the main filter by checking the RMS value
% after the validating filter has been applied
fb1 = (4000/2^(1/4)-1)/Nyq;     % start of transition band
fb2 = (4000/2^(1/4))/Nyq;       % lowest frequency
fb3 = (4000/2^(1/4)+1)/Nyq;     % end of transition band
fb4 = 4000/Nyq;                 % center frequency
fb5 = (4000*2^(1/4)-1)/Nyq;     % start of transition band
fb6 = (4000*2^(1/4))/Nyq;       % highest frequency
fb7 = (4000*2^(1/4)+1)/Nyq;     % end of transition band
% Combining the frequencies to an array for the FIR2 filter
fbandpass = [0, fb1, fb2, fb3, fb4, fb5, fb6, fb7, 1];
Lc = 0.708;                     % Cut-off frequency for mbandpass
% Magnitude array for the bandpass filter used for validation,
% order relates to the placement of frequencies in fbandpass
mbandpass = [0, 0, Lc, 1, 1, 1, Lc, 0, 0];
nbandpass = 1000;               % order of samples for validating filter
% Constructs the validating filter
bandpass = fir2(nbandpass,fbandpass,mbandpass);

nFiles = 153;                   % Number of files in the directory
% Choose a directory for the files here
% All files should be in the format Tal101.wav, Tal102.wav etc
directory = 'The directory of the original files here';
check = zeros(length(ratio),nFiles,4);
 
% Filtrates all files with all filtration levels
for i = 1:length(ratio)
    % Cutoff level (-3 dB) for the current level of the main filter,
    % in terms of ratio
    Lc = 10^((dB(i)-3)/20);
   
    % Magnitude array for the main filter
    % Order relates to the placement of frequencies in array f
    % Magnitude depends on the current ratio in the array ratio(i)
    m = [1, 1, Lc, ratio(i), ratio(i), ratio(i), Lc, 1, 1, 0.708, 0, 0];
    
    % Constructs the main filter
    h = fir2(n,f,m);

    % Makes a folder to store all files with same filtration
    mkdir(directory, num2str(100 + i - 1));

    % Cycles through all the files and filter them with the same filter
    for j = 1:nFiles
        % Loads the file
        % Here you can change the nameformat of the files
        filenameRead = [directory 'Tal' num2str(100 + j - 1) '.wav'];
        [y,Fs] = audioread(filenameRead);

        % RMS check all frequencies
        check(i,j,1) = 20*log10(rms(y));                   % RMS dB FS
        % RMS check converted to dB SPL
        check(i,j,2) = 20*log10(rms(y*levelDiffLinear));   % RMS dB SPL
        % RMS check the part that will be filtered, dB SPL
        check(i,j,3) = 20*log10(rms(conv(bandpass,y*levelDiffLinear)));
        
        % Applying main filter
        fW = filter(h,1,y);                 % Filtrerad wave

        % RMS check all frequencies after using main filter
        check(i,j,4) = 20*log10(rms(fW));                  % RMS dB FS
        % RMS check all frequencies converted to dB SPL
        check(i,j,5) = 20*log10(rms(fW*levelDiffLinear));  % RMS dB SPL
        % RMS check validating the part that has been filtered, dB SPL
        check(i,j,6) = 20*log10(rms(conv(bandpass,fW*levelDiffLinear)));
        
        % Saves filtered wave to file
        % 100 + i - 1 is only used for easier sorting by name
        filenameWrite = [directory num2str(100 + i - 1) ...
            '\Talmod' num2str(100 + j - 1) '.wav'];
        audiowrite(filenameWrite,fW,Fs);

        clear fW
        clear y
    end
    clear h
    clear m
end
% Reshapes the 3d matrix check to a easier to read 2d matrix appendCheck
appendCheck = reshape(check,nFiles*length(ratio),6);