
configurations = {
    
    'qemu' : {
        "command" : "qemu-system-mips -kernel {kernel} -nographic -machine mips -cpu 4kc",
        "srec" : False
    },
    
    'luajit' : {
        "name" : 'luamips - jit',
        "command" : "luajit ../../luamips/emu.lua {kernel}",
        "srec" : True
    },
    
    'lua' : {
        "name" : 'luamips - slow',
        "command" : "lua ../../luamips/emu.lua {kernel}",
        "srec" : True
    },
    
    'cmips' : {
        "name" : 'cmips - native',
        "command" : "../../cmips/emu {kernel}",
        "srec" : True
    }
    
}


for k in configurations.keys():
    if configurations[k].get('name',None) == None:
        configurations[k]['name'] = k
