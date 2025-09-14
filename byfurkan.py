from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms  # SendSms sınıfının mevcut olduğunu varsayıyorum
from concurrent.futures import ThreadPoolExecutor, wait

# SendSms sınıfındaki tüm SMS gönderme servislerini dinamik olarak toplama
def get_sms_services(sms_class):
    services = []
    for attribute in dir(sms_class):
        # '__' ile başlamayan ve çağrılabilir (metod) olanları al
        if callable(getattr(sms_class, attribute)) and not attribute.startswith('__'):
            services.append(attribute)
    return services

servisler_sms = get_sms_services(SendSms)

def clear_screen():
    """Ekranı temizler."""
    system("cls||clear")

def display_main_menu(num_services):
    """Ana menüyü ve ASCII art'ı gösterir."""
    clear_screen()
    print(f"""{Fore.LIGHTCYAN_EX}
    ,        ,
              /(        )`
              \ \___   / |
              /- _  `-/  '
             (/\/ \ \   /\    
             / /   | `    \
             O O   ) /    |
             `-^--'`<     '
            (_.)  _ )    /
             `.___/`/    /
               `-----' /
  <----.     __ / __   \
  <----|====O)))==) \) /====
  <----'    `--' `.__,' \    
    Sms: {num_services}{Style.RESET_ALL}           {Fore.LIGHTRED_EX}coder @mustafa.enes23
    """)
    print(Fore.LIGHTMAGENTA_EX + " 1- SMS Gönder (Normal)\n")
    print(" 2- SMS Gönder (Turbo😈)\n")
    print(" 3- Çıkış\n")
    return input(Fore.LIGHTYELLOW_EX + " Seçim: ")

def get_user_input(prompt, input_type=str, error_message="Hatalı giriş yaptın. Tekrar deneyiniz."):
    """Kullanıcıdan belirli bir türde giriş alır ve hata kontrolü yapar."""
    while True:
        try:
            print(prompt, end="")
            user_input = input(Fore.LIGHTGREEN_EX)
            if input_type == int:
                return int(user_input) if user_input else None  # Boşsa None döndür
            elif input_type == str:
                return user_input
            return input_type(user_input)
        except ValueError:
            clear_screen()
            print(Fore.LIGHTRED_EX + error_message)
            sleep(2)  # Hata mesajını daha kısa tuttum
            clear_screen() # Tekrar denemeden önce ekranı temizle
            continue
        except Exception: # Mail kontrolü için eklenen catch bloğu
            clear_screen()
            print(Fore.LIGHTRED_EX + error_message)
            sleep(2)
            clear_screen()
            continue

def validate_phone_number(phone_num):
    """Telefon numarasını doğrular."""
    try:
        int(phone_num)
        return len(phone_num) == 10
    except ValueError:
        return False

def validate_email(email):
    """Mail adresini doğrular."""
    return ("@" in email and ".com" in email) or email == ""

def normal_sms_sender():
    """Normal SMS gönderme modunu çalıştırır."""
    clear_screen()
    tel_no_input = get_user_input(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız (Birden çoksa 'enter' tuşuna basınız): ", str)
    
    tel_liste = []
    if tel_no_input == "":
        dizin = get_user_input(Fore.LIGHTYELLOW_EX + "Telefon numaralarının kayıtlı olduğu dosyanın dizinini yazınız: ", str)
        try:
            with open(dizin, "r", encoding="utf-8") as f:
                for num in f.read().strip().split("\n"):
                    if validate_phone_number(num):
                        tel_liste.append(num)
                if not tel_liste: # Dosyada geçerli numara yoksa
                    clear_screen()
                    print(Fore.LIGHTRED_EX + "Dosyada geçerli telefon numarası bulunamadı.")
                    sleep(2)
                    return
            sonsuz_mesaj = ""
        except FileNotFoundError:
            clear_screen()
            print(Fore.LIGHTRED_EX + "Hatalı dosya dizini. Tekrar deneyiniz.")
            sleep(2)
            return
    else:
        if validate_phone_number(tel_no_input):
            tel_liste.append(tel_no_input)
            sonsuz_mesaj = "(Sonsuz ise 'enter' tuşuna basınız)"
        else:
            clear_screen()
            print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.") 
            sleep(2)
            return

    clear_screen()
    mail = get_user_input(Fore.LIGHTYELLOW_EX + "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): ", str)
    if not validate_email(mail):
        clear_screen()
        print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.") 
        sleep(2)
        return

    clear_screen()
    kere = get_user_input(Fore.LIGHTYELLOW_EX + f"Kaç adet SMS göndermek istiyorsun {sonsuz_mesaj}: ", int)
    
    clear_screen()
    aralik = get_user_input(Fore.LIGHTYELLOW_EX + "Kaç saniye aralıkla göndermek istiyorsun: ", int)
    if aralik is None: # aralık boş bırakılırsa varsayılan değer atama
        aralik = 1 

    clear_screen()
    for tel in tel_liste:
        sms_instance = SendSms(tel, mail)
        
        if kere is None: # Sonsuz döngü
            print(Fore.LIGHTYELLOW_EX + f"{tel} numarasına sonsuz SMS gönderiliyor. Çıkış için Ctrl+C.")
            try:
                while True:
                    for service_name in servisler_sms:
                        getattr(sms_instance, service_name)()
                        sleep(aralik)
            except KeyboardInterrupt:
                print(Fore.LIGHTRED_EX + "\nSMS gönderme durduruldu.")
        else: # Belirli sayıda döngü
            print(Fore.LIGHTYELLOW_EX + f"{tel} numarasına {kere} adet SMS gönderiliyor...")
            count = 0
            while count < kere:
                for service_name in servisler_sms:
                    if count == kere:
                        break
                    try:
                        getattr(sms_instance, service_name)()
                        count += 1
                        sleep(aralik)
                    except Exception as e:
                        print(Fore.LIGHTRED_EX + f"Hata oluştu ({service_name}): {e}")
            print(Fore.LIGHTGREEN_EX + f"{tel} numarasına {kere} adet SMS gönderme tamamlandı.")

    print(Fore.LIGHTRED_EX + "\nMenüye dönmek için 'enter' tuşuna basınız..")
    input()

def turbo_sms_sender():
    """Turbo SMS gönderme modunu çalıştırır."""
    clear_screen()
    tel_no = get_user_input(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız: ", str)
    if not validate_phone_number(tel_no):
        clear_screen()
        print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.") 
        sleep(2)
        return

    clear_screen()
    mail = get_user_input(Fore.LIGHTYELLOW_EX + "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): ", str)
    if not validate_email(mail):
        clear_screen()
        print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.") 
        sleep(2)
        return

    clear_screen()
    print(Fore.LIGHTYELLOW_EX + f"SMS'ler {tel_no} numarasına turbo modda gönderiliyor. Çıkış için Ctrl+C.")
    send_sms_instance = SendSms(tel_no, mail)
    try:
        while True:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(getattr(send_sms_instance, service_name)) for service_name in servisler_sms]
                wait(futures)
    except KeyboardInterrupt:
        clear_screen()
        print(Fore.LIGHTRED_EX + "\nCtrl+C tuş kombinasyonu algılandı. Menüye dönülüyor..")
        sleep(2)

# Ana döngü
while True:
    secim = display_main_menu(len(servisler_sms))
    
    try:
        secim = int(secim)
    except ValueError:
        clear_screen()
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
        sleep(2)
        continue

    if secim == 1:
        normal_sms_sender()
    elif secim == 2:
        turbo_sms_sender()
    elif secim == 3:
        clear_screen()
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        sleep(1) # Daha hızlı çıkış
        break
    else:
        clear_screen()
        print(Fore.LIGHTRED_EX + "Geçersiz seçim. Tekrar deneyiniz.")
        sleep(2)

