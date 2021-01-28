
基本来自：***[angr Documentation](https://docs.angr.io/)***；Angr的详细内容位于：***[angr docs](http://angr.io/api-doc/index.html)***

## Top Level Interfaces

顶层接口概述，大致熟悉angr。angr工程以Project开始

```python
In [1]: import angr

In [2]: proj = angr.Project("./test")
WARNING | 2021-01-14 09:15:09,913 | cle.loader | The main binary is a position-independent executable. It is being loaded with a base address of 0x400000.
```

### basic properties

可以得到二进制程序的基本信息。

```python
In [3]: proj.arch
Out[3]: <Arch AMD64 (LE)>

In [4]: hex(proj.entry)
Out[4]: '0x401060'
```



### The loader

二进制程序的加载信息，包括内存地址范围，共享库等

### The factory

用于各种分析API需要的通用对象的生成。

#### block

基本块分析的句柄，通过`block = proj.factory.block(起始指令地址)`得到。

```python
In [5]: block = proj.factory.block(proj.entry)
In [6]: block.pp()
0x401060:       endbr64
0x401064:       xor     ebp, ebp
0x401066:       mov     r9, rdx
0x401069:       pop     rsi
0x40106a:       mov     rdx, rsp
0x40106d:       and     rsp, 0xfffffffffffffff0
0x401071:       push    rax
0x401072:       push    rsp
0x401073:       lea     r8, [rip + 0x186]
0x40107a:       lea     rcx, [rip + 0x10f]
0x401081:       lea     rdi, [rip + 0xc1]
0x401088:       call    qword ptr [rip + 0x2f52]
In [7]: block.vex.pp()
IRSB {
   t0:Ity_I32 t1:Ity_I32 t2:Ity_I32 t3:Ity_I64 t4:Ity_I64 t5:Ity_I64 t6:Ity_I64 t7:Ity_I64 t8:Ity_I64 t9:Ity_I64 t10:Ity_I64 t11:Ity_I64 t12:Ity_I64 t13:Ity_I64 t14:Ity_I64 t15:Ity_I32 t16:Ity_I64 t17:Ity_I64 t18:Ity_I64 t19:Ity_I64 t20:Ity_I32 t21:Ity_I64 t22:Ity_I32 t23:Ity_I64 t24:Ity_I64 t25:Ity_I64 t26:Ity_I64 t27:Ity_I64 t28:Ity_I64 t29:Ity_I64 t30:Ity_I64 t31:Ity_I64 t32:Ity_I64 t33:Ity_I64 t34:Ity_I64 t35:Ity_I64 t36:Ity_I64

   00 | ------ IMark(0x401060, 4, 0) ------
   01 | ------ IMark(0x401064, 2, 0) ------
   02 | PUT(rbp) = 0x0000000000000000
   03 | ------ IMark(0x401066, 3, 0) ------
   04 | t26 = GET:I64(rdx)
   05 | PUT(r9) = t26
   06 | PUT(rip) = 0x0000000000401069
   07 | ------ IMark(0x401069, 1, 0) ------
   08 | t4 = GET:I64(rsp)
   09 | t3 = LDle:I64(t4)
   10 | t27 = Add64(t4,0x0000000000000008)
   11 | PUT(rsi) = t3
   12 | ------ IMark(0x40106a, 3, 0) ------
   13 | PUT(rdx) = t27
   14 | ------ IMark(0x40106d, 4, 0) ------
   15 | t5 = And64(t27,0xfffffffffffffff0)
   16 | PUT(cc_op) = 0x0000000000000014
   17 | PUT(cc_dep1) = t5
   18 | PUT(cc_dep2) = 0x0000000000000000
   19 | PUT(rip) = 0x0000000000401071
   20 | ------ IMark(0x401071, 1, 0) ------
   21 | t8 = GET:I64(rax)
   22 | t29 = Sub64(t5,0x0000000000000008)
   23 | PUT(rsp) = t29
   24 | STle(t29) = t8
   25 | PUT(rip) = 0x0000000000401072
   26 | ------ IMark(0x401072, 1, 0) ------
   27 | t31 = Sub64(t29,0x0000000000000008)
   28 | PUT(rsp) = t31
   29 | STle(t31) = t29
   30 | ------ IMark(0x401073, 7, 0) ------
   31 | PUT(r8) = 0x0000000000401200
   32 | ------ IMark(0x40107a, 7, 0) ------
   33 | PUT(rcx) = 0x0000000000401190
   34 | ------ IMark(0x401081, 7, 0) ------
   35 | PUT(rdi) = 0x0000000000401149
   36 | PUT(rip) = 0x0000000000401088
   37 | ------ IMark(0x401088, 6, 0) ------
   38 | t17 = LDle:I64(0x0000000000403fe0)
   39 | t33 = Sub64(t31,0x0000000000000008)
   40 | PUT(rsp) = t33
   41 | STle(t33) = 0x000000000040108e
   42 | t35 = Sub64(t33,0x0000000000000080)
   43 | ====== AbiHint(0xt35, 128, t17) ======
   NEXT: PUT(rip) = t17; Ijk_Call
}
In [10]: block.vex
Out[10]: IRSB <0x2e bytes, 12 ins., <Arch AMD64 (LE)>> at 0x401060

In [11]: block.capstone
Out[11]: <CapstoneBlock for 0x401060>
```

#### states

程序在某个执行点的状态，包含可程序执行时的内存，寄存器等运行时(模拟)信息。

通过`state = proj.factory.*_state(argv)`类API获得。

```python
In [12]: state = proj.factory.entry_state()
#获取程序入口点状态
In [13]: state
Out[13]: <SimState @ 0x401060>
#访问寄存器
In [14]: state.regs.rip
Out[14]: <BV64 0x401060>

In [15]: state.regs.rax
Out[15]: <BV64 0x1c>
#访存
In [16]: state.mem[state.regs.rip]
Out[16]: <<untyped> <unresolvable> at 0x401060>

In [17]: state.mem[state.regs.rip].int.resolved
Out[17]: <BV32 0xfa1e0ff3>

In [18]: state.mem[proj.entry].int.resolved
Out[18]: <BV32 0xfa1e0ff3>
    
    
#访问符号化的寄存器
In [26]: state.regs.rcx
WARNING | 2021-01-14 09:35:40,021 | angr.storage.memory_mixins.default_filler_mixin | The program is accessing memory or registers with an unspecified value. This could indicate unwanted behavior.
WARNING | 2021-01-14 09:35:40,021 | angr.storage.memory_mixins.default_filler_mixin | angr will cope with this by generating an unconstrained symbolic variable and continuing. You can resolve this by:
WARNING | 2021-01-14 09:35:40,021 | angr.storage.memory_mixins.default_filler_mixin | 1) setting a value to the initial state
WARNING | 2021-01-14 09:35:40,021 | angr.storage.memory_mixins.default_filler_mixin | 2) adding the state option ZERO_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to make unknown regions hold null
WARNING | 2021-01-14 09:35:40,021 | angr.storage.memory_mixins.default_filler_mixin | 3) adding the state option SYMBOL_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to suppress these messages.
WARNING | 2021-01-14 09:35:40,021 | angr.storage.memory_mixins.default_filler_mixin | Filling register rcx with 8 unconstrained bytes referenced from 0x401060 (_start+0x0 in test (0x1060))
Out[26]: <BV64 reg_18_40_64{UNINITIALIZED}>
```

#### simulation manager

angr的模拟执行管理器。给定一个状态，可以通过此对象的方法让angr从此状态点模拟执行。**key**

```python
#获取句柄
In [27]: simgr = proj.factory.simulation_manager(state)

In [28]: simgr
Out[28]: <SimulationManager with 1 active>
#当前执行状态下的active状态
In [29]: simgr.active
Out[29]: [<SimState @ 0x401060>]
#所有的stash
In [31]: simgr.stash
Out[31]: <bound method SimulationManager.stash of <SimulationManager with 1 active>>
#执行一步(默认是一个基本块)
In [32]: simgr.step()
Out[32]: <SimulationManager with 1 active>

In [33]: simgr.active
Out[33]: [<SimState @ 0x526fc0>]

#模拟执行一个指令
In [68]: simgr.step()
Out[68]: <SimulationManager with 1 active>

In [69]: simgr.active
Out[69]: [<SimState @ 0x4010c0>]

In [70]: block = proj.factory.block(0x4010c0)

In [71]: block.pp()
0x4010c0:       lea     rdi, [rip + 0x2f49]
0x4010c7:       lea     rsi, [rip + 0x2f42]
0x4010ce:       sub     rsi, rdi
0x4010d1:       mov     rax, rsi
0x4010d4:       shr     rsi, 0x3f
0x4010d8:       sar     rax, 3
0x4010dc:       add     rsi, rax
0x4010df:       sar     rsi, 1
0x4010e2:       je      0x4010f8
#模拟执行一条指令
In [72]: simgr.step(num_inst=1)
Out[72]: <SimulationManager with 1 active>

In [73]: cur_state = simgr.active[0]

In [74]: cur_state.regs.rip
Out[74]: <BV64 0x4010c7>
```

### Analyses

angr提供的分析模块，基于project句柄

```python
 In [3]: proj.analyses.
 proj.analyses.BackwardSlice        proj.analyses.CongruencyCheck      proj.analyses.reload_analyses       
 proj.analyses.BinaryOptimizer      proj.analyses.DDG                  proj.analyses.StaticHooker          
 proj.analyses.BinDiff              proj.analyses.DFG                  proj.analyses.VariableRecovery      
 proj.analyses.BoyScout             proj.analyses.Disassembly          proj.analyses.VariableRecoveryFast  
 proj.analyses.CDG                  proj.analyses.GirlScout            proj.analyses.Veritesting           
 proj.analyses.CFG                  proj.analyses.Identifier           proj.analyses.VFG                   
 proj.analyses.CFGEmulated          proj.analyses.LoopFinder           proj.analyses.VSA_DDG               
 proj.analyses.CFGFast              proj.analyses.Reassembler
In [3]: cfg = proj.analyses.CFGFast()

In [4]: cfg.graph
Out[4]: <networkx.classes.digraph.DiGraph at 0x7f68234bb520>

In [5]: len(cfg.graph.nodes())
Out[5]: 111010

In [6]: entry_node = cfg.get_any_node(proj.entry)
Deprecation warning: Use self.model.get_any_node() instead of get_any_node

In [7]: entry_node = cfg.model.get_any_node(proj.entry)

In [8]: len(list(cfg.graph.successors(entry_node)))
Out[8]: 1
```

## Loading binary

加载部分，angr的加载器模块基于CLE。涉及到程序的运行加载环境控制部分。

### loaded objects

#### objects  all in one

所有加载的对象都可以通过`proj.loader`(cle.Loader类)访问。

```python
In [1]: import angr, monkeyhex

In [2]: proj = angr.Project("./test")
#获取cle.Loader对象
#cle.Loader是所有加载的程序与库的一个集合
In [3]: proj.loader
Out[3]: <Loaded test, maps [0x400000:0xa07fff]>
#查看所有加载的对象
In [4]: proj.loader.all_objects
Out[4]:
[<ELF Object test, maps [0x400000:0x404037]>,
 <ELF Object libc-2.31.so, maps [0x500000:0x6f14d7]>,
 <ELF Object ld-2.31.so, maps [0x700000:0x72f18f]>,
 <ExternObject Object cle##externs, maps [0x800000:0x87ffff]>,
 <ELFTLSObjectV2 Object cle##tls, maps [0x900000:0x91500f]>,
 <KernelObject Object cle##kernel, maps [0xa00000:0xa07fff]>]
#查看各种类型的加载对象
In [5]: proj.loader.main_object
Out[5]: <ELF Object test, maps [0x400000:0x404037]>

In [6]: proj.loader.shared_objects
Out[6]:
OrderedDict([('test', <ELF Object test, maps [0x400000:0x404037]>),
             ('libc.so.6',
              <ELF Object libc-2.31.so, maps [0x500000:0x6f14d7]>),
             ('ld-linux-x86-64.so.2',
              <ELF Object ld-2.31.so, maps [0x700000:0x72f18f]>),
             ('extern-address space',
              <ExternObject Object cle##externs, maps [0x800000:0x87ffff]>),
             ('cle##tls',
              <ELFTLSObjectV2 Object cle##tls, maps [0x900000:0x91500f]>)])

In [7]: proj.loader.all_elf_objects
Out[7]:
[<ELF Object test, maps [0x400000:0x404037]>,
 <ELF Object libc-2.31.so, maps [0x500000:0x6f14d7]>,
 <ELF Object ld-2.31.so, maps [0x700000:0x72f18f]>]

In [8]: proj.loader.extern_object
Out[8]: <ExternObject Object cle##externs, maps [0x800000:0x87ffff]>

In [9]: proj.loader.kernel_object
Out[9]: <KernelObject Object cle##kernel, maps [0xa00000:0xa07fff]>

In [10]: proj.loader.find_object_containing(0x400000)
Out[10]: <ELF Object test, maps [0x400000:0x404037]>
```

#### object self

上面是访问加载的所有对象中的一个或多个。下面是对得到的单个对象进行分析处理。

```python
#可以通过加载的文件名查找对象，如test对象
In [9]: obj_test = proj.loader.find_object("test")

In [10]: obj_test
Out[11]: <ELF Object test, maps [0x400000:0x404037]>

#获取单个加载对象句柄进行分析
In [11]: obj = proj.loader.main_object

In [12]: obj.entry
Out[12]: 0x401050

In [14]: obj.min_addr,obj.max_addr
Out[14]: (0x400000, 0x404037)

In [15]: obj.segments
Out[15]: <Regions: [<ELFSegment flags=0x4, relro=0x0, vaddr=0x400000, memsize=0x4d0, filesize=0x4d0, offset=0x0>, <ELFSegment flags=0x5, relro=0x0, vaddr=0x401000, memsize=0x1f5, filesize=0x1f5, offset=0x1000>, <ELFSegment flags=0x4, relro=0x0, vaddr=0x402000, memsize=0x158, filesize=0x158, offset=0x2000>, <ELFSegment flags=0x4, relro=0x1, vaddr=0x403e10, memsize=0x1f0, filesize=0x1f0, offset=0x2e10>, <ELFSegment flags=0x6, relro=0x0, vaddr=0x404000, memsize=0x38, filesize=0x30, offset=0x3000>]>

In [16]: obj.find_segment_containing(obj.entry)
Out[16]: <ELFSegment flags=0x5, relro=0x0, vaddr=0x401000, memsize=0x1f5, filesize=0x1f5, offset=0x1000>

In [17]: obj.find_section_containing(obj.entry)
Out[17]: <.text | offset 0x1050, vaddr 0x401050, size 0x195>

In [18]: obj.sections
Out[18]: <Regions: [<Unnamed | offset 0x0, vaddr 0x0, size 0x0>, <.interp | offset 0x318, vaddr 0x400318, size 0x1c>, <.note.gnu.property | offset 0x338, vaddr 0x400338, size 0x20>, <.note.gnu.build-id | offset 0x358, vaddr 0x400358, size 0x24>, <.note.ABI-tag | offset 0x37c, vaddr 0x40037c, size 0x20>, <.gnu.hash | offset 0x3a0, vaddr 0x4003a0, size 0x1c>, <.dynsym | offset 0x3c0, vaddr 0x4003c0, size 0x60>, <.dynstr | offset 0x420, vaddr 0x400420, size 0x3f>, <.gnu.version | offset 0x460, vaddr 0x400460, size 0x8>, <.gnu.version_r | offset 0x468, vaddr 0x400468, size 0x20>, <.rela.dyn | offset 0x488, vaddr 0x400488, size 0x30>, <.rela.plt | offset 0x4b8, vaddr 0x4004b8, size 0x18>, <.init | offset 0x1000, vaddr 0x401000, size 0x1b>, <.plt | offset 0x1020, vaddr 0x401020, size 0x20>, <.plt.sec | offset 0x1040, vaddr 0x401040, size 0x10>, <.text | offset 0x1050, vaddr 0x401050, size 0x195>, <.fini | offset 0x11e8, vaddr 0x4011e8, size 0xd>, <.rodata | offset 0x2000, vaddr 0x402000, size 0xf>, <.eh_frame_hdr | offset 0x2010, vaddr 0x402010, size 0x44>, <.eh_frame | offset 0x2058, vaddr 0x402058, size 0x100>, <.init_array | offset 0x2e10, vaddr 0x403e10, size 0x8>, <.fini_array | offset 0x2e18, vaddr 0x403e18, size 0x8>, <.dynamic | offset 0x2e20, vaddr 0x403e20, size 0x1d0>, <.got | offset 0x2ff0, vaddr 0x403ff0, size 0x10>, <.got.plt | offset 0x3000, vaddr 0x404000, size 0x20>, <.data | offset 0x3020, vaddr 0x404020, size 0x10>, <.bss | offset 0x3030, vaddr 0x404030, size 0x8>, <.comment | offset 0x3030, vaddr 0x0, size 0x2a>, <.symtab | offset 0x3060, vaddr 0x0, size 0x5e8>, <.strtab | offset 0x3648, vaddr 0x0, size 0x1ca>, <.shstrtab | offset 0x3812, vaddr 0x0, size 0x11f>]>
        
#函数的plt地址
In [19]: addr = obj.plt['strcmp']
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-19-0be98c749d52> in <module>
----> 1 addr = obj.plt['strcmp']

KeyError: 'strcmp'

In [20]: addr = obj.plt['printf']

In [21]: addr
Out[21]: 0x401040

In [22]: obj.reverse_plt[addr]
Out[22]: 'printf'

#加载的基址信息与内存映射信息
In [23]: obj.linked_base
Out[23]: 0x400000

In [24]: obj.mapped_base
Out[24]: 0x400000
    
# 获取某个section的句柄
In [25]: st = obj.sections[15]

In [26]: st
Out[26]: <.text | offset 0x1050, vaddr 0x401050, size 0x195>

In [27]: st.name
Out[27]: '.text'

In [28]: st.offset
Out[28]: 0x1050

In [31]: st.filesize
Out[31]: 0x195

In [32]: st.vaddr
Out[32]: 0x401050
```

### Symbols and Relocations

加载对象中的符号信息与重定位。

#### Symbols

对于在所有加载对象中查找符号的情况，基于加载对象集合的句柄`cle.Loader`，通过`find_symbol(name)`得到名称对应的符号句柄。

```python
#获取符号句柄
In [36]: s_printf = proj.loader.find_symbol("printf")

In [37]: s_printf
Out[37]: <Symbol "printf" in libc-2.31.so at 0x564e10>
#符号句柄包含此符号所有信息
In [38]: s_printf.name
Out[38]: 'printf'

In [39]: s_printf.owner
Out[39]: <ELF Object libc-2.31.so, maps [0x500000:0x6f14d7]>

In [40]: s_printf.rebased_addr
Out[40]: 0x564e10

In [41]: s_printf.linked_addr
Out[41]: 0x64e10

In [42]: s_printf.relative_addr
Out[42]: 0x64e10

In [43]: s_printf.is_export
Out[43]: True

In [44]: s_printf.is_import
Out[44]: False

#也可以通过find_all_symbols找到所有加载对象中的此符号，返回一个迭代器
In [49]: s_printf = proj.loader.find_all_symbols("printf")

In [50]: s_printf
Out[50]: <generator object Loader.find_all_symbols at 0x7fea87cbd6d0>
```

对于在某个加载对象中寻找符号的情况，基于此对象的句柄, 通过`get_symbol(name)`获得。

```python
#查找main_object中的对象
In [66]: main_printf = proj.loader.main_object.get_symbol('printf')

In [67]: main_printf
Out[67]: <Symbol "printf" in test (import)>

In [68]: main_printf.resolvedby
Out[68]: <Symbol "printf" in libc-2.31.so at 0x564e10>
```

#### Relocations

分析处理加载对象的重定位信息。

对于一个加载对象，分析其中的重定位信息依然从拿到此加载对象的句柄开始。

```python
In [71]: main_obj = proj.loader.main_object

In [72]: main_obj
Out[72]: <ELF Object test, maps [0x400000:0x404037]>

#重定位信息
In [73]: main_obj.relocs
Out[73]:
[<cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89b14970>,
 <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89b14a90>,
 <cle.backends.elf.relocation.amd64.R_X86_64_JUMP_SLOT at 0x7fea89b14cd0>]

#重定位涉及的详细符号信息
In [74]: main_obj.imports
Out[74]:
{'__libc_start_main': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89b14970>,
 '__gmon_start__': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89b14a90>,
 'printf': <cle.backends.elf.relocation.amd64.R_X86_64_JUMP_SLOT at 0x7fea89b14cd0>}

In [80]: libc_obj = proj.loader.shared_objects['libc.so.6']

In [81]: libc_obj
Out[81]: <ELF Object libc-2.31.so, maps [0x500000:0x6f14d7]>

In [82]: libc_obj.imports
Out[82]:
{'__libpthread_freeres': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89a3aeb0>,
 '_rtld_global': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89a3aa90>,
 '__libc_enable_secure': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89a40310>,
 '_rtld_global_ro': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89a40d90>,
 '_dl_starting_up': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89a4ac70>,
 '__libdl_freeres': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89a4afd0>,
 '_dl_argv': <cle.backends.elf.relocation.amd64.R_X86_64_GLOB_DAT at 0x7fea89a40fd0>,
 '__tls_get_addr': <cle.backends.elf.relocation.amd64.R_X86_64_JUMP_SLOT at 0x7fea89a56880>,
 '_dl_exception_create': <cle.backends.elf.relocation.amd64.R_X86_64_JUMP_SLOT at 0x7fea89a561c0>,
 '__tunable_get_val': <cle.backends.elf.relocation.amd64.R_X86_64_JUMP_SLOT at 0x7fea89a56250>,
 '_dl_find_dso_for_object': <cle.backends.elf.relocation.amd64.R_X86_64_JUMP_SLOT at 0x7fea89a56b50>}
```

对于无法通过任何加载对象导出项解决的导入项，CLE引入了`extern object`(声明具有此符号项对应的导出项)。

```python
In [76]: extern_obj = proj.loader.extern_object

In [77]: extern_obj
Out[77]: <ExternObject Object cle##externs, maps [0x800000:0x87ffff]>

In [78]: extern_obj.relocs
Out[78]: []

In [79]: extern_obj.imports
Out[79]: {}
```

### Loading Options

主要是关于加载对象依赖的选项。在使用`angr.Project`创建工程时，便会调用CLE来加载二进制程序。可以通过`Project`来给CLE传参,参考[CLE API docs](http://angr.io/api-doc/cle.html)。

#### basic options

一些基础选项。

最常用的选项`auto_load_libs`: 决定了是否让CLE尝试自动解析所有共享库依赖，默认`auto_load_libs=True`；

`except_missing_libs`: 在存在无法解决的依赖时抛出exception；

`force_load_libs`: 强制加载，传入字符串列表中的每个库都会被视为未解析的共享库依赖；

`skip_libs`: 跳过加载，传入字符串列表中的每个库都不会被视为依赖；

通过传入字符串列表给`ld_path`，作为附加的共享库搜索路径，并且优先于所有默认搜索路径(加载的二进制程序所在文件夹、当前文件夹以及系统库)

#### Per-Binary Options

针对某个加载对象的选项。

对于加载的二进制程序主对象，以`main_opts={[dict]}`的形式传入参数；对于库函数，以`lib_opts={[dict]}`的形式传入参数。

一些常用的参数选项：

- backend：加载时使用的后端
- base_addr：加载的基地址
- entry_point：入口点
- arch：架构

示例

```python
In [85]: proj = angr.Project('./test', main_opts={'backend': 'blob','arch':'x64'}, lib_opts={'libc.so.6': {'backend': 'elf'}})
WARNING | 2021-01-14 16:38:16,261 | cle.backends.blob | No entry_point was specified for blob test, assuming 0
WARNING | 2021-01-14 16:38:16,262 | cle.backends.blob | No base_addr was specified for blob test, assuming 0
```

#### Backends

大多数情况下CLE自己能检测出加载对象需要的后端，特殊情况下需要指定。指定方式如上。下面是一些后端的描述表。

| backend name | description                                                  | requires `arch` |
| ------------ | ------------------------------------------------------------ | --------------- |
| elf          | Static loader for ELF files based on PyELFTools              | no              |
| pe           | Static loader for PE files based on PEFile                   | no              |
| mach-o       | Static loader for Mach-O files. Does not support dynamic linking or rebasing. | no              |
| cgc          | Static loader for Cyber Grand Challenge binaries             | no              |
| backedcgc    | Static loader for CGC binaries that allows specifying memory and register backers | no              |
| elfcore      | Static loader for ELF core dumps 👉这个有点意思               | no              |
| blob         | Loads the file into memory as a flat image                   | yes             |

### Symbolic Function Summaries

符号化函数摘要，用来简化处理一些常见函数。angr通过`SimProcedures`替换的方式实现函数结果的符号化。[SimProcedures列表](https://github.com/angr/angr/tree/master/angr/procedures)。

可以在angr.SIM_PROCEDURES以`angr.SIM_PROCEDURES[package name][name]`的方式引用，如下。

```python
In [88]: angr.SIM_PROCEDURES['libc']['strcmp']
Out[88]: angr.procedures.libc.strcmp.strcmp
```

当某个函数没有摘要时的处理，具体逻辑在[angr.Project._register_object](https://github.com/angr/angr/blob/master/angr/project.py#L233)：

- 如果`auto_load_libs==True`,会执行真实的函数；可能会产生状态爆炸等问题；
- 如果`auto_load_libs==False`,函数暂时无法处理；angr会生成一个通用替换例程`ReturnUnconstrained `来解析，在每次调用时不进行任何操作直接返回一个唯一的无约束符号值。
- 如果`angr.Project`中传入了`use_sim_procedures=False`(默认为真)，那么只有extern object中的符号项会被替换为通用例程`ReturnUnconstrained `。

- 通过给`angr.Project`传入`exclude_sim_procedures_list`与`exclude_sim_procedures_func`黑名单列表排除不用被替换的函数。

#### Hooking

除了angr自己提供的替换例程，也可以编写替换例程。

```python
#得到一个SimProcedures例程
In [89]: stub_func = angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained']

In [90]: proj.hook(0x10000, stub_func())

In [91]: proj.is_hooked(0x10000)
Out[91]: True

In [92]: proj.hooked_by(0x10000)
Out[92]: <SimProcedure ReturnUnconstrained>

In [93]: proj.unhook(0x10000)
```

也可以hook某段指令(长度)，替换为自己的函数

```python
In [94]: @proj.hook(0x20000, length=5)
    ...: def my_hook(state):
    ...:     state.regs.rax = 1
    ...:

In [95]: proj.is_hooked(0x20000)
Out[95]: True
```

也可以通过hook_symbol来创建自己的例程替换。

```python
In [97]: class fakemain(SimProcedure):
    ...:     def run(self, argc, argv):
    ...:         print('Program running with argc=%s and argv=%s' % (argc, argv))
    ...:         return 0
    ...:
In [113]: proj.hook_symbol('main', fakemain())
Out[113]: 0x401136
```



## Solve Engine

angr的求解引擎部分，底层是z3。

### Working with Bitvectors 

数据以bitvector(下文简称BV)组织，方便于二进制程序的分析。

#### concrete value

```python
#创建angr工程
>>> import angr
>>> proj = angr.Project('./test')
>>> state = proj.factory.entry_state()
#常量计算操作   state.solver.BVV(value,bit num)
#64位常量1
>>> one = state.solver.BVV(1, 64)
>>> one
<BV64 0x1>

>>> one_h= state.solver.BVV(100, 64)
>>> one+one_h
<BV64 0x65>
# 27位的位向量9
>>> nine = state.solver.BVV(9, 27)
>>> nine
<BV27 0x9>
#计算必须在等位长的bitvector上进行
>>> one+nine
---------------------------------------------------------------------------
ClaripyOperationError                     Traceback (most recent call last)
<ipython-input-8-9e4ad504243f> in <module>
----> 1 one+nine

~/.virtualenvs/sym/lib/python3.8/site-packages/claripy/operations.py in _op(*args)
     48                 success, msg = extra_check(*fixed_args)
     49                 if not success:
---> 50                     raise ClaripyOperationError(msg)
     51
     52         #pylint:disable=too-many-nested-blocks

ClaripyOperationError: args' length must all be equal

#可以扩展位长，多种扩展模式:zero_extend sign_extend
#0扩展，长度64-27
>>> ex_nine = nine.zero_extend(64 - 27)
>>> ex_nine
<BV64 0x9>
>>> one+ex_nine
<BV64 0xa>

#sign_extend
>>> sign_nine = nine.sign_extend(64 - 27)
>>> sign_nine
<BV64 0x9>

```

#### symbolic value

```python
>>> x = state.solver.BVS("x", 64)
>>> x
<BV64 x_40_64>

>>> y = state.solver.BVS("y", 64)
>>> y
<BV64 y_41_64>

#与其他位向量混合计算 会得到一个抽象语法树AST
>>> (x + y + one) / 2
<BV64 (x_40_64 + y_41_64 + 0x1) / 0x2>
```

#### AST

位向量的计算会生成一个抽象语法树AST，位向量本身也可以看作一个AST，可以对这个抽象语法树进行处理。

```python
>>> tree = (x + 1) / (y + 2)
#AST的根
>>> tree
<BV64 (x_40_64 + 0x1) / (y_41_64 + 0x2)>
>>> tree.op
'__floordiv__'
>>> tree.args
(<BV64 x_40_64 + 0x1>, <BV64 y_41_64 + 0x2>)

#AST的第1层
>>> tree.args[0]
<BV64 x_40_64 + 0x1>
>>> tree.args[1]
<BV64 y_41_64 + 0x2>

#AST的第2层
>>> tree.args[1].op
'__add__'
>>> tree.args[1].args[0]
<BV64 y_41_64>
>>> tree.args[1].args[1]
<BV64 0x2>

#AST的最底层
>>> tree.args[1].args[1].args
(2, 64)
>>> tree.args[1].args[1].op
'BVV'
```

需要注意的是，不管是具体值还是符号值，虽然创建的时候时通过state.solver创建的，但其本身的存在并不依赖于状态，而是独立存在，可以在所有状态中使用的。

### Symbolic Constraints

符号约束。当位向量代表的AST进行比较时，会得到一个符号化的布尔值。

```python
>>> x==1
<Bool x_40_64 == 0x1>

>>> x + y == one_h + 5
<Bool x_40_64 + y_41_64 == 0x69>

>>> one_h>5
<Bool True>

>>> x>2
<Bool x_40_64 > 0x2>

#注意 比较为无符号比较  有符号比较用SGT方法
>>> one_h>-5
<Bool False>
>>> one_h.SGT(-5)
<Bool True>

```

由于比较总是返回一个bool的符号，所以实际使用中，用到的是`solver.is_true`或者`solver.is_false`。

```python
>>> state.solver.is_true(x>y)
False

>>> state.solver.is_true(one_h>one)
True

>>> yes = one == 1

>>> state.solver.is_true(yes)
True
```

### Constraint Solving

约束求解。添加的每个bool符号表达式可以看作一个对符号变量的约束，利用z3求解器可以得到一个满足所有约束的变量值。

```python
>>> state.solver.add(x > y)
[<Bool x_40_64 > y_41_64>]

>>> state.solver.add(y > 2)
[<Bool y_41_64 > 0x2>]

>>> state.solver.add(10 > x)
[<Bool x_40_64 < 0xa>]

>>> state.solver.eval(x)
8
```

一个程序运行时约束求解的类似过程：

```python
#程序某个状态
>>> state = proj.factory.entry_state()
#构建输入符号
>>> input = state.solver.BVS('input', 64)

>>> operation = (((input+4)*3)>>1)+input

>>> output=200
#构建约束  op(输入)==输出
>>> state.solver.add(operation == output)
[<Bool ((input_42_64 + 0x4) * 0x3 >> 0x1) + input_42_64 == 0xc8>]
#求得输入
>>> state.solver.eval(input)
0x3333333333333381

#可以提前检查是否存在满足条件的解
>>> state.satisfiable()
True
```

### Floating point numbers

浮点数处理。相比于bitvector

具体值：`BVV`对应`FPV`; 符号值：`BVS`对应`FPS`

```python
>>> a = state.solver.FPV(3.2, state.solver.fp.FSORT_DOUBLE)
>>> a
<FP64 FPV(3.2, DOUBLE)>

>>> b = state.solver.FPS('b', state.solver.fp.FSORT_DOUBLE)
>>> b
<FP64 FPS(FP_b_43_64, DOUBLE)>

#计算操作与比较操作
>>> a+b
<FP64 fpAdd(RM.RM_NearestTiesEven, FPV(3.2, DOUBLE), FPS(FP_b_43_64, DOUBLE))>

>>> a + 4.4
<FP64 FPV(7.6000000000000005, DOUBLE)>

>>> b + 2 < 0
<Bool fpLT(fpAdd(RM.RM_NearestTiesEven, FPS(FP_b_43_64, DOUBLE), FPV(2.0, DOUBLE)), FPV(0.0, DOUBLE))>
```

可以看到浮点数计算相比bitvector的话多出了第一个参数，这是支持四舍五入模式(solver.fp.RM_*)的操作需要的参数。

求解操作基本和BV差不多

```python
>>> state.solver.add(b + 2 < 0)
[<Bool fpLT(fpAdd(RM.RM_NearestTiesEven, FPS(FP_b_43_64, DOUBLE), FPV(2.0, DOUBLE)), FPV(0.0, DOUBLE))>]

>>> state.solver.add(b + 2 > -1)
[<Bool fpGT(fpAdd(RM.RM_NearestTiesEven, FPS(FP_b_43_64, DOUBLE), FPV(2.0, DOUBLE)), FPV(-1.0, DOUBLE))>]

>>> state.solver.eval(b)
-2.000000000253086
```

#### BV<=>FP

##### ①各位不变的转换

也就是保留各位，只是不同的解释；使用`raw_to_bv`与`raw_to_fp`方法可实现转换。

```
>>> a.raw_to_bv()
<BV64 0x400999999999999a>

>>> b.raw_to_bv()
<BV64 fpToIEEEBV(FPS(FP_b_43_64, DOUBLE))>

>>> state.solver.BVV(0, 64).raw_to_fp()
<FP64 FPV(0.0, DOUBLE)>

>>> state.solver.BVS('x', 64).raw_to_fp()
<FP64 fpToFP(x_44_64, DOUBLE)>
```

##### ②值近似的转换

也就是尽可能地转为近似的值；使用方法`val_to_fp`与`val_to_bv`实现转换。

```python
>>> a
<FP64 FPV(3.2, DOUBLE)>

>>> a.val_to_bv(12)
<BV12 0x3>

>>> a.val_to_bv(12).val_to_fp(state.solver.fp.FSORT_FLOAT)
<FP32 FPV(3.0, FLOAT)>
```

### More Solving Methods

​	前面只用到了eval求解表达式的一个可能值，下面是更多其他的求解相关API

| API                                | 用途                                             |
| ---------------------------------- | ------------------------------------------------ |
| solver.eval(expression)            | 得到表达式的一个可能值                           |
| solver.eval_one(expression)        | 得到表达式的一个值，如果多余一个可能值则抛出报错 |
| solver.eval_upto(expression, n)    | 得到表达式的至多n个可能值                        |
| solver.eval_atleast(expression, n) | 得到表达式的至少n个可能值，少于n个抛出报错       |
| solver.eval_exact(expression, n)   | 表达式的n个值，多余或少于n个都会抛出报错         |
| solver.min(expression)             | 表达式最小可能值                                 |
| solver.max(expression)             | 表达式最大可能值                                 |

#### extra paraments

上述API都能接受一些额外的参数

- extra_constraints：被用进此次约束求解，但是不会被放入模型状态中(存放)。
- cast_to(只能是cast_to=int 或 cast_to=bytes)：将结果转换为相应的形式。

```python
>>> x
<BV64 x_40_64>

>>> y
<BV64 y_41_64>

>>> state.solver.add(x+y>one)
[<Bool x_40_64 + y_41_64 > 0x1>]

>>> state.solver.add(x+y<100)
[<Bool x_40_64 + y_41_64 < 0x64>]
#extra constraints
>>> state.solver.eval(x,extra_constraints=(x>44,y<30))
0x30
>>> state.solver.constraints
[<Bool x_40_64 + y_41_64 > 0x1>, <Bool x_40_64 + y_41_64 < 0x64>]

#cast to
>>> state.solver.eval(state.solver.BVV(0x41424344, 32), cast_to=bytes)
b'ABCD'
```



## Program State

前面其实已经使用过很多次`simstate`了，这里对`simstate`中保存的所有可获取的运行时信息，包括`simstate`的结构与使用方式进行一个统一的解释。

### registers and memory

首先是最基础的，符号化的内存与寄存器访问，任何BV类型的AST都能放入寄存器或者内存中。

```python
>>> import angr,claripy

>>> proj = angr.Project("./check")

>>> state =proj.factory.entry_state()

>>> state.regs.rbp
<BV64 0x0>

>>> state.regs.rsp
<BV64 0x7fffffffffeff88>

>>> state.regs.rbp = state.regs.rsp

>>> state.regs.rbp
<BV64 0x7fffffffffeff88>

>>> state.mem[0x1000].uint64_t
WARNING | 2021-01-15 10:28:03,985 | angr.storage.memory_mixins.default_filler_mixin | The program is accessing memory or registers with an unspecified value. This could indicate unwanted behavior.
WARNING | 2021-01-15 10:28:03,985 | angr.storage.memory_mixins.default_filler_mixin | angr will cope with this by generating an unconstrained symbolic variable and continuing. You can resolve this by:
WARNING | 2021-01-15 10:28:03,985 | angr.storage.memory_mixins.default_filler_mixin | 1) setting a value to the initial state
WARNING | 2021-01-15 10:28:03,985 | angr.storage.memory_mixins.default_filler_mixin | 2) adding the state option ZERO_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to make unknown regions hold null
WARNING | 2021-01-15 10:28:03,985 | angr.storage.memory_mixins.default_filler_mixin | 3) adding the state option SYMBOL_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to suppress these messages.
WARNING | 2021-01-15 10:28:03,986 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0x1000 with 8 unconstrained bytes referenced from 0x4010d0 (_start+0x0 in check (0x4010d0))
<uint64_t <BV64 mem_1000_38_64{UNINITIALIZED}> at 0x1000>

>>> state.regs.rdx
<BV64 0x800018>

>>> state.mem[0x1000].uint64_t = state.regs.rdx

#resolved 解析为BV
>>> state.mem[0x1000].uint64_t
<uint64_t <BV64 0x800018> at 0x1000>
>>> state.mem[0x1000].uint64_t.resolved
<BV64 0x800018>

>>> state.regs.rbp = state.mem[state.regs.rbp].uint64_t.resolved
>>> state.regs.rbp
<BV64 0x1>

>>> state.regs.rax += state.mem[state.regs.rsp + 8].uint64_t.resolved
>>> state.regs.rax
<BV64 0x7fffffffffeffe4>
```

### Basic Execution

符号执行可以看作一个one_state 到next_state的过程。

类似调试，angr使用`state.step()`完成步进操作。每次步进会返回[SimSuccessors](http://angr.io/api-doc/angr.html#module-angr.engines.successors)，包含这次步进操作后的所有后继状态，如下：

```python
>>> import angr,claripy

>>> proj = angr.Project("./check")

>>> state = proj.factory.entry_state(stdin=angr.SimFile)

>>> succ = state.step()

>>> succ.successors
[<SimState @ 0x526fc0>]

>>> while True:
...     succ = state.step()
...     if len(succ.successors)==2:
...         break
...     state = succ.successors[0]
...
...
>>> state1, state2 = succ.successors
>>> state1
<SimState @ 0x401215>
>>> state2
<SimState @ 0x401223>
```

当遇到分支时，会执行所有的分支。因此在使用angr进行符号执行时需要注意出现路径爆炸的问题。

尝试求两种状态下的输入，使用`state.posix.stdin.load(0, state.posix.stdin.size)`，这个后面会具体讲。

```python
>>> input_data = state1.posix.stdin.load(0, state.posix.stdin.size)
>>> input_data
<BV472 file_1_stdin_0_40_1024{UNINITIALIZED}[1023:552]>

>>> state1.solver.eval(input_data, cast_to=bytes)
b'hello_angr\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x89\x00\x00\x00\x00\x00!I\x00\x00\x02\x00\x02\x00\x04\x02\x02\x02\x02\x02\x02\x02\x02\x04\x04\x01\x01\xa0\x0e\x02\x8a)K\x00\x89\x08\x08\x08\x08'

>>> state2.solver.eval(input_data, cast_to=bytes)
b'\x0cK+)J\x19\x89\x89\x02\x01\x02\x01\x01\x0e\x02\x00\x02\xc1\x08+)\x00\x19\x01\x01\x00\x01\x00\x0e\x02\xf0+\x01\x02N\x02\x02)\x01\x08!\x01\x02\x02\x89\x00\x08\x08\x89\x89\x01\x19@\x01)MJ\x00\x00'

```

### State Presets

关于`SimState`模拟执行状态的设置。前面我们创建完angr工程后，都是通过`proj.factory.entry_state()`将初始状态设置在程序执行入口处。

除此之外，还有些其他的初始状态设置函数可以方便我们灵活的设置初始状态。

| API                | 含义                                                         |
| ------------------ | ------------------------------------------------------------ |
| .blank_state()     | 创建一个空状态，此状态下的大多数数据都处于未初始化状态       |
| .entry_state()     | 创建一个位于主加载对象入口点的状态                           |
| .full_init_state() | 和entry_state很相似，不过更前一点，程序还未被初始化时(也就是还没执行动态加载之前)，从这个状态开始会先执行各初始器然后到达entry_state |
| .call_state()      | 创建一个准备执行给定函数的状态                               |

上述API接受的参数定制

- addr：选择一个特定的地址
- env：对于需要外部环境命令行参数运行的，可以通过env传入参数到`entry_state`和`full_init_state`。默认args为空，对于需要args的程序，依赖此参数。
- argc：通过将argc设置为一个符号化的BV来符号化argc；此外需要手动添加约束`argc<=argvs中参数数量`
- call_state调用形式`.call_state(addr, arg1, arg2, ...)`，addr是需要调用的函数地址，argN是传入参数，可以是python 整数，字符串，数组或者BV。如果需要传入对象指针的话，使用指针包装，`angr.PointerWrapper("point to me!")`

- 还有些其他的参考 [docs on the project.factory object (an AngrObjectFactory)](http://angr.io/api-doc/angr.html#angr.factory.AngrObjectFactory) 

### Low level interface for memory

关于符号化内存，更加细节的使用描述。

前面关于内存操作都是使用`state.mem`，这里介绍更为灵活更底层的API`state.memory`和`state.registers`

- 读内存`state.memory.load(addr, size)`
- 写内存`state.memory.store(addr,val)`
- `state.registers.load`与`state.registers.store`
- endness：大端`archinfo.Endness.LE`与小端`archinfo.Endness.LE`

```python
>>> state = proj.factory.blank_state()

>>> state.memory.store(0x4000,state.solver.BVV(0x0123456789abcdef0123456789abcdef, 128))
>>> state.memory.load(0x4000,16)
<BV128 0x123456789abcdef0123456789abcdef>

>>> import archinfo

>>> state.arch.memory_endness
'Iend_LE'
>>> state.memory.load(0x4000, 4, endness=archinfo.Endness.LE)
<BV32 0x67452301>
>>> state.memory.load(0x4000, 4, endness=archinfo.Endness.BE)
<BV32 0x1234567>

>>> state.registers.load("rax",4)
<BV32 reg_10_45_64{UNINITIALIZED}[31:0]>

>>> state.regs.rax
<BV64 reg_10_45_64{UNINITIALIZED}>

>>> state.registers.store("rax",state.solver.BVV(0xff,64))

>>> state.regs.rax
<BV64 0xff>
```

### State Options

一些状态设置选项，用来在某些情况下优化程序。[文档](https://docs.angr.io/appendix/options)

对于每个模拟执行的状态，`state.options`表示其所有State Options，可以通过add操作加入选项或remove移除选项。

也可以在创建状态时传入`add_options`或者`remove_options`来添加或移除选项。

```python
>>> state.options.add(angr.options.LAZY_SOLVES)

#注意 大写的option是单个选项对象，小写的option为一个集合，所以可以看到add和remove传入的对象不一样
>>> s = proj.factory.entry_state(add_options={angr.options.LAZY_SOLVES})

>>> s = proj.factory.entry_state(remove_options=angr.options.simplification)
```

### State Plugins

除了`State Options`,其他的所有`SimState`存放的信息均以插件的形式存在，包括`memory`, `registers`, `mem`, `regs`, `solver`等，以方便使用者定制以及加入新的存储信息或者修改现有存储信息的实现。

比如可以自己实现`memory`插件以将angr中的平坦内存区域改为动态抽象内存。这种实现也能简化某些操作，比如`state.registers`和`state.memory`其实是一个插件的不同实例。

#### The globals plugin

即`states.globals`，实现了一个标准的python dict接口，方便在一个状态中存放任何数据。

#### The history plugin

即`state.history`，记录了程序执行到此状态的路径历史数据信息，是一系列的历史节点，可以通过如`state.history.parent.parent`方式进行访问。

数据信息存放在`state.history.recent_数据名`中，可供迭代的对象为`state.history.数据名`。

```python
>>> for addr in state.history.bbl_addrs:
...     print(hex(addr))
...
0x4010d0
0x526fc0
0x401240
0x401000
0x401016
0x401271
0x401277
0x4011b0
0x401140
0x401170
0x40128d
0x401296
0x800050
0x4011b6
0x4010b0
0x59d260
0x4011cc
0x401090
0x5a36c0
0x4011e6
0x4010c0
0x566230
0x4011fe
0x4010a0
0x5a22d0
#前一个基本块地址
>>> hex(state.history.recent_bbl_addrs[0])
'0x5a22d0'
#前一个的前一个基本块地址
>>> hex(state.history.parent.recent_bbl_addrs[0])
'0x4010a0'
#这样迭代非常麻烦，可以通过hardcopy函数来快速获得所有的
>>> state.history.bbl_addrs.hardcopy
[4198608, 5402560, 4198976, 4198400, 4198422, 4199025, 4199031, 4198832, 4198720, 4198768, 4199053, 4199062, 8388688, 4198838, 4198576, 5886560, 4198860, 4198544, 5912256, 4198886, 4198592, 5661232, 4198910,4198560,5907152]
```

除此之外，history插件还存放了一些其他东西，这里盘点一下

| 对象                 | 含义                                                         |
| -------------------- | ------------------------------------------------------------ |
| history.descriptions | 每轮执行的字符串列表                                         |
| history.bbl_addrs    | 到此状态时执行的所有基本块地址(部分是SimProcedures hook的地址) |
| history.jumpkinds    | 状态历史上的所有控制流转换类型                               |
| history.jump_guards  | 记录路径上的所有跳转的判定（True or False）                  |
| history.events       | 记录状态历史上的一些有趣事件的字符串列表(比如符号化的跳转，弹框，程序结束以及退出代码) |
| history.actions      | 通常为空，当给状态添加`angr.options.refs`选项时，会记录程序执行到此状态的所有的内存，寄存器和临时值获取情况；内存消耗巨大，但是对于反向回溯程序执行过程很有效 |

下面是一些示例

```python
>>> state.history.descriptions.hardcopy
['<IRSB from 0x4010d0: 1 sat>',
 '<SimProcedure __libc_start_main from 0x526fc0: 1 sat>',
 '<IRSB from 0x401240: 1 sat>',
 '<IRSB from 0x401000: 1 sat 1 unsat>',
 '<IRSB from 0x401016: 1 sat>',
 '<IRSB from 0x401271: 1 sat 1 unsat>',
 '<IRSB from 0x401277: 1 sat>',
 '<IRSB from 0x4011b0: 1 sat>',
 '<IRSB from 0x401140: 1 sat 1 unsat>',
 '<IRSB from 0x401170: 1 sat>',
 '<IRSB from 0x40128d: 1 sat 1 unsat>',
 '<IRSB from 0x401296: 1 sat>',
 '<SimProcedure __libc_start_main from 0x800050: 1 sat>',
 '<IRSB from 0x4011b6: 1 sat>',
 '<IRSB from 0x4010b0: 1 sat>',
 '<SimProcedure malloc from 0x59d260: 1 sat>',
 '<IRSB from 0x4011cc: 1 sat>',
 '<IRSB from 0x401090: 1 sat>',
 '<SimProcedure memset from 0x5a36c0: 1 sat>',
 '<IRSB from 0x4011e6: 1 sat>',
 '<IRSB from 0x4010c0: 1 sat>',
 '<SimProcedure __isoc99_scanf from 0x566230: 1 sat>',
 '<IRSB from 0x4011fe: 1 sat>',
 '<IRSB from 0x4010a0: 1 sat>',
 '<SimProcedure strcmp from 0x5a22d0: 1 sat>']

>>> state.history.jumpkinds.hardcopy
['Ijk_Boring', 'Ijk_Call', 'Ijk_Call', 'Ijk_Call', 'Ijk_Boring', 'Ijk_Ret', 'Ijk_Boring', 'Ijk_Call', 'Ijk_Boring', 'Ijk_Boring', 'Ijk_Ret', 'Ijk_Boring', 'Ijk_Ret', 'Ijk_Call', 'Ijk_Call', 'Ijk_Boring', 'Ijk_Ret', 'Ijk_Call', 'Ijk_Boring', 'Ijk_Ret', 'Ijk_Call', 'Ijk_Boring', 'Ijk_Ret', 'Ijk_Call', 'Ijk_Boring', 'Ijk_Ret']

>>> state.history.jump_guards.hardcopy
[<Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>, <Bool True>]

>>> state.history.events.hardcopy
[<SimActionData __libc_start_main() reg/read>,
 <SimActionData __libc_start_main() reg/read>,
 <SimActionData __libc_start_main() reg/read>,
 ...
 <SimActionData strcmp() reg/read>,
 <SimActionData strcmp() reg/write>,
 <SimActionData strcmp() reg/write>]


```

其中history.actions这个在AEG中很常用到，来反向搜索crash原因。下面是一个演示

```
#由于此功能启用需要添加angr.options.refs选项
>>> state = proj.factory.entry_state(stdin=angr.SimFile,add_options=angr.options
... .refs)

>>> while True:
...     succ = state.step()
...     if len(succ.successors)==2:
...         break
...     state = succ.successors[0]
...
WARNING | 2021-01-15 17:11:56,344 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0xc0000f7c with 68 unconstrained bytes referenced from 0x5a22d0 (strcmp+0x0 in libc.so.6 (0xa22d0))

>>> state.history.actions.hardcopy
[<SimActionData 0x4010d0:2 reg/write>,
 <SimActionData 0x4010d0:4 reg/read>,
...
 <SimActionData __isoc99_scanf() file_5_stdin/read>,
 <SimActionConstraint __isoc99_scanf() <SAO <Bool file_5_stdin_0_55_1024{UNINITIALIZED}[767:760] != 10>>>,
 ...]

>>> state.history.recent_actions
[<SimActionData strcmp() reg/read>,
 <SimActionData strcmp() reg/read>,
 ...
 <SimActionData strcmp() reg/write>,
 <SimActionExit strcmp() conditional>,
 <SimActionData strcmp() reg/write>]

```

#### The callstack plugin

记录了调用栈信息。通过`state.call_stack`查看，上一个的`call_stack`通过`state.call_stack.next`查看。

```python
>>> state.callstack
<CallStack (depth 3)>

>>> state.callstack.next
<CallStack (depth 2)>

>>> state.callstack.func_addr
4198838

>>> hex(state.callstack.func_addr)
'0x4011b6'
```

call_stack的一些属性

| 属性                     | 含义                     |
| ------------------------ | ------------------------ |
| callstack.func_addr      | 当前执行的函数地址       |
| callstack.call_site_addr | 调用当前函数的基本块地址 |
| callstack.stack_ptr      | 当前函数开始时的栈指针   |
| callstack.ret_addr       | 当前函数执行后的返回地址 |

### More about I/O: Files, file systems, and network sockets

参考文档 [Working with File System, Sockets, and Pipes](https://docs.angr.io/advanced-topics/file_system)

### Copying and Merging

#### copy

为了支持更加方便的对状态进行探索和操作，angr提供了快速的拷贝。

```python
>>> proj = angr.Project("./check")

>>> state =  proj.factory.blank_state()

>>> s1 = state.copy()

>>> s2 = state.copy()

>>> s1.mem[0x1000].uint32_t = 0x41414141

>>> s2.mem[0x1000].uint32_t = 0x42424242
```

#### merge

状态合并操作: `state1.merge(state2)`。会返回一个元组(合并后的状态，描述状态flag的符号变量，描述是否合并完成的布尔值)

```python
>>> (s_merged, m, anything_merged) = s1.merge(s2)

>>> aaaa_or_bbbb = s_merged.mem[0x1000].uint32_t

>>> aaaa_or_bbbb
<uint32_t <BV32 0x414141 .. (if state_merge_0_82_16 == 0x1 then 66 else (if state_merge_0_82_16 == 0x0 then 65 else 0))> at 0x1000>

>>> m
[<Bool state_merge_0_82_16 == 0x0>, <Bool state_merge_0_82_16 == 0x1>]

>>> anything_merged
True
```

## Simulation Managers

符号执行引擎的主要控制接口。通过其`step`命令可以以基本块或单条指令的方式模拟步进执行，配合用户定义的算法，可以自由的探索程序的执行状态。

angr为了方便状态的管理，提供了一个被称为`stash`的结构用于将需要的状态分类组织起来。大多数操作的默认stash是`active`stash。

对simgr的使用从创建它开始。simgr可以直接通过proj进行创建，也可以创建从某个状态开始的simgr。

```python
>>> import angr

>>> proj = angr.Project("./check",auto_load_libs=False)

>>> simgr = proj.factory.simgr()

>>> state = proj.factory.full_init_state()

>>> simgr = proj.factory.simgr(state)

>>> simgr
<SimulationManager with 1 active>
```

### stepping

基础用法`simgr.step()`，与上一节的state.step有些相似，用来进行模拟执行。

```python
>>> import angr

>>> proj = angr.Project("./check")

>>> proj = angr.Project("./check",auto_load_libs=False)

>>> state = proj.factory.entry_state()

>>> simgr = proj.factory.simgr(state)

>>> simgr.active
[<SimState @ 0x4010d0>]

>>> simgr.step()
<SimulationManager with 1 active>

>>> simgr.active
[<SimState @ 0x500000>]
```

在step过程中，会将所有遇到的状态归类放入相应的stash中。比如active stash收集了当前的所有在活跃的分支。当一个活跃的状态无法产生任何的successor(见`simstate.successors`)的时候，会被转移到deadended stash。

```python
>>> while len(simgr.active)==1:
...     simgr.step()
...
WARNING | 2021-01-17 15:51:08,720 | angr.storage.memory_mixins.default_filler_mixin | The program is accessing memory or registers with an unspecified value. This could indicate unwanted behavior.
WARNING | 2021-01-17 15:51:08,720 | angr.storage.memory_mixins.default_filler_mixin | angr will cope with this by generating an unconstrained symbolic variable and continuing. You can resolve this by:
WARNING | 2021-01-17 15:51:08,720 | angr.storage.memory_mixins.default_filler_mixin | 1) setting a value to the initial state
WARNING | 2021-01-17 15:51:08,720 | angr.storage.memory_mixins.default_filler_mixin | 2) adding the state option ZERO_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to make unknown regions hold null
WARNING | 2021-01-17 15:51:08,720 | angr.storage.memory_mixins.default_filler_mixin | 3) adding the state option SYMBOL_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to suppress these messages.
WARNING | 2021-01-17 15:51:08,720 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0xc0000f7d with 67 unconstrained bytes referenced from 0x500018 (strcmp+0x0 in extern-address space (0x18))

>>> simgr
<SimulationManager with 2 active>

>>> simgr.active
[<SimState @ 0x401215>, <SimState @ 0x401223>]

>>> simgr.run()
<SimulationManager with 2 deadended>

>>> simgr.deadended
[<SimState @ 0x601058>, <SimState @ 0x601058>]
```

### stash management

由前面可以知道，当通过simgr进行符号执行时，一般通过stash来对同一类状态进行组织。下面部分便是解释如何对这些stash以及其中的状态进行管理。

```python
#将符合条件的状态在stash间移动
#simgr.move(from_stash='源stash名称',to_stash='目的stash名称',filter_func=筛选函数)
>>> simgr.move(from_stash='deadended',to_stash='target',filter_func=lambda s
... : b'good flag' in s.posix.dumps(1))
<SimulationManager with 1 deadended, 1 target>

>>> simgr
<SimulationManager with 1 deadended, 1 target>
```

这里面的每个stash就是一个类的列表，可以简单的通过迭代器访问：

```python
>>> for sta in simgr.deadended + simgr.target :
...     print(hex(sta.addr))
...
0x601058
0x601058
```

对每个stash，可以通过`simgr.one_stashName`的方式访问其状态列表的第一个状态，亦可以通过`simgr.mp_stashName`同时对stash中的所有状态进行操作。那些针对`SimState`的操作也可以通过这个方式应用到stash中的状态。

```python
>>> simgr.one_target
<SimState @ 0x601058>

>>> simgr.mp_target
MP([<SimState @ 0x601058>, <SimState @ 0x601058>])

>>> simgr.mp_target.posix.dumps(0)
MP([b'hello_angr\x00\x02\x02\x02\x02\x08I\x02\x02\x89\x89\x06"\x08\x02\x01\x01\x08F\x01\x08\x02\x02\x01\x01)\x06\x01\x01I\x02\x80\x02\x02\x08\x19\x19\x89\x89\x8a\x01\x02\x08\x89\x89\x01\x89\x89\x00\x08', b'J\x0f)\x19\x1a\x8aI)I\x0c\x02I\x89\x1a\x89\x02IIJ\x89\x89\x02\x80IJ\x0e\x02\x89V\x08\x08\x00\x04)\x19\x89\x0eI)I\x0e\x02I\x89\x19\x89\x02IIJ\x89\x89\x02\x94IJ\x01\x02\x02\x00'])

>>> simgr.mp_target.step()
MP([<SimProcedure PathTerminator from 0x601058: empty>, <SimProcedure PathTerminator from 0x601058: empty>])
```

### stash type

上面使用到了两个默认的stash：`active` 和`deadended`，除此之外还通过move操作间接创建了自定义的一个stash：`target`。除了这两个默认的stash，angr还提供了一些默认的其他stash。

| Stash         | 含义                                                         |
| ------------- | ------------------------------------------------------------ |
| active        | 包含了下一次会被step的state,除非选定了其他的stash            |
| deadended     | 包含了所有因为某种原因(如无可用指令，后继状态皆无解或者非法指令指针等)无法再继续执行下去的state |
| pruned        | 这个涉及到前面讲的`LAZY_SOLVES`,在此运行模式下，除非必要，一般不会检查模型的可满足性。一旦某个状态在此模式下被检查为unsat，那么便会反向追溯到其历史上的第一个unsat状态，并将从此状态点之后的所有状态(均为unsat)均放入此stash。根据其中文意思修剪可知，这些都是被剪掉的无解状态。 |
| unconstrained | 如果给simgr构造器提供了`save_unconstrained`参数，便会将模拟执行中所有指令指针受用户数据或其他符号化数据控制的状态归纳到此stash |
| unsat         | 如果给simgr构造器提供了`save_unsat`参数，所有无解状态都会归纳到此stash |

除了stash意外，还有个状态列表叫做`errored`。当一个状态抛出了错误时，此状态和抛出的错误会被包装为一个`ErrorRecord`对象，被记录到`errored`中。通过`record.state`获取此状态，`record.error`获取抛出的错误，`record.debug()`获得一个debug shell(这个目前本人似乎没咋用过)。

### Simple Exploration

在符号执行的过程中，需求往往是找打一个能执行到某个地址或满足某个需求的状态，angr提供了`simgr.explore()`来满足这个需求。

- 通过给explore传入`find`参数，来锁定目标，angr会一直运行所有的状态直到找到一个满足find条件的状态；
- find可以是一条指令地址，一系列的指令地址，或者是一个可以对`SimState`进行分析判定是否满足需求的函数；
- 当active中有状态满足find条件时，angr会将其放入`found stash`，当找到了需要个数的状态后，angr会终止执行。通过`num_find`来设置需要的状态个数，默认是1；
- 也可以给explore传入`avoid`参数，格式和find一样，用来避开某些状态，所有触发avoid的状态都会被放入avoided stash。

```python
>>> import angr

>>> proj = angr.Project("./check",auto_load_libs=False)

>>> simgr = proj.factory.simgr()

>>> simgr = proj.factory.simgr()

>>> simgr.explore(find=lambda s: b"good flag" in s.posix.dumps(1))
WARNING | 2021-01-17 16:59:50,503 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0xc0000f7d with 67 unconstrained bytes referenced from 0x500018 (strcmp+0x0 in extern-address space (0x18))
<SimulationManager with 1 active, 1 found>

>>> len(simgr.found)
1

>>> state = simgr.one_found

>>> print(state.posix.dumps(0))
b'hello_angr\x00\x89\x89\x08(\x08\x80\x80\x04\x02J\x02\x04\x02\x08\x01\x10\x08\x02\x02\x01\x01\x01\x01\x01\x01\x01\x08\x10\x08\x02@\x00\x02\x02\x80\x80\x0e\x02\x01\x01\x02\x19\x80\x80\x80\x80\x80\x00\x00'

#试一下avoid
>>> simgr = proj.factory.simgr()

>>> simgr.explore(avoid=lambda s: b"good flag" in s.posix.dumps(1))
WARNING | 2021-01-17 17:01:59,742 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0xc0000f7d with 67 unconstrained bytes referenced from 0x500018 (strcmp+0x0 in extern-address space (0x18))
<SimulationManager with 1 deadended, 1 avoid>

>>> state = simgr.one_avoid

>>> print(state.posix.dumps(0))
b'hello_angr\x00)\x00\x00\x00\x02\x08\x00\x00\x00I\x00\x00\x00\x00I\x01\x02\x00\x02\x00\x01\x01\x02\x02\x08\x01\x01\x01*\x02I\x02\x8a\x0e\x02\x02\x80*\x02\x19@\x08\x89\x89\x89\x89\x89\x89\x04'
```

### Exploration Techniques

前面一小节讲了使用`explore`函数对程序进行探索，包括之前的章节的`step`其实也是一种探索，在使用step函数进行探索的时候其实可以发现，这是一种广度优先探索，每一步会执行掉当前所有active中的状态，而非沿着一条路径执行到底(深度优先)后执行另一条路径。

因此angr提供了`Exploration Techniques`来定义探索的模式，使得分析更加的灵活。后续章节还会讲如何写一个自己的`Exploration Techniques`。

通过`simgr.use_technique(tech)`来使用一个探索技术。其中tech是一个`ExplorationTechnique`类的实例。angr提供了内建的一些`ExplorationTechnique`，在`angr.exploration_techniques`下。

下面是一个内建探索技术的概览。其中加粗的explorer、Oppologist以及Tracer这三个在aeg下比较好用。

- DFS
  - 深度优先。具体实现为每次只将一个状态放入`active` stash，剩余的放入`deferred`stash 直到当前这个执行终止或出错。
- **Explorer**
  - 也就是explorer函数的实现方式，可以搜索或者绕开某个地址或满足某个条件的状态。
- LengthLimiter
  - 设置一个状态经过的路径长度上限
- LoopSeer
  - 使用合理的循环计数近似值来丢弃经历了多次循环的状态；这些状态会被放入`spinning`stash中，等到无可用状态后再拉出来
- ManualMergepoint
  - 人为设置一个合并点。所有到达此合并点地址的状态都会被暂时保存起来，并且在超时前到达同一点的任何其他状态都将被合并在一起。(?)
- MemoryWatcher
  - 如果内存过低时，监控在step与stop探索间有多少空闲内存(?)
- **Oppologist**
  - 这是一个用来维持执行的技术。当angr遇到不支持的指令(比如某些特殊的浮点指令)时，会将所有此指令相关的输入具体化，并将此指令交割unicorn引擎取模拟执行，是的执行能够继续。
- Spiller
  - 在active状态过多时，将部分状态导出到硬盘，防止内存消耗太大
- Threading
  - 线程相关的，暂时不看了。
- **Tracer**
  - 让angr沿着某条trace执行。angr提供了生成trace的库[tracer](https://github.com/angr/tracer)
- Veritesting
  - 一个基于[CMU paper](https://users.ece.cmu.edu/~dbrumley/pdf/Avgerinos%20et%20al._2014_Enhancing%20Symbolic%20Execution%20with%20Veritesting.pdf)自动化识别有用的合并点的实现。可以通过在创建simgr时传入参数`veritesting=True`启用；需要注意的是，因为它实现静态符号执行的方式比较具有侵入性，对其他模块有影响

更多关于simgr和探索技术的东西参考文档[simgr](http://angr.io/api-doc/angr.html#module-angr.manager)， [exploration techniques](http://angr.io/api-doc/angr.html#angr.exploration_techniques.ExplorationTechnique)。

## Execution Engines

前面介绍了angr的上层API，其中符号执行部分一个很重要的api就是step,`state.step()`和`simgr.step()`。本节文档介绍了关于在step，或者说angr引擎在每一step做了什么。

angr使用了一系列的引擎(SimEngine类的子类)去模拟对于某一个状态，执行给定片段的代码的结果。angr会按顺序尝试所有可用的引擎，选取第一个可以处理step的。下面是一个默认引擎的列表

- failure engine：当上一步将程序带入一些`uncontinuable`状态时调用
- syscall engine：上一步结束为系统调用时调用
- hook engine：当前地址被hook时调用
- unicorn engine：当`UNICORN` state option 开启，并且状态中无符号化数据时调用
- VEX engine：最终的回调

### SimSuccessors

实际尝试所有引擎的代码位于`project.factory.successors(state, **kwargs)`，此函数是`state.step()`和`simgr.step()`的核心部分，会返回一个`SimSuccessors`对象。SimSuccessors的目的是对后继状态进行简单分类，存储在各种列表属性中。

| Attribute                | guard conditions                   | 指令指针                                                     | 描述                                                         |
| ------------------------ | ---------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| successors               | 真(可以是符号化的，但是要约束为真) | 可以是符号化的，但解少于等于256，相对应的见`unconstrained_successors` | 最普通的可满足后继状态集；但是指令指针也可能是符号化的(比如switch这种基于用户输入计算得到的跳转)，所以其中的状态也表示了多个可能的后续执行状态。 |
| unsat_successors         | 假(可以是符号化的，但是要约束为假) | 可以是符号化的                                               | 求解器约束不满足的后继。guard conditions为假(即使符号化也要约束为假)。 |
| flat_successors          | 真(可以是符号化的，但是要约束为真) | 具体值                                                       | 状态flat，简答地将就是将解少于256的后继全部求解，flat得到对应数量的具体值的指令指针。比如`successors`的指令指针是`X+5`，而X需要满足条件`X > 0x800000`和`X <= 0x800010`，那么会出现`X=0x800001`直到`X=0x8000010`也就是指针为`0x800006`到`0x8000015`这些状态。 |
| unconstrained_successors | 真(可以是符号化的，但是要约束为真) | 符号化的(解数超过256)                                        | 如果解超过了256，angr会认为指令指针被未受约束数据覆盖了(比如用户数据产生的栈溢出)。 |
| all_successors           | 任何                               | 可以是符号化的                                               | successors+unsat_successors+unconstrained_successors         |

### Breakpoints

angr支持断点设置。一个使用示例

```python
>>> import angr

>>> proj = angr.Project("./check")

>>> state = proj.factory.entry_state()

#默认掉齐ipdb
>>> state.inspect.b('mem_write')
<BP before-action with conditions {}, no condition func, no action func>

>>> def debug_func(state):
...     print("State %s is about to do a memory write!")
...
#设置断点处的动作函数
>>> state.inspect.b('mem_write', when=angr.BP_AFTER, action=debug_func)
<BP after-action with conditions {}, no condition func, with action func>
```

完整的event列表以及包含的属性名见[docs](https://docs.angr.io/core-concepts/simulation#breakpoints)。

#### Caution about `mem_read` breakpoint

`mem_read`断点会在每次访问内存时触发，不管是程序执行程序时还是在二进制分析时(比如使用`state.mem`时)。如果需要在不触发断点，可以使用`state.memory.load`函数，并传入`disable_actions=True`和`inspect=False`参数。使用`state.find`时也可以传入同样的参数防止触发断点。

## Analyses

angr的分析模块。一般位于`project.analyses`下面。后续会说明如何写自己的分析模块。

### Built-in Analyses

内建的分析模块如下。

| 名称          | 描述                                                         |
| ------------- | ------------------------------------------------------------ |
| CFGFast       | 构建一个快速控制流图                                         |
| CFGEmulated   | 构建一个准确的控制流图                                       |
| VFG           | 对程序的每个函数进行VSA分析，构建`Value Flow Graph`，并检测栈变量 |
| DDG           | 计算数据依赖图，可以判断一给定数据的依赖                     |
| BackwardSlice | 针对一个特定的目标进行反向切片                               |
| Identifier    | 识别CGC程序中的通用库函数                                    |
| More!         | 其他的一些分析功能                                           |

