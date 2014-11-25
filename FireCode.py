from time import sleep

class GF2(object):
    def __init__(self, value, bits):
        self.value = value
        self.bits = bits

    def __add__(self, other):
        return self.value ^ other.value

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

        return actual

class Encoder(GF2):
    def __init__(self, codeword, generator):
        self.word = codeword
        self.gen = generator
        self.gen_bits = generator.bits
        
    def run(self):
        self.word.value = self.word.value << self.gen_bits-1
        rest = self.word % self.gen
        return self.word.value ^ rest

class Decoder(GF2):
    def __init__(self, receive, generator):
        self.recv = receive
        self.gen = generator

    def check_parity(self):
        print 'Syndrom: ' + str(self.recv % self.gen)
        if self.recv % self.gen == 0:
            print 'Poprawne'
        else:
            print 'Wystapil blad'

if __name__ == '__main__':
    a = 0b1000
    b = 0b1011
    c=GF2(a, 7)
    d=GF2(b, 4)
    #print a + b
    #print c + d
    #print a%b
    #print bin(c%d)+'\n'

    encoder=Encoder(c, d)
    
    result = encoder.run()
    print bin(result)

    decoder = Decoder(GF2(result,7), d)

    decoder.check_parity()
    
