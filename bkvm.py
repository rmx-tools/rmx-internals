#!/usr/bin/python

import commands, time

def prepareTarget():
   print "prepare backup Target"
   print "---------------------"
   cmd = "mount -t cifs //xxxxxx/public/BK\ VM\ XEN -o username=xxx,password=yyy /bak/"
   output = commands.getoutput(cmd)
   cmd = "ls -lht --time-style=\"long-iso\"  /bak/"
   output = commands.getoutput(cmd)
   print output
   print "..."

def releaseTarget():
   print "release backup Target"
   print "---------------------"
   cmd = "ls -lht --time-style=\"long-iso\"  /bak/"
   output = commands.getoutput(cmd)
   print output
   cmd = "umount /bak/"
   output = commands.getoutput(cmd)
   print "..."

def get_backup_vms():
   result = []
   cmd = "xe vm-list is-control-domain=false is-a-snapshot=false power-state=running"
   output = commands.getoutput(cmd)

   for vm in output.split("\n\n\n"):
      lines = vm.splitlines()
      uuid = lines[0].split(":")[1][1:]
      name = lines[1].split(":")[1][1:]
      result += [(uuid, name)]
   return result

def backup_vm(uuid, filename, timestamp):
  cmd = "xe vm-snapshot uuid=" + uuid + " new-name-label=" + timestamp
  snapshot_uuid = commands.getoutput(cmd)

  cmd = "xe template-param-set is-a-template=false ha-always-run=false uuid="
  cmd = cmd + snapshot_uuid
  commands.getoutput(cmd)

  cmd = "rm " + filename+".tmp"
  commands.getoutput(cmd)

  cmd = "xe vm-export vm=" + snapshot_uuid + " filename=" + filename+".tmp"
  (status,output)=commands.getstatusoutput(cmd)
  if (status==0):
    cmd = "rm " + filename + " ; mv " + filename+".tmp"+ " " + filename 
    commands.getoutput(cmd)
  else:
    print "Error"
    print output

  cmd = "xe vm-uninstall uuid=" + snapshot_uuid + " force=true"
  commands.getoutput(cmd)


prepareTarget()

print "Backup Running VMs"
print "------------------"
for (uuid, name) in get_backup_vms():
   timestamp = time.strftime("%Y%m%d-%H%M", time.gmtime())
#  filename = "\"/bak/" + timestamp + " " + name + ".xva\""
   filename = "\"/bak/" + name + ".xva\""
   print timestamp, uuid, name," to ", filename
   backup_vm(uuid, filename, timestamp)
print "..."

releaseTarget()
