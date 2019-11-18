import socket
import optparse

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='')
parser.add_option('-p', dest='port', type='int', default=12345)
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((options.ip, options.port))

f = open('foo.txt', 'w')
while True:
    data, addr = s.recvfrom(512)
    f.write("%s: %s\n" % (addr, data))
    f.flush()