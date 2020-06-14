import imghdr
import struct

import ac

from constants import FC

def get_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                ac.log("%s: Error getting image size %s" % (FC.APP_NAME, fname))
                return
            width, height = struct.unpack('>ii', head[16:24])
        return width, height

def time_to_string(t, include_ms=True):
	try:
		hours, x = divmod(int(t), 3600000)
		mins, x = divmod(x, 60000)
		secs, ms = divmod(x, 1000)
		if not include_ms:
			return '%d:%02d' % (mins, secs)
		return '%d.%03d' % (secs, ms) if mins == 0 else '%d:%02d.%03d' % (mins, secs, ms)
	except Exception:
		return '--:--.---'
