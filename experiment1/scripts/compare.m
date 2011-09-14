% Before you run this script you need to construct a 26x26
% matrix using the GUI which pops op up if you type:
% ScanMatchInfo = ScanMatch_struct();
% You need to set the threshold to 2 times the standard deviation of the
% saccade sizes, which is calculated by the noiselogtostring.py script.
%
% This script will crosscompare all trials stored
% as strings in a given directory and output
% the results to a specified text file

in_dir = '0016B';
out_file = '0016B_scanmatch_output.txt'

% Create a list of all data files 
listing = dir(in_dir);

% Open the target data file
fid = fopen(out_file, 'w');

% Walk through all files
for fnr = 3:length(listing)
        
    fname = strcat(sprintf('%s/', in_dir), listing(fnr).name);
    
    % Read the contents of the file into two lists
    [TrialID Scanpath] = TextRead(fname, '%s %s');
    
    % Walk through all combinations of scanpaths
    for t1 = 1:length(Scanpath)
        for t2 = 1:length(Scanpath)
            
            % Get the scanpaths
            seq1 = char(Scanpath(t1));
            seq2 = char(Scanpath(t2));
            
            % Get the scanpaths ids
            id1 = char(TrialID(t1));
            id2 = char(TrialID(t2));
            
            % Calculate the score
            Score = ScanMatch(seq1, seq2, ScanMatchInfo);
            
            % Write the score to the output and the file
            s = sprintf('%s %s %s %f\n', fname, id1, id2, Score);
            fwrite(fid, s);           
        end
    end
end

% Close the file
fclose(fid);
