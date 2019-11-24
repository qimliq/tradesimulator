import os.path
from stocks import allstocks, euronext, stockgroup100

import struct
from stocks import allstocks

class MetaConverter():
    MASTER_READ_COUNT = 53
    XMASTER_READ_COUNT = 150
    FDATA_READ_COUNT = 24

    MASTER_FX          = 0
    MASTER_SYMBOL      = 36
    MASTER_NAME        = 7
    MASTER_FIRST_DATE  = 25
    MASTER_LAST_DATE   = 29


    XMASTER_MARK            = 0
    XMASTER_SYMBOL          = 1
    XMASTER_NAME            = 16
    XMASTER_D               = 62
    XMASTER_FN              = 65
    XMASTER_END_DATE_1      = 80
    XMASTER_START_DATE_1    = 104
    XMASTER_START_DATE_2    = 108
    XMASTER_END_DATE_2      = 116

    DataPath = "testdata/"

    def __init__(self):
        print("init")

    def fmsbintoieee(self, buffer):
        v3 = 0
        v2 = 0
        v1 = 0
        v0 = 0

        if buffer[3] == 0:
            return 0

        # print(buffer)

        sign = buffer[2] & 0x80
        v3 |= sign
        exp = buffer[3] - 2

        v3 |= ((exp >> 1) & 0xff)
        v2 |= ((exp << 7) & 0xff)
        v2 |= (buffer[2] & 0x7f)
        #v2 &= 0x7f
        v1 = buffer[1]
        v0 = buffer[0]

        # print("%x" % v3)
        # print("%x" % v2)
        # print("%x" % v1)
        # print("%x" % v0)

        h = hex((v3 << 24) + (v2 << 16) + (v1 << 8) + (v0))
        # print(h)
        v = float(struct.unpack('<f', struct.pack('<I', int(h,0)))[0])

        # print(v)

        return v

    def parse_data(self, name, number, extension):

        fname = self.DataPath + "/F%d.%s" % (number, extension)

        if os.path.isfile(fname) == False:
            return



        if not allstocks.__contains__(name):
            if not euronext.__contains__(name):
                if not stockgroup100.__contains__(name):
                    return

        print("name :" + name)

        fo = open(fname, "rb")
        out = open("csv/" + name + ".csv", "w")
        out.write("Index,Date,Open,High,Low,Close,Volume\n")
        blk = fo.read(self.FDATA_READ_COUNT)
        while True:
            blk = fo.read(self.FDATA_READ_COUNT)

            if blk == b'':
                break

            if len(blk) != self.FDATA_READ_COUNT:
                continue
            date      = self.fmsbintoieee(blk[0:4])
            openval   = self.fmsbintoieee(blk[4:8])
            highval   = self.fmsbintoieee(blk[8:12])
            lowval    = self.fmsbintoieee(blk[12:16])
            closeval  = self.fmsbintoieee(blk[16:20])
            amountval = self.fmsbintoieee(blk[20:24])

            if int(date)/10000 < 100:
                continue;

            year  = int(date)/10000 + 1900
            month = (int(date)%10000)/100
            day   = (int(date)%10000)%100
            out.write("%d,%d-%02d-%02d,%.2f,%.2f,%.2f,%.2f,%d\n" % (int(date), year, month, day, openval, highval , lowval , closeval , int(amountval)))

            #print(date)
            #print(openval)
            # return

        fo.close()
        out.close()

    def parse_master( self, fileName ):
        print("parse_master called")
        fo = open(fileName, "rb")

        blk = fo.read(self.MASTER_READ_COUNT)
        while True:
            blk = fo.read(self.MASTER_READ_COUNT)
            if (blk) == b'':
                break

            if len(blk) == self.MASTER_READ_COUNT:
                num = blk[self.MASTER_FX]

                ind = blk.index(b'\0', self.MASTER_SYMBOL)
                #a = "%s" % blk[self.MASTER_SYMBOL:self.MASTER_SYMBOL + 5].decode('ascii')
                a = "%s" % blk[self.MASTER_SYMBOL:ind].decode('ascii')

                b = "%s" % blk[self.MASTER_NAME:self.MASTER_NAME + 16]
                c = a.replace(' ', '')
                c = c.replace('\0','')
                #print(c)

                self.parse_data(c, num, "DAT")

            #print(blk)
            #break


        fo.close()
        print("end")

    def parse_xmaster(self, fileName):
        print("parse_xmaster called")
        fo = open(fileName, "rb")

        blk = fo.read(self.XMASTER_READ_COUNT)
        while True:
            blk = fo.read(self.XMASTER_READ_COUNT)
            if (blk) == b'':
                break

            if len(blk) == self.XMASTER_READ_COUNT:
                num = (blk[self.XMASTER_FN + 1] << 8) + blk[self.XMASTER_FN]

                ind = blk.index(b'\0', self.XMASTER_SYMBOL)
                #a = "%s" % blk[self.XMASTER_SYMBOL:self.XMASTER_SYMBOL + 5].decode('ascii')
                a = "%s" % blk[self.XMASTER_SYMBOL:ind].decode('ascii')

                #b = "%s" % blk[self.MASTER_NAME:self.MASTER_NAME + 16]
                c = a.replace(' ', '')
                c = c.replace('\0','')
                # print(c)

                self.parse_data(c, num, "MWD")

                # print(blk)
                # break

        fo.close()
        print("end")


c = MetaConverter()

c.parse_master(c.DataPath + "/MASTER")
c.parse_xmaster(c.DataPath + "/XMASTER")