GP29_directories;
% load('RdBu1000.mat');
%%
preamp_gain=1e-3;


ns=[31]; %


for i = 1:length(ns)
    t=0;
    %     if mod(n,20)==0
    %         disp(n);
    %     end;
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
    display(n);
    try
        MM = loadFile_h5(n,data_dir,dv_dir,write_dir);
        exception_list=[];
    catch
        n
        disp('Exception happend');
        cd(script_directory);
        %        cd(char(strcat(dv_dir, data_dir, '\')));
        exception_list_new=[exception_list;n];
        exception_list=exception_list_new;
        continue
    end
    
    
    idx=MM(:,1);
    idy =MM(:,2);
    field =MM(:,3);
    n0= MM(:,4);
    %     n0_offset=-0.14;
    %     n0=(n0-n0_offset)*c_0;
    p0= 0;
    %     Vb =MM(:,3);
    
    Ix= MM(:,5);
    %
    V_x=MM(:,6);
    V_y=MM(:,8);
    I_y=MM(:,8);
    
    R=(V_x./(Ix));
  
    %     n_el=(1e-4)*Vgate*(5.67e-4)/(1.6e-19);
    %%

    figure(79);
    
    subplot(3,1,[1,2]);
    plot(n0, R)
    hold on;
    title('R_{xx}');
    xlabel('n_0 [V]');
    grid on;
    ylim([-1e3,50e3])
    
    
    
    subplot(3,1,3);
    plot(n0, (Ix))
    hold on;
    title('Current');
    xlabel('n_0 [V]');
    grid on;
    

    figure(555);
     ylim([-1e3,50e3])
    %color_index=round(n_colors*(t-t_min)/(t_max-t_min));
    
    %if color_index==0
    %    color_index=1;
    %end
    line_color=line_colors(color_index,:);
    
    semilogy(n0, R, 'Color',line_color);
    hold on;
    
    
    %
end

figure(555);
colorbar;
colormap(line_colors);
caxis([t_min,t_max]);
ylabel('V_{bottom} [V]');
ylabel('R [Ohm]');


%%
