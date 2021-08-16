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
    fig_name = 'roc_0.0-0.6-0.01_isn_isn0_hips_udh_openstego_v2';
%     fig_name = 'None';

    s_base = '/home/zeit/SDB/NiseEngFolder/newFile/forWork/forCooperation/forCVPR2021/ROC_csv/';

    exp_hips = [s_base, 'hips.csv'];
    exp_isn = [s_base, 'isn.csv'];
    exp_udh = [s_base, 'udh.csv'];
    exp_openstego = [s_base, 'openstego.csv'];
    exp_isn0 = [s_base, 'isn0.csv'];

    % Calculate positive rates.
    [x1, y1] = calc_pos_rate(exp_isn, zmin, zmax, zstep, 'cont', 'host');
    [x2, y2] = calc_pos_rate(exp_hips, zmin, zmax, zstep, 'cont', 'host');
    [x3, y3] = calc_pos_rate(exp_udh, zmin, zmax, zstep, 'cont', 'host');
    [x4, y4] = calc_pos_rate(exp_openstego, zmin, zmax, zstep, 'cont', 'host');
    [x5, y5] = calc_pos_rate(exp_isn0, zmin, zmax, zstep, 'forw', 'host');

    % Calculate area under roc curve (AUC).
    auc_isn = trapz(fliplr(x1), fliplr(y1));
    auc_hips = trapz(fliplr(x2), fliplr(y2));
    auc_udh = trapz(fliplr(x3), fliplr(y3));
    auc_openstego = trapz(fliplr(x4), fliplr(y4));
    auc_isn0 = trapz(fliplr(x5), fliplr(y5));
    
    % Draw ROC curve.
    n1 = strcat("ISN", " (", string(auc_isn), ")");
    n2 = strcat("DeepStego", " (", string(auc_hips), ")");
    n3 = strcat("UDH", " (", string(auc_udh), ")");
    n4 = strcat("OpenStego", " (", string(auc_openstego), ")");
    n5 = strcat("ISN\_CVPR", " (", string(auc_isn0), ")");
    disp([n1, n2, n3, n4, n5]);
    
    c1 = [255/255,   0/255, 149/255];
    c2 = [  0/255, 158/255,  89/255]; 
    c3 = [145/255, 136/255, 255/255];
    c4 = [  0/255,   0/255, 255/255];
    c5 = [255/255, 228/255,   0/255];
    c6 = [127/255, 127/255, 127/255];
    draw_roc(...
        [y1;y5;y2;y3;y4], [x1;x5;x2;x3;x4], fig_name, s_savedir, ...
        [n1,n5,n2,n3,n4], [c1;c5;c2;c3;c4;c6]);
    
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
function [fig] = draw_roc(ys, xs, save_img_name, s_savedir, ns, cc)
    sz = size(ys);
    num = sz(1);
    
    % Judge if 'ns' is empty
    sz_names = size(ns);
    num_names = sz_names(1);
    if num_names == 0
        ns = string(1:num);
    end
    
    % Judge if 'cc' is empty
    sz_cc = size(cc);
    num_cc = sz_cc(1);
    if num_cc == 0
        cc = hsv(num+1);
    end
    
    for i = 1:num % Loop Y-values.
        scatter(xs(i,:), ys(i,:), 15, cc(i,:), 'filled', 'DisplayName', ns(i));
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
%         saveas(gcf, [s_savedir, save_img_name, '.jpg']);
        print(gcf, [s_savedir, save_img_name, '.png'], '-dpng', '-r300');
    end
    fig = gcf;
end

