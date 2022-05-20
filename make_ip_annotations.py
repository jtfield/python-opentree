#!/usr/bin/env python3

import os
import argparse
import pandas as pd
import sys
import json
import dendropy

from opentree import OT
from opentree import annotations


def parse_args():
    parser = argparse.ArgumentParser(prog='make itol annotations', \
        description='make itol annotations for ip data')
    parser.add_argument('--csv', help='csv file with AMR gene values.')
    # parser.add_argument('--output_file', default='converted_tree.tre', help='newick phylogeny file.')
    return parser.parse_args()

def main():
    args = parse_args()

    csv_contents = pd.read_csv(args.csv)

    gene_dict = make_gene_dict(csv_contents)

    # write_itol_heatmap()


def make_gene_dict(csv_contents):

    columns = []
    output = {}

    # amr_genes = csv_contents['AMR genotypes']

    # for list_of_genes in amr_genes:
    for idx, row in csv_contents.iterrows():

        amr_genes = row['AMR genotypes']

        split_row = amr_genes.split(',')
        # print(split_row)

        for gene_id in split_row:

            split_gene_info = gene_id.split('=')
            gene = split_gene_info[0]
            info = split_gene_info[1]

            if gene not in columns:
                columns.append(gene)
    # print(columns)
    # print(len(columns))

    for idx, row in csv_contents.iterrows():

        amr_genes = row['AMR genotypes']

        taxon_id = row['Run']

        split_row = amr_genes.split(',')
        isolate_dict = {}

        intermediate_list = []
        for gene_id in split_row:

            split_gene_info = gene_id.split('=')
            gene = split_gene_info[0]
            info = split_gene_info[1]

            isolate_dict[gene] = 1
            intermediate_list.append(gene)

        for gene_name in columns:
            if gene_name not in intermediate_list:
                isolate_dict[gene_name] = 0

        # print(isolate_dict)
        output[taxon_id] = isolate_dict

    # print(output)







if __name__ == '__main__':
    main()
