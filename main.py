import random, string, os

def getAllNasabah():
    dataNasabah = []
    fileNasabah = open("nasabah.txt")
    for each_line in fileNasabah:
        if each_line != "\n" or "":
            data = each_line.split(",")
            nomor_rekening = data[0]
            nama_rekening = data[1]
            saldo_rekening = data[2]
            dataNasabah.append([nomor_rekening, nama_rekening, saldo_rekening])
        else:
            continue
    fileNasabah.close()
    return dataNasabah

def getAllTransfer():
    dataTransfer = []
    fileNasabah = open("transfer.txt")
    for each_line in fileNasabah:
        if each_line != "\n" or "":
            data = each_line.split(",")
            nomor_transfer = data[0]
            nomor_rekening_sumber = data[1]
            nomor_rekening_tujuan = data[2]
            nominal_transfer = data[3]
            dataTransfer.append([nomor_transfer, nomor_rekening_sumber, nomor_rekening_tujuan, nominal_transfer])
        else:
            continue
    fileNasabah.close()
    return dataTransfer

def validasiNasabah(no_rek):
    dataAllNasabah = getAllNasabah()
    validasiNasabah = False
    for nasabah in dataAllNasabah:
        if nasabah[0] == no_rek.upper():
            validasiNasabah = True
            break
    return validasiNasabah

def searchNasabah(no_rek):
    dataAllNasabah = getAllNasabah()
    cariNasabah = []
    for nasabah in dataAllNasabah:
        if nasabah[0] == no_rek.upper():
            cariNasabah.extend((nasabah[0],nasabah[1], nasabah[2]))
            break
    return cariNasabah

def kurangiSaldo(no_rek, saldo, dataAllNasabah = getAllNasabah()):
    for i in range(0, len(dataAllNasabah)):
        if dataAllNasabah[i][0] == no_rek.upper():
            # print(dataAllNasabah[i][2])
            dataAllNasabah[i][2] = int(dataAllNasabah[i][2]) - int(saldo)
            # print(dataAllNasabah[i][2])
    return dataAllNasabah

def tambahSaldo(no_rek, saldo, dataAllNasabah = getAllNasabah()):
    for i in range(0, len(dataAllNasabah)):
        if dataAllNasabah[i][0] == no_rek.upper():
            # print(dataAllNasabah[i][2])
            dataAllNasabah[i][2] = int(dataAllNasabah[i][2]) + int(saldo)
            # print(dataAllNasabah[i][2])
    return dataAllNasabah

def prosesTransfer(sumber_rek, tujuan_rek, nominal):
    tempData = kurangiSaldo(sumber_rek, nominal)
    fixedData = tambahSaldo(tujuan_rek, nominal, tempData)
    saveProses(fixedData, 'nasabah.txt')

def saveProses(data, file):
    openFile = open(file, 'w')
    for each_line in data:
        if each_line != "\n":
            dataString = str('{0},{1},{2}\n'.format(each_line[0], each_line[1], each_line[2]))
            openFile.write(dataString)

def main():
    print("--=== SELAMAT DATANG DI NF BANK ===--")
    print("[1] Buka Rekening")
    print("[2] Setoran Tunai")
    print("[3] Tarik Tunai")
    print("[4] Transfer")
    print("[5] Lihat Data Transfer")
    print("[6] Keluar")

    pilihan = int(input("Masukan Menu pilihan anda : "))
    if pilihan == 1:
        bukaRekening()
    elif pilihan == 2:
        setorTunai()
    elif pilihan == 3:
        tarikTunai()
    elif pilihan == 4:
        transfer()
    elif pilihan == 5:
        lihatDataTransfer()
    elif pilihan == 6:
        print("Terima kasih atas kunjungan anda...")

def bukaRekening():
    print("--=== Buka Rekening ===--")
    nomor_rekening = "REK" + ''.join(random.choice(string.digits) for _ in range(3))
    nama_rekening = input("Masukan nama anda disini : ")
    saldo_awal = int(input("Masukan saldo awal : "))
    if os.path.isfile("nasabah.txt"): #mengecek apakah file nasabah.txt ada atau tidak
        newData = open("nasabah.txt", "a+") #bila ada akan menggunakan metode append menambah data
    else:
        newData = open("nasabah.txt", "w") #bila tidak ada akan menggunakan metode overwrite
    stringNasabah = str('{0},{1},{2}\n'.format(nomor_rekening, nama_rekening, saldo_awal))
    newData.write(stringNasabah)
    newData.close()
    print("Rekening atas nama", nama_rekening, " berhasil dibuka!")

def setorTunai():
    nomor_rekening = input("masukan nomor rekening : ")
    nominal = int(input("masukan nominal : "))
    validasi = validasiNasabah(nomor_rekening)
    if validasi:
        data_nasabah = getAllNasabah()
        for i in range(0,len(data_nasabah)):
            if data_nasabah[i][0] == nomor_rekening.upper():
                data_nasabah[i][2] = int(data_nasabah[i][2]) + nominal
                saveProses(data_nasabah, 'nasabah.txt')
                print("Setor tunai sebesar", nominal, " dengan nomor rekening", nomor_rekening.upper(), " Berhasil!")
                break
            else:
                continue
    else:
        print("Gagal Setor Tunai! - Rekening tidak terdaftar!")

 
def tarikTunai():
    nomor_rekening = input("masukan nomor rekening : ")
    nominal = int(input("masukan nominal : "))
    validasi = validasiNasabah(nomor_rekening)
    if validasi:
        data_nasabah = getAllNasabah()
        for i in range(0,len(data_nasabah)):
            if data_nasabah[i][0] == nomor_rekening.upper():
                if int(data_nasabah[i][2]) < nominal :
                    print("Gagal tarik tunai! - Saldo tidak mencukupi.")
                    break
                elif int(data_nasabah[i][2]) >= nominal:
                    data_nasabah[i][2] = int(data_nasabah[i][2]) - nominal
                    saveProses(data_nasabah, 'nasabah.txt')
                    print("Tarik tunai sebesar", nominal, " dengan nomor rekening", nomor_rekening.upper(), " Berhasil!")
                    break
            else:
                continue
    else:
        print("Gagal Tarik Tunai! - Rekening tidak terdaftar!")

def transfer():
    nomor_trf = "TRF" + ''.join(random.choice(string.digits) for _ in range(3))
    no_rekening_sumber = input("Masukan nomor rekening sumber : ")
    dataRekeningSumber = searchNasabah(no_rekening_sumber)
    no_rekening_tujuan = input("Masukan nomor rekening tujuan : ")
    dataRekeningTujuan = searchNasabah(no_rekening_tujuan)
    if dataRekeningSumber:    
        if dataRekeningTujuan:
            nominalTransfer = int(input("Masukan Nominal Transfer : "))
            if nominalTransfer <= int(dataRekeningSumber[2]):
                dataTransfer = str('{0},{1},{2},{3}\n'.format(nomor_trf, no_rekening_sumber, no_rekening_tujuan, nominalTransfer))
                checkFileExist = os.path.isfile("transfer.txt")
                if checkFileExist: #mengecek apakah file transfer.txt ada atau tidak
                    newData = open("transfer.txt", "a+") #bila ada akan menggunakan metode append menambah data
                else:
                    newData = open("transfer.txt", "w") #bila tidak ada akan menggunakan metode overwrite
                newData.write(dataTransfer)
                newData.close()
                prosesTransfer(no_rekening_sumber, no_rekening_tujuan, nominalTransfer)
                print("Transfer Sebesar : ", nominalTransfer, " dari rekening : ", dataRekeningSumber[0], " ke rekening ", dataRekeningTujuan[0]," berhasil !")
            elif nominalTransfer > int(dataRekeningSumber[2]):
                print("Gagal Transfer! - Saldo Nomor Rekening Sumber tidak mencukupi.")
        else:
            print("Gagal Transfer! - Nomor Rekening Tujuan tidak terdaftar.")
    else:
        print("Gagal Transfer! - Nomor Rekening Sumber tidak terdaftar.")
    
    

def lihatDataTransfer():
    nomor_rekening = input("masukan No Rekening : ").upper()
    Validasi = validasiNasabah(nomor_rekening)
    if Validasi : 
        Data_Transfer = getAllTransfer()
        dataTransferSumber = []
        for i in Data_Transfer : 
            if i[1] == nomor_rekening : 
                dataTransferSumber.append(i)
            else:
                continue
        if len(dataTransferSumber) == 0:
            print("Data Transfer Kosong!")
        else:
            for i in dataTransferSumber:
               print("{0} {1} {2} {3}\n".format(i[0], i[1],i[2],i[3]))
    else:
        print("Lihat data transfer gagal! - Nomor rekening tidak terdaftar!")

if __name__ == "__main__":
    main()
    