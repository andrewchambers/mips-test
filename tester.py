from config import configurations
import sys
import os
import os.path
import subprocess
import difflib



class ProgRunner(object):
    
    def __init__(self,workingDir,args,wanterr=True):
        self.output = ""
        self.args = args
        self.workingDir = os.path.abspath(workingDir)
        self.wanterr = wanterr
        
    def run(self):
        startDir = os.getcwd()
        os.chdir(self.workingDir)
        
        
        stderr = open("/dev/null",'w')
        try:
            if self.wanterr:
                self.output = subprocess.check_output(self.args,stderr=subprocess.STDOUT)
            else:
                self.output = subprocess.check_output(self.args,stderr=stderr.fileno())
        finally:
            stderr.close()
            os.chdir(startDir)
            
    
    def getOutput(self):
        return self.output


class TestSelector(ProgRunner):
    def __init__(self,tname):
        ProgRunner.__init__(self,"./testkernel",["bash","select.sh",tname])

class TestBuilder(ProgRunner):
    def __init__(self):
        ProgRunner.__init__(self,"./testkernel",["bash","build.sh"])

class TestRunner(ProgRunner):
    def __init__(self,command,wanterr=False):
        ProgRunner.__init__(self,"./testkernel",["bash","run.sh"] + command,wanterr=wanterr)
    
def runTest(conf,testname,wanterr=False):
    sel = TestSelector(testname)
    build = TestBuilder()
    
    if conf.get('srec',False):
        kern = "kern.srec"
    else:
        kern = "kern"    
    runcmd = conf['command'].format(kernel=kern)
    run = TestRunner([runcmd],wanterr=wanterr)
    
    try:
        sel.run()
        build.run()
    except subprocess.CalledProcessError as builderr:
        print builderr.output
        raise builderr
    
    try:
        run.run()
        emuout = run.getOutput()
        return emuout,0
    except subprocess.CalledProcessError as emuErr:
        
        o = run.getOutput() + '\n' + emuErr.output
        return emuErr.output,emuErr.returncode

def collect_tests():
    return os.listdir('./testkernel/tests')

def compare_configs(config1,config2,test):
    o1,ret1 = runTest(config1,test)
    o2,ret2 = runTest(config2,test)
    
    o1 += "\nreturn code %s\n" % ret1
    o2 += "\nreturn code %s\n" % ret2
    
    o1 = o1.split('\n')
    o2 = o2.split('\n')
    
    
    if o1 == o2:
        return None
        
    return difflib.unified_diff(o1,o2,fromfile=config1['name'],tofile=config2['name'])


def help():
    pass

def main():
    #perform test scripts in the tester path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if sys.argv[1] == "cmp":
        
        conf1 = sys.argv[2]
        conf2 = sys.argv[3]
        
        if len(sys.argv) > 4:
            tests = [sys.argv[4]]
        else:
            tests = collect_tests()
        
        for t in tests:
            try:
                diff = compare_configs(configurations[conf1],configurations[conf2],t)
                if diff != None:
                    for line in diff:
                        print line
                    print "\nOutputs for %s differ!" % t
                    return
                else:
                    sys.stdout.write('.')
                    sys.stdout.flush() 
            except subprocess.CalledProcessError as e:
                print e.output
                print "Test %s failed setup!" % t
        print "\ndone!"
            
    elif sys.argv[1] == "run":
        conf = configurations[sys.argv[2]]
        o,ret = runTest(conf,sys.argv[3],wanterr=True)
        print o
        print "%s return code %s" % (conf['name'],ret)
    else:
        print("unknown command %s" % sys.argv[1]) 
        help() 
        
if __name__ == '__main__':
    main()
