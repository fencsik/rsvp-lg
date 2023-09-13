# Explicit rules

# all : fig0201.pdf fig0301.pdf fig0302.pdf tab0303.txt \
# 	fig0401.pdf fig0402.pdf tab0402.txt tab0403.txt \
# 	fig0501.pdf fig0502.pdf tab0504.txt \
# 	fig0601.pdf fig0602.pdf tab0602.txt tab0604.txt \
# 	fig0701.pdf fig0702.pdf tab0701.txt tab0702.txt \
# 	fig0801.pdf fig0802.pdf tab0801.txt tab0802.txt tab0803.txt \
# 	Exp2-ModelFits.txt

rawdata.rda : data/*
# data00.rda : rawdata.rda
# data01.rda : data00.rda
# data02.rda : data01.rda ComputeDprime.r
# fig0201.pdf : data02.rda
# data03.rda: data02.rda maxrule.r ComputeDprime.r
# fig0301.pdf : data03.rda
# fig0302.pdf : data03.rda
# tab0303.txt : data03.rda
# data04.rda : data02.rda maxrule.r ComputeDprime.r
# fig0401.pdf : data04.rda
# fig0402.pdf : data04.rda
# tab0402.txt : data03.rda data04.rda
# tab0403.txt : data04.rda
# data05.rda : data02.rda maxrule.r ComputeDprime.r
# fig0501.pdf : data05.rda
# fig0502.pdf : data05.rda
# tab0504.txt : data03.rda data05.rda
# data06.rda : data02.rda maxrule.r ComputeDprime.r
# fig0601.pdf : data06.rda
# fig0602.pdf : data06.rda
# tab0602.txt : data05.rda data06.rda
# tab0604.txt : data04.rda data06.rda
# data07.rda : data02.rda maxrule.r ComputeDprime.r
# fig0701.pdf : data07.rda
# fig0702.pdf : data07.rda
# tab0701.txt : data03.rda data07.rda
# tab0702.txt : data07.rda data04.rda
# data08.rda : data02.rda maxrule.r ComputeDprime.r
# fig0801.pdf : data08.rda
# fig0802.pdf : data08.rda
# tab0801.txt : data05.rda data08.rda
# tab0802.txt : data08.rda data06.rda
# tab0803.txt : data08.rda data07.rda
# Exp2-ModelFits.txt : data03.rda data04.rda

# Commands and implicit rules

R = /usr/local/bin/Rscript $<

%.rda: %.r; $(R)
%.pdf: %.r; $(R)
%.txt: %.r; $(R)

.PHONY : clean
clean :
	-rm -f *.rda fig*.pdf tab*.txt

# Local Variables:
# mode:makefile-gmake
# End:
