"""Convierte tp2.2026.xlsx (formato ancho: una fila por mes, una columna por
producto) a demanda.csv (formato largo: mes,producto,demanda), que es el
formato que ZIMPL puede leer directamente con `read ... as "<1n,2s> 3n"`.

No depende de librerias externas (solo stdlib) para poder correrlo en
cualquier maquina sin instalar pandas/openpyxl.
"""
import csv
import re
import zipfile
import xml.etree.ElementTree as ET

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ORIGEN = "tp2.2026.xlsx"
DESTINO = "demanda.csv"


def leer_hoja(path):
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sst.findall("a:si", NS):
                shared.append("".join(t.text or "" for t in si.findall(".//a:t", NS)))
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))

    filas = []
    for row in sheet.findall(".//a:row", NS):
        celdas = {}
        for c in row.findall("a:c", NS):
            col = re.match(r"[A-Z]+", c.get("r")).group()
            v = c.find("a:v", NS)
            val = v.text if v is not None else None
            if c.get("t") == "s" and val is not None:
                val = shared[int(val)]
            celdas[col] = val
        filas.append(celdas)
    return filas


def main():
    filas = leer_hoja(ORIGEN)
    encabezado, *datos = filas

    # Columna -> producto, a partir del encabezado ("Producto A" -> "A")
    columnas_producto = {
        col: valor.strip().split()[-1]
        for col, valor in encabezado.items()
        if col != "A" and valor
    }

    with open(DESTINO, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["mes", "producto", "demanda"])
        for t, fila in enumerate(datos, start=1):
            for col, producto in sorted(columnas_producto.items()):
                w.writerow([t, producto, int(fila[col])])

    print(f"{DESTINO} generado a partir de {ORIGEN} ({len(datos)} meses, "
          f"{len(columnas_producto)} productos).")


if __name__ == "__main__":
    main()
