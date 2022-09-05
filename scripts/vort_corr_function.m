function corr_functions(data_main_path, data_path)
%data_main_path is the parent directory where the output from simulations 
%is stored. 

%data_main_path/data_path contains a folder named 'data', where the 
%frameXX.json files are.

%run a python script that calculates the vorticity field from the cell
%centre-of-mass velocities; the files will be saved in /data/w_field and
%will follow the pattern w_frameXXX_data_path
command = strcat('python3', {' '}, 'vort.py', {' '}, ...
    data_main_path, data_path, '/data/', {' '}, data_path)
system(command{1});

basedir = pwd;
addpath(basedir);

cd(strcat(data_main_path, data_path, '/data/w_field')) 

dinfo = dir(pwd);
names = {dinfo.name};

n_frames = (length(names)-2)

extra_plots = 0;

%labelling settings
set(groot,'defaultAxesTickLabelInterpreter','latex')
set(groot,'defaulttextinterpreter','latex')
set(groot,'defaultlegendinterpreter','latex')

for i = 1:n_frames
    %Import vorticity data
    namew = cell2mat(names(2 + i));             
    frame_index = str2num(namew(11:13));
        
    w = readmatrix(namew);               
    L = size(w);
    
    if i == 1        
        cwwtot = zeros(2*L(1)-1, 2*L(1) -1, n_frames);        
        wtot = zeros(L(1), L(2), n_frames);        
    end
    
    %vorticity autocorrelation function
    cwwtot(:,:,i) = normxcorr2(w,w);
    %array from which the average vorticity is calculated    
    wtot(:, :, i) = w(:, :);
            
end 

if extra_plots == 1    
    %vorticity autocorrelation function as a function of x and y
    figure(1)    
    contour(mean(cwwtot, 3), 100)
    colorbar
    title('cww')       
end
    %this section calculates the polar radial coordinate r from the cartesian
    %ones and bins cww according to r
    %this determines the maximum radial shift for the radial version of
    %cww; if s is too large, the periodic boundary conditions lead to
    %spurious long-distance correlations
    s = floor(sqrt(L(1)*L(2))/2);
        
    cwwradialtot = zeros(s+1,n_frames);
    
    rmat0 = linspace(0, s, s+1)';
    
    %p goes through all frames under consideration so that the final result
    %is averaged over time.
    for p=1:n_frames
        n = zeros(s+1, 1);
        %i and j cycle over x and y
        for i=1:L(1)
            for j = 1:L(2)
                %radial distance from the centre of the box
                k = floor(sqrt((i - L(1))^2 + (j - L(2))^2));               
 
                if k > s
            
                else                    
                    cwwradialtot(k+1, p) = cwwradialtot(k+1, p) + cwwtot(i, j, p);                    
                    n(k+1) = n(k+1) + 1;    
                end                                      
            end
        end
                
        cwwradialtot(:, p) = cwwradialtot(:, p)./n;
        %cwwradialtot is average over the values encountered in the
        %particular bin
    end
    
    %average of cww over all frames and standard deviation
    cwwradialmean = mean(cwwradialtot, 2);        
    stdcwwradial = std(cwwradialtot, 1, 2);            
    
    %this section interpolates cww and locates its extrema
    interpcww = @(xq) interp1(rmat0, cwwradialmean, xq,'spline');
    derivcww = gradient(interpcww(rmat0));
    interpderivcww = @(xq) interp1(rmat0, derivcww, xq,'spline');

    rextrcww = []; cwwradialextr = [];
    format long
    for i = 1:length(rmat0)        
                
        [zerodcww,~,~,~] = fzero(interpderivcww, rmat0(i));
        
        if isempty(rextrcww(round(rextrcww, 2)==round(zerodcww, 2))) && ...
                zerodcww > 1
             %r values of the extrema
             rextrcww = [rextrcww, zerodcww];
             %values of cww at the extrema
             cwwradialextr = [cwwradialextr, interpcww(zerodcww)];
        else
        end
    end
    
    cd ../..;
    if ~exist('plots', 'dir')
       mkdir('plots')
    end
    
    cd 'plots';     
    
    %write the generated data to csv files
    csvwrite('cwwradialmean.csv', cwwradialmean);           
    csvwrite('stdevradialmean.csv', stdcwwradial);           
           
    csvwrite('cwwradialmean_extr_r.csv', rextrcww);
    csvwrite('cwwradialmean_extr.csv', cwwradialextr);
               
    %this section calculates the radial distribution of the vorticity w in
    %case it is needed.
    wradialtot = zeros(s+1, n_frames);
    
     for p=1:n_frames
        n = zeros(s+1, 1);
        for i=1:L(1)
            for j = 1:L(2)
        
                k = floor(sqrt((i-L(1)/2)^2 + (j-L(2)/2)^2));             
 
                if k > s
            
                else
                    wradialtot(k+1, p) = wradialtot(k+1, p)  + ...
                        wtot(i, j, p);
                    
                    n(k+1) = n(k+1) + 1;
                end                                      
            end
        end
                
        wradialtot(:,p) = wradialtot(:,p)./n;
    end
            
    wradialmean = mean(wradialtot, 2);
               
    stdwradial = std(wradialtot, 1, 2);       
    
    %plot cww +/- standard deviation, save figure
    fig = figure(100); hold on;
    plot(rmat0, cwwradialmean, 'color','red', ...
        'DisplayName', '$\langle C_{\omega-\omega}\rangle$')    
    plot(rmat0, cwwradialmean+stdcwwradial, 'r--', 'HandleVisibility','off')    
    plot(rmat0, cwwradialmean-stdcwwradial, 'r--', 'HandleVisibility','off')  
    plot(rextrcww, cwwradialextr, 'kx', 'HandleVisibility', 'off')
        
    legend; xlabel('$r$');
    saveas(fig, 'cwwradial.png');    
    save_and_close(fig, 'cwwradial.fig');
    
    %plot wradial +/- standard deviation, save figure
    fig = figure(1000); hold on;
    plot(rmat0, wradialmean,'red');
    plot(rmat0, wradialmean - stdwradial,'--r','HandleVisibility','off')
    plot(rmat0, wradialmean + stdwradial,'--r','HandleVisibility','off')
    
    title('Average $\omega$ radial distribution'); xlabel('r');
    
    saveas(fig, 'wradialmean.png');
    save_and_close(fig, 'wradialmean.fig');        
    
    %Delete the vorticity data at the end - it can be generated again from
    %the velocity data in the frames
    %cd ../data/w_field;
    %delete *.csv;
    rmdir('../data/w_field', 's');
    
    cd(basedir)
end
