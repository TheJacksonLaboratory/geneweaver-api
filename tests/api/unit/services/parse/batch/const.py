# ruff: noqa: E501
EXAMPLE_BATCH_FILE = """
# This is an example batch upload file for GeneWeaver.
# http://geneweaver.org
#
# The format of this file is described online at:
#    http://geneweaver.org/index.php?action=manage&cmd=batchgeneset
# Which is the same page that it can be submitted to.
#
# The next 5 lines apply to all the sets in this file, so they
# are re-used on upload instead of repeated in this file. If another gene set
# further in the batch file uses a different p-value threshold or species
# for example, these lines can be changed later on in the file.
#

! P-Value < 0.001
@ Mus musculus
% microarray Mouse Expression Array 430 Set
P 19958391
A Private

#
# The following lines give the label, name, and description of
# this set, respectively.
#

: STR ACTI_DIFF_05 F BXD M430v2 RMA
= Striatum Gene expression correlates of Difference in distance traveled (cm) during the first five min (saline-ethanol) in Females BXD
+ Striatum Gene Expression Correlates for ACTI_DIFF_05 measured in BXD RI Females obtained using GeneNetwork Striatum M430V2 (Apr05) RMA.
+ The ACTI_DIFF_05 measures Difference in distance traveled (cm) during the first five min (saline-ethanol) under the domain Ethanol.
+ The correlates were thresholded at a p-value of less than 0.001.

#
# Probe/gene data starts after all the gene set metadata has been specified.
#

1419895_at  4.62954E-05
1427431_at  5.21582E-05
1459099_at  5.49844E-05
1439831_at  6.81706E-05
1450206_at  7.24209E-05
1443550_at  7.74979E-05
1429056_at  8.55707E-05
1443615_at  9.26147E-05
1454179_at  0.000108698
1425459_at  0.000126946
1417874_at  0.000127752
1418440_at  0.000143051
1459437_at  0.000147362
1423335_at  0.000182977
1426146_a_at    0.000207811
1426237_at  0.000208478
1453826_at  0.000223366
1418472_at  0.000225267
1432515_at  0.000236315
1458208_s_at    0.000251702
1449365_at  0.000265399
1427614_at  0.000271715
1438721_a_at    0.000274974
1451106_at  0.000299124
1434317_s_at    0.00031313
1455170_at  0.000330622
1455782_at  0.000344905
1429428_at  0.000347363
1433781_a_at    0.000361397
1450522_a_at    0.000363282
1442297_at  0.000400537
1426960_a_at    0.000401115
1415673_at  0.000408955
1417014_at  0.00040993
1443832_s_at    0.00042933
1452045_at  0.000430262
1424823_s_at    0.00043663
1433939_at  0.000443502
1431168_at  0.000455925
1421270_at  0.00046495
1454067_a_at    0.000470904
1446485_at  0.00047431
1422757_at  0.000482093
1457240_at  0.000501097
1422306_at  0.000514778
1458362_at  0.000532965
1424315_at  0.000566445
1428568_at  0.000567672
1448948_at  0.000569434
1416081_at  0.000578466
1422634_a_at    0.00058238
1453616_at  0.000583529
1431667_s_at    0.000599767
1425234_at  0.000610597
1442013_at  0.000632513
1418041_at  0.000653667
1425153_at  0.000661747
1423518_at  0.00070306
1458854_at  0.000704167
1434701_at  0.000704734
1452517_at  0.000715244
1429595_at  0.000719228
1459327_at  0.000738269
1426467_s_at    0.000740976
1417309_at  0.000744451
1423770_at  0.000757701
1431886_at  0.000766493
1419289_a_at    0.000768622
1437208_at  0.000782469
1435627_x_at    0.000782591
1435465_at  0.000793171
1416149_at  0.000810041
1433630_at  0.000819244
1442889_at  0.000836545
1453687_at  0.00083677
1423109_s_at    0.000838646
1446050_at  0.000841425
1456717_at  0.000868755
1423382_a_at    0.000876785
1453709_at  0.000891731
1456370_s_at    0.000902406
1427944_at  0.000920491
1436508_at  0.000923192
1432024_at  0.000947824
1459710_at  0.000966139
1430370_at  0.000995187
1415864_at  0.000996862
1428483_a_at    0.000999938

# When gene set metadata symbols are encountered again, this signifies the end
# of the first gene set. The second data set follows, then other sets, until
# the end of the file is reached.
#

: STR ACTI_DIFF_05 M BXD M430v2 RMA
= Striatum Gene expression correlates of Difference in distance traveled (cm) during the first five min (saline-ethanol) in Males BXD
+ Striatum Gene Expression Correlates for ACTI_DIFF_05 measured in BXD RI Males obtained using GeneNetwork Striatum M430V2 (Apr05) RMA.
+ The ACTI_DIFF_05 measures Difference in distance traveled (cm) during the first five min (saline-ethanol) under the domain Ethanol.
+ The correlates were thresholded at a p-value of less than 0.001.

1460595_at  3.04127e-007
1455130_at  1.45388e-006
1424390_at  4.27088e-005
1426826_at  5.08465e-005
1420611_at  6.22965e-005
1416320_at  6.81489e-005
1424243_at  7.09202e-005
1460389_at  7.24103e-005
1428891_at  8.45653e-005
1460573_at  8.8657e-005
1428466_at  8.95255e-005
1415746_at  9.17271e-005
1434264_at  9.18051e-005
1436412_at  0.000106824
1443924_at  0.000125556
1432061_at  0.000133211
1453119_at  0.000134048
1430062_at  0.000134412
1434384_at  0.000144186
1415689_s_at    0.00014714
1451436_at  0.000149564
1452942_at  0.000151914
1432625_at  0.00017943
1436498_at  0.000183371
1415729_at  0.000186867
1456283_at  0.000188729
1453453_at  0.000188834
1415769_at  0.000188969
1448809_at  0.000190696
1459920_at  0.000191884
1435818_at  0.00019201
1421305_x_at    0.000194441
1419228_at  0.000194813
1418433_at  0.00019772
1454675_at  0.000207191
1427947_at  0.000209615
1415863_at  0.000210644
1448083_at  0.000216645
1429476_s_at    0.000216702
1459145_at  0.000217422
1441973_at  0.000218309
1420478_at  0.000218961
1423613_at  0.000223316
1426933_at  0.000245662
1438428_at  0.000263381
1457939_at  0.00026804
1450700_at  0.000271212
1460726_at  0.000273019
1415834_at  0.000281249
1454222_a_at    0.000285377
1425580_a_at    0.000286385
1454827_at  0.000290301
1434251_at  0.000297939
1460615_at  0.00030438
1444960_at  0.00031556
1415887_at  0.000317876
1431822_a_at    0.000321428
1451324_s_at    0.000323631
1429013_at  0.000324283
1434917_at  0.000331919
1460440_at  0.000332755
1426218_at  0.000334486
1432464_a_at    0.000349886
1437148_at  0.000350493
1456199_x_at    0.000352374
1420922_at  0.000354241
1417763_at  0.000354706
1423369_at  0.000356982
1450655_at  0.000359364
1429451_at  0.00036425
1436804_s_at    0.000402476
1435360_at  0.000408271
1428949_at  0.000416803
1439350_s_at    0.000421143
1455400_at  0.000425877
1433658_x_at    0.00043765
1454763_at  0.00043949
1428648_at  0.000442941
1429399_at  0.000444247
1423126_at  0.000452955
1452075_at  0.000453909
1420882_a_at    0.000459761
1434016_at  0.000465769
1452970_at  0.000471097
1455418_at  0.000476002
1436307_at  0.000476775
1431394_a_at    0.000477686
1424530_at  0.000480735
1429678_at  0.000483195
1418543_s_at    0.00048529
1424135_at  0.00048669
1456717_at  0.000490375
1442614_at  0.000502168
1460620_at  0.00050726
1436150_at  0.000514935
1433649_at  0.000525362
1433975_at  0.000532959
1439024_at  0.000537926
1450882_s_at    0.000538512
1436448_a_at    0.000552269
1455508_at  0.000566657
1436101_at  0.000569536
1428388_at  0.000573968
1428138_s_at    0.000574887
1422714_at  0.000588041
1433811_at  0.000590484
1418706_at  0.000608581
1433770_at  0.00061608
1455094_s_at    0.00061877
1454994_at  0.000619628
1422508_at  0.0006251
1428097_at  0.000630794
1450755_at  0.000637877
1436027_at  0.000638305
1443742_x_at    0.00064035
1458991_at  0.000656151
1416369_at  0.000658738
1434738_at  0.000666963
1433664_at  0.000672556
1455166_at  0.00067343
1442649_at  0.000678125
1452204_at  0.000684785
1428307_at  0.000686815
1444500_at  0.000689908
1424597_at  0.000690582
1459429_at  0.000695537
1428531_at  0.000700511
1416029_at  0.00070569
1427109_at  0.000710559
1428457_at  0.000711185
1441136_at  0.000715173
1433555_at  0.000717655
1433879_a_at    0.000729475
1424326_at  0.000734742
1417847_at  0.000737301
1433632_at  0.000739978
1453290_at  0.000740166
1429910_at  0.00076537
1456482_at  0.000765382
1453028_at  0.000775823
1435916_at  0.000779491
1448706_at  0.000785693
1423304_a_at    0.000796173
1423821_at  0.000806645
1426840_at  0.000819303
1418505_at  0.000824724
1456798_at  0.000830067
1455862_at  0.00083365
1424532_at  0.000852561
1428819_at  0.000852929
1434078_at  0.000860667
1426342_at  0.000868494
1428796_at  0.000880571
1418521_a_at    0.000886687
1457811_at  0.000893002
1437464_at  0.000893639
1420654_a_at    0.000896139
1435637_at  0.000898089
1428883_at  0.000909877
1435291_at  0.000913222
1429473_at  0.000920155
1415684_at  0.000920999
1452363_a_at    0.000922349
1422736_at  0.000922756
1458629_at  0.000928507
1452627_at  0.000934148
1428122_s_at    0.000943615
1436791_at  0.000950172
1427317_at  0.000953463
1434843_at  0.000977116
1422315_x_at    0.000984641
1444576_at  0.000991444


: STR ACTI05_ETHA M BXD M430v2 RMA
= Striatum Gene expression correlates of Distance traveled (cm) during the first five minutes after ethanol in Males BXD
+ Striatum Gene Expression Correlates for ACTI05_ETHA measured in BXD RI Males obtained using GeneNetwork Striatum M430V2 (Apr05) RMA.
+ The ACTI05_ETHA measures Distance traveled (cm) during the first five minutes after ethanol under the domain Ethanol.
+ The correlates were thresholded at a p-value of less than 0.001.

1459127_at  3.89433e-005
1453976_at  5.85397e-005
1446104_at  6.81255e-005
1418588_at  0.000105218
1447469_at  0.000142648
1428891_at  0.000150707
1429743_at  0.000170647
1444674_at  0.000244271
1428890_at  0.000257403
1444500_at  0.000267276
1428487_s_at    0.000317112
1460615_at  0.000328649
1450618_a_at    0.000350512
1446717_at  0.000372691
1421213_at  0.000374089
1421235_s_at    0.000426869
1433927_at  0.000448532
1419228_at  0.000489634
1425378_at  0.000491551
1453453_at  0.000552417
1431717_at  0.00057804
1459324_at  0.000648819
1425111_at  0.000675884
1418041_at  0.000732076
1447313_at  0.000738001
1452045_at  0.000772274
1430724_at  0.000844233
1450348_at  0.000872906
1460011_at  0.000884376
1452699_at  0.000958429
1420710_at  0.000994726

! Binary
% Gene Symbol
P 21223303
A Private

: Transcripts enriched in blood
= Transcripts enriched in blood of C57BL/6J mice drinking to intoxication.
+ Transcripts enriched more than 50 fold in blood of C57BL/6J mice drinking to intoxication with the fold enrichment.

Alas2	1
Car2	1
Cd24a	1
Ctla2a	1
Ctla2b	1
Epb4.1	1
Fech	1
Got2	1
Hba-a1	1
Hba-x	1
Hbb-b1	1
Pam	1
Ptpn13	1
Nfkbia	1
Gpx1	1
Dusp8	1
Ucp2	1
Bpgm	1
Slc25a39	1
Cd200	1
Atp6v0d1	1
Pik3c2a	1
Snca	1
Bnip3l	1
Ncoa4	1
Tcl1b1	1
Mkrn1	1
Ppbp	1
Gng11	1
Cryzl1	1
9130011J15Rik	1
Ube2l6	1
Slc25a37	1
Hnrnpul2	1
Isca1	1
Srsf11	1
Mex3a	1
Fbxw8	1
Sun1	1
Htra2	1
Rpap2	1
Rhbdd3	1
Prss35	1
"""
