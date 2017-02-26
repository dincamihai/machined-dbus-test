from pydbus import SystemBus
from hashlib import sha256


bus = SystemBus()
machined = bus.get(".machine1")


def images():
    return [it[0] for it in machined.ListImages() if it[0] != '.host']


def image(name):
    return bus.get('.machine1', machined.GetImage(name))


def machines():
    return [it[0] for it in machined.ListMachines() if it[0] != '.host']


def machine(name):
    return bus.get('.machine1', machined.GetMachine(name))


def clone(machine, cloneid):
    machined.CloneImage(machine, cloneid, False)
    return image(cloneid)


def shell(*args):
    return machined.OpenMachineShell(*args)


def create(image):
    machined.CreateMachine(
        image.Name,  # name
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # id
        'systemd-nspawn',  # service
        'container',  # class
        0,  # leader eg: 16722L
        image.Path,  # root_directory
        [])  # scope_properties
    return machine(image.Name)


if __name__ == "__main__":
    available = images()
    name = "test{0}".format(sha256().hexdigest()[:8])
    test = clone(available[0], name)
    try:
        create(test)
        pty, pty_path = shell(name, 'mihai', '/usr/bin/ls', ['-al'], {})
    finally:
        test.Remove()
