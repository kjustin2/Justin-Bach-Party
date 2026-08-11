#!/usr/bin/env python3
"""Build five front/back variants of Justin's Official Drinking Team shirts."""

from __future__ import annotations

import math
from dataclasses import dataclass
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "drinking-team-variants"
MOCKUPS = ROOT / "mockups-drinking-team"
FW, FH = 1800, 1200
BW, BH = 3600, 4200

FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_DISPLAY = Path(r"C:\Windows\Fonts\impact.ttf")

PAPER = "#F2EFE8"
NAVY = "#17364B"
CREAM = "#F7EFDD"
CORAL = "#ED684F"
BLACK = "#222629"
FOREST = "#173F33"
GOLD = "#E0B13C"
BONE = "#E8DDCA"
TEAL = "#2FAEB2"


@dataclass(frozen=True)
class Palette:
    shirt: str
    primary: str
    accent: str


@dataclass(frozen=True)
class Variant:
    slug: str
    title: str
    style: str
    justin_front: str
    crew_front: str
    justin: Palette
    crew: Palette


def font(size: int, display: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DISPLAY if display else FONT_BOLD), size=size)


def text(
    draw: ImageDraw.ImageDraw,
    value: str,
    x: int,
    y: int,
    size: int,
    color: str,
    max_width: int,
    *,
    display: bool = False,
) -> int:
    current_size = size
    current = font(current_size, display)
    while draw.textbbox((0, 0), value, font=current)[2] > max_width and current_size > 48:
        current_size -= 4
        current = font(current_size, display)
    draw.text((x, y), value, font=current, fill=color, anchor="mm")
    return current_size


def wave(draw: ImageDraw.ImageDraw, y: int, color: str, width: int, phase: float = 0.0) -> None:
    points = []
    for x in range(440, BW - 439, 12):
        points.append((x, y + math.sin((x / 230) + phase) * 65))
    draw.line(points, fill=color, width=width, joint="curve")


def front_art(phrase: str, palette: Palette) -> Image.Image:
    image = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    text(draw, phrase, FW // 2, 390, 245, palette.primary, 1550, display=True)
    draw.line((555, 580, 805, 580), fill=palette.accent, width=22)
    draw.ellipse((890, 569, 912, 591), fill=palette.accent)
    draw.line((995, 580, 1245, 580), fill=palette.accent, width=22)
    text(draw, "JUSTIN'S BACHELOR PARTY", FW // 2, 735, 82, palette.primary, 1450)
    text(draw, "OCEAN CITY  /  2026", FW // 2, 880, 66, palette.primary, 1200)
    return image


def beer_mugs(draw: ImageDraw.ImageDraw, palette: Palette, y: int = 2050) -> None:
    for center_x, direction in ((1380, -1), (2220, 1)):
        x1, y1, x2, y2 = center_x - 285, y - 260, center_x + 285, y + 470
        draw.rounded_rectangle((x1, y1, x2, y2), radius=60, outline=palette.primary, width=42)
        hx = x1 - 180 if direction < 0 else x2 + 20
        draw.arc((hx, y1 + 140, hx + 210, y2 - 90), 70 if direction < 0 else 110, 290 if direction < 0 else 250, fill=palette.accent, width=38)
        draw.ellipse((x1 + 15, y1 - 45, x2 - 15, y1 + 105), outline=palette.accent, width=34)
    draw.line((1580, y - 50, 2020, y + 260), fill=palette.accent, width=30)
    draw.line((2020, y - 50, 1580, y + 260), fill=palette.accent, width=30)


def back_classic(draw: ImageDraw.ImageDraw, p: Palette) -> None:
    text(draw, "JUSTIN'S", BW//2, 390, 200, p.primary, 2200)
    text(draw, "OFFICIAL", BW//2, 900, 470, p.accent, 2600, display=True)
    text(draw, "DRINKING TEAM", BW//2, 1410, 520, p.primary, 3200, display=True)
    beer_mugs(draw, p)
    text(draw, "BACHELOR WEEKEND", BW//2, 3140, 210, p.primary, 2800)
    text(draw, "OCEAN CITY, MD  /  2026", BW//2, 3500, 150, p.primary, 2600)


def back_brewery(draw: ImageDraw.ImageDraw, p: Palette) -> None:
    draw.ellipse((480, 330, 3120, 3350), outline=p.primary, width=42)
    draw.ellipse((620, 470, 2980, 3210), outline=p.accent, width=24)
    text(draw, "KRAMER BREWING CO.", BW//2, 760, 240, p.primary, 2700)
    text(draw, "OFFICIAL", BW//2, 1320, 420, p.accent, 2500, display=True)
    text(draw, "DRINKING TEAM", BW//2, 1760, 430, p.primary, 2850, display=True)
    beer_mugs(draw, p, 2360)
    text(draw, "BACHELOR WEEKEND", BW//2, 3060, 165, p.primary, 2400)
    text(draw, "OCEAN CITY  /  EST. 2026", BW//2, 3650, 145, p.primary, 2600)


def back_varsity(draw: ImageDraw.ImageDraw, p: Palette) -> None:
    text(draw, "JUSTIN'S", BW//2, 420, 210, p.primary, 2200)
    text(draw, "26", BW//2, 1440, 1100, p.accent, 2200, display=True)
    draw.line((540, 1940, 3060, 1940), fill=p.primary, width=40)
    draw.line((720, 2050, 2880, 2050), fill=p.accent, width=24)
    text(draw, "OFFICIAL DRINKING TEAM", BW//2, 2480, 340, p.primary, 3100, display=True)
    text(draw, "BACHELOR PARTY ROSTER", BW//2, 2980, 170, p.primary, 2500)
    text(draw, "OCEAN CITY, MD", BW//2, 3330, 150, p.primary, 2200)
    text(draw, "SEPTEMBER 10-13", BW//2, 3590, 120, p.primary, 2000)


def back_tiki(draw: ImageDraw.ImageDraw, p: Palette) -> None:
    text(draw, "JUSTIN'S TIKI BAR", BW//2, 500, 300, p.primary, 2900)
    text(draw, "OFFICIAL", BW//2, 1020, 420, p.accent, 2500, display=True)
    text(draw, "DRINKING TEAM", BW//2, 1490, 470, p.primary, 3000, display=True)
    draw.polygon([(1450,1800),(2150,1800),(1980,2700),(1620,2700)], outline=p.primary, width=42)
    draw.ellipse((1510,1740,2090,1900), outline=p.accent, width=30)
    wave(draw, 2470, p.accent, 50)
    wave(draw, 2650, p.primary, 42, 1.3)
    text(draw, "BACHELOR WEEKEND", BW//2, 3150, 185, p.primary, 2600)
    text(draw, "OCEAN CITY, MD  /  2026", BW//2, 3480, 145, p.primary, 2500)


def back_badge(draw: ImageDraw.ImageDraw, p: Palette) -> None:
    draw.ellipse((420, 300, 3180, 3500), outline=p.primary, width=46)
    draw.ellipse((590, 470, 3010, 3330), outline=p.accent, width=26)
    text(draw, "JUSTIN'S BACHELOR PARTY", BW//2, 800, 190, p.primary, 2900)
    text(draw, "OFFICIAL", BW//2, 1320, 410, p.accent, 2500, display=True)
    text(draw, "DRINKING TEAM", BW//2, 1780, 440, p.primary, 2950, display=True)
    draw.rounded_rectangle((1540,2080,2060,2760), radius=45, outline=p.primary, width=40)
    draw.line((1540,2290,2060,2290), fill=p.accent, width=30)
    draw.ellipse((1500,2000,2100,2190), outline=p.accent, width=30)
    text(draw, "OCEAN CITY CHAPTER", BW//2, 3090, 170, p.primary, 2500)
    text(draw, "EST. 2026", BW//2, 3670, 135, p.primary, 1800)


def back_art(style: str, palette: Palette) -> Image.Image:
    image = Image.new("RGBA", (BW, BH), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    {"classic":back_classic,"brewery":back_brewery,"varsity":back_varsity,"tiki":back_tiki,"badge":back_badge}[style](draw, palette)
    return image


def front_svg(phrase: str, p: Palette) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1200"><g text-anchor="middle" font-family="Arial, sans-serif" font-weight="700"><text x="900" y="470" font-family="Impact, Arial Black, sans-serif" font-size="245" fill="{p.primary}">{escape(phrase)}</text><path d="M555 580H805 M995 580H1245" stroke="{p.accent}" stroke-width="22"/><circle cx="901" cy="580" r="11" fill="{p.accent}"/><text x="900" y="765" font-size="82" fill="{p.primary}">JUSTIN'S BACHELOR PARTY</text><text x="900" y="905" font-size="66" fill="{p.primary}">OCEAN CITY / 2026</text></g></svg>'''


def back_svg(v: Variant, p: Palette) -> str:
    subtitles = {
        "classic": ("JUSTIN'S OFFICIAL", "DRINKING TEAM", "BACHELOR WEEKEND"),
        "brewery": ("KRAMER BREWING CO.", "OFFICIAL DRINKING TEAM", "EST. 2026"),
        "varsity": ("JUSTIN'S 26", "OFFICIAL DRINKING TEAM", "BACHELOR PARTY ROSTER"),
        "tiki": ("JUSTIN'S TIKI BAR", "OFFICIAL DRINKING TEAM", "BACHELOR WEEKEND"),
        "badge": ("JUSTIN'S BACHELOR PARTY", "OFFICIAL DRINKING TEAM", "OCEAN CITY CHAPTER"),
    }[v.style]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3600 4200"><g text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" fill="{p.primary}"><ellipse cx="1800" cy="2050" rx="1320" ry="1600" fill="none" stroke="{p.accent}" stroke-width="34"/><text x="1800" y="750" font-size="220">{escape(subtitles[0])}</text><text x="1800" y="1700" font-family="Impact, Arial Black, sans-serif" font-size="470">{escape(subtitles[1])}</text><path d="M1180 2130H2420 M1380 2440H2220" stroke="{p.accent}" stroke-width="38"/><text x="1800" y="3120" font-size="180">{escape(subtitles[2])}</text><text x="1800" y="3480" font-size="145">OCEAN CITY, MD / 2026</text></g></svg>'''


def shirt_layer(color: str, back: bool = False) -> Image.Image:
    w,h=650,1040
    image=Image.new("RGBA",(w,h),(0,0,0,0)); draw=ImageDraw.Draw(image)
    pts=[(w*.39,h*.10),(w*.28,h*.16),(w*.06,h*.33),(w*.20,h*.47),(w*.29,h*.40),(w*.29,h*.92),(w*.71,h*.92),(w*.71,h*.40),(w*.80,h*.47),(w*.94,h*.33),(w*.72,h*.16),(w*.61,h*.10)]
    draw.polygon(pts,fill=color); draw.ellipse((w*.42,h*.07,w*.58,h*(.18 if back else .22)),fill=PAPER)
    return image


def mockup(v: Variant, arts: dict[str,Image.Image]) -> None:
    canvas=Image.new("RGB",(2800,1350),PAPER); draw=ImageDraw.Draw(canvas)
    draw.text((1400,65),v.title.upper(),font=font(58),fill=NAVY,anchor="mm")
    entries=[("JUSTIN FRONT",v.justin,False,arts["justin_front"]),("JUSTIN BACK",v.justin,True,arts["justin_back"]),("CREW FRONT",v.crew,False,arts["crew_front"]),("CREW BACK",v.crew,True,arts["crew_back"])]
    for i,(label,p,back,art) in enumerate(entries):
        x=30+i*690; shirt=shirt_layer(p.shirt,back); shadow=shirt_layer("#00000066",back).filter(ImageFilter.GaussianBlur(18))
        canvas.paste(shadow,(x+10,150),shadow); canvas.paste(shirt,(x,130),shirt)
        if back:
            scaled=art.resize((250,292),Image.Resampling.LANCZOS); canvas.paste(scaled,(x+200,420),scaled)
        else:
            scaled=art.resize((205,137),Image.Resampling.LANCZOS); canvas.paste(scaled,(x+340,370),scaled)
        draw.text((x+325,1275),label,font=font(30),fill=NAVY,anchor="mm")
    MOCKUPS.mkdir(parents=True,exist_ok=True); canvas.save(MOCKUPS/f"{v.slug}.png",dpi=(150,150),optimize=True)


def variants() -> tuple[Variant,...]:
    return (
        Variant("01-classic","Classic Drinking Team","classic","BUY ME A SHOT","I'M WITH THE GROOM",Palette(CORAL,NAVY,CREAM),Palette(NAVY,CREAM,CORAL)),
        Variant("02-brewery","Kramer Brewing Co.","brewery","HEAD BREWER","TASTING CREW",Palette(CREAM,FOREST,GOLD),Palette(FOREST,CREAM,GOLD)),
        Variant("03-varsity","Varsity Drinking Team","varsity","TEAM CAPTAIN","STARTING LINEUP",Palette(GOLD,BLACK,CREAM),Palette(BLACK,CREAM,GOLD)),
        Variant("04-tiki","Official Tiki Drinking Team","tiki","TIKI CAPTAIN","DECK CREW",Palette(CORAL,NAVY,CREAM),Palette(NAVY,CREAM,TEAL)),
        Variant("05-bar-badge","Ocean City Bar Badge","badge","LAST CALL","BAR SUPPORT",Palette(BONE,BLACK,CORAL),Palette(BLACK,CREAM,CORAL)),
    )


def main() -> None:
    for v in variants():
        out=OUT/v.slug/"artwork"; out.mkdir(parents=True,exist_ok=True)
        arts={"justin_front":front_art(v.justin_front,v.justin),"crew_front":front_art(v.crew_front,v.crew),"justin_back":back_art(v.style,v.justin),"crew_back":back_art(v.style,v.crew)}
        for name,image in arts.items(): image.save(out/f"{name.replace('_','-')}.png",dpi=(300,300),optimize=True)
        (out/"justin-front.svg").write_text(front_svg(v.justin_front,v.justin),encoding="utf-8")
        (out/"crew-front.svg").write_text(front_svg(v.crew_front,v.crew),encoding="utf-8")
        (out/"justin-back.svg").write_text(back_svg(v,v.justin),encoding="utf-8")
        (out/"crew-back.svg").write_text(back_svg(v,v.crew),encoding="utf-8")
        mockup(v,arts)


if __name__=="__main__": main()
