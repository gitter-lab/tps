% Plot a heatmap of the EGFR phoshoproteomic data

clear

% Load peptide, gene, med, neglog10pval
load ../../phosphorylation-data-sets/McKenna2014/aggregated_replicateABC_tukey_orig_firstprev.mat

times = [0 2 4 8 16 32 64 128];

fprintf('%d significant peptides before filtering\n', sum(neglog10pval >= 2));

% Remove peptides that have 0 values at any time point because these lead
% to -log10 fold change that the clustergram can't handle
missing = any(med == 0,2);
fprintf('Removing %d peptides with 0 at some time point:\n', sum(missing));
fprintf('%s\n', peptide{missing});

peptide(missing) = [];
gene(missing) = [];
med(missing,:) = [];
neglog10pval(missing) = [];

% Combine gene and peptide labels
labels = strcat(gene, {': '}, peptide);

% Compute log2 fold change
log2fc = log2(bsxfun(@rdivide,med,med(:,1)));

% Create copies for significant peptides only
fprintf('%d significant peptides after filtering\n', sum(neglog10pval >= 2));
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
