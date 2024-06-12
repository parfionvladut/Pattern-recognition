1.	Enuntarea Problemei:
In acest proiect se doreste a se construi un program care se identifica daca in poza se afla un caine sau o pisica.
2.	Limitari:
•	Antrenarea algoritmului ia destul de mult timp, in special daca este folosit CPU
•	Pentru a scadea timpul de antrenare este necesar un GPU destul de puternic, cu sufficient VRAM, altfel riscam sa nici nu inceapa antrenarea din cauza lipsei de spatiu necesar alocarii.
•	Este nevoie de un dataset pentru antrenare destul de mare pentru a obtine rezultatele dorite.
•	De foarte multe ori trebuie sa validam manual dataset-ul pentru a nu avea informatie eronata.
•	Folosirea unei reetele neuronale convolutionale (CNN) necesita o putere de procesare sporita.
3.	Dataset-ul folosit:
https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip
Datele initiale sunt formate din 23422 de imagini dintre care 18738 sunt folosite pentru antrenare si 4684 sunt folosite pentru testare. In urma eliminarii pozelor corupte si duplicate, s-au pierdut 1590 
