import sys
import argparse

from qiime2 import Artifact
from qiime2.plugins.feature_classifier import methods



# Training feature classifiers with q2-feature-classifier
# https://docs.qiime2.org/2019.1/tutorials/feature-classifier/
silva_132 = Artifact.import_data('FeatureData[Sequence]',
                                 'rep_set/rep_set_16S_only/99/silva_132_99_16S.fna')

silva_132_taxonomy = Artifact.import_data('FeatureData[Taxonomy]',
                                          'taxonomy/16S_only/99/majority_taxonomy_7_levels.txt',
                                           view_type = 'HeaderlessTSVTaxonomyFormat')
   
# extract reference reads
# V3-V4: 341f: CCTACGGGNGGCWGCAG; 806r: GACTACHVGGGTATCTAATCC
ref_seqs_s = methods.extract_reads(sequences = silva_132,
                           f_primer = 'CCTACGGGNGGCWGCAG',
                           r_primer = 'GACTACHVGGGTATCTAATCC')

# train the classifier
silva_classifier = methods.fit_classifier_naive_bayes(reference_reads = ref_seqs_s.reads,
                                              reference_taxonomy = silva_132_taxonomy)

# save the classifier
silva_classifier.classifier.save('silva_132_99_v3v4')
