# 외부 구성요소

게임 원본 실행 파일, Assembly-CSharp.dll, level1, resources.assets, 영어 및 Data XML 전체는 배포하지 않습니다.

## Noroshi Code

* 공식 저장소: https://github.com/Honoka55/noroshi
* 고정 출처 커밋: 0f8e671affc0bdfa909a055085f43e596b689c91
* 원본 경로: fonts/NoroshiCode/ttf/unhinted/NoroshiCode-Regular.ttf 및 NoroshiCode-Bold.ttf
* 라이선스: SIL Open Font License 1.1. `Turing Complete/asset/font/NoroshiCode-OFL.txt` 동봉.
* Copyright 2024 Honoka55 (Reserved Font Name Noroshi), Copyright 2017 IBM Corp. (Reserved Font Name Plex).
* **수정본(Modified Version)** 입니다. 변경 내용: 한글 음절·자모 글리프의 가로 폭을 1200→900 단위로 줄이고 가운데 정렬, U+2009(가는 공백) 폭을 300 단위로 설정(표 정렬 보정용).
* OFL 1.1 제3조(Reserved Font Name)에 따라 글꼴 이름을 `TCKorean Code`(PostScript `TCKoreanCode-Regular`/`-Bold`)로 바꾸었습니다. 저작권 고지와 라이선스 문구(name ID 0, 13, 14)는 유지하고, 설명(name ID 10)에 원본 출처를 적었습니다.
* 게임이 `font/NoroshiCode_Regular.ttf`, `font/NoroshiCode_Bold.ttf` 파일 이름을 고정해서 읽기 때문에 파일 이름만 원래대로 둡니다. OFL FAQ는 사용자에게 보이는 글꼴 이름을 기준으로 설명하며 파일 이름은 명시하지 않습니다. 배포 전 필요하면 원저작자에게 확인하세요.
* 생성 방법: 아래 공식 원본에서 fontTools로 폭만 조정(윤곽선 모양은 그대로).

SHA-256 (공식 원본):
```text
Regular 772e812787c08f0792095c36d3678292416b1f0c56f09301c64a545466d68cef
Bold    52c95fd196b7212a872d9a938757e6982e5ffd09c1131d8d8fcce7866e4d7c5c
```

SHA-256 (배포 수정본):
```text
Regular 0d8af12bf2349226e8d73f5b85991171eca2c9ee280634140dfc9c3888435bdb
Bold    3a8dc5882dff5c097c06583a53a5cde840f29c74f9ebd122a9914f0e5b899ba3
```

기존 합성 폰트는 한글 글리프의 공급원을 확정하지 못해 v2 배포에서 제외했습니다. 게임의 Icon_Complete.ttf는 원본 그대로 사용하며 배포하지 않습니다.
