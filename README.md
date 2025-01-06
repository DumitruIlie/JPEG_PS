# Tema Procesarea semnalelor

## Descriere

Tema prezinta o versiune incompleta de codificare JPEG, un mod de stocare al acesteia pe disc, citirea imaginii codificate si randarea acesteia. Programul permite lucrul cu imagini alb-negru cat si color. Mai jos gasiti un mic ghid de utilizare si in repo gasiti cateva poze in format `.png` pe care puteti incerca sa le convertiti. Efectele cele mai mari se observa atunci cand parametrul de calitate este setat la 1.

**Mentiuni**:

* Stocarea pe disc nu este de loc standard. Nu cred ca exista vreun program de vizualizare in afara celui pe care l-am scris care ar putea citi fisierul final.
* Mare parte din cod este scris in decursul unei singure zile (05.01.2025). Nu este foarte optimizat sau usor de inteles. Scuze.
* Comentariile sunt la misto sau deloc. Scuze.
* Scriu cod foarte urat. Scuze.
* Am folosit parte din ce a trimis Negrescu Theodor pe grupul de Teams. Din cate stiu doar fisierul `utils.py` contine cod scris de acesta si eventual cu mici modificari personale. Am pastrat de asemenea un fisier care contine tot codul trimis de el (`de_la_Theodor.py`).

## Ghid folosire

Pentru a convertii si randa o imagine urmati acesti 3 pasi.

1. Conversie in fisier text. Acest pas este doar pentru convenienta dezvoltatorului. Imi cer scuze pentru inconvenientele create utilizatorilor.

```Bash
python3 bmp2txt.py %path_imagine% > %path_fisier_intermediar%
```

2. Codare si stocare pe disc a imaginii.

```Bash
python3 encode.py %path_fisier_intermediar% <-Q %calitate%> <-O %path_imagine_format_propriu%>
```

Daca lipseste parametrul `calitate`, aceasta va fi implicit setat la 50.

Daca lipseste parametrul `path_imagine_format_propriu` atunci fisierul unde formatul propriu va fi stocat este `img.myjpeg`.

3. Decodarea si randarea imaginii.

```Bash
python3 decode.py %path_imagine_format_propriu%
```

### Exemplu de folosire

```Bash
python3 bmp2txt.py jpeg_wiki.png > jpeg_wiki.txt
python3 encode.py jpeg_wiki.txt -O jpeg_wiki.myjpeg -Q 1
python3 decode.py jpeg_wiki.myjpeg
```

### Resurse folosite

* [Wiki Y'CbCr](https://en.wikipedia.org/wiki/YCbCr)
* [Playlist care explica JPEG](https://www.youtube.com/watch?v=CPT4FSkFUgs&list=PLpsTn9TA_Q8VMDyOPrDKmSJYt1DLgDZU4&index=1&t=0s)
* [Conversie sir de biti in sir de bytes](https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3)
* [Stocare pe disc a unui arbore Huffman](https://stackoverflow.com/questions/72550738/how-to-store-huffman-tree-in-file)
