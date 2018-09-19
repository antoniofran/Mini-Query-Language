import shlex

class MiniBaza:
    def __init__(self,nazivBaze):
        self.nazivBaze = nazivBaze
        self.kolekcije = {} #inicijalizacija mape

    def dodaj_kolekciju(self, nazivKolekcije):
        self.kolekcije[nazivKolekcije] = []

    def dodaj_dokument(self, nazivKolekcije, dokument):
        try:
            self.kolekcije[nazivKolekcije].append(dokument)
        except KeyError:
            print("Nepostojeca kolekcija")

    def ispisi_kolekciju(self, nazivKolekcije):
        try:
            trazenaKolekcija = self.kolekcije[nazivKolekcije]
            
            for dokument in trazenaKolekcija: print(dokument)
        except KeyError:
            print("Nepostojeca kolekcija")

    def dohvati_kolekcije(self):
        return self.kolekcije

    def nadji_dokumente(self, nazivKolekcije, poslaniDokument, uvjetFunkcija = lambda a,b: a == b):
        rezultat = []

        try:
            trazenaKolekcija = self.kolekcije[nazivKolekcije]
            trazeniKljucevi = [kljuc for kljuc in poslaniDokument.keys()]
            
            for trenutniDokument in trazenaKolekcija:
                brPotrebPodudaranja = len(trazeniKljucevi)
                
                for kljuc in trazeniKljucevi:
                    if ( uvjetFunkcija(trenutniDokument[kljuc],poslaniDokument[kljuc]) ):
                        brPotrebPodudaranja = brPotrebPodudaranja - 1

                if ( brPotrebPodudaranja == 0 ):
                    rezultat.append(trenutniDokument)
        except KeyError:
            print("Nepostojeca kolekcija")

        return rezultat

    def ukloni_dokumente(self ,nazivKolekcije, poslaniDokument, uvjetFunkcija = lambda a,b: a == b):
        try:
            trazenaKolekcija = self.kolekcije[nazivKolekcije]
            trazeniKljucevi = [kljuc for kljuc in poslaniDokument.keys()]
            
            for trenutniDokument in trazenaKolekcija:
                brPotrebPodudaranja = len(trazeniKljucevi)
                
                for kljuc in trazeniKljucevi:
                    if ( uvjetFunkcija(trenutniDokument[kljuc],poslaniDokument[kljuc]) ):
                        brPotrebPodudaranja = brPotrebPodudaranja - 1

                if ( brPotrebPodudaranja == 0 ):
                    trazenaKolekcija.remove(trenutniDokument)
        except KeyError:
            print("Nepostojeca kolekcija")

class MiniQueryLanguage:
    def __init__(self):
        self.varijable = {}
        
    def parsirajStringIzraz(self,izraz):
        izraz = shlex.split( izraz.replace('(',' ( ').replace(')',' ) ').replace('{',' ( :new ').replace('}',' ) ').replace('[',' ( ~new ').replace(']',' ) '), False, False )

        indexBeginDeepestBracket = -1
        indexEndDeepestBracket = -1

        if ( izraz.count("(") == izraz.count(")") ):
            while( izraz.count("(") > 0 ):
                indexBeginDeepestBracket = len(izraz) - izraz[::-1].index("(") - 1

                indexEndDeepestBracket = indexBeginDeepestBracket + izraz[indexBeginDeepestBracket:].index(")")

                izraz[indexBeginDeepestBracket] = izraz[indexBeginDeepestBracket + 1 : indexEndDeepestBracket] #[index:(index -1)]

                izraz[indexBeginDeepestBracket + 1 : indexEndDeepestBracket +1] = []
        else:
            #print("Nebalansirane zagrade")
            return None

        return izraz[0]

    def varDefOper(self,izraz):
        imeVarijable = izraz[1]
            
        self.varijable[imeVarijable] = self.printOper(izraz[2],True)

        return self.varijable[imeVarijable]

    def osnOper(self,operandi,operatorFunkcija):
        
        brOperandi = len(operandi)

        for i in range(1,brOperandi):
            prviOperand = self.printOper(operandi[i-1],True)

            drugiOperand = self.printOper(operandi[i],True)

            operandi[i] = operatorFunkcija(prviOperand,drugiOperand)

        return operandi[brOperandi-1] #zadnji element je rezultat

    def listaOper(self,izraz,operator):
        
        if (operator == "new"):
            tempStvarnaLista = izraz[1:]

            for i in range(len(tempStvarnaLista)):
                tempStvarnaLista[i] = self.printOper(tempStvarnaLista[i],True)

            return tempStvarnaLista
        elif (operator == "get"):
            nazivListe = izraz[1]
            
            indexListe = int(self.printOper(izraz[2],True))
            
            return self.dohvatiVarValue(nazivListe)[indexListe]
        elif (operator == "set"):
            nazivListe = izraz[1]
            
            indexListe = int(self.printOper(izraz[2],True))

            novaVrijednost = self.printOper(izraz[3],True)
            
            self.dohvatiVarValue(nazivListe)[indexListe] = novaVrijednost
            
            return novaVrijednost
        elif (operator == "add"):
            nazivListe = izraz[1]

            novaVrijednost = self.printOper(izraz[2],True)
            
            self.dohvatiVarValue(nazivListe).append(novaVrijednost)
        else:
            #print("Nepostojeci operator")
            return None

    def dictionaryOper(self,izraz,operator):

        if (operator == "new"):
            tempStvarnaLista = izraz[1:]

            tempDictionary = {}

            index = 0

            while (index < len(tempStvarnaLista)):
                
                kljuc = self.printOper(tempStvarnaLista[index],True)

                vrijednost = self.printOper(tempStvarnaLista[index + 1],True)

                tempDictionary[kljuc] = vrijednost

                index = index + 2

            return tempDictionary
        elif (operator == "get"):
            
            nazivDictionary = izraz[1]
            
            tempKljuc = self.printOper(izraz[2],True)

            try:
                return self.dohvatiVarValue(nazivDictionary)[tempKljuc]
            except KeyError:
                return None
        elif (operator == "set"):
            nazivDictionary = izraz[1]
            
            tempKljuc = self.printOper(izraz[2],True)

            novaVrijednost = self.printOper(izraz[3],True)

            self.dohvatiVarValue(nazivDictionary)[tempKljuc] = novaVrijednost        
        else:
            #print("Nepostojeci operator")
            return None

    def bazaPodOper(self,izraz,operator):
        
        if (operator == "0"):
            return MiniBaza( izraz[1].replace("\'","").replace("\"","") )
        elif (operator == "+"):
            tempKolekcije = self.dohvatiVarValue(izraz[1]).dohvati_kolekcije()
            
            nazivKolekcije = izraz[2].replace("\'","").replace("\"","")

            dokument = self.printOper(izraz[3],True)

            try:
                tempKolekcije[nazivKolekcije].append(dokument)
            except KeyError:
                tempKolekcije[nazivKolekcije] = [dokument]
                
            return dokument
        elif ( operator == ">" or operator == ">=" or operator == "<" or operator == "<=" or operator == "=" ):
            tempBaza = self.dohvatiVarValue(izraz[1])
            
            nazivKolekcije = izraz[2].replace("\'","").replace("\"","")

            dokument = self.printOper(izraz[3],True)

            if (operator == ">"):
                return tempBaza.nadji_dokumente(nazivKolekcije,dokument,lambda a,b: a > b)
            elif (operator == ">="):
                return tempBaza.nadji_dokumente(nazivKolekcije,dokument,lambda a,b: a >= b)
            elif (operator == "<"):
                return tempBaza.nadji_dokumente(nazivKolekcije,dokument,lambda a,b: a < b)
            elif (operator == "<="):
                return tempBaza.nadji_dokumente(nazivKolekcije,dokument,lambda a,b: a <= b)
            else:
                return tempBaza.nadji_dokumente(nazivKolekcije,dokument,lambda a,b: a == b)
        else:
            #print("Nepostojeci operator")
            return None

    def zaSvakiOper(self,izraz):
        nazivTempVar = izraz[1]

        self.varijable[nazivTempVar] = None

        tempLista = self.printOper(izraz[2],True)

        listaNaredbi = izraz[3:]

        for element in tempLista:
            self.varijable[nazivTempVar] = element

            for naredba in listaNaredbi:
                self.obradiIzraz(naredba,True)

        return tempLista

    def printOper(self,izraz,evaluateCall = False):
        
        izlaz = None
        
        if (evaluateCall):
            izlaz = izraz
        else:
            izlaz = izraz[1]

        if ( isinstance(izlaz,list) ):
            izlaz = self.obradiIzraz(izlaz,True)
        elif ( izlaz in self.varijable ):
            izlaz = self.varijable[izlaz]
        else:
            try:
                izlaz = float(izlaz)
            except ValueError:
                izlaz = izlaz.replace("\'","").replace("\"","")
        
        if (evaluateCall == False):
            print(izlaz)
        
        return izlaz

    def uvjetOper(self,izraz):
        
        prviOperand = self.printOper(izraz[1],True)

        drugiOperand = self.printOper(izraz[2],True)
        
        if (izraz[0] == ">"):
            return prviOperand > drugiOperand
        elif (izraz[0] == ">="):
            return prviOperand >= drugiOperand
        elif (izraz[0] == "<"):
            return prviOperand < drugiOperand
        elif (izraz[0] == "<="):
            return prviOperand <= drugiOperand
        elif (izraz[0] == "="):
            return prviOperand == drugiOperand
        else:
            return False

    def akoOper(self,izraz):
        if ( self.uvjetOper(izraz[1]) ):
            return self.printOper(izraz[2],True)
        else:
            return self.printOper(izraz[3],True)
        
    def obradiIzraz(self,izraz,parsed=False):
        if (parsed == False):
            izraz = self.parsirajStringIzraz(izraz)
            
        #print(" >> " + str(izraz))

        if (izraz == None):
            return "Error"
        if (izraz[0] == "def"):
            return self.varDefOper(izraz)
        elif (izraz[0] == "+"):
            return self.osnOper(izraz[1:],lambda n, m: n + m)
        elif (izraz[0] == "-"):
            return self.osnOper(izraz[1:],lambda n, m: n - m)
        elif (izraz[0] == "*"):
            return self.osnOper(izraz[1:],lambda n, m: n * m)
        elif (izraz[0] == "/"):
            return self.osnOper(izraz[1:],lambda n, m: n / m)
        elif (izraz[0].startswith("~")):
            return self.listaOper(izraz,izraz[0][1:])
        elif (izraz[0].startswith(":")):
            return self.dictionaryOper(izraz,izraz[0][1:])
        elif (izraz[0].startswith("?")):
            return self.bazaPodOper(izraz,izraz[0][1:])
        elif (izraz[0] == "za-svaki"):
            return self.zaSvakiOper(izraz)
        elif (izraz[0] == "print"):
            return self.printOper(izraz)
        elif (izraz[0] == "ako"):
            return self.akoOper(izraz)
        else:
            #print("Nepostojeci operator")
            return None

    def dohvatiVarValue(self,varName, dictionaryFormat=False):
        
        tempVarValue = None
        
        try:
            tempVarValue = self.varijable[varName]
        except KeyError:
            #print("Nepostojeca varijabla")
            tempVarValue = None

        if (dictionaryFormat):
            return {varName : tempVarValue}
        else:
            return tempVarValue
        
        
def main():
    komandnaLinija = MiniQueryLanguage()

    print("=======================")

    print( komandnaLinija.obradiIzraz("(* (+ 5 5) 5)") )

    komandnaLinija.obradiIzraz("(def trecaVar (def prvaVar 78))")

    komandnaLinija.obradiIzraz("(def drugaVar (* (* (+ 7 5 8 7) 2) 1.5))")

    print( komandnaLinija.dohvatiVarValue("prvaVar",True) )

    print( komandnaLinija.dohvatiVarValue("drugaVar",True) )

    print( komandnaLinija.dohvatiVarValue("trecaVar",True) )

    print( komandnaLinija.dohvatiVarValue("nepostojeca") )

    print("=======================")

    komandnaLinija.obradiIzraz("(def lista ['1' 2 3 4 trecaVar 6])")

    print( komandnaLinija.dohvatiVarValue("lista",True) )

    komandnaLinija.obradiIzraz("(def lista [prvaVar drugaVar trecaVar nepostojeca 5])")

    print( komandnaLinija.dohvatiVarValue("lista",True) )

    print("=======================")

    komandnaLinija.obradiIzraz("(def zavisnaVar (* 5 prvaVar))")

    print( komandnaLinija.dohvatiVarValue("zavisnaVar",True) )

    komandnaLinija.obradiIzraz("(def zavisnaVar drugaVar)")

    print( komandnaLinija.dohvatiVarValue("zavisnaVar",True) )

    komandnaLinija.obradiIzraz("(def zavisnaVar nepostojeca)")

    print( komandnaLinija.dohvatiVarValue("zavisnaVar",True) )

    print("=======================")

    komandnaLinija.obradiIzraz("(def osobe (?0 'knjige'))")

    komandnaLinija.obradiIzraz("(def dok {'ime' 'Pero' 'prihod' (+ prvaVar 50)})")

    komandnaLinija.obradiIzraz("(?+ osobe 'prihodi' dok)")

    komandnaLinija.obradiIzraz("(?+ osobe 'prihodi' {'ime' 'Luka' 'prihod' 50})")

    komandnaLinija.obradiIzraz("(?+ osobe 'prihodi' {'ime' 'Pero' 'prihod' 150})")

    komandnaLinija.obradiIzraz("(?+ osobe 'prihodi' {'ime' 'Marko' 'prihod' 450})")

    print( komandnaLinija.obradiIzraz("(?> osobe 'prihodi' {'prihod' 128})") )

    print( komandnaLinija.obradiIzraz("(?>= osobe 'prihodi' {'prihod' 128})") )

    print( komandnaLinija.obradiIzraz("(?< osobe 'prihodi' {'prihod' 128})") )

    print( komandnaLinija.obradiIzraz("(?<= osobe 'prihodi' {'prihod' 128})") )

    print( komandnaLinija.obradiIzraz("(?= osobe 'prihodi' {'prihod' 128})") )

    print("=======================")

    komandnaLinija.obradiIzraz("(za-svaki dokument (?>= osobe 'prihodi' {'prihod' 150}) (print dokument))")

    print("=======================")

    komandnaLinija.obradiIzraz("(za-svaki elementizer lista (print elementizer) (print elementizer))")

    print("=======================")

    komandnaLinija.obradiIzraz("(def listaTestPrvi (~get lista 1))")

    print( komandnaLinija.dohvatiVarValue("lista",True) )

    print( komandnaLinija.dohvatiVarValue("listaTestPrvi",True) )

    komandnaLinija.obradiIzraz("(def listaTestDrugi (~set lista 1 99))")

    print( komandnaLinija.dohvatiVarValue("lista",True) )

    print( komandnaLinija.dohvatiVarValue("listaTestDrugi",True) )

    komandnaLinija.obradiIzraz("(def listaTestTreci (~set lista 3 (+ 45 prvaVar)))")

    print( komandnaLinija.dohvatiVarValue("lista",True) )

    print( komandnaLinija.dohvatiVarValue("listaTestTreci",True) )

    print("=======================")

    komandnaLinija.obradiIzraz("(def lista [1 2 {'a' 5}])")

    komandnaLinija.obradiIzraz("(def dictionaryTest (~get lista 2))")

    print( komandnaLinija.dohvatiVarValue("lista",True) )

    print( komandnaLinija.dohvatiVarValue("dictionaryTest",True) )
    
    print("=======================")

    komandnaLinija.obradiIzraz("(def brojevi [-3 -2 -1 0 1.5 2 3])")

    komandnaLinija.obradiIzraz("(def opisBrojeva [])")

    komandnaLinija.obradiIzraz("(def brojac 0)")

    komandnaLinija.obradiIzraz("(za-svaki x brojevi (~add opisBrojeva (ako (> x 0) 'pozitivan' (ako (< x 0) 'negativan' 'neutralan'))) (print [(~get brojevi brojac) (~get opisBrojeva brojac)]) (def brojac (+ brojac 1)) )")

    print("=======================")

    komandnaLinija.obradiIzraz("(def testniDict {})")

    komandnaLinija.obradiIzraz("(print (:get testniDict testniKljuc))")

    komandnaLinija.obradiIzraz("(:set testniDict testniKljuc 54)")

    komandnaLinija.obradiIzraz("(print (:get testniDict testniKljuc))")

    print("=======================")
    
    input()

if __name__ == "__main__":
    main()
