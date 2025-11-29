from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading

servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value):
        if not attribute.startswith('__'):
            servisler_sms.append(attribute)

while True:
    system("cls||clear")

    # ASCII çizimini raw string ile koyuyoruz, böylece \ ve ` gibi karakterler sorun çıkarmaz
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
        print(
            Fore.LIGHTYELLOW_EX
            + "Telefon numarasını başında '+90' olmadan yazınız (Birden çoksa 'enter' tuşuna basınız): "
            + Fore.LIGHTGREEN_EX,
            end="",
        )
        tel_no = input().strip()
        tel_liste = []

        if tel_no == "":
            system("cls||clear")
            print(
                Fore.LIGHTYELLOW_EX
                + "Telefon numaralarının kayıtlı olduğu dosyanın dizinini yazınız: "
                + Fore.LIGHTGREEN_EX,
                end="",
            )
            dizin = input().strip()
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    for i in f.read().strip().splitlines():
                        i = i.strip()
                        if len(i) == 10 and i.isdigit():
                            tel_liste.append(i)
                if not tel_liste:
                    system("cls||clear")
                    print(Fore.LIGHTRED_EX + "Dosyada geçerli telefon numarası bulunamadı.")
                    sleep(2)
                    continue
                sonsuz = ""
            except FileNotFoundError:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Hatalı dosya dizini. Tekrar deneyiniz.")
                sleep(3)
                continue
        else:
            try:
                if not tel_no.isdigit() or len(tel_no) != 10:
                    raise ValueError
                tel_liste.append(tel_no)
                sonsuz = "(Sonsuz ise 'enter' tuşuna basınız)"
            except ValueError:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.")
                sleep(3)
                continue

        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "('enter' tuşuna basın): " + Fore.LIGHTGREEN_EX, end="")
            mail = input().strip()
            if mail != "" and ("@" not in mail or ".com" not in mail):
                raise ValueError
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.")
            sleep(3)
            continue

        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + f"Kaç adet SMS göndermek istiyorsun {sonsuz}: " + Fore.LIGHTGREEN_EX, end="")
            kere = input().strip()
            if kere:
                kere = int(kere)
                if kere <= 0:
                    raise ValueError
            else:
                kere = None
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
            sleep(3)
            continue

        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "Kaç saniye aralıkla göndermek istiyorsun: " + Fore.LIGHTGREEN_EX, end="")
            aralik = int(input().strip())
            if aralik < 0:
                raise ValueError
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
            sleep(3)
            continue

        system("cls||clear")

        # Gönderme mantığı:
        # - tel_liste içindeki her numara için SendSms örneği oluşturup servisleri çalıştıracağız.
        # - kere is None ise sonsuz döngü; aksi halde her numara için kere adet gönderim yapılacak.
        try:
            if kere is None:
                # Sonsuz mod: her numara için sürekli döngü
                while True:
                    for i in tel_liste:
                        sms = SendSms(i, mail)
                        for fonk in servisler_sms:
                            try:
                                getattr(sms, fonk)()
                            except Exception:
                                # Servis hata verirse atla
                                pass
                            sleep(aralik)
            else:
                # Belirli adette gönderim
                for i in tel_liste:
                    sms = SendSms(i, mail)
                    # Eğer SendSms sınıfında 'adet' isimli bir sayaç varsa onu kullan. Yoksa biz manuel sayalım.
                    adet_sayaci = 0
                    while adet_sayaci < kere:
                        for fonk in servisler_sms:
                            if adet_sayaci >= kere:
                                break
                            try:
                                getattr(sms, fonk)()
                            except Exception:
                                pass
                            adet_sayaci += 1
                            sleep(aralik)
        except KeyboardInterrupt:
            system("cls||clear")
            print("\nGönderim iptal edildi. Menüye dönülüyor..")
            sleep(2)
            continue

        print(Fore.LIGHTRED_EX + "\nMenüye dönmek için 'enter' tuşuna basınız..")
        input()

    elif menu == 3:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        break

    elif menu == 2:
        system("cls||clear")
        print(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız: " + Fore.LIGHTGREEN_EX, end="")
        tel_no = input().strip()
        try:
            if not tel_no.isdigit() or len(tel_no) != 10:
                raise ValueError
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.")
            sleep(3)
            continue

        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "('enter' tuşuna basın): " + Fore.LIGHTGREEN_EX, end="")
            mail = input().strip()
            if mail != "" and ("@" not in mail or ".com" not in mail):
                raise ValueError
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.")
            sleep(3)
            continue

        system("cls||clear")
        send_sms = SendSms(tel_no, mail)
        dur = threading.Event()

        def Turbo():
            while not dur.is_set():
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
            system("cls||clear")
            print("\nCtrl+C tuş kombinasyonu algılandı. Menüye dönülüyor..")
            sleep(2)
            continue

    else:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Geçersiz seçim. Tekrar deneyiniz.")
        sleep(2)
        continue
