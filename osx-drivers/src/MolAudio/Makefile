
include			../../rules/Makefile.top

MolAudioDevice-VERSION	= 1.1
KMODS			= MolAudioDevice
MolAudioDevice-OBJS	= MolAudioClip.o MolAudioDevice.o MolAudioEngine.o \
			  PCMBlitterLibPPC.o ../common/$(ODIR)/libcommon.a

CXXCOMPILE_FPU		= $(shell echo $(CXXCOMPILE) | sed s/-msoft-float//g)
COMPILE_FPU		= $(shell echo $(COMPILE) | sed s/-msoft-float//g)

$(ODIR)/MolAudioClip.o: CXXCOMPILE=$(CXXCOMPILE_FPU)

$(ODIR)/_blitter.s: PCMBlitterLibPPC.c
	$(COMPILE_FPU) $(DEPFLAGS) -S -c $< -o $@
	@$(DEPEXTRA)

$(ODIR)/PCMBlitterLibPPC.o: $(ODIR)/_blitter.s
	$(CC) -force_cpusubtype_ALL -c $< -o $@

include			$(rules)/Rules.osx
include			$(rules)/Rules.make
