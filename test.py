import FireCode_tablice as fc
from random import randint, sample

#1-12 kolejnyh bitow w czesci korekcyjnej
#1-12 kolejnyh bitow w czesci informacyjnej
#2-12 bitow rozrzuconych na szerokosci nie wiekszej niz 40 bitow
#2-12 bitow rozrzuconych na szerokosci wiekszej niz 40 bitow
#13 kolejnych blednych bitow
#13 rozrzuconyh bitow

class Test(object):

    def __init__(self, information, rest, generator):
        self.inf = information
        self.rest = rest
        self.gen = generator

    def correction_error(self, error):
        '''zwraca uszkodzony w czesci korekcyjnej objekt klasy Decoder()'''
        return fc.Decoder((fc.GF2(self.inf.value), fc.GF2(self.rest.value)+error), self.gen)

    def information_error(self, error):
        '''zwraca uszkodzony w czesci informacyjnej objekt klasy Decoder()'''
        return fc.Decoder((fc.GF2(self.inf.value)+error, fc.GF2(self.rest.value)), self.gen)

    def check(self, repaired, msg):
        try:
            if ((fc.GF2((self.inf+self.rest).value) + repaired).value).count(1) > 0:
                print 'bledne dekodowanie: ' + msg
            else:
                print 'wszystko ok: ' + msg
        except:
            print 'nie mozna poprawic bledow: ' + msg
            

    def test1_15kor(self):
        print '''\nTest dla od 1 do 15 bledow w czesci korekcyjnej.\n
            Bledy na kolejnych pozycjach.
            '''
        for i in range(1, 16):
            num = randint(0, 40-i)
            zeros = [0 for x in range(40)]
            for n, j in enumerate(range(i)):
                zeros[num+n] = 1
            error = ''.join(str(x) for x in zeros)

            decoder = self.correction_error(fc.GF2(error))
            repaired = decoder.check()
            self.check(repaired, 'blednych bitow %d'%(i))

    def test1_15inf(self):
        print '''\nTest dla od 1 do 15 bledow w czesci informacyjnej.\n
            Bledy na kolejnych pozycjach.
            '''
        for i in range(1, 16):
            result = fc.GF2(self.inf.value)
            rest = fc.GF2(self.rest.value)

            num = randint(0, 184-i)
            zeros = [0 for x in range(224)]
            for n, j in enumerate(range(i)):
                zeros[num+n] = 1
            error = ''.join(str(x) for x in zeros)
            
            decoder = self.information_error(fc.GF2(error))#fc.Decoder((result+fc.GF2(error), rest), self.gen)
            repaired = decoder.check()

            self.check(repaired, 'blednych bitow %d'%(i))
    
    def test2_15more40(self):
        
        print '''\nTest dla od 2 do 15 bledow.\n
            Bledy rozrzucone na wiecej niz 40 pozycjach.
            '''
        for i in range(2, 16):
            diff = 0
            while diff < 40:
                num = sample(range(0, 184), i)
                diff = max(num)-min(num)

            zeros = [0 for x in range(224)]
            for j in num:
                zeros[j] = 1
            error = ''.join(str(x) for x in zeros)

            decoder = self.information_error(fc.GF2(error))
            repaired = decoder.check()
            self.check(repaired, 'blednych bitow %d'%(i))

    def test2_15less40(self):
        
        print '''\nTest dla od 2 do 15 bledow.\n
            Bledy rozrzucone na mniej niz 40 pozycjach.
            '''
        for i in range(2, 16):
            num = sample(range(0, 40), i)
            diff = max(num)-min(num)+1
            #print diff, num
            num2 = randint(0,184-diff)

            zeros = [0 for x in range(224)]
            for j in num:
                zeros[j+num2] = 1
            error = ''.join(str(x) for x in zeros)
            #print error
            decoder = self.information_error(fc.GF2(error))
            repaired = decoder.check()
            self.check(repaired, 'blednych bitow %d'%(i))
            
    def __call__(self):
        self.test1_15kor()
        self.test1_15inf()
        self.test2_15more40()
        self.test2_15less40()

if __name__ == '__main__':

    inf = fc.GF2(''.join([str(randint(0,1)) for x in range(184)]))  #informacja
    gen = fc.GF2('10000000000000100100000100000000000001001')  #generator

    encoder = fc.Encoder(inf, gen)

    (result, rest) = encoder.run()

    test = Test(result, rest, gen)
    test()
    
