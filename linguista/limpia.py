# -*- coding: utf-8 -*-


def main():
    fe = open("./datos/silabas.txt", "r")
    fs = open("./datos/silabaslimpio.txt", "w")
    lon = 0
    for line in fe:
        linea = line.split("|")
        linea = linea[0].replace(" ", "")
        fs.write("{}\n".format(linea))
        le = len(linea)
        if lon < le:
            lon = le
    print(lon)


if __name__ == "__main__":
    main()
