import os
import sys
import shutil
import threading
from time import sleep
from colorama import Fore, Style
from sms import SendSms

# Servisleri otomatik çek
servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

def alt_yazi_sabit():
    cols, lines = shutil.get_terminal_size()
    # Alt satırı sabitler ve uyarıyı yazar
    sys.stdout.write(f"\033[0;{lines-1}r")
    sys.stdout.write(f"\033[{lines};0H\033[1;31m DURDUR VE MENUYE DON: CTRL + C \033[0m")
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def ekran_temizle():
    # Ekranı resetler ve temizler
    sys.stdout.write("\033[r\033[H\033[J")
    sys.stdout.flush()

while True:
    ekran_temizle()
    # ASCII Banner
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
                while True:
                    sms = SendSms(tel_no, mail)
                    for fonk in servisler_sms:
                        alt_yazi_sabit()
                        getattr(sms, fonk)()
                        if kere > 0:
                            adet += 1
                            if adet >= kere: break
                        sleep(aralik)
                    if kere > 0 and adet >= kere: break
            else: # Turbo Mod
                send_sms = SendSms(tel_no, mail)
                while True:
                    alt_yazi_sabit()
                    threads = []
                    for fonk in servisler_sms:
                        t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                        threads.append(t)
                        t.start()
                    for t in threads: t.join()
        except KeyboardInterrupt:
            # İşlemi durdurup menüye döner
            ekran_temizle()
            continue

    elif menu == 3:
        ekran_temizle()
        print(Fore.LIGHTRED_EX + "Termux kapatılıyor...")
        # TERMUX'U ANINDA ÖLDÜREN VE PENCEREYİ KAPATAN KOMUT
        os.system("kill -9 $PPID")
        os._exit(0)
