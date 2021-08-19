import libvirt
import os
import shutil
import sys
import time
from xml.etree import ElementTree as ET

def create_vm(machine_details):
    conn = libvirt.open(None)
    conn.defineXML(machine_details)

def remove_disk(Disk):
    os.remove(Disk.path + Disk.name)

def start_vm(machine_details):
    '''Запускает виртуальную машину'''

    hypervisor = machine_details.hypervisor
    conn = libvirt.open('qemu:///system')
    machine = conn.lookupByName(machine_details.name)
    machine.create()

def stop_vm(machine, action):
    '''Останавливает виртуальную машину'''

    name= machine.name
    hypervisor = machine.hypervisor
    conn = libvirt.open('qemu:///system')

    machine = conn.lookupByName(name)
    if (action == "forceoff"):
        machine.destroy()
        try:
            VM.objects.filter(name=name).update(state='OFF')
        except:
            pass
    elif (action == "shutdown"):
        machine.shutdown()
        VM.objects.filter(name=name).update(state='OFF')
    elif (action == "reset"):
        machine.destroy()
        machine.create()
    conn.close()

def del_vm(vm):
    '''Удаляет виртуальную машину'''

    try:
        hypervisor = VirtualMachine.hypervisor
        conn = libvirt.open("qemu:///system")
        machine = conn.lookupByName(vm.name)
        machine.undefine()
        conn.close()
    except:
        pass

def save_state(vm,filename):
    conn = libvirt.open("qemu:///system")

    dom = conn.lookupByName(vm)
    if dom == None:
        conn.close()
        return 'Не могу найти пространство имён'

    info = dom.info()
    if info == None:
        conn.close()
        return 'Не могу получить статуст пространства имён'

    if info.state == VIR_DOMAIN_SHUTOFF:
        conn.close()
        return 'Не могу сохранить, так как выключено'

    if dom.save(filename) < 0:
        conn.close()
        return 'Не могу сохранить так как произошла ошибка'
    
    conn.close()
    return 'Всё гут'

def restore_state(filename):
    conn = libvirt.open("qemu:///system")

    id = conn.restore(filename)
    if id < 0:
        conn.close() 
        return 'Ошибка восстановления сессии'
    
    dom = conn.lookupByID(id)
    if dom == None:
        conn.close()
        return 'Ошибка восстановления сессии'
    
    conn.close()
    return 'Сессия восстановлена успешно'

def create_qemu_xml(vm_info):
    storage_device = vm_info['storage_disk']

    try:
        optical_path = OpticalDisk.objects.get(name=vm_info['optical_disk']).ISOFile.path
        optical_attached = True
    except:
        optical_attached = False

    try:
        drive_path = StorageDisk.objects.get(name=storage_device).path
        drive_name = StorageDisk.objects.get(name=storage_device).name
        drive_attached = True
    except:
        drive_attached = False

    HardDisk = ""
    OpticalDiskDevice = ""
    #Generate XML template for VM
    xmlp1 = """<domain type='kvm'>
        <name>{}</name>
        <memory unit='MiB'>{}</memory>
        <vcpu placement='static'>{}</vcpu>
        <os>
            <type>hvm</type>
        </os>
        <clock offset='utc'/>
        <features>
            <acpi/>
            <apic/>
            <pae/>
        </features>
        <on_poweroff>destroy</on_poweroff>
        <on_reboot>restart</on_reboot>
        <on_crash>destroy</on_crash>
        """.format(vm_info['name'], int(vm_info['ram']), vm_info['cpus'])

    if (drive_attached == True):
        HardDisk ="""
        <disk type='file' device='disk'>
            <source file='{}{}'/>
            <driver name='qemu' type='qcow2'/>
            <target dev='vda' bus='virtio'/>
        </disk>
        """.format(drive_path,drive_name)

    if (optical_attached == True):
        OpticalDiskDevice ="""
        <disk type="file" device="cdrom">
        <driver name="qemu" type="raw"/>
        <source file="{}"/>
        <target dev="sda" bus="sata"/>
        <readonly/>
        <boot order="1"/>
        <address type="drive" controller="0" bus="0" target="0" unit="0"/>
        </disk>
        """.format(optical_path)

    Network = """
    <interface type="network">
    <source network="default" />
    <model type='virtio'/>
    </interface>
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
    <listen type='address' address='0.0.0.0'/>
    </graphics>
    <video>
      <model type="qxl" ram="65536" vram="65536" vgamem="16384" heads="1" primary="yes"/>
      <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x0"/>
    </video>
    </devices>
    """
    devices = "<devices>" + HardDisk + OpticalDiskDevice + Network

    xml = xmlp1 + devices + "</domain>"
    conn = libvirt.open("qemu:///system")

    try:
        machine = conn.lookupByName(vm_info['name'])
        machine.undefine()
    except:
        pass
    conn.defineXML(xml)
    conn.close()
