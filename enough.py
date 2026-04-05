from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading
import shutil
import sys
import os

# Global durdurma değişkeni
durma_bayragi = False

# Servisleri hazırla
servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

def alt_yazi_sabit():
    cols, lines = shutil.get_terminal_size()
    sys.stdout.write(f"\033[0;{lines-1}r")
    sys.stdout.write(f"\033[{lines};0H\033[1;31m DURDUR VE MENUYE DON: CTRL + C \033[0m")
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def ekran_temizle():
    sys.stdout.write("\033[r\033[H\033[J")
    sys.stdout.flush()

def guvenli_yazdir(mesaj):
    # Eğer durdurma tuşuna basıldıysa ekrana hiçbir şey yazma
    if not durma_bayragi:
        sys.stdout.write(mesaj + "\n")
        sys.stdout.flush()

def sms_calistir(fonk_adi, tel, mail):
    if not durma_bayragi:
        sms = SendSms(tel, mail)
        try:
            # SendSms içindeki printleri yakalayamayacağımız için 
            # sadece kendi akışımızı kontrol ediyoruz.
            getattr(sms, fonk_adi)()
        except:
            pass

while True:
    durma_bayragi = False
    ekran_temizle()
    print(r"""
    .    .
       _..;|;__;|;
     ,'   ';` \';`-.
     7;-..     :   )
.--._)|   `;==,|,=='
 `\`@; \_ `<`G," G).
   `\/-;,(  )  .>. )
       < ,-;'-.__.;'
        `\_ `-,__,'
           `-..,;,>
              `;;;;
               `  `
    """)
    print(f"Sms: {Fore.LIGHTRED_EX}{len(servisler_sms)}{Style.RESET_ALL}      {Fore.LIGHTCYAN_EX}°∞°BYFURKAN°∞°{Style.RESET_ALL}\n")

    try:
        secim = input(Fore.LIGHTMAGENTA_EX + " 1- SMS Gönder (Normal)\n\n 2- SMS Gönder (Turbo)\n\n 3- Termuxu Kapat\n\n" + Fore.LIGHTYELLOW_EX + " Seçim: ")
        if not secim: continue
        menu = int(secim)
    except KeyboardInterrupt:
        ekran_temizle()
        sys.exit(0)
    except: continue

    if menu == 1 or menu == 2:
        ekran_temizle()
        tel_no = input(Fore.LIGHTYELLOW_EX + "Telefon no (90 sız): " + Fore.LIGHTGREEN_EX).strip()
        mail = input(Fore.LIGHTYELLOW_EX + "Mail (boş geç): " + Fore.LIGHTGREEN_EX).strip()
        
        kere = 0; aralik = 0
        if menu == 1:
            try:
                kere = int(input(Fore.LIGHTYELLOW_EX + "Kaç adet: " + Fore.LIGHTGREEN_EX) or 0)
                aralik = int(input(Fore.LIGHTYELLOW_EX + "Saniye: " + Fore.LIGHTGREEN_EX) or 0)
            except: pass

        ekran_temizle()
        alt_yazi_sabit()

        try:
            if menu == 1:
                adet = 0
                while not durma_bayragi:
                    for fonk in servisler_sms:
                        if durma_bayragi: break
                        alt_yazi_sabit()
                        sms_calistir(fonk, tel_no, mail)
                        if kere > 0:
                            adet += 1
                            if adet >= kere: 
                                durma_bayragi = True
                                break
                        sleep(aralik)
                    if kere > 0 and adet >= kere: break
            else: # Turbo
                while not durma_bayragi:
                    alt_yazi_sabit()
                    threads = []
                    for fonk in servisler_sms:
                        if durma_bayragi: break
                        t = threading.Thread(target=sms_calistir, args=(fonk, tel_no, mail))
                        t.daemon = True
                        threads.append(t)
                        t.start()
                    for t in threads:
                        t.join(0.1)
        except KeyboardInterrupt:
            durma_bayragi = True # Yazdırmayı anında yasakla
            ekran_temizle()
            continue

    elif menu == 3:
        ekran_temizle()
        os._exit(0)
            
