from time import sleep

class GF2(object):
    def __init__(self, value, bits):
        self.value = value
        self.bits = bits

    def __add__(self, other):
        return GF2(self.value ^ other.value, self.bits)

    def __mod__(self, other):
        #print self.bits,other.bits
        if self.bits > other.bits:
            ovalue = other.value << (self.bits-other.bits)
            d = 1 << self.bits-1
        else:
            return self.value

        actual = self.value
        for i in range(self.bits-other.bits+1):
            if (d & actual) > 0:
                #print bin(actual)
                #print bin(ovalue)
                actual = actual ^ ovalue
            ovalue = ovalue >> 1
            d = d >> 1

        return GF2(actual, self.bits-other.bits+1)

class Encoder(GF2):
    def __init__(self, codeword, generator):
        self.word = codeword
        self.gen = generator
        self.gen_bits = generator.bits
        
    def run(self):
        self.word.value = self.word.value << self.gen_bits-1
        self.word.bits = self.word.bits + self.gen_bits-1 
        rest = self.word % self.gen
        return self.word.value ^ rest.value

class Decoder(GF2):
    def __init__(self, receive, generator):
        self.recv = receive
        self.gen = generator
        self.zeros = 4

    def check_parity(self):
        print 'Syndrom: ' + bin((self.recv % self.gen).value)
        if self.recv % self.gen == 0:
            print 'Poprawne'
        else:
            print 'Wystapil blad'
            print 'Odebrane:' + bin(self.recv.value)
            d = 1 << self.recv.bits - 1
            #actual = GF2(0b0, 0)
            #actual.value = self.recv.value
            #actual.bits = self.recv.bits
            actual = self.recv
            i = 0 #licznik przsuniec
            c = GF2(0b0, 0)

            syndrom = actual % self.gen
            ones = bin(syndrom.value).count('1')
            #print bin(syndrom), ones
            
            t = 1
            while ones > t:
                if (d & actual.value) > 0:
                    actual.value = (actual.value ^ d) << 1
                    c.value = c.value << 1
                    c.value = c.value ^ 1
                else:
                    actual.value = actual.value << 1
                    c.value = c.value << 1
                    c.bits = c.bits + 1
                syndrom = (actual + c) % self.gen
                #print bin(actual.value), bin(self.gen.value)
                ones = bin(syndrom.value).count('1')
                #actual.value = actual.value ^ c.value
            
                #print syndrom, bin(syndrom)
                #print '\n'
                #print bin(actual.value+c.value)
                #print bin(syndrom), ones
                i = i+1

            actual = actual+c+syndrom

            for k in range(i):
                if (1 & actual.value) > 0:
                    actual.value = (actual.value >> 1) ^ (1 << actual.bits-1)
                else:
                    actual.value = (actual.value >> 1)

            print 'Wartosc naprawiona:' + bin(actual.value)
                    

    

if __name__ == '__main__':
    a = 0b1101
    b = 0b1011
    c=GF2(a, 7)
    d=GF2(b, 4)
    #print a + b
    #print c + d
    #print a%b
    #print bin(c%d)+'\n'

    encoder=Encoder(c, d)
    
    result = encoder.run()
    print 'Wyslano:' + bin(result)

    #0b1101001

    decoder = Decoder(GF2(0b1111001,7),d)#result^0b001000,7), d)

    decoder.check_parity()

    #print GF2(0b111110, 7) % GF2(b,4)
    
