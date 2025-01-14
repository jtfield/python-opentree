import unittest

from opentree import taxonomy_helpers, util, OT
from dendropy import Tree

ott_loc = "./"
corr_tax_path = ott_loc + "/ott3.3"

class TestTaxonomyHelpers(unittest.TestCase):
    def test_get_taxonomy(self):
        tax_path = taxonomy_helpers.download_taxonomy_file(loc = ott_loc, version = "3.3")
        assert tax_path == ott_loc + "/ott3.3", tax_path
    def test_get_forward(self):
        tax_path = taxonomy_helpers.download_taxonomy_file(loc = ott_loc, version = "3.3")
        ott_ids = ['ott5859962', 'ott773110']
        forwards_file = tax_path + "/forwards.tsv"
        taxonomy_helpers.get_forwards_dict(forwards_file=forwards_file)
    def test_clean_taxonomy(self):
        cfi = taxonomy_helpers.clean_taxonomy_file(taxonomy_file="{}/taxonomy.tsv".format(corr_tax_path))
    def test_get_by_rank(self):
        ids = taxonomy_helpers.get_ott_ids_for_rank(rank="family", taxonomy_file="{}/taxonomy.tsv".format(corr_tax_path), synth_only = False)
        assert type(ids) is list
        assert type(ids[0]) is str
        assert ids[0].isdigit()
    def test_get_by_group(self):
        aves = taxonomy_helpers.get_ott_ids_for_group(group_ott_id=81461)
        # assert len(aves) == 27465, len(aves) # I would remove this test, it will fail everytime there is an update to the taxonomy or tree that modifies the number of taxa in aves.
        # The following test that the result has the correct structure
        assert type(aves) is list
        assert type(aves[0]) is str
        assert aves[0].isdigit()
        aves_synth = taxonomy_helpers.get_ott_ids_for_group(group_ott_id=81461, synth_only = True)
        assert type(aves_synth) is list
        assert type(aves_synth[0]) is str
        assert aves_synth[0].isdigit()
        assert len(aves) >= len(aves_synth)
    def test_rank_in_taxon(self):
        bird_families = taxonomy_helpers.get_ott_ids_group_and_rank(group_ott_id=81461, rank='family', synth_only = False, taxonomy_file="{}/taxonomy.tsv".format(corr_tax_path))
        assert type(bird_families) is list
        assert type(bird_families[0]) is str
        assert bird_families[0].isdigit()
        bird_families_synth = taxonomy_helpers.get_ott_ids_group_and_rank(group_ott_id=81461, rank='family', taxonomy_file="{}/taxonomy.tsv".format(corr_tax_path))
        assert type(bird_families_synth) is list
        assert type(bird_families_synth[0]) is str
        assert bird_families_synth[0].isdigit()
        assert len(bird_families) >= len(bird_families_synth)
    def test_relabel(self): ## JUST PUT A LIST OF IDS TO SIMPLIFY
        jetz = OT.get_tree(study_id='ot_809', tree_id = 'tree1', tree_format="newick", label_format="ot:ottId")
        jetz_tree = Tree.get(string=jetz.response_dict['content'].decode(), schema='newick', suppress_internal_node_taxa=True, suppress_leaf_node_taxa=True)
        tips = [tip.label for tip in jetz_tree.leaf_node_iter()]
        ott_ids =  set()
        for tip in tips:
            try:
                ott_ids.add(int(tip))
            except:
                pass
        ret = taxonomy_helpers.labelled_induced_synth(ott_ids = list(ott_ids), label_format='name')
        tips = [tip.taxon.label for tip in ret['labelled_tree'].leaf_node_iter() if tip.taxon]
        assert len(tips) == 6624

        ret = taxonomy_helpers.labelled_induced_synth(ott_ids = list(ott_ids), label_format='name_and_id')
        nodes = [node.taxon.label for node in ret['labelled_tree'] if node.taxon]
        assert 'MRCA of taxa in Amazona auropalliata_ott1118 Amazona oratrix_ott1119' in nodes, nodes
