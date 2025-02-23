import json
from abc import ABC, abstractmethod


class Person:
    def __init__(self, ism, telefon):
        self.ism = ism
        self.telefon = telefon

    def __str__(self):
        return f"{self.ism} ({self.telefon})"


class Transport(ABC):
    def __init__(self, davlat_raqami, egasi):
        self._davlat_raqami = davlat_raqami
        self._egasi = egasi

    @abstractmethod
    def transport_turi(self):
        pass

    def get_davlat_raqami(self):
        return self._davlat_raqami

    def get_egasi(self):
        return self._egasi


class Mashina(Transport):
    def transport_turi(self):
        return "Mashina"


class Motosikl(Transport):
    def transport_turi(self):
        return "Motosikl"


class Yuk_Mashina(Transport):
    def transport_turi(self):
        return "Yuk mashina"


class Avtoturargoh:
    def __init__(self, sigim):
        self.sigim = sigim
        self.saqlangan_transportlar = []
        self.malumot_yuklash()

    def transport_qoshish(self, transport):
        if len(self.saqlangan_transportlar) < self.sigim:
            self.saqlangan_transportlar.append(transport)
            self.malumot_saqlash()
            print(f"{transport.transport_turi()} ({transport.get_davlat_raqami()}) muvaffaqiyatli qo'shildi.")
        else:
            print("Avtoturargoh to'la!")

    def transport_ochirish(self, davlat_raqami):
        yangi_transportlar = [t for t in self.saqlangan_transportlar if t.get_davlat_raqami() != davlat_raqami]
        if len(yangi_transportlar) < len(self.saqlangan_transportlar):
            self.saqlangan_transportlar = yangi_transportlar
            self.malumot_saqlash()
            print(f"Transport {davlat_raqami} avtoturargohdan olib tashlandi.")
        else:
            print("Transport topilmadi!")

    def transport_royxati(self):
        if not self.saqlangan_transportlar:
            print("Avtoturargoh bo'sh.")
        else:
            for transport in self.saqlangan_transportlar:
                print(f"{transport.transport_turi()} - {transport.get_davlat_raqami()} - {transport.get_egasi()}")

    def malumot_saqlash(self):
        malumot = [
            {"turi": t.transport_turi(), "raqami": t.get_davlat_raqami(), "egasi": {"ism": t.get_egasi().ism, "telefon": t.get_egasi().telefon}}
            for t in self.saqlangan_transportlar
        ]
        with open("avtoturargoh_malumot.json", "w") as file:
            json.dump(malumot, file)

    def malumot_yuklash(self):
        try:
            with open("avtoturargoh_malumot.json", "r") as f:
                malumot = json.load(f)
                self.saqlangan_transportlar = []  # Tozalash
                for t in malumot:
                    if isinstance(t["egasi"], dict):  # Egasi dictionary ekanligini tekshiramiz
                        egasi = Person(t["egasi"]["ism"], t["egasi"]["telefon"])
                    else:
                        print(f"Xatolik: Noto'g'ri egasi formati: {t['egasi']}")
                        continue  # Xato bo'lsa, uni o'tkazib yuboramiz

                    if t["turi"] == "Mashina":
                        self.saqlangan_transportlar.append(Mashina(t["raqami"], egasi))
                    elif t["turi"] == "Motosikl":
                        self.saqlangan_transportlar.append(Motosikl(t["raqami"], egasi))
                    elif t["turi"] == "Yuk mashina":
                        self.saqlangan_transportlar.append(Yuk_Mashina(t["raqami"], egasi))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Xatolik: {e}")


if __name__ == "__main__":
    avtoturargoh = Avtoturargoh(5)
    while True:
        print("\n--- Avtoturargoh boshqaruv tizimi ---")
        print("1. Transport qo'shish")
        print("2. Transport o'chirish")
        print("3. Transport ro'yxatini ko'rish")
        print("4. Chiqish")
        tanlov = input("Tanlovingizni kiriting: ")

        if tanlov == "1":
            turi = input("Transport turi (Mashina/Motosikl/Yuk mashina): ")
            raqam = input("Davlat raqami: ")
            ism = input("Egasi ismi: ")
            telefon = input("Egasi telefon raqami: ")
            egasi = Person(ism, telefon)
            if turi.lower() == "mashina":
                avtoturargoh.transport_qoshish(Mashina(raqam, egasi))
            elif turi.lower() == "motosikl":
                avtoturargoh.transport_qoshish(Motosikl(raqam, egasi))
            elif turi.lower() == "yuk mashina":
                avtoturargoh.transport_qoshish(Yuk_Mashina(raqam, egasi))
            else:
                print("Noto'g'ri transport turi!")

        elif tanlov == "2":
            raqam = input("O'chirmoqchi bo'lgan transport raqamini kiriting: ")
            avtoturargoh.transport_ochirish(raqam)

        elif tanlov == "3":
            avtoturargoh.transport_royxati()

        elif tanlov == "4":
            print("Dasturdan chiqildi.")
            break

        else:
            print("Noto'g'ri tanlov, qayta urinib ko'ring!")
