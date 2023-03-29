clear; clc;
Ox_ITC_directories;

%%

Num_ticks = 5;

ns=[12]; % Number of file




% Try load the files specified in ns
for i = 1:length(ns)
    t=0;
    n = num2str(ns(i));
    if numel(n) == 2
        n = strcat('000',n);
    elseif numel(n) ==1
        n = strcat('0000',n);
    elseif numel(n) ==3
        n = strcat('00',n);
    elseif numel(n) ==4
        n = strcat('0',n);
    elseif numel(n) ==5
        n = strcat(n);
    end
    % Construct the string in the format of files generated by Data Vault
    
    display(n);
    
    try
        MM = loadFile_h5(n,data_dir,dv_dir,write_dir);
        exception_list=[];
    catch
        n
        disp('Exception happend');
        cd(script_directory);
        exception_list_new=[exception_list;n];
        exception_list=exception_list_new;
        continue
    end
end

% Plot the figure
T = MM(:,1);  % Time
T_matlab = MM(:,2);  % Matlab datenum
Probe_T = MM(:,3);  % Probe temperature
Pressure = MM(:,4);  % Pressure
Mag_T = MM(:,5);  % Temperature of Magnet
PT1 = MM(:,6);  % Temperature of PT1
PT2 = MM(:,7);  % Temperature of PT2

Numofpoints = size(MM(:,1));
Numofpoints_int = Numofpoints(1,1);
T_RealTime_str = strings(Numofpoints_int);

T_starttime = MM(1,2);
T_endtime = MM(Numofpoints_int,2);
T_title = datetime(T_starttime,'Convertfrom','datenum');
T_titile_str = string(T_title);

TData = linspace(T_starttime,T_endtime,Numofpoints_int); % Create x array

figure(1);
subplot(2,1,1);
plot(TData,Probe_T);
ylabel("Probe T(K)");
title('Start at',T_titile_str)
xlim([T_starttime,T_endtime])
%ax=gca;
%ax.XTick=TData;
x_range = xlim;
X_ticks = linspace(x_range(1),x_range(2),Num_ticks);
xticks(X_ticks)
datetick('x','dd-mmm HH:MM','keepticks');   % Control the format of the xtick
zoom on;
zoomObj = zoom(gcf);
set(zoomObj, 'ActionPostCallback', @myCallback);  % Adjust ticks upon zooming

subplot(2,1,2);
plot(TData,Pressure);
ylabel("Pressure(m)");
xlim([T_starttime,T_endtime])
ax=gca;
ax.XTick=TData;
x_range = xlim;
X_ticks = linspace(x_range(1),x_range(2),Num_ticks);
xticks(X_ticks)
datetick('x','dd-mmm HH:MM','keepticks');
zoom on;
zoomObj = zoom(gcf);
set(zoomObj, 'ActionPostCallback', @myCallback);


figure(2);
subplot(3,1,1);
plot(TData,Mag_T);
ylabel("Magnet T(K)");
xlim([T_starttime,T_endtime])
title('Start at',T_titile_str)
ax=gca;
ax.XTick=TData;
x_range = xlim;
X_ticks = linspace(x_range(1),x_range(2),Num_ticks);
xticks(X_ticks)
datetick('x','dd-mmm HH:MM','keepticks');
zoomObj = zoom(gcf);
set(zoomObj, 'ActionPostCallback', @myCallback);

subplot(3,1,2);
plot(TData,PT1);
ylabel("PT1 temperature(K)");
xlim([T_starttime,T_endtime])
ax=gca;
ax.XTick=TData;
x_range = xlim;
X_ticks = linspace(x_range(1),x_range(2),Num_ticks);
xticks(X_ticks)
datetick('x','dd-mmm HH:MM','keepticks');
zoomObj = zoom(gcf);
set(zoomObj, 'ActionPostCallback', @myCallback);

subplot(3,1,3);
plot(TData,PT2);
ylabel("PT2 temperature(K)");
xlim([T_starttime,T_endtime]);
ax=gca;
ax.XTick=TData;
x_range = xlim;
X_ticks = linspace(x_range(1),x_range(2),Num_ticks);
xticks(X_ticks)
datetick('x','dd-mmm HH:MM','keepticks');
zoomObj = zoom(gcf);
set(zoomObj, 'ActionPostCallback', @myCallback);


% Define a callback function that updates the datetick
function myCallback(obj, evt)
    Num_ticks = 5;
    x_range = xlim;
    X_ticks = linspace(x_range(1),x_range(2),Num_ticks);
    xticks(X_ticks)
    datetick('x', 'dd-mmm HH:MM', 'keepticks');
end



