# -*- coding: utf-8 -*-
"""
Utility functions for processing Wolf-Yadlin EGFR proteomic data.
Created on 1/12/15

editited (for python 3) by Adam Shedivy 05/22/2020

@author: Anthony Gitter
"""

from collections import defaultdict
from functools import partial
import itertools
import numpy as np
import pandas as pd

# A copy of PrepTemporalCytoscape that is modified to work with TPS input
# and output files
# TODO: make the log transformation more robust, handle 0s without requiring
# a default value


def PrepTemporalCytoscapeTPS(peptideMapFile, timeSeriesFile, peptideFirstScoreFile,
                             peptidePrevScoreFile, windowsFile, networkFile,
                             goldStandardFile, pvalThresh, logTransform,
                             styleTemplateFile, outAnnotFile, outStyleFile,
                             logDefault=-1.0, addZero=False, repairMissing=False):
    """Merges multiple data sources to prepare an annotation table for proteins
    that can be imported into Cytoscape to display temporal information
    about the network.

    Input:
    peptideMapFile - TPS input peptide to protein mapping, does not yet support
    mapping to multiple proteins
    timeSeriesFile - TPS input file with peptide time series
    peptideFirstScoreFile - TPS input file with peptide significance scores
    when comparing to first time point
    peptidePrevScoreFile - TPS input file with peptide significance scores
    when comparing to previous time point
    windowsFile - TPS output file with activity windows
    networkFile -TPS output sif file with network edges
    goldStandardFile - list of proteins in the gold standard reference pathway
    pvalThresh - p-value threshold to apply to TPS input first and prev score
    files, peptides with p-value <= the threshold are significant, set to
    1E-10 if less than 1E-10
    logTransform - Boolean, if true take log2 of the time series data
    styleTemplateFile - a Cytoscape style file template
    outAnnotFile - filename of the Cytoscape annotation file to write
    outStyleFile - filename of the Cytoscape style file
    logDefault - default value to use instead of log2(0) when taking the log
    transform, defaults to -1.0 if a value is not provided
    addZero - prepend a 0 to the peptide time series
    repairMissing - fill in values for missing data; if the first time point is
    missing, set it to 1 if logTransform is True or 0 otherwise; if later time
    points are missing, set them to the previous observed time point

    Return:
    pepsPerProt - a list of the peptides counts for each protein
    """
    pvalThresh = max(pvalThresh, 1E-10)

    # Load a map from peptides to the protein (UniProt id) associated with them
    pep2Prot = dict()
    with open(peptideMapFile) as f:
        # Skip the header
        next(f)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 2:
                raise RuntimeError(
                    "All peptide id map lines must have 2 columns\n%s" % line)
            assert not "|" in parts[1], "Do not yet support peptides mapping to multiple protiens"
            pep2Prot[parts[0]] = parts[1]

    print("Loaded protein id map for %d peptides" % len(pep2Prot))

    # Load a map from peptides to their prize
    # Returns -log10(min p-value)
    peptidePrizeDf = LoadScores(peptideFirstScoreFile, peptidePrevScoreFile)
    # Could work with data frame directly, but convert to dict to reuse old code
    # The peptide id has already been set as the index
    pep2Prize = peptidePrizeDf["prize"].to_dict()
    sigThresh = -np.log10(pvalThresh)

    print("Loaded prizes for %d peptides" % len(pep2Prize))
    print("%d peptides with significant prizes (>= %d)" %
          (len([p for p in pep2Prize.values() if p >= sigThresh]), sigThresh))

    defaultFirstValue = '0'
    if logTransform:
        print("Using default value of %f for log2(0)" % logDefault)
        # Set that value that will be used as the first value in the time
        # series if it is missing
        defaultFirstValue = '1'
    # A wrapper function that returns the default if we try to take log2(0)
    robustLog = partial(RobustLog2, default=logDefault)

    # Load the phosphorylation time series.  Create three maps from a protein
    # to a list of peptide time series (string representation of a list of
    # floats) associated with that protein.  One contains all peptides, one
    # contains the subset of significant peptides, the only contains the
    # insignificant peptides.
    # prot2TimeSeries map from proteins to all peptide time series is only needed
    # to create the pepsPerProt statistics but is not written in the output file
    prot2TimeSeries = {"all": defaultdict(list),
                       "sig": defaultdict(list),
                       "insig": defaultdict(list)}
    # Track the global max and min for the Cytoscape style file
    timeSeriesMin = np.Infinity
    timeSeriesMax = np.NINF
    print('timeseries min {}'.format(timeSeriesMin))
    print('timeseries max {}'.format(timeSeriesMax))
    with open(timeSeriesFile) as f:
        # Use the header to get the expected number of columns
        header = next(f).strip().split("\t")
        numCols = len(header)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != numCols:
                raise RuntimeError(
                    "All peptide time series lines must have %d columns\n%s" % (numCols, line))
            prot = pep2Prot[parts[0]]

            timeSeries = parts[1:]
            print('init timeSeries {}'.format(timeSeries))
            # Replace missing values if necessary
            if repairMissing:
                timeSeries = RepairMissingData(timeSeries, defaultFirstValue)

            # Create a string representation of the time series that Cytoscape can parse
            if logTransform:
                timeSeries, timeSeriesMinq, timeSeriesMaxq = map(robustLog, map(float, timeSeries)), map(
                    robustLog, map(float, timeSeries)), map(robustLog, map(float, timeSeries))
            else:
                timeSeries, timeSeriesMinq, timeSeriesMaxq = map(float, timeSeries), map(float, timeSeries), map(float, timeSeries)

#             print('timeSeries max: ', max(timeSeriesMax))
#             # print('timeSeries after map {}'.format(timeSeries))
#             print('timeSeries min: ', min(timeSeriesMin))

            timeSeriesMin = min(timeSeriesMin, min(timeSeriesMinq))
            timeSeriesMax = max(timeSeriesMax, max(timeSeriesMaxq))
            timeSeries = ", ".join(map(str, timeSeries))

            if addZero:
                timeSeries = "0, " + timeSeries

            # All peptide time series are added to the "all" map
            prot2TimeSeries["all"][prot].append(timeSeries)
            # Use the peptide prize to determine whether to add the time series
            # to the significant or insignificant map
            # All peptides with a time series should have a prize in this map
            if pep2Prize[parts[0]] >= sigThresh:
                prot2TimeSeries["sig"][prot].append(timeSeries)
            else:
                prot2TimeSeries["insig"][prot].append(timeSeries)

    print("Loaded time series for %d proteins (and pseudonodes)" %
          len(prot2TimeSeries["all"]))
    # Only some datasets need an initial 0 value to be added, some may already
    # include it
    if addZero:
        print("Added 0 to the start of every time series")
    print("Min value in time series: %f" % timeSeriesMin)
    print("Max value in time series: %f" % timeSeriesMax)

    # Statistics on the peptide to protein mappings for all, significant,
    # and significant peptides
    pepsPerProt = dict()
    for timeSeriesType in prot2TimeSeries.keys():
        pepsPerProt[timeSeriesType] = map(
            len, prot2TimeSeries[timeSeriesType].values())
#     print("Mean peptides per protein: %f" % np.mean(pepsPerProt["all"]))
#     print("Max peptides per protein: %d" % max(pepsPerProt["all"]))
#     print("Max significant peptides per protein: %d" % max(pepsPerProt["sig"]))
#     print("Max insignificant peptides per protein: %d" %
#           max(pepsPerProt["insig"]))

    # Load and summarize the temporal activity windows
    # The map from proteins to all windows maps to a list where there is a set
    # of inferred activity states for each time point/window.  These are
    # collapsed later
    prot2AllWindows = dict()
    with open(windowsFile) as f:
        # Use the header to get the time points of the activity windows
        header = next(f).strip().split("\t")
        numCols = len(header)
        times = header[1:]
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != numCols:
                raise RuntimeError(
                    "All activity window lines must have %d columns\n%s" % (numCols, line))
            # The protein id may be followed by the peptide id
            prot = parts[0].split("#")[0]
            windows = prot2AllWindows.setdefault(
                prot, [set() for i in range(len(times))])
            for i, state in enumerate(parts[1:]):
                windows[i].add(state)

    print("Loaded activity windows for %d proteins" % len(prot2AllWindows))

    # Summarize the temporal activity windows and convert them to a numerical
    # format.  Also store the time point when the protein is first active
    # (activation/inhibition/ambiguous state)
    prot2WindowsSummary = dict()
    prot2FirstActive = dict()
    for prot in prot2AllWindows.keys():
        prot2WindowsSummary[prot] = map(ConvertWindowState, map(
            SummarizeWindow, prot2AllWindows[prot]))
        prot2FirstActive[prot] = FirstActiveGeneral(
            prot2WindowsSummary[prot], times)

    # Load the list of gold standard proteins
    goldStandard = set()
    with open(goldStandardFile) as f:
        # No header
        for line in f:
            goldStandard.add(line.strip().upper())

    print("Loaded %d gold standard reference pathway proteins" %
          len(goldStandard))

    # Load the list of pathway members
    networkProts = set()
    with open(networkFile) as f:
        # No header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                raise RuntimeError(
                    "All network lines must have 3 columns\n%s" % line)
            networkProts.add(parts[0])
            networkProts.add(parts[2])

    print("Loaded %d proteins on the synthesized pathway" % len(networkProts))

    # Ensure all proteins in the pathway have activity windows
    if not len(networkProts) == len(networkProts.intersection(prot2AllWindows.keys())):
        raise RuntimeError(
            "All synthesized pathway members must have an activity window")

    # Write the output file which contains one line per protein with all annotations
    sigPepCols = max(pepsPerProt["sig"])
    insigPepCols = max(pepsPerProt["insig"])
    timepoints = len(times)
    steinerCount = 0
    sigPrizeCount = 0
    insigPrizeCount = 0
    with open(outAnnotFile, "w") as f:
        # NodeType column shows whether the protein was a prize node, Steiner
        # node, or excluded form the netowrk.  Only pertains to nodes in the
        # sythesized pathway summary.  If a prize node, specifies whether the
        # maximum peptide prize for that protein is significant or not.
        f.write("Protein\tNodeType\t")
        # Write whether the protein is in the gold standard pathway
        f.write("ReferencePathway\t")
        # The header has one column for each peptide time series where there
        # are enough columns for the maximum number of peptides mapped to a protein
        # Split significant and insignificant peptides into separate attributes
        # so they can be drawn with different colors
        f.write("%s\t" % "\t".join(["SigPeptide%d" %
                                    (i+1) for i in range(sigPepCols)]))
        f.write("%s\t" % "\t".join(["InsigPeptide%d" %
                                    (i+1) for i in range(insigPepCols)]))
        # # There is one column for each activity window summary
        # f.write("%s\t" % "\t".join(
        #     ["ActivitySummary%s" % time for time in times]))
        # # One column for the first time a protein is active
        # f.write("FirstActive\t")
        # # There is one column for T-1 timepoints that are used to fill in blank
        # # rows in the heat map
        # f.write("%s" % "\t".join(["HeatMapBg%d" % (i+1)
        #                           for i in range(timepoints-1)]))
        f.write("\n")

        allProts = set(itertools.chain(
            prot2TimeSeries["all"].keys(), prot2WindowsSummary.keys()))
        for prot in sorted(allProts):
            f.write("%s\t" % prot)
            # Write whether the protein is a prize node, Steiner node, or
            # not in the network
            if prot in networkProts:
                # Test above assures that all proteins on the synthesized
                # pathway have an activity window
                if prot in prot2TimeSeries["sig"]:
                    f.write("SigPrize")
                    sigPrizeCount += 1
                elif prot in prot2TimeSeries["insig"]:
                    f.write("InsigPrize")
                    insigPrizeCount += 1
                else:
                    f.write("Steiner")
                    steinerCount += 1
            else:
                # Proteins that were excluded from either the Steiner forest
                # or the pathway synthesis
                f.write("Excluded")

            # Write whether the protein is on a reference pathway
            if prot in goldStandard:
                f.write("\ttrue")
            else:
                f.write("\tfalse")

            # Write the significant time series that map to this protein in an arbitrary order
            padCols = sigPepCols - \
                len(prot2TimeSeries["sig"].setdefault(prot, []))
            if padCols < sigPepCols:
                f.write("\t")
            f.write("\t".join(prot2TimeSeries["sig"][prot]))
            # Write empty values in the columns if there are fewer than the
            # max number of peptides for this protein
            if padCols > 0:
                f.write("".join(itertools.repeat("\t", padCols)))

            # Write the insignificant time series that map to this protein in an arbitrary order
            padCols = insigPepCols - \
                len(prot2TimeSeries["insig"].setdefault(prot, []))
            if padCols < insigPepCols:
                f.write("\t")
            f.write("\t".join(prot2TimeSeries["insig"][prot]))
            # Write empty values in the columns if there are fewer than the
            # max number of peptides for this protein
            if padCols > 0:
                f.write("".join(itertools.repeat("\t", padCols)))

            # # Write the activity window summary
            # windowSummary = prot2WindowsSummary.setdefault(
            #     prot, itertools.repeat("", timepoints))
            # f.write("\t%s\t" % "\t".join(windowSummary))

            # # Write the first active time point
            # f.write("%s\t" % prot2FirstActive.setdefault(prot, "Not active"))

            # # Write the heat map background fill columns
            # fill = ", ".join(itertools.repeat("0", timepoints))
            # f.write("\t".join(itertools.repeat(fill, timepoints-1)))
            f.write("\n")

    print("Wrote attributes for %d Steiner nodes in the TPS pathway" % steinerCount)
    print("Wrote attributes for %d prize nodes in the TPS pathway with a significant peptide" % sigPrizeCount)
    print("Wrote attributes for %d prize nodes in the TPS pathway with no significant peptides" % insigPrizeCount)
    print("Wrote attributes for %d proteins excluded by PCSF or TPS" %
          (len(allProts) - (steinerCount + sigPrizeCount + insigPrizeCount)))

    # Read the entire file, then use string replacement to substitute
    # the placeholder text with actual values
    with open(styleTemplateFile) as f:
        styleContents = f.read()

    # Replace the following placeholder strings
    # $$$_MIN_VALUE_$$$
    styleContents = styleContents.replace(
        "$$$_MIN_VALUE_$$$", str(timeSeriesMin))
    # $$$_MAX_VALUE_$$$
    styleContents = styleContents.replace(
        "$$$_MAX_VALUE_$$$", str(timeSeriesMax))
    # $$$_INSIG_COLORS_$$$
    insigColors = ["&quot;#CCCCCC&quot;"] * insigPepCols
    insigColors = ",".join(insigColors)
    styleContents = styleContents.replace("$$$_INSIG_COLORS_$$$", insigColors)
    # $$$_INSIG_COLS_$$$
    insigCols = ",".join(["&quot;InsigPeptide%d&quot;" % (i+1)
                          for i in range(insigPepCols)])
    styleContents = styleContents.replace("$$$_INSIG_COLS_$$$", insigCols)
    # $$$_SIG_COLORS_$$$
    sigColors = ["&quot;#000000&quot;"] * sigPepCols
    sigColors = ",".join(sigColors)
    styleContents = styleContents.replace("$$$_SIG_COLORS_$$$", sigColors)
    # $$$_SIG_COLS_$$$
    sigCols = ",".join(["&quot;SigPeptide%d&quot;" % (i+1)
                        for i in range(sigPepCols)])
    styleContents = styleContents.replace("$$$_SIG_COLS_$$$", sigCols)
    # $$$_HEATMAP_RANGE_$$$
    heatmapCols = ",".join(["-1.0,1.0"] * (2 * timepoints - 1))
    styleContents = styleContents.replace("$$$_HEATMAP_RANGE_$$$", heatmapCols)
    # $$$_REV_ACTIVITY_COLS_$$$
    revActivityCols = ",".join(
        reversed(["ActivitySummary%s" % time for time in times]))
    styleContents = styleContents.replace(
        "$$$_REV_ACTIVITY_COLS_$$$", revActivityCols)
    # $$$_BACKGROUND_COLS_$$$
    bgCols = ",".join(["HeatMapBg%d" % (i+1) for i in range(timepoints-1)])
    styleContents = styleContents.replace("$$$_BACKGROUND_COLS_$$$", bgCols)

    with open(outStyleFile, "w") as f:
        f.write(styleContents)

    return pepsPerProt["all"]


def RobustLog2(val, default):
    """If the value is 0, return the default.  Otherwise return log2(val)."""
    if val == 0:
        return default
    else:
        return np.log2(val)

# Copied from generate_prizes.py in TPS codebase
# Sets a cap on the maximum prize by mapping p-values below 1E-10 to 1E-10
# This allows for p-values that are not real p-values but rather fold change
# threhsolds that were mapped to 0 or 1 "p-values"


def LoadScores(firstfile, prevfile):
    """Load the first and previous scores.  For each peptide, compute a prize
    that is -log10(min p-value across all time points).  Assumes the scores
    are p-values or equivalaent scores in (0, 1].  p-values < 1E-10 are mapped
    to 1E-10.  Do not allow null or missing scores.

    Return: data frame with scores and prize for each peptide
    """
    first_df = pd.read_csv(firstfile, sep="\t",
                           comment="#", header=None, index_col=0)
    prev_df = pd.read_csv(prevfile, sep="\t", comment="#",
                          header=None, index_col=0)
    first_shape = first_df.shape
    assert first_shape == prev_df.shape, "First and previous score files must have the same number of peptides and time points"

    assert not first_df.isnull().values.any(
    ), "First scores file contains N/A values.  Replace with 1.0"
    assert not prev_df.isnull().values.any(
    ), "Previous scores file contains N/A values.  Replace with 1.0"

    print("Loaded {} peptides and {} scores in the first and previous score files".format(
        first_shape[0], first_shape[1]))

    # Merge the two types of scores
    merged_df = pd.concat([first_df, prev_df], axis=1, join="outer")
    merged_shape = merged_df.shape
    assert merged_shape[0] == first_shape[0], "First and previous significance scores contain different peptides"
    assert merged_shape[1] == 2 * \
        first_shape[1], "Unexpected number of significance scores after merging first and previous scores"

    # Compute prizes
    merged_df["prize"] = merged_df.apply(CalcPrize, axis=1)
    return merged_df


def CalcPrize(row):
    """Compute the peptide prize as -log10(min p-value).  If min p-value
    < 1E-10, set it to 1E-10."""
    return -np.log10(max(min(row), 1E-10))


def PrepTemporalCytoscape(peptideMapFile, timeSeriesFile, peptidePrizeFile,
                          windowsFile, goldStandardFile, networkFile, outFile):
    """Merges multiple data sources to prepare an annotation table for proteins
    that can be imported into Cytoscape to display temporal information
    about the network.  Returns a list of the peptides counts for each protein.
    """

    # Load a map from peptides to the protein (UniProt id) associated with them
    pep2Prot = dict()
    with open(peptideMapFile) as f:
        # Skip the header
        next(f)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 2:
                raise RuntimeError(
                    "All peptide id map lines must have 2 columns\n%s" % line)
            pep2Prot[parts[0]] = parts[1]

    print("Loaded protein id map for %d peptides" % len(pep2Prot))

    # Load a map from peptides to their prize
    sigThresh = 2
    pep2Prize = dict()
    with open(peptidePrizeFile) as f:
        # No header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 2:
                raise RuntimeError(
                    "All peptide prize lines must have 2 columns\n%s" % line)
            pep2Prize[parts[0]] = float(parts[1])

    print("Loaded prizes for %d peptides" % len(pep2Prize))
    print("%d peptides with significant prizes (>= %d)" %
          (len([p for p in pep2Prize.values() if p >= sigThresh]), sigThresh))

    # Load the phosphorylation log2 fold changes.  Create three maps from a protein
    # to a list of peptide time series (string representation of a list of
    # floats) associated with that protein.  One contains all peptides, one
    # contains the subset of significant peptides, the only contains the
    # insignificant peptides.
    # prot2TimeSeries map from proteins to all peptide time series is only needed
    # to create the pepsPerProt statistics but is not written in the output file
    prot2TimeSeries = {"all": defaultdict(list),
                       "sig": defaultdict(list),
                       "insig": defaultdict(list)}
    with open(timeSeriesFile) as f:
        # Skip the header
        next(f)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 8:
                raise RuntimeError(
                    "All peptide time series lines must have 8 columns\n%s" % line)
            prot = pep2Prot[parts[0]]
            # Create a string representation of the time series that Cytoscape can parse
            # Add back the 0 value for the 0 min log2 fold change
            timeSeries = "0, " + ", ".join(map(str, map(float, parts[1:])))
            # All peptide time series are added to the "all" map
            prot2TimeSeries["all"][prot].append(timeSeries)
            # Use the peptide prize to determine whether to add the time series
            # to the significant or insignificant map
            # All peptides with a time series should have a prize in this map
            if pep2Prize[parts[0]] >= sigThresh:
                prot2TimeSeries["sig"][prot].append(timeSeries)
            else:
                prot2TimeSeries["insig"][prot].append(timeSeries)

    print("Loaded time series for %d proteins (and pseudonodes)" %
          len(prot2TimeSeries["all"]))

    # Statistics on the peptide to protein mappings for all, significant,
    # and significant peptides
    pepsPerProt = dict()
    for timeSeriesType in prot2TimeSeries.keys():
        pepsPerProt[timeSeriesType] = map(
            len, prot2TimeSeries[timeSeriesType].values())
    print("Mean peptides per protein: %f" % np.mean(pepsPerProt["all"]))
    print("Max peptides per protein: %d" % max(pepsPerProt["all"]))
    print("Max significant peptides per protein: %d" % max(pepsPerProt["sig"]))
    print("Max insignificant peptides per protein: %d" %
          max(pepsPerProt["insig"]))

    # Load and summarize the temporal activity windows
    # The map from proteins to all windows maps to a list where there is a set
    # of inferred activity states for each time point/window.  These are
    # collapsed later
    prot2AllWindows = dict()
    with open(windowsFile) as f:
        # Skip the header
        next(f)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 8:
                raise RuntimeError(
                    "All activity window lines must have 8 columns\n%s" % line)
            # The protein id may be followed by the peptide id
            prot = parts[0].split("#")[0]
            windows = prot2AllWindows.setdefault(
                prot, [set(), set(), set(), set(), set(), set(), set()])
            for i, state in enumerate(parts[1:]):
                windows[i].add(state)

    print("Loaded activity windows for %d proteins" % len(prot2AllWindows))

    # Summarize the temporal activity windows and convert them to a numerical
    # format.  Also store the time point when the protein is first active
    # (activation/inhibition/ambiguous state)
    prot2WindowsSummary = dict()
    prot2FirstActive = dict()
    for prot in prot2AllWindows.keys():
        prot2WindowsSummary[prot] = map(ConvertWindowState, map(
            SummarizeWindow, prot2AllWindows[prot]))
        prot2FirstActive[prot] = FirstActive(prot2WindowsSummary[prot])

    # Load the list of gold standard proteins
    goldStandard = set()
    with open(goldStandardFile) as f:
        # No header
        for line in f:
            goldStandard.add(line.strip().upper())

    print("Loaded %d gold standard EGFR reference pathway proteins" %
          len(goldStandard))

    # Load the list of pathway members
    networkProts = set()
    with open(networkFile) as f:
        # No header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                raise RuntimeError(
                    "All network lines must have 3 columns\n%s" % line)
            networkProts.add(parts[0])
            networkProts.add(parts[1])

    print("Loaded %d proteins on the synthesized pathway" % len(networkProts))

    # Ensure all proteins in the pathway have activity windows
    if not len(networkProts) == len(networkProts.intersection(prot2AllWindows.keys())):
        raise RuntimeError(
            "All synthesized pathway members must have an activity window")

    # Write the output file which contains one line per protein with all annotations
    sigPepCols = max(pepsPerProt["sig"])
    insigPepCols = max(pepsPerProt["insig"])
    timepoints = 7
    steinerCount = 0
    sigPrizeCount = 0
    insigPrizeCount = 0
    with open(outFile, "w") as f:
        # NodeType column shows whether the protein was a prize node, Steiner
        # node, or excluded form the netowrk.  Only pertains to nodes in the
        # sythesized pathway summary.  If a prize node, specifies whether the
        # maximum peptide prize for that protein is significant or not.
        f.write("Protein\tNodeType\t")
        # Write whether the protein is in one of the EGFR gold standards
        # aka EGFR reference pathway
        f.write("ReferenceEGFR\t")
        # The header has one column for each peptide time series where there
        # are enough columns for the maximum number of peptides mapped to a protein
        # Split significant and insignificant peptides into separate attributes
        # so they can be drawn with different colors
        f.write("%s\t" % "\t".join(
            ["SigPeptide%dLog2FC" % (i+1) for i in range(sigPepCols)]))
        f.write("%s\t" % "\t".join(
            ["InsigPeptide%dLog2FC" % (i+1) for i in range(insigPepCols)]))
        # There is one column for each activity window summary
        f.write("%s\t" % "\t".join(
            ["ActivitySummary%dMin" % 2**(i+1) for i in range(timepoints)]))
        # One column for the first time a protein is active
        f.write("FirstActive\t")
        # There is one column for T-1 timepoints that are used to fill in blank
        # rows in the heat map
        f.write("%s" % "\t".join(["HeatMapBg%d" % (i+1)
                                  for i in range(timepoints-1)]))
        f.write("\n")

        allProts = set(itertools.chain(
            prot2TimeSeries["all"].keys(), prot2WindowsSummary.keys()))
        for prot in sorted(allProts):
            f.write("%s\t" % prot)
            # Write whether the protein is a prize node, Steiner node, or
            # not in the network
            if prot in networkProts:
                # Test above assures that all proteins on the synthesized
                # pathway have an activity window
                if prot in prot2TimeSeries["sig"]:
                    f.write("SigPrize")
                    sigPrizeCount += 1
                elif prot in prot2TimeSeries["insig"]:
                    f.write("InsigPrize")
                    insigPrizeCount += 1
                else:
                    f.write("Steiner")
                    steinerCount += 1
            else:
                # Proteins that were excluded from either the Steiner forest
                # or the pathway synthesis
                f.write("Excluded")

            # Write whether the protein is on a reference pathway
            if prot in goldStandard:
                f.write("\ttrue")
            else:
                f.write("\tfalse")

            # Write the significant time series that map to this protein in an arbitrary order
            padCols = sigPepCols - \
                len(prot2TimeSeries["sig"].setdefault(prot, []))
            if padCols < sigPepCols:
                f.write("\t")
            f.write("\t".join(prot2TimeSeries["sig"][prot]))
            # Write empty values in the columns if there are fewer than the
            # max number of peptides for this protein
            if padCols > 0:
                f.write("".join(itertools.repeat("\t", padCols)))

            # Write the insignificant time series that map to this protein in an arbitrary order
            padCols = insigPepCols - \
                len(prot2TimeSeries["insig"].setdefault(prot, []))
            if padCols < insigPepCols:
                f.write("\t")
            f.write("\t".join(prot2TimeSeries["insig"][prot]))
            # Write empty values in the columns if there are fewer than the
            # max number of peptides for this protein
            if padCols > 0:
                f.write("".join(itertools.repeat("\t", padCols)))

            # Write the activity window summary
            windowSummary = prot2WindowsSummary.setdefault(
                prot, itertools.repeat("", timepoints))
            f.write("\t%s\t" % "\t".join(windowSummary))

            # Write the first active time point
            f.write("%s\t" % prot2FirstActive.setdefault(prot, "Not active"))

            # Write the heat map background fill columns
            fill = ", ".join(itertools.repeat("0", timepoints))
            f.write("\t".join(itertools.repeat(fill, timepoints-1)))
            f.write("\n")

    print("Wrote attributes for %d Steiner nodes in the synthesized pathway" %
          steinerCount)
    print("Wrote attributes for %d prize nodes in the synthesized pathway with a significant peptide" % sigPrizeCount)
    print("Wrote attributes for %d prize nodes in the synthesized pathway with no significant peptides" % insigPrizeCount)
    print("Wrote attributes for %d proteins excluded by PCSF or synthesis" %
          (len(allProts) - (steinerCount + sigPrizeCount + insigPrizeCount)))

    return pepsPerProt["all"]


def SummarizeWindow(states):
    """Collapse the set or list of values in a particular temporal activity window
    into a single summary.  Valid values are ambiguous, inactive, activation,
    inhibition.
    """
    # Verify that all states are recognized
    validStates = set(["ambiguous", "inactive", "activation", "inhibition"])
    for state in states:
        if state not in validStates:
            raise RuntimeError("Invalid temporal activity state: %s" % state)

    # If any are ambiguous, the entire window is ambiguous
    if "ambiguous" in states:
        return "ambiguous"

    # If all are activation or inhibition, return that state
    if all([s == "activation" for s in states]):
        return "activation"
    if all([s == "inhibition" for s in states]):
        return "inhibition"

    # A combination of activation and inhibition is ambiguous, regardless
    # of whether there is also inactive
    if "activation" in states and "inhibition" in states:
        return "ambiguous"

    # If all inactive, return inactive
    if all([s == "inactive" for s in states]):
        return "inactive"

    # Otherwise the states are a mix of inactive and activation or inhibition
    # so activation/inhibition dominates
    if "activation" in states:
        return "activation"
    if "inhibition" in states:
        return "inhibition"

    raise RuntimeError("Invalid case reached")


def ConvertWindowState(state):
    """Map a string representation of an activity window to a code for the
    Cytoscape heat map
    """
    stateMap = {"ambiguous": "", "inactive": "0",
                "activation": "1", "inhibition": "-1"}
    return stateMap[state]


def FirstActiveGeneral(activities, timepoints):
    """Given a list of temporal activities in the coded activity state from
    ConvertWindowState, return the time point at which the protein is first
    active (not in the 0 inactive state) or 'Not active'.  Does not assume
    any knowledge of the time points.  Returns the 0-based index.
    """
    assert len(list(activities)) == len(
        list(timepoints)), "Must have same length activities and time points"

    for t in range(len(list(activities))):
        if not activities[t] == "0":
            return str(timepoints[t])
    return "Not active"


def FirstActive(activities):
    """Given a list of temporal activities in the coded activity state from
    ConvertWindowState, return the time point at which the protein is first
    active (not in the 0 inactive state) or 'Not active'
    """
    for t in range(len(list(activities))):
        if not activities[t] == "0":
            return str(2**(t+1))
    return "Not active"


def FirstSignificant(pvals, thresh):
    """Given a list of temporal p-values for peptide phoshorylation changes
    return the time point at which the peptide is first significant
    or 'Not significant'
    """
    for t in range(len(pvals)):
        if pvals[t] <= thresh:
            return str(2**(t+1))
    return "Not significant"


def RepairMissingData(time_series, first_value):
    """Given a list of time series value in a string format, replace missing
    values.  If the first time point is missing, set it to first_value. This
    should be 1 if the log transform will be taken or 0 otherwise. If later
    time points are missing, set them to the previous observed time point.
    """
    if time_series[0] == '':
        time_series[0] = first_value

    for i in range(1, len(time_series)):
        if time_series[i] == '':
            time_series[i] = time_series[i-1]

    return time_series