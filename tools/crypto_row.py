"""Печатает готовый HTML-блок криптостроки для docs/donate.html.

QR-код вшит в страницу инлайновым SVG, руками его не собрать — поэтому новую
монету добавляем через этот скрипт, а вывод вставляем в карточку "Криптовалюта"
(последним блоком .entry).

    pip install segno
    py tools/crypto_row.py doge "Ð" Dogecoin Mainnet D8vFz4p1L37jdg47...

Аргументы: id символ монета сеть адрес
  id     — латиницей, попадёт в id="qr-<id>", должен быть уникальным на странице
  сеть   — то, что видно в кошельке: Mainnet, "TRC-20 · Tron", "BEP-20 · BNB Chain"

Адрес перед вставкой стоит сверить: скрипт печатает его же в data-copy и в
QR, но правильность самого адреса он не проверяет.
"""
import html
import sys

import segno

TEMPLATE = '''      <div class="entry">
        <div class="method">
          <span class="glyph">{glyph}</span>
          <span class="body">
            <span class="label">{coin} <span class="net">{net}</span></span>
            <span class="value mono">{addr}</span>
          </span>
          <span class="tools">
            <button type="button" class="copy" data-copy="{addr}"></button>
            <button type="button" class="qr-toggle" data-qr="qr-{cid}"
                    aria-expanded="false" aria-controls="qr-{cid}">QR</button>
          </span>
        </div>
        <div class="qr" id="qr-{cid}" hidden>{svg}</div>
      </div>'''


def row(cid, glyph, coin, net, addr):
    # Параметры QR обязаны совпадать с уже вставленными кодами, иначе строки
    # будут выглядеть по-разному.
    svg = segno.make(addr, error='m').svg_inline(
        scale=1, border=2, dark='#0F141B', light='#FFFFFF', omitsize=True)
    esc = html.escape(addr)
    return TEMPLATE.format(glyph=glyph, coin=html.escape(coin),
                           net=html.escape(net), addr=esc, cid=cid, svg=svg)


if __name__ == '__main__':
    # Консоль Windows по умолчанию не cp1251-совместима с ₿/Ξ/Ð — форсируем UTF-8.
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(1)
    print(row(*sys.argv[1:]))
