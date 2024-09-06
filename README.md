# BI-PYT-B232

This repository contains a semestral project for the course named Programming in Python at FIT CTU for the summer academic semester of 2023 - 2024. It is a Sokoban remake that also contains a custom level editor and a score calculator. Also included is a [report](./Sokoban___BI_PYT.pdf) for this project in czech.

The history of this repository had to be modified to only contain commits made by me. The original repository was a fork from a repository made by faculty staff that contained commits from a long time ago from previous runs of the course.

Below is the original README content in czech:

# Sokoban

Tento python program implementuje logickou retro video hru, kde hráč posouvá bedny v bludišti na vyznačená místa. Součástí implementace je i editor úrovní a nalezení efektivního řešení pro výpočet skóre (a tedy i splnitelnost úrovně).

## Závislosti

Program využívá balíčků numpy a tkinter a byl testován pomocí pytest a byl použit interpreter Python 3.12.3.

## Spuštení testů

Testy se pouští následujícím příkazem:
`pytest tests.py`

## Spuštění programu a ovládání

Program se spustí pomocí příkazu:
`python main.py`

Po spuštění příkazu se objeví nové okno, které slouží jako hlavní menu hry. Toto menu se ovládá pomocí šipek nahoru a dolu. Resetovat výběr lze pomocí klávesy R. Pro potvrzení výběru slouží klávesa Enter (i na numerické klávesnici). Pro vrácení zpět či případném ukončení programu lze využít klávesy Escape nebo křížek na okně (pokud to GUI operačního systému umožňuje).

Uživatel si pomocí těchto menu může vybrat, zda chce hrát level a který, nebo či chce nějaký level editovat, případně vytvořit nový. Tyto level se nachází ve složce `levels` (nezachází se hloubš).

### Hraní hry

Pokud si uživatel vybere úroveň, kterou chce hrát, program nejdřív zkontroluje, pokud je level hratelný a kolik kroků činí optimální řešení. Pak úroveň zobrazí uživateli.

Samotný hráč se pohybuje pomocí šipek. Level lze předčasně ukončit pomocí Escape. Level lze znovu načíst pomocí klávesy R.

Platí základní pravidla Sokobanu, tedy nelze vstoupit do zdi, nelze posunout krabici do zdi a lze posouvat nanejvýš jednu krabici najednou. Hráč vyhrává, jakmile jsou všechny krabice na označených místech.

Po vyhrání se hráči zobrazí jeho skóre, tedy kolik tahů provedl a kolik tahů má efektivní řešení.

### Editování levelu

Pokud si uživatel vybere úroveň, kterou chce editovat, či začne vytvářet novou, zobrazí se nové okno s touto úrovní.

Uživatel ovládá kurzor (červený čtverec) a pomocí kláves pokládá na kurzor objekty. Pomocí W se položí zeď, pomocí P se položí hráč, pomocí B se položí krabice a pomocí D se položí cíl.

Pokud chce uživatel změnit velikost úrovně, lze tak učinit pomocí klávesy R, načež se zobrazí dvě dialogové okna, kde uživatel zadá požadovanou novou velikost.

Pomocí Escape nebo křížku se pak úroveň ukládá. Pokud uživatel vytvářel novou úroveň, program zobrazí dialogové okno, které se ho zeptá na název úrovně. Pokud uživatel zvolí jiné tlačítko než "OK", ukládání se zruší, jinak se provede.

## Použité úrovně

Level 1, 2 a 3 byly převzaty ze hry Cheese Terminator Reloaded, dostupné zde: https://www.chroscielski.pl/cheese-terminator-reloaded/.

Na ukázku je dostupný i originallevel1, který byl převzat z originální hry od Thinking Rabbit, dostupné zde: https://www.sokobanonline.com/play/web-archive/thinking-rabbit/original/4364_original-1.
