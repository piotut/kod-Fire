# -*- coding: cp1250 -*-
from time import sleep
from random import randint

class GF2(object):
    '''
    Klasa implementujaca działania w GF(2)
    '''
    def __init__(self, value):
        '''
        value: string bitow (big endian)
        '''
        self.value = [int(x) for x in list(value)]

    def deleteZeros(self, value):
        '''
        Usuwa nieznaczace zera.
        '''
        value = list(value)
        
        try:
            del value[:value.index(1)]
        except ValueError:
            value = [0]

        return value

    def __add__(self, other):
        '''
        Dodawanie list bitowych.
        '''
        
        a = list(self.value)
        b = list(other.value)

        if len(a) > len(b):
            for x in range(len(a)-len(b)):
                b.insert(0,0)
        else:
            for x in range(len(b)-len(a)):
                a.insert(0,0)

        result = [x ^ y for x, y in zip(a,b)]

        return GF2(result)

    def __mod__(self, other):
        '''
        Operacja modulo na listach bitowych.
        '''
        a = list(self.deleteZeros(self.value))
        b = list(self.deleteZeros(other.value))
        
        if len(a) < len(b):
            return GF2(a)

        current = list(a)

        for i in range(len(a)-len(b)+1):
            if (current[0]) > 0:
                for j in range(len(b)):
                    current[j] = current[j] ^ b[j]
            del current[0]

        return GF2(self.deleteZeros(current))

    def __mul__(self, other):
        '''
        Mnozenie dwoch tablic bitowych.
        '''
    
        a = list(self.deleteZeros(self.value))
        b = list(self.deleteZeros(other.value))
        
        result = [0 for x in range(len(a)+len(b)-1)]
        for x in range(len(a)):
            for y in range(len(b)):
                result[x+y] = int(result[x+y]) ^ (a[x] and b[y])

        return GF2(self.deleteZeros(result))


class Encoder(GF2):
    '''
    Koduje czesc informacyjna przy pomocy generatora
    '''
    def __init__(self, codeword, generator):
        '''
        Parametry jako obiekty klasy GF2.
        codeword: slowo do zakodowania
        generator: generator kodujacy
        '''
        self.word = codeword
        self.gen = generator
        
    def run(self):
        '''
        Metoda kodujaca.

        Zwraca (slowo zakodowane przesuniete o bity generatora, reszta).
        '''
        p = GF2('1000101110110100100000010001011100101001')
        self.word.value.extend([0 for x in range(len(self.gen.value)-1)]) 

        rest = ((self.word % self.gen) * p) % self.gen

        return (self.word, rest)

class Decoder(GF2):
    ''' parametry GF2 '''

    def __init__(self, receive, generator):
        '''
        receive = (informacja, reszta)
        '''
        self.recv = receive[0]
        self.rest = receive[1]
        self.gen = generator

    def check(self):
        i = 0
        c = GF2('')
        p = GF2('1000101110110100100000010001011100101001')
        actual = GF2(self.recv.value)
        for x in range(224-len(actual.value)):
            actual.value.insert(0,0)
    
        syndrom = ((actual % self.gen) *p + self.rest % self.gen ) % self.gen
       
        if syndrom.value == [0]:
            print 'Poprawne'
        else:
            print 'Wystapil blad'
            print 'Odebrane:\n' + str((self.recv + self.rest).value)
            ones = str(syndrom.value).count('1')
            (min_syn, iteracja, s) = (ones, 0, list(syndrom.value))

            t = 12  #zdolnosc korekcyjna
            while i<184:
                if (actual.value[0] == 1):
                    self.rest.value.extend([1])
                else:
                    self.rest.value.extend([0])

                del actual.value[0]
                actual.value.extend([0])

                syndrom = ((actual % self.gen) *p + self.rest % self.gen ) % self.gen % self.gen   
                ones = syndrom.value.count(1)
                    
                sleep(0)
                i = i+1
                if(min_syn > ones):
                    (min_syn, iteracja, s) = (ones, i, list(syndrom.value))

            correct = actual + self.rest
            print min_syn
            print iteracja
            if min_syn > 12:
                print 'Nie mozna poprawic bledow'
                return
            else:
                for k in range(i):
                    if (correct.value[-1]) == 0:
                        correct.value.insert(0, 0)
                    else:
                        correct.value.insert(0, 1)
                    del correct.value[-1]

                    if i-1-k == iteracja:
                        print 'dodajemy'
                        correct = correct + GF2(s)

            return correct
    

if __name__ == '__main__':

    a = GF2(''.join([str(randint(0,1)) for x in range(184)]))  #informacja
    b = GF2('10000000000000100100000100000000000001001')  #generator

    encoder=Encoder(a, b)
    
    (result, rest) = encoder.run()

    poprawny = GF2((result+rest).value)
    print 'Wartosc zakodowana (wyslana):'
    print poprawny.value
    
    rest = rest + GF2('10')
    result.value[2] = result.value[2] ^ 1
    result.value[37] = result.value[37] ^ 1
    #zeros = ''.join(['0' for x in range(40)])
    #result = result + GF2('111100000'+zeros)
    decoder = Decoder((result, rest), b)
    
    naprawione = decoder.check()
    try:
        print naprawione.value
        
        print 'Wartosc poprawna XOR wartosc po naprawieniu'
        print (poprawny + naprawione).value
        print 'liczba rozniacych sie bitow: ' + str(((poprawny + naprawione).value).count(1))
    except:
        pass

    
