# -*- coding: utf-8 -*-
"""블록마다 영역(슬롯) 좌표를 돌려준다 — 블록 왼쪽 위 기준 px. 레이아웃 상세 페이지의 가이드와 좌표 표에 쓴다."""
from blocks import *


def _ladder(self, W):
    wl = self._wc(W); H = self.height(W); out = [('사다리 표 외곽', 0, 0, wl, H)]
    yy = 3
    for i, r in enumerate(self.rows):
        rh = self.row_h(r, W)
        out.append((f'레일 {i + 1} · {r["label"].replace(chr(10), " ")}', 2, yy, self.rail, rh))
        xc, xr = self.rail + 8, wl - 5; by = yy + 4
        for b in r['bands']:
            bh = band_h(b, xr - xc)
            out.append((f'띠 {i + 1} · {b["k"]}', xc, by, xr - xc, bh)); by += bh + 3
        yy += rh + 3
    if self.side:
        out.append(('성과 사이드 패널', wl + 36, 0, W - wl - 36, H))
    if self.photos:
        ys = []; yy = 3
        for r in self.rows:
            ys.append((yy, self.row_h(r, W))); yy += self.row_h(r, W) + 3
        for k, ph in enumerate(self.photos):
            i0, i1 = ph['rows']
            out.append((f'사진 열 {k + 1}', wl + 8, ys[i0][0], W - wl - 8, ys[i1][0] + ys[i1][1] - ys[i0][0]))
    return out


def _label_rows(self, W):
    out = []; yy = 0
    for i, r in enumerate(self.rows):
        h = self.row_h(r, W)
        out.append((f'행 {i + 1} 라벨 · {r["label"]}', 0, yy, self.label_w, h))
        out.append((f'행 {i + 1} 내용 · {r["k"]}', self.label_w + 6, yy, W - self.label_w - 12, h)); yy += h + self.rgap
    return out


def _twin(self, W):
    pw = (W - 9) / 2; rows = self._rows(W); out = [('왼쪽 패널 머리', 0, 0, pw, 44), ('오른쪽 패널 머리', pw + 9, 0, pw, 44)]
    y = 48
    for i, h in enumerate(rows):
        for side, (lab_w, x0) in enumerate(((self.lw[0], 0), (self.lw[1], pw + 9))):
            tag = '좌' if side == 0 else '우'
            out.append((f'행 {i + 1} 라벨({tag})', x0 + 6, y, lab_w, h)); out.append((f'행 {i + 1} 글({tag})', x0 + 6 + lab_w + 8, y, pw - lab_w - 20, h))
        y += h
    return out


def _three(self, W):
    pw = self._pw(W); H = self.height(W); out = []
    for i, p in enumerate(self.panels):
        xa = i * (pw + 8); fh = 44 if p.get('footer') else 0
        out += [(f'패널 {i + 1} 머리', xa, 0, pw, 42), (f'패널 {i + 1} 본문', xa, 44, pw, H - 44 - fh - 4)]
        if fh: out.append((f'패널 {i + 1} 요약 바', xa + 4, H - 44, pw - 8, 40))
    return out


def _table(self, W):
    cw = self._cw(W); rh = self._rh(W); out = [('머리글', 0, 0, W, 42)]; y = 42
    for i, h in enumerate(rh):
        out.append((f'행 {i + 1} 구분', 0, y, cw[0] + cw[1], h)); out.append((f'행 {i + 1} 내용', cw[0] + cw[1], y, cw[2], h)); y += h
    return out


def _result(self, W):
    h = self.height(W); return [('성과 라벨', 6, 7, 120, h - 14), ('성과 문구', 142, 3, W - 154, h - 6)]


def _eval(self, W):
    h = self.height(W); return [('평가내용 라벨', 0, 0, 178, h), ('제목 박스', 180, 2, W - 180, h - 4)]


def _num(self, W):
    return [('번호 탭', 4, 4, 90, 48), ('제목 띠', 118, 4, W - 130, 48)]


def _sub(self, W):
    return [('소제목 글(+ 민트 밑줄)', 0, 0, text_w(self.text, SZ_SUB, True) / K + 4, 44)] + ([('태그칩', text_w(self.text, SZ_SUB, True) / K + 22, 6, 90 * len(self.chips), 32)] if self.chips else [])


def _chapter(self, W):
    return [('장 제목', 50, 2, W - 312, 73), ('CI 칸', W - 262, 1, 261, 75)]


def _conn(self, W):
    return [('연결 화살표', (W + 114) / 2 - 32, 0, 64, 36)]


def _note(self, W):
    return [('주석', 300, 0, W - 300, 32)]


Ladder.slots = _ladder; LabelRows.slots = _label_rows; TwinPanel.slots = _twin; ThreePanel.slots = _three
DataTable.slots = _table; Result.slots = _result; EvalBand.slots = _eval; NumBar.slots = _num
SubHead.slots = _sub; ChapterBand.slots = _chapter; Connector.slots = _conn; Note.slots = _note
