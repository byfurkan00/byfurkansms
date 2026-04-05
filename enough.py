from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading
import shutil

servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value):
        if not attribute.startswith('__'):
            servisler_sms.append(attribute)

def durdurma_uyarisi():
    print(Fore.LIGHTRED_EX + "--------------------------------------------------------------")
    print(" PROGRAMI DURDURMAK VEYA MENÜYE DONMEK ICIN: CTRL + C BASINIZ.")
    print("--------------------------------------------------------------" + Style.RESET_ALL)

def sabit_footer():
    cols, lines = shutil.get_terminal_size()
    # İmleci en alt satıra taşır, uyarıyı yazar ve imleci eski yerine (yukarı) almaz
    # Bu sayede yazılar aksa da bu satır en dipte kalır
    print(f"\033[{lines};0H\033[1;31m PROGRAMI DURDURMAK VEYA   MENUYE DONMEK ICIN: CTRL + C BASINIZ.\033[0m", end="", flush=True)

while True:
    system("cls||clear")

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
        menu = input(
            Fore.LIGHTMAGENTA_EX
            + " 1- SMS Gönder (Normal😼)\n\n 2- SMS Gönder (Turbo😈)\n\n 3- Çıkış\n\n"
            + Fore.LIGHTYELLOW_EX
            + " Seçim: "
        )
        if menu.strip() == "":
            continue
        menu = int(menu)
    except ValueError:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
        sleep(3)
        continue

    if menu == 1:
        system("cls||clear")
        durdurma_uyarisi()
        print(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız: " + Fore.LIGHTGREEN_EX, end="")
        tel_no = input().strip()
        tel_liste = []

        if tel_no == "":
            system("cls||clear")
            durdurma_uyarisi()
            print(Fore.LIGHTYELLOW_EX + "Dosya dizinini yazınız: " + Fore.LIGHTGREEN_EX, end="")
            dizin = input().strip()
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    for i in f.read().strip().splitlines():
                        i = i.strip()
                        if len(i) == 10 and i.isdigit():
                            tel_liste.append(i)
            except FileNotFoundError:
                continue
        else:
            tel_liste.append(tel_no)

        system("cls||clear")
        durdurma_uyarisi()
        print(Fore.LIGHTYELLOW_EX + "Mail adresi (opsiyonel): " + Fore.LIGHTGREEN_EX, end="")
        mail = input().strip()

        system("cls||clear")
        durdurma_uyarisi()
        print(Fore.LIGHTYELLOW_EX + "Kaç adet SMS: " + Fore.LIGHTGREEN_EX, end="")
        kere = input().strip()
        kere = int(kere) if kere else None

        system("cls||clear")
        durdurma_uyarisi()
        print(Fore.LIGHTYELLOW_EX + "Saniye aralığı: " + Fore.LIGHTGREEN_EX, end="")
        aralik = int(input().strip())

        system("cls||clear")
        # Alt satırı sabitlemek için terminale kaydırma alanı sınırı koyuyoruz
        cols, lines = shutil.get_terminal_size()
        print(f"\033[0;{lines-1}r", end="") 

        try:
            while True:
                for i in tel_liste:
                    sms = SendSms(i, mail)
                    for fonk in servisler_sms:
                        sabit_footer()
                        # İmleci tekrar yazı alanına (en başa) gönder
                        print("\033[H", end="")
                        try:
                            getattr(sms, fonk)()
                        except: pass
                        sleep(aralik)
                if kere is not None: break
        except KeyboardInterrupt:
            print("\033[r") # Kaydırma alanını sıfırla
            continue

    elif menu == 3:
        system("cls||clear")
        break

    elif menu == 2:
        system("cls||clear")
        durdurma_uyarisi()
        print(Fore.LIGHTYELLOW_EX + "Telefon no: " + Fore.LIGHTGREEN_EX, end="")
        tel_no = input().strip()
        
        system("cls||clear")
        durdurma_uyarisi()
        print(Fore.LIGHTYELLOW_EX + "Mail adresi: " + Fore.LIGHTGREEN_EX, end="")
        mail = input().strip()

        system("cls||clear")
        cols, lines = shutil.get_terminal_size()
        print(f"\033[0;{lines-1}r", end="") 
        
        send_sms = SendSms(tel_no, mail)
        dur = threading.Event()

        def Turbo():
            while not dur.is_set():
                sabit_footer()
                print("\033[H", end="")
                thread_list = []
                for fonk in servisler_sms:
                    t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                    thread_list.append(t)
                    t.start()
                for t in thread_list:
                    t.join()

        try:
            Turbo()
        except KeyboardInterrupt:
            dur.set()
            print("\033[r")
            continue

    else:
        continue
        
