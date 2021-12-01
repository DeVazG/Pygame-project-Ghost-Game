# Vertaisarvioijalle/muulle tiedoston lukijalle/pelin kokeilijalle:
# Keräilypelissä tarkoitus on kerätä kolikoita eri puolilta karttaa. 
# Kolikoista kertyy pisteitä
# Pisteiden kertyessä myöskin väisteltävien hirviöiden määrä kasvaa
# Häviät, jos robo osuu hirviöön.
# Hirviöiden käännökset risteyksissä ja kulmissa ovat satunnaisia
# Hirviö voi pienellä todennäköisyydellä kääntyä risteyksestä myöskin tulosuuntaan
# Roboa ohjataan pitämällä nuolinäppäimiä pohjassa
# Voit pitää useampia nuolinäppäimiä pohjassa samaan aikaan, jolloin
# robo liikkuu kumpaankin suuntaan, jos pystyy. Esimerkiksi kääntyminen on nopeinta niin,
# että ennakoi kääntymistä painamalla käännöksen puoleisen nuolinäppäimen pohjaan ennen käännöstä.
# Enteriä painamalla saa tauon kesken pelihetken.
import pygame, random

class Robo:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
class Hirvio(Robo):
    def __init__(self,x,y,suunta:list=[0,0]):
        super().__init__(x,y)
        self.suunta=suunta

class Kolikko(Robo):
    def __init__(self,x,y):
        super().__init__(x,y)


class Keräily:
    def __init__(self):
        pygame.init()
        self.kenttä=self.kentta()
        self.leveys=35
        self.resoluutio=(20+len(self.kenttä[0])*self.leveys,20+len(self.kenttä)*self.leveys)
        self.naytto=pygame.display.set_mode(self.resoluutio)
        self.robo=Robo(6,2)
        self.kolikko=Kolikko(0,0)
        pygame.display.set_caption("Collecting Game")

        #Näppäimet
        self.vasen=False
        self.oikea=False
        self.ylös=False
        self.alas=False

        self.keskipistelista=self.kplista()
        self.oliokuvat=self.oliot()
        self.kello=pygame.time.Clock()
        self.ohjaimet={"K_LEFT":False,"K_RIGHT":False,"K_DOWN":False,"K_UP":False}
        #self.toiminto kertoo pelin tilan. 1 - aloitusnäyttö, 2 - peli, 3 - Pelin tulokset
        self.hlista=[Hirvio(11+20*self.leveys, 11+0*self.leveys),
                Hirvio(11+10*self.leveys, 11+2*self.leveys),
                Hirvio(11+9*self.leveys, 11+7*self.leveys),
                Hirvio(11+3*self.leveys, 11+6*self.leveys),
                Hirvio(11+3*self.leveys, 11+15*self.leveys),
                Hirvio(11+7*self.leveys, 11+9*self.leveys)]
        self.toiminto=1
        self.lisays=False
        self.pisteet=-1
        self.edellisetpisteet=0
        self.maksimipisteet=0
        self.pisteetnäytölle=False
        self.tauko=False
        self.fontti=pygame.font.SysFont("Bell MT", 70)
        self.teksti1=self.fontti.render("GhostGame", True, (255,255,255))
        self.fonttip=pygame.font.SysFont("Bell MT", 40)
        self.teksti2=self.fonttip.render("Press Enter", True, (255,255,255))
        self.fontti2=pygame.font.SysFont("Arial", 24)
        while True:

            self.kentan_piirto()
            self.hirviot()
            if self.toiminto==1:
                self.teksti1=self.fontti.render("GhostGame", True, (255,255,255))
                w1=self.teksti1.get_width()
                h1=self.teksti1.get_height()
                w2=self.teksti2.get_width()
                x=self.resoluutio[0]/2-250
                y=self.resoluutio[1]/2-150
                pygame.draw.rect(self.naytto, (0,0,0),(x,y,500,300))
                self.naytto.blit(self.teksti1, (self.resoluutio[0]/2-w1/2,self.resoluutio[1]/2-5*h1/4))
                self.naytto.blit(self.teksti2, (self.resoluutio[0]/2-w2/2,self.resoluutio[1]/2))
                if self.pisteetnäytölle:
                    self.naytto.blit(self.teksti3,(self.resoluutio[0]/2-self.teksti3.get_width()/2,self.resoluutio[1]/2+30))
                pygame.display.flip()
                self.tapahtumat()
                self.kello.tick(60)

            if self.toiminto==2:
                self.looppi()
            
    def nollaa(self):
        self.hlista=[Hirvio(11+20*self.leveys, 11+0*self.leveys),
                Hirvio(11+10*self.leveys, 11+2*self.leveys),
                Hirvio(11+9*self.leveys, 11+7*self.leveys),
                Hirvio(11+3*self.leveys, 11+6*self.leveys),
                Hirvio(11+3*self.leveys, 11+15*self.leveys),
                Hirvio(11+7*self.leveys, 11+9*self.leveys)]
        self.edellisetpisteet=self.pisteet
        if self.pisteet>self.maksimipisteet:
            self.maksimipisteet=self.pisteet
        self.teksti3=self.fontti2.render(f"Score: {self.edellisetpisteet}, High Score: {self.maksimipisteet}", True, (255,255,255))
        self.pisteetnäytölle=True
        self.pisteet=-1
        self.robo.x=0
        self.robo.y=0
        self.kolikko.x=0
        self.kolikko.y=0

    def kolikkko(self):
        if self.robo.x+15>=self.kolikko.x and self.robo.x<=self.kolikko.x+35:
            if self.robo.y>=self.kolikko.y-25 and self.robo.y<=self.kolikko.y+35:
                self.pisteet+=1
                while True:
                    uusix=random.randint(0,len(self.kenttä[0])-1)
                    uusiy=random.randint(0,len(self.kenttä)-1)
                    if self.kenttä[uusiy][uusix]==0 and self.leveys*7<abs(self.robo.x-uusix*self.leveys):
                        if self.leveys*7<abs(self.robo.y-uusiy*self.leveys):
                            break
                self.kolikko.x=uusix*self.leveys
                self.kolikko.y=uusiy*self.leveys
                self.lisays=True
        self.piirrä_kolikko()
        
    def piirrä_kolikko(self):
        x=7+self.kolikko.x+(self.leveys-self.oliokuvat[2].get_width())/2
        y=12+self.kolikko.y+(self.leveys-self.oliokuvat[2].get_height())/2
        self.naytto.blit(self.oliokuvat[1], (x,y))

    def looppi(self):
        while True:
            while self.tauko:
                self.tapahtumat()
                self.kello.tick(15)
                pygame.display.flip()
            self.tapahtumat()
            self.kentan_piirto()
            self.kolikkko()
            self.paivita_robo()
            self.piirrä_robo()
            self.hirvioita=len(self.hlista)
            teksti3=self.fontti2.render(f"Score: {self.pisteet}, Ghosts: {self.hirvioita}", True, (255,255,255))
            self.naytto.blit(teksti3, (14+self.leveys*15, 13+self.leveys*16))
            if self.hirviot():
                self.toiminto=1
                self.nollaa()
                break
            
            pygame.display.flip()
            self.kello.tick(60)

    def lisaa_hirvio(self):
        if len(self.hlista)<21:
            if self.pisteet%3==0 and self.pisteet!=0:
                while True:
                    x=random.randint(0,len(self.kenttä[0])-1)
                    y=random.randint(0,len(self.kenttä)-1)
                    if self.kenttä[y][x]==0 and self.leveys*7<abs(self.robo.x-x*self.leveys):
                        if self.leveys*7<abs(self.robo.y-y*self.leveys):
                            break
                self.hlista.append(Hirvio(11+x*self.leveys, 11+y*self.leveys))
                self.lisays=False
                

    def hirviot(self):
        #Tämä funktio koostaa kaikki loopin sisällä olevat hirviöfunktiot
        z=self.uusi_sijainti()
        self.hirviosuunnat()   
        self.piirra_hirviot()
        if self.lisays:
            self.lisaa_hirvio()
        if z:
            return True

    def kentta(self):
        #21*16
        kenttä=[
        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,1,0,1,0,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0],
        [0,1,0,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0],
        [0,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0],
        [0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0],
        [0,1,1,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,0,1,0],
        [0,0,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,0,0,1,0],
        [0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0],
        [0,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,0,1,0],
        [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0],
        [0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0],
        [0,1,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1],
        [0,1,1,0,1,1,0,1,1,1,0,1,0,0,0,1,0,1,0,0,0],
        [0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0],
        [1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,1,1,1,1]
        ]
        return kenttä

    def oliot(self):
        #etsii kuvat ja skaalaa ne ruudun leveyden mukaan, palauttaa listan
        oliolista=["robo", "kolikko", "hirvio"]
        ol=[]
        for i in oliolista:
            kuva=pygame.image.load(f"{i}.png")

            skaala=kuva.get_height()/self.leveys
            dx=int(kuva.get_width()//skaala)
            dy=int(kuva.get_height()//skaala)
            ol.append(pygame.transform.scale(kuva, (dx,dy)))
        return ol

    def kplista(self):
        #ainoa tarkoitus on luoda pistelista toteutuneen ruudukon/pelikentän
        #yksittäisten ruutujen keskipisteistä (leveys on pariton luku)
        kplista=[]
        keskipiste=self.leveys//2
        for i in range(len(self.kenttä)):
            for j in range(len(self.kenttä[i])):
                kplista.append((10+self.leveys*j+keskipiste, 10+self.leveys*i+keskipiste))
        return kplista

    def kp_ruutu(self, piste:tuple):
        #Tämä funktio muuttaa ruudun keskipisteen pelitaulukon indeksikoordinantiksi, tarvitaan hirviöliikefunktiossa.
        #Funktio tekee siis saman, kuin kplista, mutta käänteisesti ja vain yhdelle pisteelle.
        indeksix=(piste[0]-11)/self.leveys
        indeksiy=(piste[1]-11)/self.leveys
        if indeksix%1==0 and indeksiy%1==0:
            return (int(indeksix),int(indeksiy))
        return

    def uusi_sijainti(self):
        #Funktio päivittää hirviön sijainnin joka frame, käytetään while-loopin sisällä.
        for hirvio in self.hlista:
            hirvio.x+=hirvio.suunta[0]
            hirvio.y+=hirvio.suunta[1]
            #alla hirviöx+9 muutettu, alkuperäinen hirviöx+5
            if hirvio.x+9>self.robo.x and hirvio.x<self.robo.x+15:
                if hirvio.y+25>self.robo.y and hirvio.y<self.robo.y+30:
                    return True

    def hirviosuunnat(self):
        #tämä funktio tarkistaa, onko hirviöllä mahdollisuus kääntyä. Jos on, niin funktio arpoo, käännytäänkö, ja jos käännytään, niin mihin.
        for hirvio in self.hlista:
            uudet_suunnatt=[]
            uudet_suunnatt.clear()
            sijainti=self.kp_ruutu((hirvio.x,hirvio.y))
            if sijainti is not None:
                if (hirvio.x+16, hirvio.y+16) in self.keskipistelista:
                    #Try lauseet, jotta ei tule index out of range- erroria.
                    try: 
                        if self.kenttä[sijainti[1]][sijainti[0]+1]==0:
                            uudet_suunnatt.append([1,0])
                    except:
                        pass
                    try: 
                        if self.kenttä[sijainti[1]][sijainti[0]-1]==0 and sijainti[0]-1>=0:
                            uudet_suunnatt.append([-1,0])
                    except:
                        pass
                    try: 
                        if self.kenttä[sijainti[1]+1][sijainti[0]]==0:
                            uudet_suunnatt.append([0,1])
                    except:
                        pass
                    try: 
                        if self.kenttä[sijainti[1]-1][sijainti[0]]==0 and sijainti[1]-1>=0:
                            uudet_suunnatt.append([0,-1])
                    except:
                        pass
                    #poistetaan tulosuunta vaihtoehdoista suurimmalla osalla kerroista.
                    #Jätetään pienet mahdollisuudet sille, että hirviö kääntyy
                    #taaksepäin risteyksen kohdalla.
                    arpa=random.randint(1,20)
                    try:
                        if arpa<19 or len(uudet_suunnatt)<=2:
                            uudet_suunnatt.remove([-hirvio.suunta[0], -hirvio.suunta[1]])
                    except:
                        pass
                    if len(uudet_suunnatt)>=1:
                        uusi_suunta=uudet_suunnatt[random.randint(0,len(uudet_suunnatt)-1)]
                        hirvio.suunta=uusi_suunta
                    else:
                        hirvio.suunta=[-hirvio.suunta[0], -hirvio.suunta[1]]    

    def piirra_hirviot(self):
        #Funktio piirtää hirviöt kartalle joka frame erikseen.
        for hirvio in self.hlista:
            x=hirvio.x+(self.leveys-self.oliokuvat[2].get_width())/2
            y=hirvio.y+(self.leveys-self.oliokuvat[2].get_height())/2
            self.naytto.blit(self.oliokuvat[2], (x,y))
    
    def piirrä_robo(self):
        x=6+self.robo.x+(self.leveys-self.oliokuvat[2].get_width())/2
        y=10+self.robo.y+(self.leveys-self.oliokuvat[2].get_height())/2
        self.naytto.blit(self.oliokuvat[0], (x,y))

    def paivita_robo(self):
        yind=(self.robo.y)//self.leveys
        xind=(self.robo.x)//self.leveys
        robokuva=self.oliokuvat[0]

        if self.alas:
            if self.robo.y<(yind+1)*self.leveys-1-robokuva.get_height():
                self.robo.y+=1
                if self.votarkistus(robokuva):
                    return
            elif yind+1<len(self.kenttä) and self.kenttä[yind+1][xind]==0:
                if self.robo.x>=xind*self.leveys-2 and self.robo.x<(xind)*self.leveys+18:
                    self.robo.y+=2
                    if self.votarkistus(robokuva):
                        return
        if self.ylös:
            if self.robo.y>(yind)*self.leveys+1:
                self.robo.y-=2
                if self.votarkistus(robokuva):
                    return
            elif self.kenttä[yind-1][xind]==0 and yind-1>=0:
                if self.robo.x>=xind*self.leveys-2 and self.robo.x<(xind)*self.leveys+18:
                    self.robo.y-=2
                    if self.votarkistus(robokuva):
                        return
        self.oikealle(xind,yind,robokuva)
        self.vasemmalle(xind,yind)

    def tapahtumat(self):
        #Funktio käsittelee tapahtumat
        for tapahtuma in pygame.event.get():
            if tapahtuma.type==pygame.QUIT:
                quit()
            if tapahtuma.type==pygame.KEYDOWN:
                totuus=True
            if tapahtuma.type==pygame.KEYUP:
                totuus=False
                
            try:
                if tapahtuma.key==pygame.K_DOWN:
                    self.alas=totuus
                elif tapahtuma.key==pygame.K_UP:
                    self.ylös=totuus
                elif tapahtuma.key==pygame.K_LEFT:
                    self.vasen=totuus
                elif tapahtuma.key==pygame.K_RIGHT:
                    self.oikea=totuus
            except:
                pass

            if tapahtuma.type==pygame.KEYDOWN and tapahtuma.key==pygame.K_RETURN:
                if self.toiminto==1:
                    self.toiminto=2
                elif self.toiminto==2:
                    if self.tauko==False:
                        self.tauko=True
                    elif self.tauko==True:
                        self.tauko=False

    def vasemmalle(self,xind,yind):
        #Tutkii robotin liikettä vasemmalle
        if self.vasen:
            if self.robo.x>(xind)*self.leveys+1:
                self.robo.x-=2
            elif self.kenttä[yind][xind-1]==0 and xind-1>=0:
                if self.robo.y>=yind*self.leveys-15 and self.robo.y<(yind)*self.leveys+4:
                    self.robo.x-=2
    
    def oikealle(self,xind,yind,robokuva):
        #Tutkii robotin liikettä oikealle
        if self.oikea:
            if self.robo.x<(xind+1)*self.leveys-robokuva.get_width()-1:
                self.robo.x+=2
            elif xind+1<len(self.kenttä[yind]) and self.kenttä[yind][xind+1]==0:
                if self.robo.y>=yind*self.leveys-15 and self.robo.y<(yind)*self.leveys+4:
                    self.robo.x+=2

    def votarkistus(self, robokuva):
        #Tämä methodi tarkistaa tuplainputit robotin liikkeisiin
        if self.vasen or self.oikea:
            xind2=(self.robo.x)//self.leveys
            yind2=(self.robo.y)//self.leveys
            self.vasemmalle(xind2,yind2)
            self.oikealle(xind2,yind2,robokuva)
            return True

    def kentan_piirto(self):
    #Funktio piirtää kentän joka Framen aikana uudestaan.
        self.naytto.fill((0,0,0))
        for y in range(len(self.kenttä)):
            for x in range(len(self.kenttä[y])):
                if self.kenttä[y][x]==0:
                    pygame.draw.rect(self.naytto, (50,50,50), (11+x*self.leveys, 11+y*self.leveys, self.leveys, self.leveys))


if __name__=="__main__":
    Keräily()