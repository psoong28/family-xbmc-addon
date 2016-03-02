import dbus
import xbmc




os.system('/usr/bin/connmanctl enable wifi')

try:
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
except:
    pass

dbusSystemBus = dbus.SystemBus()


wifi = dbusSystemBus.get_object('net.connman','/net/connman/technology/wifi')
dbus.Interface(wifi, 'net.connman.Technology').Scan()

wifi = None
del wifi

xbmc.executebuiltin("XBMC.RunScript(service.openelec.settings)")


