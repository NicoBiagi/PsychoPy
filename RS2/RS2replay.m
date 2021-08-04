% Clear the workspace and the screen
close all;
clear all;
clc;
sca;
rng('default');
rng('shuffle');
commandwindow;
% Initialize variables.
filename = 'C:\Users\zj903545\OneDrive - University of Reading\PhD\Undergraduate Project\2nd Project\Script\TMS Muller-Lyer\DATA\PPT\RS2-ID-8.csv';
delimiter = ',';
startRow = 2;

formatSpec = '%f%f%f%f%f%f%f%C%C%f%f%f%[^\n\r]';

% Open the text file.
fileID = fopen(filename,'r');

% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');

% Close the text file.
fclose(fileID);

% Create output variable
data = table(dataArray{1:end-1}, 'VariableNames', {'time','xp','yp','ps','trial_num','ML_on','ID','session','TMS_area','wing_type','stim_loc','shft_len'});

% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans;
%%
% Hide the cursor
HideCursor();

%Calling a function with all the screen settings
AFCScreenSettings;

% Define black and white (white will be 1 and black 0). This is because
% luminace values are (in general) defined between 0 and 1.
% For help see: help WhiteIndex and help BlackIndex
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = white / 2;

% reduce white brightness  to 80%
white = white/1.25;

% number of pixels per DOVA (from ViewPixx)
pixPerDeg = 42.2238;

%Set the size of the red/white rect
RedRectDeg = 0.5; %degrees
RectPix = round(RedRectDeg * pixPerDeg);

% make sure that the Pix dimension is an even number
if mod(RectPix,2)==1
    RectPix = RectPix+1;
end

% Make a base Rect
baseRect = [0 0 RectPix RectPix];

% get the all screen coordinates
allScreen = [0 0 screenXpixels screenYpixels];

% Set the color of the rect to red
rectColor2 = [1 0 0];
rectColor = WhiteIndex(screenNumber);

% Get the size in mm of the screen
[width, height]=Screen('DisplaySize', screenNumber);

% Get the refresh rate of the screen
hertz = FrameRate(window);

% Length of time and number of frames we will use for each drawing test
numSecs = 1;
numFrames = round(numSecs / ifi);
waitframes = 1;
numSecsFix = 1.2;
numFramesFix = round(numSecsFix / ifi);

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;
time = 0;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);

%setting the keyboard
KbName('UnifyKeyNames');
KbQueueCreate(); %0 is main keyboard
KbQueueStart();
escapeKey = KbName('ESCAPE');
leftKey = KbName('LeftArrow');
rightKey = KbName('RightArrow');
Space=KbName('space');
% Draw text in the middle of the screen in Times in white
Screen('TextSize', window, 100);
Screen('TextFont', window, 'Times');
DrawFormattedText(window, 'Welcome to the experiment', 'center', 'center', white);
% Draw text in the bottom of the screen in Times in white
Screen('TextSize', window, 50);
Screen('TextFont', window, 'Times');
DrawFormattedText(window, 'Press any key to continue', 'center',...
    screenYpixels * 0.85, white);

% Flip to the screen
Screen('Flip', window);

KbWait;
WaitSecs(0.2);

% get the number of trials
trials = unique( data.trial_num );

% get the id and convert it to char
ids = unique(data.ID);
ID= num2str(ids);

% get the session and convert it to string
session =unique(data.session);

% get the tms_area and convert it to string
tms = unique(data.TMS_area);

% start the timer
tic

% loop through each TMS area
for z = 2
    
    % select the TMS area
    subset2_idx = data.TMS_area == tms(z);
    
    % slice the data so that just the eye location recorded during this
    % TMS area are selected
    subset2 = data(subset2_idx, :);
    
    % loop through each session
    for t = 1:length(session)
        
        % select the session
        subset1_idx = subset2.session == session(t);
        
        % slice the data so that just the eye location recorded during this
        % session are selected
        subset1 = subset2(subset1_idx, :);
        
        % loop through each trial
        for x =1:length(trials)
            
            % select the trial number
            index = subset1.trial_num == x;
            
            % slice the data so that just the eye location recorded during this
            % trial are selected
            subset = subset1(index, :);
            
            % get the x-cooridnate
            xpos = subset.xp;
            
            % get rid of the last 25% of the data (end of trial)
            remove = (round(length(xpos)*0.75));
            xpos(remove:end) = [];
            
            % select 1 sample every 10
            xpos = xpos(2:10:end,:);
            
            % get the y-cooridnate
            ypos = subset.yp;
            
            % get rid of the last 25% of the data (end of trial)
            ypos(remove:end)=[];
            
            % select 1 sample every 10
            ypos = ypos(2:10:end,:);
            
            % get the wing_type of the stimulus used in this trial
            wing = unique(subset.wing_type);
            
            % get the direction of the stimulus in this trial
            direction = unique(subset.stim_loc);
            
            % get the length of the stimulus in this trial
            shft_len = unique(subset.shft_len);
            
            TMS=string(unique(subset.TMS_area));
            
            SES=string(unique(subset.session));
            
            % create a prefix
            prefix = string('ID');
            
            % combine the string together
            str1 = prefix + ' ' + ID + ' ' + TMS + ' ' + SES;
            
            % convert the string to char
            str1 = char(str1);
            
            % use this in case you need to end presentation before natural end
            exitDemo = false;
            
            while exitDemo == false
                
                for xx = 1:length(xpos)
                    % Check the keyboard to see if a button has been pressed
                    [keyIsDown,secs, keyCode] = KbCheck;
                    
                    % Depending on the button press, either move the position of the
                    % rectangle or exit the script
                    if keyCode(escapeKey)
                        exitDemo = true;
                        %if the press the esc button they stop the experiment
                        sca;
                    end
                    
                    % x-coordinate
                    X = xpos(xx);
                    
                    % y-coordinate
                    Y = ypos(xx);
                    
                    % wing_type
                    WING = wing;
                    
                    % direction
                    DIRECTION = direction;
                    
                    % shaft length
                    SHFT_LEN = shft_len;
                    
                    % Draw the eye position as a square
                    EyePosition = CenterRectOnPointd(baseRect, X, Y);
                    
                    % based on the location of the stimulus draw the end of the
                    % horizontal line of the stimulus
                    if  DIRECTION == -1
                        stim_end_x = round(xCenter - ( 2* pixPerDeg * SHFT_LEN));
                        
                    elseif DIRECTION == 0
                        stim_end_x = round(xCenter + ( 2* pixPerDeg * SHFT_LEN));
                    end
                    
                    % y- coordinate for the end of the horizontal line of the
                    % stimulus
                    stim_end_y = 540;
                    
                    % draw the end of the horizontal line of the
                    % stimulus as a grey square
                    StimEnd = CenterRectOnPointd(baseRect, stim_end_x, stim_end_y);
                    
                    % convert the trial number to char
                    sc= num2str(x);
                    
                    % draw the eye position on the screen
                    Screen('FillRect', window, rectColor, EyePosition);
                    
                    % draw the end of the horizontal line of the
                    % stimulus on the screen
                    Screen('FillRect', window, grey, StimEnd);
                    
                    Screen('TextSize', window, 50);
                    Screen('TextFont', window, 'Times');
                    % draw trial number on the screen
                    DrawFormattedText(window, sc, 'center',screenYpixels * 0.85, white);
                    DrawFormattedText(window, 'trial n:', xCenter * 0.75 ,screenYpixels * 0.85, white);
                    % draw reminder of participant ID, session, and TMS location on
                    % the screen
                    DrawFormattedText(window, str1, xCenter * 0.15 ,yCenter * 0.15, white);
                    
                    % Flip to the screen
                    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
                end
                KbWait;
                exitDemo = true;
            end
            Screen('TextSize', window, 50);
            Screen('TextFont', window, 'Times');
            % draw reminder of participant ID, session, and TMS location on
            % the screen
            DrawFormattedText(window, str1, xCenter * 0.15 ,yCenter * 0.15, white);
            DrawFormattedText(window, 'END OF TRIAL', 'center','center', white);
            vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
            % Wait 0.2 second
            WaitSecs(0.2);
        end
        Screen('TextSize', window, 50);
        Screen('TextFont', window, 'Times');
        % draw reminder of participant ID, session, and TMS location on
        % the screen
        DrawFormattedText(window, str1, xCenter * 0.15 ,yCenter * 0.15, white);
        DrawFormattedText(window, 'END OF SESSION', 'center','center', white);
        vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
        % Wait 0.2 second
        KbWait;
    end
    Screen('TextSize', window, 50);
    Screen('TextFont', window, 'Times');
    % draw reminder of participant ID, session, and TMS location on
    % the screen
    DrawFormattedText(window, str1, xCenter * 0.15 ,yCenter * 0.15, white);
    DrawFormattedText(window, 'END OF TMS AREA', 'center','center', white);
    vbl  = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    % Wait 0.2 second
    KbWait;
    
end

% Clear the screen
sca;
ShowCursor();

toc