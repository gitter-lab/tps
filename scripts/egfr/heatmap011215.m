% Plot a heatmap of the EGFR phosphoproteomic data

clear

% Load peptide, gene, med, neglog10pval, rep1, rep2, rep3
load ../../phosphorylation-data-sets/McKenna2014/aggregated_replicateABC_tukey_orig_firstprev.mat

times = [0 2 4 8 16 32 64 128];

% Clean peptides that have 0 values at any time point because these lead
% to -log2 fold change that the clustergram can't handle
missing = any(med == 0,2);
fprintf('Cleaning %d peptides with 0 at some time point:\n', sum(missing));
fprintf('%s\n', peptide{missing});
fprintf('Replace 0 median value with the non-zero replicate\n')

% Manually checked that all peptides that have a median 0 value
% have a non-zero replicate at that time point so use that value
% as a pseudo-median instead of the actual median
% Take the max across the three replicates because we already know
% that exactly one replicate will have a non-zero value
pseudoMed = max([rep1(med == 0) rep2(med == 0) rep3(med == 0)],[],2);
% Replace the 0 median values with these pseudo-medians
med(med == 0) = pseudoMed;
if any(any(med == 0))
    error('Still have 0 values after cleaning medians');
end


% Combine gene and peptide labels
labels = strcat(gene, {': '}, peptide);

% Compute log2 fold change
log2fc = log2(bsxfun(@rdivide,med,med(:,1)));

% Create copies for significant peptides only
fprintf('%d significant peptides\n', sum(neglog10pval >= 2));
sig = neglog10pval >= 2;
sigPeptide = peptide(sig);
sigGene = gene(sig);
sigLabels = labels(sig);
sigMed = med(sig,:);
sigLog2fc = log2fc(sig,:);

% Plot the significant time series
% plot(sigLog2fc');

% Create a heat map of all peptides, ignoring the 0 min
% time point where all log2 fold changes are 0
% There are so many unchanging peptides that this plot is not interesting
%cg = clustergram(log2fc(:,2:end),'RowLabels',labels,'ColumnLabels',times(2:end),'Cluster','column','Colormap',redbluecmap,'DisplayRange',2,'DisplayRatio',0.1);

% Create a heat map of the significant peptides, ignoring the 0 min
% time point where all log2 fold changes are 0
sigCg = clustergram(sigLog2fc(:,2:end),'RowLabels',sigLabels,'ColumnLabels',times(2:end),'Cluster','column','Colormap',redbluecmap,'DisplayRange',2,'DisplayRatio',0.1);
addXLabel(sigCg,'Time (min)')
addYLabel(sigCg,'Differentially phosphorylated peptides')

% Obtain the peptide labels in the permuted order after clustering
% Need to flip the label order so that the first element is the top row
% of the figure
sortedSigLabels = flip(get(sigCg, 'RowLabels'));
% Write the sorted labels to a temporary file
fid = fopen('sigPeptideHeatmapLabels_tmp.txt','w');
fprintf(fid,'%s\n',sortedSigLabels{:});
fclose(fid);

% Write the log2 fold changes to a temporary file
% Write the header
fid = fopen('log2FoldChange_tmp.txt','w');
fprintf(fid, 'Peptide');
fprintf(fid, '\t%d min', times(2:end));
fprintf(fid, '\n');
% Write the fold changes for each line
for p = 1:length(peptide)
    fprintf(fid, '%s', peptide{p});
    fprintf(fid, '\t%f', log2fc(p,2:end));
    fprintf(fid, '\n');
end
fclose(fid);