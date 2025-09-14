#Needed for make
#Replace with whatever command to run WitchyBND.exe from cmndline...  (I couldn't get wine to work with it lol :P)
export WitchyBND := ./Tools/proton Tools/WitchyBND.exe
#Command to compile shader files
export CGcomp := ./Tools/cgcomp/cgcomp

#Needed for make run
#Path to USDIR folder, find this in rpcs3 using "open disk game folder" ~Make Backup copies of any folders/files you intend to mod!
export DeS_USRDIR := ~/.config/rpcs3/dev_hdd0/game/NPUB30910/USRDIR
#Command to launch RPCS3, ie <path to rpcs3 executable>
export RPCS3 := ~/Documents/DesktopPrograms/rpcs3-v0.0.37-17995-d6853486_linux64.AppImage



fragmentShaders = $(wildcard source/*.fcg)
vertexShaders = $(wildcard source/*.vcg)
SHADERS		:=	shaders
VCGFILES	:=	$(foreach dir,$(SHADERS),$(notdir $(wildcard $(dir)/*.vcg)))
FCGFILES	:=	$(foreach dir,$(SHADERS),$(notdir $(wildcard $(dir)/*.fcg)))

VPOFILES	:=	$(VCGFILES:.vcg=.vpo)
FPOFILES	:=	$(FCGFILES:.fcg=.fpo)


#PSL1GHT cgcomp compiler ONLY
#Compile vcg source files into vertex program object files
%.vpo: $(SHADERS)/%.vcg
	$(CGcomp) -v $(filter %.vcg,$?) $(notdir $(subst .vcg,.vpo,$(filter %.vcg,$?)))

#Compile fcg source files into fragment program object files
%.fpo: $(SHADERS)/%.fcg
	$(CGcomp) -f $(filter %.fcg,$?) $(notdir $(subst .fcg,.fpo,$(filter %.fcg,$?)))

#sce-cgc.exe compiler ONLY
#Compile vcg source files into vertex program object files
#	%.vpo: $(SHADERS)/%.vcg
#		$(CGcomp) -p sce_fv_rsx $(filter %.vcg,$?) -o $(notdir $(subst .vcg,.vpo,$(filter %.vcg,$?)))

#Compile fcg source files into fragment program object files
#	%.fpo: $(SHADERS)/%.fcg
#		$(CGcomp) -f sce_fp_rsx $(filter %.fcg,$?) -o $(notdir $(subst .fcg,.fpo,$(filter %.fcg,$?)))


#Append appropiate header data to each shader file, and compress dcx folder
build/ds_filter.shaderbnd.dcx: $(VPOFILES) $(FPOFILES)
	python Tools/InjectShaderCode.py $?
	$(WitchyBND) build/ds_filter-shaderbnd-dcx

#If no uncompressed dcx folder in the build folder, we need to uncompress the original .dcx file
build/ds_filter-shaderbnd-dcx: OriginalDCX/ds_filter.shaderbnd.dcx
	cp OriginalDCX/ds_filter.shaderbnd.dcx ./build
	$(WitchyBND) build/ds_filter.shaderbnd.dcx

run: build/ds_filter.shaderbnd.dcx
	cp $< $(DeS_USRDIR)/shader
	$(RPCS3) $(DeS_USRDIR)/EBOOT.BIN	$(CGcomp) -v $(filter %.vcg,$?) $(notdir $(subst .vcg,.vpo,$(filter %.vcg,$?)))

#Compile fcg source files into fragment program object files
%.fpo: $(SHADERS)/%.fcg
	$(CGcomp) -f $(filter %.fcg,$?) $(notdir $(subst .fcg,.fpo,$(filter %.fcg,$?)))
