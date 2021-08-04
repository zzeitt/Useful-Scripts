%% -----------------------------------------------------------------------
% ██████╗  ██████╗  ██████╗     ██████╗██╗   ██╗██████╗ ██╗   ██╗███████╗
% ██╔══██╗██╔═══██╗██╔════╝    ██╔════╝██║   ██║██╔══██╗██║   ██║██╔════╝
% ██████╔╝██║   ██║██║         ██║     ██║   ██║██████╔╝██║   ██║█████╗  
% ██╔══██╗██║   ██║██║         ██║     ██║   ██║██╔══██╗╚██╗ ██╔╝██╔══╝  
% ██║  ██║╚██████╔╝╚██████╗    ╚██████╗╚██████╔╝██║  ██║ ╚████╔╝ ███████╗
% ╚═╝  ╚═╝ ╚═════╝  ╚═════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝
%
% Author:   zeit
% Date:     2021-08-03
% Detail:   Calculate the positive rates, then draw the receiver operating 
%           characteristic (ROC) curve.
% License:  MIT License
% ------------------------------------------------------------------------

my_main()


%% ------------- Main -----------------
function [] = my_main()
    clear all; close all; clc;
    zmin = 0.0;
    zmax = 0.6;
    zstep = 0.01;
    s_savedir = './figures/';

    s_base = '/home/zeit/';

    exp_hips = [s_base, 'for_roc_hips.csv'];
    exp_isn = [s_base, 'for_roc_isn.csv'];

    [x1, y1] = calc_pos_rate(exp_isn, zmin, zmax, zstep, 'cont', 'host');
    [x2, y2] = calc_pos_rate(exp_hips, zmin, zmax, zstep, 'cont', 'host');

    draw_roc([y1;y2], x2, 'roc_0.0-0.6-0.01_isn_hips', s_savedir, ["isn", "hips"]);
end


%% -------- Calc Positive Rate --------
function [fprs, tprs]=calc_pos_rate(fname, zmin, zmax, zstep, kw_c, kw_h)
    tbl = readtable(fname);
    lbl = tbl.FileName;
    pred = tbl.Fusion_mean_;
    c = [lbl, num2cell(pred)];
    fprs = [];
    tprs = [];
    for thr = zmin:zstep:zmax
        ntp = length(find(contains(c(:,1), kw_c) & cell2mat(c(:,2))>thr));
        nfp = length(find(contains(c(:,1), kw_h) & cell2mat(c(:,2))>thr));
        nfn = length(find(contains(c(:,1), kw_c) & cell2mat(c(:,2))<thr));
        ntn = length(find(contains(c(:,1), kw_h) & cell2mat(c(:,2))<thr));
        fpr = nfp ./ (nfp + ntn);
        tpr = ntp ./ (ntp + nfn);
        fprs = [fprs, fpr];
        tprs = [tprs, tpr];
    end
end


%% --------- Draw ROC curve ----------
function [fig] = draw_roc(ys, x, save_img_name, s_savedir, li_names)
    sz = size(ys);
    num = sz(1);
    
    % Judge if 'li_names' is empty
    sz_names = size(li_names);
    num_names = sz_names(1);
    if num_names == 0
        li_names = string(1:num);
    end
        
    cc = hsv(num+1);
    for i = 1:num % Loop Y-values.
        scatter(x, ys(i,:), 15, cc(i,:), 'filled', 'DisplayName', li_names(i));
        hold on;
        plot(x, ys(i,:), 'Color', cc(i,:), 'LineStyle', '-', 'LineWidth', 1, 'HandleVisibility', 'off');
        hold on;
    end
    
    % Draw diagonal line.
    x3 = linspace(0,1,30);
    y3 = x3;
    % plot(x3,y3,'Color', cc(end, :), 'LineWidth',1, 'HandleVisibility', 'on', 'DisplayName', 'diagonal'); % Use the 8th HSV color.
    plot(x3,y3,'Color', cc(end, :), 'LineWidth',1, 'HandleVisibility', 'off');
    
    % Set legend.
    lgd = legend;
    set(lgd, 'FontSize', 11, 'Fontname', 'STSong', 'FontWeight', 'Bold', 'Location', 'southeast');
    
    % Set ticks.
    xlim([0, 1]);
    xticks(0:0.1:1);
    xlb = xlabel('False Positive Rate', 'FontSize', 13, 'Fontname', 'STSong', 'FontWeight', 'bold');
    
    ylim([0, 1]);
    yticks(0:0.1:1);
    ylb = ylabel('True Positive Rate', 'FontSize', 13, 'Fontname', 'STSong', 'FontWeight', 'bold');
    pbaspect([1,1,1]);
    
    box on;
    grid on;
    if ~strcmp(save_img_name, 'None')
        mkdir(s_savedir);
        saveas(gcf, [s_savedir, save_img_name, '.jpg']);
    end
    fig = gcf;
end

