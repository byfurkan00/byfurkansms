from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading
import shutil
import sys
import os
import signal

# Servisleri hazırla
servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

# --- Ekran Ayarları ---
def alt_yazi_sabit():
    cols, lines = shutil.get_terminal_size()
    sys.stdout.write(f"\033[0;{lines-1}r")
    sys.stdout.write(f"\033[{lines};0H\033[1;31m DURDUR VE MENUYE DON: CTRL + C \033[0m")
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def ekran_temizle():
    sys.stdout.write("\033[r\033[H\033[J")
    sys.stdout.flush()

# --- CTRL + C Bastığın An Her Şeyi Keser ---
def sinyal_isleyici(sig, frame):
    ekran_temizle()
    raise KeyboardInterrupt

signal.signal(signal.SIGINT, sinyal_isleyici)

while True:
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
        menu = input(Fore.LIGHTMAGENTA_EX + " 1- SMS Gönder (Normal)\n\n 2- SMS Gönder (Turbo)\n\n 3- Termuxu Kapat\n\n" + Fore.LIGHTYELLOW_EX + " Seçim: ")
        if not menu: continue
        menu = int(menu)
    except KeyboardInterrupt:
        # Menüde CTRL+C yapılırsa terminale çıkış menüsü tetiklenir
        print("\nÇıkış yapılıyor...")
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
            else: # TURBO MOD
                send_sms = SendSms(tel_no, mail)
                while True: 
                    alt_yazi_sabit()
                    threads = []
                    for fonk in servisler_sms:
                        t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                        threads.append(t)
                        t.start()
                    # Thread'lerin bitmesini bekle ama CTRL+C'ye duyarlı kal
                    for t in threads:
                        while t.is_alive():
                            t.join(timeout=0.1)
        except KeyboardInterrupt:
            # Durdurulduğu an buraya düşer ve ekranı temizleyip menüye döner
            ekran_temizle()
            continue 

    elif menu == 3:
        ekran_temizle()
        print(Fore.LIGHTRED_EX + "Kapatılıyor...")
        os._exit(0)
        
