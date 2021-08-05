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
    fig_name = 'roc_0.0-0.6-0.01_isn_hips_udh_openstego_2';
%     fig_name = 'None';

    s_base = '/home/zeit/SDB/NiseEngFolder/newFile/forWork/forCooperation/forCVPR2021/ROC_csv/';

%     exp_hips = [s_base, 'for_roc_hips.csv'];
%     exp_isn = [s_base, 'for_roc_isn.csv'];
%     exp_udh = [s_base, 'for_roc_udh.csv'];
%     exp_openstego = [s_base, 'for_roc_openstego.csv'];
    exp_hips = [s_base, 'hips.csv'];
    exp_isn = [s_base, 'isn.csv'];
    exp_udh = [s_base, 'udh.csv'];
    exp_openstego = [s_base, 'openstego.csv'];

    % Calculate positive rates.
    [x1, y1] = calc_pos_rate(exp_isn, zmin, zmax, zstep, 'cont', 'host');
    [x2, y2] = calc_pos_rate(exp_hips, zmin, zmax, zstep, 'cont', 'host');
    [x3, y3] = calc_pos_rate(exp_udh, zmin, zmax, zstep, 'cont', 'host');
    [x4, y4] = calc_pos_rate(exp_openstego, zmin, zmax, zstep, 'cont', 'host');

    % Calculate area under roc curve (AUC).
    auc_isn = trapz(fliplr(x1), fliplr(y1));
    auc_hips = trapz(fliplr(x2), fliplr(y2));
    auc_udh = trapz(fliplr(x3), fliplr(y3));
    auc_openstego = trapz(fliplr(x4), fliplr(y4));
    disp(['====> AUC ISN: ', string(auc_isn)]);
    disp(['====> AUC HIPS: ', string(auc_hips)]);
    disp(['====> AUC UDH: ', string(auc_udh)]);
    disp(['====> AUC OpenStego: ', string(auc_openstego)]);
    
    % Draw ROC curve.
    draw_roc(...
        [y1;y2;y3;y4], [x1;x2;x3;x4], fig_name, s_savedir, ...
        ["ISN", "HIPS", "UDH", "OpenStego"]);
    
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
function [fig] = draw_roc(ys, xs, save_img_name, s_savedir, li_names)
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
        scatter(xs(i,:), ys(i,:), 15, cc(i,:), 'filled', 'DisplayName', li_names(i));
        hold on;
        plot(xs(i,:), ys(i,:), 'Color', cc(i,:), 'LineStyle', '-', 'LineWidth', 1, 'HandleVisibility', 'off');
        hold on;
    end
    
    % Draw diagonal line.
    x0 = linspace(0,1,30);
    y3 = x0;
    % plot(x0,y3,'Color', cc(end, :), 'LineWidth',1, 'HandleVisibility', 'on', 'DisplayName', 'diagonal'); % Use the 8th HSV color.
    plot(x0,y3,'Color', cc(end, :), 'LineWidth',1, 'HandleVisibility', 'off');
    
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

