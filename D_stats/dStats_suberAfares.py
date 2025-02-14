# executes d-stats in ipyrad

import ipyrad.analysis as ipa
import ipyparallel as ipp
import toytree
import toyplot

# Before running, execute:
# `ipcluster start -n 40 --cluster-id="baba" --daemonize`
# ... replacing `-n 40` with the number of cores you want to use.
# this is already done in doitall.sh
ipyclient = ipp.Client(cluster_id="baba")

locifile = '../DATA/cerrisdstat.loci'
newick = '../PHY.NEW/RAxML_bestTree.cerris.2022-01-04.m15.rax'

bb = ipa.baba(data = locifile, newick = newick)

# Q. afares hybrid origin with suber test constraints:
#  p4 - Q. chenii, Q. variabilis, and Q. acutissima as outgroups
#  p3 - Q. suber potential introgressor 1
#  p2 - Q. afares potential introgressor 2
#  p1 - undefined --- anyone who fits the topology

bb.generate_tests_from_tree(
    constraint_dict={
        "p4": ["OAK-MOR-982", "OAK-MOR-981", "OAK-MOR-578.fq.barcodeStripped"],
        "p3": ["OAK-MOR-1144", "OAK-MOR-588.fq.barcodeStripped", "OAK-MOR-985"],
        "p2": ["OAK-MOR-983"]
    })

bb.run(ipyclient)

out_suberAfares = bb.results_table.sort_values(by="Z", ascending=False)
taxa_suberAfares = bb.taxon_table.iloc[out_suberAfares.index]

out_suberAfares.to_csv('bb.dstat.sorted_suberAfares_full.csv', sep = ',')
taxa_suberAfares.to_csv('bb.dstat.taxa_suberAfares_full.csv', sep = ',')
