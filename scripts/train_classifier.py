#!/usr/bin/env python
"""QIIME2 q2 classifier
"""

import sys
import argparse

from qiime2 import Artifact
from qiime2.plugins.feature_classifier import methods


def load_data(rep_set, taxa):
    q2_repset = Artifact.import_data('FeatureData[Sequence]', rep_set)
    q2_taxa = Artifact.import_data('FeatureData[Taxonomy]', taxa, view_type='HeaderlessTSVTaxonomyFormat')
   return q2_repset, q2_taxa

def extract_region_fasta(q2_repset, fwd='CCTACGGGNGGCWGCAG', rev='GACTACHVGGGTATCTAATCC'):
    # V3-V4: 341f: CCTACGGGNGGCWGCAG; 806r: GACTACHVGGGTATCTAATCC
    q2_refseq_filtered = methods.extract_reads(sequences=q2_repset, f_primer = fwd, r_primer = rev)
    return q2_refseq_filtered

def train_classifier(q2_refseq, q2_taxa):
    # train the classifier
    clf = methods.fit_classifier_naive_bayes(reference_reads=q2_refseq, reference_taxonomy=q2_taxa)
    return clf



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--fasta', help='rep set sequences', type=argparse.FileType('r'))
    parser.add_argument('--taxa', help='taxonomy files', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', help="classifier output file, if empty stdout is used", default=sys.stdout, type=argparse.FileType('w'))
    parser.add_argument('--f-primer', help="filer reference fasta wrt forward primer compatibility")
    parser.add_argument('--r-primer', help="filer reference fasta wrt forward reverse compatibility")
    args = parser.parse_args(sys.argv[1:])

    q2_repset, q2_taxa = load_data(args.fasta, args.taxa)
    q2_refseq_filtered = extract_region_fasta(q2_repset, args.f_primer, args.r_primer)
    classifier = train_classifier(q2_refseq_filtered, q2_taxa)
    classifier.classifier.save(args.output)
