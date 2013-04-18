#!/usr/bin/python

import CloudStack
import time

api='https://api.ucloudbiz.olleh.com/server/v1/client/api'
apiKeyList = []
'''
apiKeyList.append({'apikey': '12341234', 'secretkey': '12341234', 'account':'email@email.com'})
apiKeyList.append({'apikey': '12341235', 'secretkey': '12341235', 'account':'email2@email.com'})
'''

for apiKey in apiKeyList:

   cloudstack = CloudStack.Client(api, apiKey['apikey'], apiKey['secretkey'])

   '''
   1. VM Stopping 
   '''
   vms = cloudstack.listVirtualMachines()

   print "========================================================================================================================="
   print "Account\tVmID\tName\tdomian\tdomainid\tStatus\tTemplate Name"
   print "========================================================================================================================="

   for vm in vms: 
      if(vm['templatename'] == 'ImageAnalysor'):
         if(vm['state'] != 'Stopped'):
            print "Virtual Machine : %s\t%s\t%s\t%s\t%s\t%s\t%s" % (apiKey['account'], vm['id'], vm['name'], vm['domain'], vm['domainid'], vm['state'], vm['templatename'])
            
            stopVm = cloudstack.stopVirtualMachine({'id': vm['id'], 'forced': 'true'})

            myjob = stopVm['jobid']
            while True:
               qr=cloudstack.queryAsyncJobResult({
                  'jobid':str(myjob)
               })
               if qr['jobstatus'] == 1:
                  print qr
                  break
               elif qr['jobstatus'] == 2:
                  print "Job fail"
                  break
               else:
                  print qr['jobstatus']
                  print "Sleep"
                  time.sleep(5)
            
   print

   '''
   2. Volume Detach & Delete
   '''
   vols = cloudstack.listVolumes()

   print "========================================================================================================================="
   print "Account\tVolume ID\tName\tDevice ID\tVm Name\tVm Display Name\tVm Status\tVolume Status"
   print "========================================================================================================================="

   for vol in vols:
      if(vol['name'].endswith('AnalysisVolume')):
         if(vol.has_key('virtualmachineid')):
            print "Volume : %s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (apiKey['account'], vol['id'], vol['name'], vol['virtualmachineid'], vol['vmname'], vol['vmdisplayname'], vol['vmstate'], vol['state'])
            detachVol = cloudstack.detachVolume({'id': vol['id']})
            myjob = detachVol['jobid']
            while True:
               qr=cloudstack.queryAsyncJobResult({
                  'jobid':str(myjob)
               })
               if qr['jobstatus'] == 1:
                  print qr
                  break
               elif qr['jobstatus'] == 2:
                  print "Job fail"
                  break
               else:
                  print qr['jobstatus']
                  print "Sleep"
                  time.sleep(5)

         deleteVol = cloudstack.deleteVolume({'id': vol['id']})
         print(deleteVol)
   print
   
   '''
   1. VM Destroy  
   '''
   vms = cloudstack.listVirtualMachines()

   print "========================================================================================================================="
   print "Account\tVmID\tName\tdomian\tdomainid\tStatus\tTemplate Name"
   print "========================================================================================================================="

   for vm in vms: 
      if(vm['templatename'] == 'ImageAnalysor'):
         if(vm['state'] == 'Stopped'):
            print "Virtual Machine : %s\t%s\t%s\t%s\t%s\t%s\t%s" % (apiKey['account'], vm['id'], vm['name'], vm['domain'], vm['domainid'], vm['state'], vm['templatename'])
            
            destroyVm = cloudstack.destroyVirtualMachine({'id': vm['id']})

            myjob = destroyVm['jobid']
            while True:
               qr=cloudstack.queryAsyncJobResult({
                  'jobid':str(myjob)
               })
               if qr['jobstatus'] == 1:
                  print qr
                  break
               elif qr['jobstatus'] == 2:
                  print "Job fail"
                  break
               else:
                  print qr['jobstatus']
                  print "Sleep"
                  time.sleep(5)

   print


print "Fin"

