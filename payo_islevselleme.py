import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from payo_giris import Ui_GirisSayfasi
from payo_anasayfa import Ui_AnaPencere
from payo_tablo import Ui_BilgilerTablosu
import sqlite3
import time

class TabloSayfasi(QtWidgets.QDialog):
    def __init__(self):
        super(TabloSayfasi, self).__init__()

        self.arayuz_tablo = Ui_BilgilerTablosu()
        self.arayuz_tablo.setupUi(self)

        self.arayuz_tablo.dgmKapat.clicked.connect(self.kapat)

        self.baglanti = sqlite3.connect("veritabani.db")
        self.imlec = self.baglanti.cursor()
        self.tablo_sorgusu = ("CREATE TABLE IF NOT EXISTS Bilgiler(Numara INTEGER NOT NULL PRIMARY "
                              "KEY AUTOINCREMENT, Uygulama TEXT NOT NULL, Kullanici TEXT NOT NULL, "
                              "Acarga TEXT NOT NULL, EkBilgi TEXT)")
        self.imlec.execute(self.tablo_sorgusu)
        self.baglanti.commit()

        self.listeyeYansit()

    def kayitSayisiVer(self):
        self.imlec.execute("SELECT COUNT(*) FROM Bilgiler")
        kayit_sayisi = self.imlec.fetchone()
        self.arayuz_tablo.lblKayitGosterim.setText(str(kayit_sayisi[0]))

    def listeyeYansit(self):
        self.arayuz_tablo.tblKayitlar.clear()
        self.arayuz_tablo.tblKayitlar.setHorizontalHeaderLabels(("Nu", "Uygulama", "Kullanıcı", "Parola", "Ek Bilgi"))
        self.arayuz_tablo.tblKayitlar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.imlec.execute("SELECT * FROM Bilgiler")
        for satir_indisi, satir_verisi in enumerate(self.imlec):
            for sutun_indisi, sutun_verisi in enumerate(satir_verisi):
                self.arayuz_tablo.tblKayitlar.setItem(satir_indisi, sutun_indisi, QTableWidgetItem(str(sutun_verisi)))
        self.arayuz_tablo.tblKayitlar.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.kayitSayisiVer()

    def kapat(self):
        yanit = QMessageBox.question(self, "Kapat", "Tablo kapatılsın mı?", QMessageBox.Yes | QMessageBox.No)
        if yanit == QMessageBox.Yes:
            self.baglanti.close()
            self.close()
        else:
            self.show()

class AnaSayfa(QtWidgets.QMainWindow):
    def __init__(self):
        super(AnaSayfa, self).__init__()

        self.arayuz_ana = Ui_AnaPencere()
        self.arayuz_ana.setupUi(self)

        self.gecis = TabloSayfasi()

        self.baglanti = sqlite3.connect("veritabani.db")
        self.imlec = self.baglanti.cursor()
        self.tablo_sorgusu = ("CREATE TABLE IF NOT EXISTS Bilgiler(Numara INTEGER NOT NULL PRIMARY "
                              "KEY AUTOINCREMENT, Uygulama TEXT NOT NULL, Kullanici TEXT NOT NULL, "
                              "Acarga TEXT NOT NULL, EkBilgi TEXT)")
        self.imlec.execute(self.tablo_sorgusu)
        self.baglanti.commit()

        self.arayuz_ana.dgmSakla.clicked.connect(self.sakla)
        self.arayuz_ana.dgmSil.clicked.connect(self.sil)
        self.arayuz_ana.anaSayfaTablosu.itemSelectionChanged.connect(self.doldur)
        self.arayuz_ana.dgmGuncelle.clicked.connect(self.guncelle)
        self.arayuz_ana.dgmAra.clicked.connect(self.ara)
        self.arayuz_ana.dgmTemizle.clicked.connect(self.temizle)
        self.arayuz_ana.dgmTumu.clicked.connect(self.tumunuAc)
        self.arayuz_ana.dgmCik.clicked.connect(self.cik)

        self.listeyeYansit()

    def listeyeYansit(self):
        self.arayuz_ana.anaSayfaTablosu.clear()
        self.arayuz_ana.anaSayfaTablosu.setHorizontalHeaderLabels(("Nu", "Uygulama", "Kullanıcı", "Parola", "Ek Bilgi"))
        self.arayuz_ana.anaSayfaTablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.imlec.execute("SELECT * FROM Bilgiler")
        for satir_indisi, satir_verisi in enumerate(self.imlec):
            for sutun_indisi, sutun_verisi in enumerate(satir_verisi):
                self.arayuz_ana.anaSayfaTablosu.setItem(satir_indisi, sutun_indisi, QTableWidgetItem(str(sutun_verisi)))
        self.arayuz_ana.anaSayfaTablosu.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.arayuz_ana.lneUygulama.clear()
        self.arayuz_ana.lneKullanici.clear()
        self.arayuz_ana.lneAcarga.clear()
        self.arayuz_ana.lneEkBilgi.clear()

    def sakla(self):
        uygulama = self.arayuz_ana.lneUygulama.text()
        kullanici = self.arayuz_ana.lneKullanici.text()
        acarga = self.arayuz_ana.lneAcarga.text()
        ek_bilgi = self.arayuz_ana.lneEkBilgi.text()

        if uygulama and kullanici and acarga != 0:
            self.imlec.execute("INSERT INTO Bilgiler(Uygulama, Kullanici, Acarga, EkBilgi) VALUES"
                               "(?, ?, ?, ?)", (uygulama, kullanici, acarga, ek_bilgi))
            self.baglanti.commit()
            self.arayuz_ana.durumCubugu.showMessage("Bilgileriniz saklandı.", 7000)
        else:
            self.arayuz_ana.durumCubugu.showMessage("Gerekli bilgiler girilmeden bilgi saklanamaz.", 7000)

        self.listeyeYansit()

    def doldur(self):
        secili_satir = self.arayuz_ana.anaSayfaTablosu.selectedItems()
        if len(secili_satir) != 0:
            self.arayuz_ana.lneUygulama.setText(secili_satir[1].text())
            self.arayuz_ana.lneKullanici.setText(secili_satir[2].text())
            self.arayuz_ana.lneAcarga.setText(secili_satir[3].text())
            self.arayuz_ana.lneEkBilgi.setText(secili_satir[4].text())
            self.arayuz_ana.durumCubugu.showMessage("Seçilen satır için işlem yapılabilir.", 3000)
        else:
            self.arayuz_ana.lneUygulama.clear()
            self.arayuz_ana.lneKullanici.clear()
            self.arayuz_ana.lneAcarga.clear()
            self.arayuz_ana.lneEkBilgi.clear()
            self.arayuz_ana.durumCubugu.showMessage("Seçilen satır boştur.", 3000)

    def guncelle(self):
        secili_satir = self.arayuz_ana.anaSayfaTablosu.selectedItems()
        if len(secili_satir) != 0:
            yanit = QMessageBox.question(self, "Güncelleme", "Kayıt güncellensin mi?", QMessageBox.Yes | QMessageBox.No)
            if yanit == QMessageBox.Yes:
                try:
                    secili_urun = self.arayuz_ana.anaSayfaTablosu.selectedItems()
                    nu = int(secili_urun[0].text())
                    uygulama = self.arayuz_ana.lneUygulama.text()
                    kullanici = self.arayuz_ana.lneKullanici.text()
                    acarga = self.arayuz_ana.lneAcarga.text()
                    ek_bilgi = self.arayuz_ana.lneEkBilgi.text()

                    self.imlec.execute("UPDATE Bilgiler SET Uygulama=?, Kullanici=?, Acarga=?, EkBilgi=? "
                                       "WHERE Numara=?", (uygulama, kullanici, acarga, ek_bilgi, nu))
                    self.baglanti.commit()
                    self.listeyeYansit()
                    self.arayuz_ana.durumCubugu.showMessage("Güncelleme işlemi başarıyla gerçekleşti.", 7000)
                except Exception as hata:
                    self.arayuz_ana.durumCubugu.showMessage(str(hata) + "adlı bir hata ile karşılaşıldı.", 5000)
            else:
                self.arayuz_ana.durumCubugu.showMessage("Güncelleme işlemi iptal edildi.", 7000)
        else:
            self.arayuz_ana.durumCubugu.showMessage("Güncellemek için önce dolu bir satır seçmelisiniz.", 7000)

    def sil(self):
        secili_satir = self.arayuz_ana.anaSayfaTablosu.selectedItems()
        if len(secili_satir) != 0:
            yanit = QMessageBox.question(self, "Silme", "Silmek mi istiyorunuz?", QMessageBox.Yes | QMessageBox.No)
            if yanit == QMessageBox.Yes:
                secili_urun = self.arayuz_ana.anaSayfaTablosu.selectedItems()
                silinecek_urun = secili_urun[0].text()
                try:
                    self.imlec.execute("DELETE FROM Bilgiler WHERE Numara='%s'" % silinecek_urun)
                    self.baglanti.commit()
                    self.listeyeYansit()
                    self.arayuz_ana.durumCubugu.showMessage("Kayıt silme işlemi başarıyla gerçekleşti.", 7000)
                except Exception as hata:
                    self.arayuz_ana.durumCubugu.showMessage(str(hata) + "adlı bir hata ile karşılaşıldı.", 5000)
            else:
                self.arayuz_ana.durumCubugu.showMessage("Silme işlemi iptal edildi.", 7000)
        else:
            self.arayuz_ana.durumCubugu.showMessage("Öncelikle silmek istediğiniz satırı seçmelisiniz.", 3000)

    def ara(self):
        aranan = self.arayuz_ana.lneAra.text()
        if len(aranan) != 0:
            try:
                self.imlec.execute("SELECT * FROM Bilgiler WHERE Uygulama=? OR Kullanici=? OR Acarga=? OR EkBilgi=?",
                                   (aranan, aranan, aranan, aranan))
                self.baglanti.commit()
                self.arayuz_ana.durumCubugu.showMessage("Arama sonuçları bulundu ve gösterildi.", 5000)
            except Exception as hata:
                self.arayuz_ana.durumCubugu.showMessage(str(hata) + "adlı bir hata ile karşılaşıldı.", 5000)
            self.arayuz_ana.anaSayfaTablosu.clear()
            for satir_indisi, satir_verisi in enumerate(self.imlec):
                for sutun_indisi, sutun_verisi in enumerate(satir_verisi):
                    self.arayuz_ana.anaSayfaTablosu.setItem(satir_indisi, sutun_indisi, QTableWidgetItem(str(sutun_verisi)))
        else:
            self.arayuz_ana.durumCubugu.showMessage("Herhangi bir şey aratmadınız.", 3000)

    def temizle(self):
        self.arayuz_ana.lneAra.clear()
        self.listeyeYansit()

    def tumunuAc(self):
        self.gecis.show()

    def cik(self):
        yanit = QMessageBox.question(self, "Çık", "Uygulamadan çıkılsın mı?", QMessageBox.Yes | QMessageBox.No)
        if yanit == QMessageBox.Yes:
            self.baglanti.close()
            self.close()
        else:
            self.show()

class GirisSayfasi(QtWidgets.QDialog):
    def __init__(self):
        super(GirisSayfasi, self).__init__()

        self.arayuz_giris = Ui_GirisSayfasi()
        self.arayuz_giris.setupUi(self)
        self.gecis = AnaSayfa()

        self.arayuz_giris.dgmGirisYap.clicked.connect(self.gir)
        self.arayuz_giris.dgmHesapAc.clicked.connect(self.hesapAc)

    def gesisYap(self):
        self.gecis.show()

    def gir(self):
        kullanici_adi = self.arayuz_giris.lneKullaniciAdi.text()
        parola = self.arayuz_giris.lneParola.text()

        if kullanici_adi == "cs" and parola == "79":
            self.arayuz_giris.lblBilgilendirme.setText("Giriş başarılı. Hoş geldiniz.")
            time.sleep(3)
            self.gesisYap()
            self.close()
        else:
            self.arayuz_giris.lblBilgilendirme.setText("Hatalı bir giriş yapıldı!")

    def hesapAc(self):
        kullanici_adi = self.arayuz_giris.lneKullaniciAdi.text()
        parola = self.arayuz_giris.lneParola.text()

        if kullanici_adi and parola != 0:
            self.arayuz_giris.lblBilgilendirme.setText("Hesabınız oluşturuldu. Şimdi giriş yapabilirsiniz.")
        else:
            self.arayuz_giris.lblBilgilendirme.setText("Öncelikle hesap bilgilerinizi giriniz!")

def uygulamaGirisSayfasi():
    uyg = QApplication(sys.argv)
    giris = GirisSayfasi()
    giris.show()
    sys.exit(uyg.exec_())

uygulamaGirisSayfasi()
