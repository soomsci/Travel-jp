#!/usr/bin/env python3
"""규슈여행.html(완전판)에서 개인정보를 지운 공개용 index.html을 만든다.

저장소가 공개라 예약번호·탑승객명은 그대로 올릴 수 없다.
예약번호를 알면 제3자가 예약을 조회하거나 취소할 수 있기 때문이다.
일정·지도·맛집·통행료 같은 내용은 그대로 둔다.

    python3 build_public.py
"""
import re
import sys
from pathlib import Path

SRC = Path(__file__).parent / "규슈여행.html"
DST = Path(__file__).parent / "index.html"

# 그대로 치환할 예약번호들
TOKENS = {
    "E8LZ62": "••••••",           # 진에어
    "K26051101458": "••••••",     # 다이와 로이넷
    "140793666": "••••••",        # 오릭스 렌터카
    "22315095674463": "••••••",   # 유라리 로쿠묘
}

# 문맥이 필요한 것 (짧은 숫자라 통째로 바꾸면 오작동한다)
PATTERNS = [
    (r"예약 269", "예약 •••"),
    (r"\['예약번호','269'\]", "['예약번호','•••']"),
    # 탑승객 이름 행은 통째로 삭제
    (r'<div class="kv"><span>탑승객</span><b>KIM/MINSU<br>LEE/SOOMIN</b></div>\s*', ""),
]


def main() -> int:
    if not SRC.exists():
        print(f"원본을 찾을 수 없습니다: {SRC}", file=sys.stderr)
        return 1

    html = SRC.read_text(encoding="utf-8")
    for old, new in TOKENS.items():
        html = html.replace(old, new)
    for pat, new in PATTERNS:
        html = re.sub(pat, new, html)

    # 지우려던 게 남아 있으면 배포를 막는다
    leftovers = [t for t in TOKENS if t in html]
    leftovers += [n for n in ("KIM/MINSU", "LEE/SOOMIN") if n in html]
    if leftovers:
        print("아직 남아 있는 민감 정보: " + ", ".join(leftovers), file=sys.stderr)
        return 1

    DST.write_text(html, encoding="utf-8")
    print(f"{DST.name} 생성 완료 ({len(html) / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
