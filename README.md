# DemonsSouls-PS3-Shader-Modding
Tools to help mod .fpo/.vpo shader files in Demon's Souls (PS3)

!!WARNING!!
This is still a *very* janky hack, a *proof of concept*, not a fully fleshed out or tested workflow!
I myself have had a bit of trouble getting everything to work smoothly on my own, so I appologize in advance if you encounter 
any issues trying to get these tools to work for you, my hope is that this can at the very least point someone in the right direction, 
on how to get started with modifying shaders for Demon's Souls / PS3 games...

# Usefull Information
- [NVidia CG shader language documentation](https://developer.download.nvidia.com/cg/index.html)
- [Souls Modding Wiki](https://www.soulsmodding.com)
- [PS3 Dev Wiki](https://www.psdevwiki.com/ps3/)
- [FPO/VPO information](https://www.psdevwiki.com/ps3/Multimedia_Formats_and_Tools#FPO_and_VPO)

# Requirements

[WitchyBND](https://github.com/ividyon/WitchyBND/releases) to unpack / repack shaderbnd.dcx files
  - Download and place WitchyBND.exe file under Tools

[cg toolkit](https://developer.nvidia.com/cg-toolkit) needed by cgcomp
[cgcomp](https://github.com/ps3dev/PSL1GHT/tree/master/tools/cgcomp) to compile fcg / vcg CG program files into fpo / vpo binary files
  - cgcomp is a part of PSL1GHT, an open-source PlayStation 3 homebrew SDK.
  - to compile the files needed for this project we only need cgcomp from PSL1GHT
  - you can download the entire PSL1GHT repo then copy the tools/cgcomp folder to our Tools folder
  - you will need to compile cgcomp from source, as of writing this document (Sep-2025) cgcomp is not fully functional as of yet...
  - an alternative to using cgcomp would be to use sce-cgc.exe, the CG compiler from the official PS3-SDK (not publicly available)

(if you happen to find a PS3-SDK lying around and want to use sce-cgc to compile shaders, you will ned to uncomment some code in the makefile and InjectShaderCode python script.)

(Optional)
[RPCS3](https://rpcs3.net/) - to test shader mods on PC

# Preperation

Once you have the required tools installed, you will need to unpack your copy of Demon's Souls..
- open the USRDIR/shader folder
- copy ds_filter.shaderbnd.dcx into the OriginalDCX folder
- open Makefile using a text editor
- double check the first two commands will properly run WitchyBND.ex/cgcomp
- check the next two commands needed for the `make run` command to mod Demon's Souls and launch it in RPCS3
- run `cp OriginalDCX/ds_filter.shaderbnd.dcx ./build` (or just copy the .dcx folder to the build folder manually...
- run `<command to launch WitchyBND> build/ds_filter.shaderbnd.dxc` to decompress the dxc folder,
- ( on windows just `WitchyBND.exe` on MAC/Linux you will need to use wine / proton from the command line)
- ( make sure to change `$(WitchyBND):=` in the Makefile!)

# Build

After making any changes to shaders/someFragmentShader.fcg or shaders/someVertexShader.vcg, run `make` and the makefile will attempt to
- Compile all .fcg/.vcg files in the shaders folder to .fpo/.vpo files
- Inject the microcode from each compiled .fpo/.vpo file into the corisponding file in the uncompressed build/ds_filter-shaderbnd-dcx folder
- use WitchyBND to re-compress the updated ds_filter-shaderbnd-dcx into a ds_filter.shaderbnd.dcx file (new dcx will be under build)
- if using `make run` then the makefile will copy the newly created dcx file into the /shader folder specified by DeS_USRDIR
- then use RPCS3 to launch DeS_USRDIR/EBOOT.BIN

# Final Thoughts
- First shoutout to [Demon's Souls Demastered](https://www.nexusmods.com/demonssouls/mods/142) by [thegreatgramcracker](https://next.nexusmods.com/profile/thegreatgramcracker?gameId=2952) which served as the insperation for me to work out how to compile shader files for demonSouls (and to do so in a way using open source tools so that knowledge can more easily be shared)
- Even with getting the shader code to compile and run in RPCS3, it won't mean that the shader will run well on real hardware.
- Compiling for the RSX can be a bit finiky, I found myself often using a tool like sce-cgcdisasm.exe to double check the output of the compiler(s)
- Feel free to reach out to me if you have any questions, even if you aren't sure you have the technical knowledge to do something like this, I encourage anyone with the interest to give it a try, and I'd be more then happy to help! 😄
