import sys, struct
shaderFile = sys.argv[1]

if shaderFile[-4:] == ".fpo":	
	isFragmentShader = True
elif shaderFile[-4:] == ".vpo":
	isFragmentShader = False
else:
	raise ValueError(f"Unrecgonized file extension {shaderFile[-4:]}")

""""
The compiler used in the opensource PSL1GHT sdk uses a slightly different format and header
then the official sce-cgc.exe produces (the shaderprogram compiler found in the offical PS3_SDK).
Ideally we would create our own NV Binary header from scratch, but that's too much work for me right now, 
so instead we are just going to inject the microcode produced by cgcomp directly into the vpo / fpo files used by Demon's Souls.

This shortcut means we can just re-use the header data from the original files, 
however this limits our input / output parameters to whatever the original shader files used.
this means we can't, for example, take samples from a texture (unless it's one the original shader used)

For the basic goal of creating a "post-render filter" effect like the kind seen in re-shade projects,
this isn't a big issue. We can just inject our code into the depth of feild or bloom shader files that Demon's Souls uses,
effectivly replaceing those shader effects with our own custom ones.
"""





"""
#First 24 bytes of cgcomp's rsx_vp/rsx_fp are the same  
	u16 magic;
	u16 _pad0;

	u16 num_regs;
	u16 num_attr;
	u16 num_const;
	u16 num_insn;

	u32 attr_off;
	u32 const_off;
	u32 ucode_off;
"""

with open(shaderFile,'rb') as f:
	header = f.read(24)
	#Header structure is based on cgcomp/include/types.h
	L1ghtCGpHeader = struct.unpack('>HHHHHHIII',header)
	instructionCount = L1ghtCGpHeader[5]
	registerCount = L1ghtCGpHeader[2]
	ucode_off = L1ghtCGpHeader[8]
	f.seek(ucode_off,0)
	ucode = f.read()





with open("build/ds_filter-shaderbnd-dcx/"+shaderFile,'rb') as f:
	oldShader = bytearray(f.read())
	pCgProgramHeader = struct.unpack('>I',oldShader[4:8])[0] #bytes 4-8 point to CgBinaryProgramHeader (usually at 0x20, but not allways...) 
	CgHeaderData = list(struct.unpack('>IIIIIIII',oldShader[pCgProgramHeader:pCgProgramHeader+32]))
	
"""	
**Info taken from Cg_Compiler-Users_Guide, included with the Official PS3 SDK**
	although not needed for modding demon souls, for those curious,
	more info on the PS3 SDK can be found here: https://www.psdevwiki.com/ps3/SCEI_PS3_SDK

# CgHeaderData format:
{
	profile										//Indicates whether this is a vertex program (7003) or a fragment program (7004).
	binaryFormatRevision			//for DeS this appears to have ben rev 6
	totalSize									//size of file, (not including the mystery extra header info...)
	parameterCount
	parameterArray						//offset of the first parameter in the table
	program										//offest to (fragment or vertex) program header
	ucodeSize									//size of microcode
	ucode											//offset to the first byte of microcode (offset not including mHeader)
	data[] 										//variable length data
}

// program points to either Vertex or Fragment program header, PSL1GHT's compiler dose not create this header info either,
// ideally we'd recreate this header information as well, but for now we will just re-use the header found in the current fpo/vpo file...


#VertexProgram header
{
	unsigned int instructionCount;
	unsigned int instructionSlot;
	unsigned int registerCount;
	unsigned int attributeInputMask;
	unsigned int attributeOutputMask;
	unsigned int userClipMask;
}

#FragmentProgram header
{
	unsigned int	instructionCount; 0
	unsigned int	attributeInputMask; 4
	unsigned int	partialTexType; 8
	unsigned short texCoordsInputMask; 10
	unsigned short texCoords2D; 12
	unsigned short texCoordsCentroid; 14
	unsigned char registerCount; 15
	unsigned char outputFromH0;
	unsigned char depthReplace;
	unsigned char pixelKill;
}


"""
olducodesize = CgHeaderData[6]
ucodeStart = CgHeaderData[7]

print(f"instructionCount:{instructionCount}");
print(f"registerCount:{registerCount}");
oldShader[pCgProgramHeader+CgHeaderData[5]:pCgProgramHeader+CgHeaderData[5]+4] = struct.pack('>I',instructionCount) #overwrite instruction count

CgHeaderData[6] = len(ucode)
CgHeaderData[2] = ucodeStart+len(ucode)

if isFragmentShader:
	oldShader[pCgProgramHeader+CgHeaderData[5]+18] = registerCount
else:
	oldShader[pCgProgramHeader+CgHeaderData[5]+8:pCgProgramHeader+CgHeaderData[5]+12] = struct.pack('>I',registerCount)

oldShader[pCgProgramHeader:pCgProgramHeader+32] = struct.pack('>IIIIIIII',*CgHeaderData)


with open("build/ds_filter-shaderbnd-dcx/"+shaderFile,'wb') as f:
	f.write(oldShader[:-olducodesize])
	f.write(ucode)

print(f"{shaderFile} microcode injection complete")
