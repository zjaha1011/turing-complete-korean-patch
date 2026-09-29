> 원본 검토 요청서입니다. 현재 설치 방법과 검증 상태는 README.md와 COMPATIBILITY.md를 확인하세요.

# Stationeers / Turing Complete 한국어 패치 — 리뷰·배포 가이드

> Codex 등 코드 에이전트가 이 저장소를 리뷰하고 GitHub에 배포할 때 알아야 할 사항과, 배포 시 게임에 적용해야 하는 패치 목록.
> 작성 기준일: 2026-09-29 · 작성 근거: 실제 설치 폴더의 원본 백업과 현재 파일을 직접 비교한 결과.

---

## 0. 가장 먼저 지킬 것 (저작권)

- **게임 원본 파일과 그것을 수정한 바이너리 전체를 저장소에 올리지 않는다.**
  - 금지: `Assembly-CSharp.dll`, `level1`, `resources.assets`, `Turing Complete.exe`, 원본 `english.xml`·`Data/*.xml` 전체 사본.
  - 대신 **패치 방식**(바이트 패치 / XML 삽입 스크립트 / 번역 파일)으로 배포한다.
- 저장소에 올려도 되는 것: 직접 만든 한국어 번역 파일, 패치 스크립트, 바이트 패치 정의(오프셋·원래 바이트·새 바이트), 문서.
- 폰트는 라이선스를 확인한 뒤에만 포함한다(4-2 참고).
- `.gitignore`에 게임 원본 확장자(`*.dll`, `*.exe`, `*.assets`, `*.resS`, `level*`)를 넣어 실수로 올라가는 것을 막는다.

---

## 0-1. 배포 목표: "압축 풀고 게임 폴더에 덮어쓰기 = 한국어 적용"

사용자는 **릴리스 zip을 받아 게임 설치 폴더에 그대로 덮어쓰기만 하면 한국어가 되어야 한다.** 저장소와 릴리스는 이 목표에 맞춰 만든다.

### 릴리스 zip 구조 (게임 폴더 구조 그대로)
```
Stationeers-Korean-vX.Y.zip
└─ Stationeers/                                  ← 이 폴더 안의 내용을 게임 폴더에 덮어쓰기
   ├─ rocketstation_Data/StreamingAssets/Language/
   │  ├─ korean.xml
   │  ├─ korean_help.xml
   │  ├─ korean_keys.xml
   │  ├─ korean_tips.xml
   │  └─ korean_tooltips.xml
   ├─ KoreanPatcher.exe  (또는 KoreanPatcher.bat + patcher.py)   ← 선택: 추가 패치용
   └─ 한국어패치_설치방법.txt

TuringComplete-Korean-vX.Y.zip
└─ Turing Complete/                              ← 이 폴더 안의 내용을 게임 폴더에 덮어쓰기
   ├─ translations/
   │  ├─ Korean.txt
   │  └─ Swedish.txt        (Korean.txt와 동일 파일)
   ├─ asset/font/
   │  ├─ NoroshiCode_Regular.ttf   (한글 포함 폰트, 라이선스 확인 후)
   │  └─ NoroshiCode_Bold.ttf
   ├─ KoreanPatcher.exe  (또는 .bat)   ← 선택: 언어 메뉴 이름 변경용
   └─ 한국어패치_설치방법.txt
```
- zip 최상위 폴더 이름을 게임 설치 폴더 이름과 같게 해서, `steamapps\common\`에 풀면 바로 덮어써지게 한다.
- 텍스트·폰트처럼 **직접 만든 파일만** zip에 넣는다. 수정한 `dll`/`exe`/`assets`/`level1`은 절대 zip에 넣지 않는다(0장).

### 덮어쓰기만으로 되는 것 / 추가 패처가 필요한 것
| 게임 | 덮어쓰기만 했을 때 | 패처까지 실행했을 때 추가되는 것 |
|---|---|---|
| Stationeers | 설정 → 언어 → **한국어** 선택 시 아이템·설명·UI·도움말·팁·툴팁 대부분 한국어로 표시 (게임에 원래 한국어 슬롯과 한글 폰트 `font_hangul`이 있음) | 하드코딩돼 있던 일부 UI 문구(키 설정 분류, 로켓 목적지 이름, 월드 목표 이름 등 추가 키 251개) 한국어화 — **BepInEx 플러그인으로 처리(0-2장)**, 원본 파일 수정 없음 |
| Turing Complete | 설정 → 언어 → **Svenska (3% done)** 선택 시 전체 한국어 표시 (슬롯 대체 방식) | 언어 메뉴 이름이 `한국어(Korean)`으로 표시 — exe **시그니처 치환**(0-2장) |

→ **기본 배포는 "덮어쓰기만"으로 완결되게 만들고, 패처는 선택 기능으로 분리한다.** 패처가 실패해도(게임 업데이트로 원본 바이트가 달라져도) 번역 자체는 동작해야 한다.

### 덮어쓰기 배포가 성립하기 위한 조건 (Codex가 반드시 검증)
- [ ] `korean.xml`은 `english.xml`에 **없는 키를 참조하지 않아도** 게임이 오류 없이 로드되는지 확인. 패처 없이 설치했을 때 `korean.xml`에만 있는 `KoreanDataName*` 등 추가 키는 무시되어야 한다(게임 실행해서 Unity 로그 `%USERPROFILE%\AppData\LocalLow\<개발사>\<게임>\Player.log`에 언어 로드 오류가 없는지 확인 — 정확한 폴더명은 PC에서 확인).
- [ ] 반대로 게임 업데이트로 `english.xml`에 새 키가 생기면 `korean.xml`에 없는 키는 영어로 표시된다 → 릴리스마다 `english.xml` 기준 누락 키 목록을 `validate.py`로 출력하고 번역 추가.
- [ ] Turing Complete는 게임 업데이트 때 `translations/Swedish.txt`가 원본으로 덮어써질 수 있다 → 설치 안내문에 "업데이트 후 다시 덮어쓰기" 명시.
- [ ] Turing Complete 폰트 교체 없이 번역 파일만 덮어쓰면 한글이 □로 나오는지 확인(원본 NoroshiCode에는 한글 0자). 폰트 라이선스 문제로 폰트를 zip에 못 넣게 되면, 패처가 사용자 PC에서 폰트를 생성(병합)하도록 해야 한다.
- [ ] 두 게임 모두 **패치 전 원본 파일 백업**을 설치 안내문에 포함하거나 패처가 자동 백업.

### 사용자용 설치 안내문(`한국어패치_설치방법.txt`)에 들어갈 내용
1. Steam 라이브러리 → 게임 우클릭 → 관리 → 로컬 파일 보기로 게임 폴더 열기.
2. zip 안의 게임 이름 폴더 **안의 내용**을 게임 폴더에 복사 → "대상 폴더의 파일 덮어쓰기" 선택.
3. (선택) `KoreanPatcher` 실행 → 추가 한국어화 적용.
4. 게임 실행 → 설정 → 언어:
   - Stationeers: `한국어`
   - Turing Complete: `한국어(Korean)` (패처 미실행 시 `Svenska (3% done)`)
5. 게임 업데이트 후 영어로 돌아가거나 글자가 깨지면 2~3번을 다시 실행.
6. 제거: Steam → 게임 우클릭 → 속성 → 설치된 파일 → **게임 파일 무결성 검사**.

### GitHub 릴리스 방식
- 저장소 루트에 게임 폴더 구조를 그대로 두고(`Stationeers/…`, `Turing Complete/…`), GitHub Actions에서 태그 푸시 시 각 게임 폴더를 zip으로 묶어 Releases에 업로드.
- 릴리스 노트에 대상 게임 버전(1장)과 이 버전에서 확인한 항목을 적는다.
- 패처 exe를 배포하면 백신 오탐이 잦으므로 `.bat + .py` 소스도 같이 올리고, exe는 Actions에서 PyInstaller로 빌드해 출처를 투명하게 한다.

---

## 0-2. 안정적인 패치 방식 (권장 아키텍처)

현재 패치 중 **게임 업데이트에 가장 잘 깨지는 부분**은 오프셋 고정 바이너리 패치다(DLL 8곳, `level1`, `resources.assets`, TC exe). 아래 원칙으로 전부 대체한다.

### 원칙
1. **원본 게임 파일을 가능한 한 수정하지 않는다.** 추가 파일(번역·폰트·플러그인)만 넣는다.
2. 파일 수정이 불가피하면 **오프셋이 아니라 내용(시그니처) 검색 → 검증 → 치환**으로 한다.
3. 모든 패치는 **멱등**(여러 번 실행해도 결과 동일)이고, **실패해도 번역 기본 기능은 유지**(부분 실패 허용).
4. 적용 전 자동 백업, 원클릭 제거 제공.
5. 게임 버전이 바뀌면 패처가 스스로 감지해서 "호환됨 / 일부만 적용 / 건너뜀"을 보고.

### 방식별 안정성 비교
| 방식 | 업데이트 내성 | 사용처 |
|---|---|---|
| 번역 파일 덮어쓰기 (게임이 원래 읽는 파일) | 매우 높음 | Stationeers `korean*.xml`, TC `Korean.txt`/`Swedish.txt` |
| 느슨한 에셋 파일 교체 | 높음 | TC `asset/font/*.ttf` |
| 런타임 패치(BepInEx + Harmony 플러그인) | 높음 (메서드 이름만 유지되면 동작) | Stationeers DLL·`level1` 패치 대체 |
| 텍스트 파일 구조적 삽입(XML 파싱 후 키 단위 추가) | 중간~높음 | 불가피할 때만 `english.xml`, `Data/*.xml` |
| 시그니처 검색 바이트 치환 | 중간 | TC exe 메뉴 이름 |
| 오프셋 고정 바이트 패치 | **낮음 (업데이트마다 깨짐)** | **사용 금지** |
| 에셋 번들 재패킹(`resources.assets`) | **매우 낮음 + 재배포 위험** | **사용 금지** |

### Stationeers: BepInEx 플러그인으로 전환 (권장)
- Stationeers는 Unity Mono 빌드(`Managed/Assembly-CSharp.dll` 존재)라 BepInEx 5 + Harmony 방식 적용 대상이다. **실제 호환 여부와 게임 측 공식 모드 로더와의 충돌 여부는 배포 전에 테스트로 확인**(미검증).
- 플러그인 `StationeersKorean.dll`이 할 일:
  - **DLL 바이트 패치 대체:** 기존 IL 패치가 바꾼 메서드(8곳)를 dnSpy로 확인한 뒤, 같은 동작을 Harmony Prefix/Postfix로 구현. 원본 DLL은 건드리지 않음.
  - **`english.xml` 키 251개 추가 대체:** 게임 로컬라이제이션 딕셔너리가 로드된 직후(Postfix) 한국어 키·값을 메모리에 주입. `english.xml` 수정 불필요.
  - **`Data/*.xml`의 `Key=` 속성 추가 대체:** 로켓 목적지·월드 목표·거래품 이름을 표시하는 지점에서 영어 이름 → 한국어로 변환하는 사전(`data_names.ko.json`)을 적용. Data XML 수정 불필요.
  - **`startconditions.xml`·`level1` 직접 문자열 교체 대체:** 현재 언어가 한국어일 때만 치환 → 영어 설정에서 한국어가 섞여 나오는 문제도 해결.
  - 대상 메서드를 못 찾으면 해당 기능만 비활성화하고 로그 경고(게임은 정상 실행).
- 배포 구조:
  ```
  Stationeers/
  ├─ rocketstation_Data/StreamingAssets/Language/korean*.xml   ← 덮어쓰기(기본)
  └─ BepInEx/plugins/StationeersKorean/
     ├─ StationeersKorean.dll
     ├─ extra_keys.ko.json      (기존 english.xml 추가 키 251개의 한국어 값)
     └─ data_names.ko.json      (Data XML 이름 번역)
  ```
  BepInEx 본체는 zip에 동봉하지 말고 공식 배포처 링크 + 설치 순서를 안내(BepInEx 라이선스 확인 후 동봉 여부 결정).
- 결과: 설치 = 폴더 덮어쓰기 하나로 끝. 게임 업데이트 후에도 플러그인과 번역 파일은 Steam이 지우지 않는 경로라 대부분 유지(Steam이 관리하는 `korean*.xml`만 원본으로 돌아갈 수 있음 → 7번 참고).

### Turing Complete
- 번역·폰트는 덮어쓰기(이미 안정적).
- 메뉴 이름 패치는 오프셋 대신 **시그니처 치환**:
  - exe 전체에서 `Svenska (` 로 시작하는 문자열을 검색 → 찾은 문자열 **바이트 길이 그대로** `한국어(Korean)`을 맞춰 넣고 남는 칸은 원래 문자열 뒤 공백/NULL 규칙에 맞게 채움. 길이가 모자라면 `한국어` 등으로 축약.
  - 일치 항목이 0개 또는 2개 이상이면 **쓰지 않고 종료**(오탐 방지).
  - 이 패치는 표시 이름만 바꾸므로 실패해도 번역은 정상 동작.
- 장기적으로는 개발사에 한국어 번역 파일을 정식 기여(공식 번역 슬롯 추가 요청)하는 것이 가장 안정적.

### 패처가 해야 할 일 (공통)
1. 게임 경로 자동 탐지(Steam `libraryfolders.vdf`) + 수동 선택.
2. 게임 실행 중이면 중단.
3. 버전 감지: Stationeers `version.ini`, TC exe 해시 → 호환 표(`compat.json`)와 비교.
4. 수정 대상 백업(`_korean_patch_backup/<날짜>/`, 기존 백업 덮어쓰기 금지).
5. 파일 배치 → 구조적 삽입/시그니처 치환(필요한 경우만).
6. 검증: XML 파싱, 키 개수, `Swedish.txt == Korean.txt`, 해시 기록.
7. 결과 리포트: 적용/건너뜀/실패 항목 표시.
8. `--uninstall`: 백업에서 복원, 추가한 파일 제거.
9. `--repair`: Steam 업데이트 후 번역 파일만 다시 덮어쓰기.

### Steam 업데이트 대응
- Steam 업데이트·무결성 검사는 Steam이 관리하는 파일(`korean*.xml`, `Swedish.txt`, exe, 폰트)을 원본으로 되돌릴 수 있다. 추가한 파일(BepInEx 플러그인 폴더 등)은 보통 남는다.
- 대응: 패처 `--repair` 한 번 실행 또는 zip 다시 덮어쓰기. 설치 안내문에 명시.
- 릴리스마다 `compat.json`에 확인한 게임 버전을 추가하고, CI에서 `validate.py`로 최신 `english.xml` 대비 누락 키를 점검.

### 이 전환으로 없어지는 위험
- DLL 8곳 오프셋 패치 → 업데이트 때 게임 크래시 가능성 제거
- `resources.assets` 재패킹 → 제거(480MB 파일 수정·재배포 위험 제거)
- `level1`·`startconditions.xml` 직접 교체 → 영어 설정에서 한국어가 보이는 문제 제거
- 게임 원본 바이너리 재배포 필요 → 제거

---

## 1. 대상 버전 (버전이 바뀌면 바이너리 패치는 무효)

| 게임 | 버전 | 확인 방법 |
|---|---|---|
| Stationeers | Update 0.2.6428.27798 (2026-08-13) | `rocketstation_Data/StreamingAssets/version.ini` |
| Turing Complete | 버전 문자열 미확인 | 원본 exe MD5 `4df7a68d4a5028f91db4eb1f2712e960` |

원본(패치 전) 파일 MD5:

| 파일 | 원본 MD5 | 패치 후 MD5 |
|---|---|---|
| Stationeers `Managed/Assembly-CSharp.dll` | `6d01f6c5e9d31156ead2eeb1fb5b91fd` | `6215b5cef098ad1cc393a64a6a1f6ebf` |
| Stationeers `level1` | `334a9216efd6d53df1cc1e15a69a0615` | `4b0058ba7a3de3d4c9cc7164d34d0f12` |
| Turing Complete `Turing Complete.exe` | `4df7a68d4a5028f91db4eb1f2712e960` | `67eb032f1c8a430514d00f8aedd1d6dd` |

**패치 스크립트는 적용 전에 원본 MD5를 검사하고, 다르면 바이너리 패치를 건너뛰고 경고해야 한다.** Steam 업데이트나 "게임 파일 무결성 확인"을 하면 수정 파일이 원본으로 되돌아가므로 재적용이 필요하다.

---

## 2. Stationeers — 적용해야 하는 패치 전체 목록

경로 기준: `...\steamapps\common\Stationeers\`

> 2-2 ~ 2-6은 **기존 패치가 원본을 어떻게 바꿨는지에 대한 기록**이다. 새 배포에서는 이 방식 대신 0-2장의 BepInEx 플러그인 방식으로 같은 결과를 재현한다. 2-1(번역 파일)만 그대로 사용.

### 2-1. 번역 파일 (그대로 배포 가능, 덮어쓰기)
| 파일 | 내용 |
|---|---|
| `rocketstation_Data/StreamingAssets/Language/korean.xml` | 본문 번역 (항목 9,492개 중 비어 있지 않은 8,768개) |
| `.../Language/korean_help.xml` | 스테이션피디아 도움말 |
| `.../Language/korean_keys.xml` | 키 이름 |
| `.../Language/korean_tips.xml` | 로딩 팁 |
| `.../Language/korean_tooltips.xml` | 화면 툴팁 |

- 인코딩 UTF-8(BOM 없음), 줄바꿈 **CRLF**, 선언부 `<?xml version='1.0' encoding='utf-8'?>`.
- `<Font>font_hangul</Font>` 유지.

### 2-2. `english.xml` — 키 추가 (파일째 배포 금지 → 삽입 스크립트)
- `Interface` 섹션에 **Record 251개 추가**. 이 중 173개는 `KoreanDataName*` 키, 나머지 78개는 원래 하드코딩돼 있던 UI 문자열용 키(`General`, `Movement`, `Forward`, `Ascend` 등).
- 이 키가 없으면 DLL/Data 쪽에서 참조하는 키를 못 찾아 영어 원문이나 키 이름이 그대로 나온다.
- 스크립트: 백업의 원본 `english.xml`과 비교해 **없는 Key만 추가**하도록 구현(이미 있으면 건너뜀, 멱등성 보장).
- 추가할 251개 (Key, Value) 목록은 원본/패치본 diff로 추출해 `patch/stationeers/english_additions.xml` 로 저장해 두고 배포한다(값은 영어 원문이므로 목록 형태로만 보관).

### 2-3. `StreamingAssets/Data/*.xml` — 속성 추가 (삽입 스크립트)
| 파일 | 변경 |
|---|---|
| `rocketlocations.xml` | `<Name Value="..."/>` 에 `Key="KoreanDataName..."` 속성 추가 320곳 |
| `WorldObjectives.xml` | 같은 방식 10곳 |
| `scriptTradables.xml` | 같은 방식 1곳 |
| `startconditions.xml` | `StartScreenHeader` 값을 **한국어로 직접 교체** 4곳 (아래 주의) |

- `startconditions.xml` 교체 4곳: `착륙 캡슐`, `부활용 착륙 캡슐`, `인간 플레이어`, `즈릴리안 플레이어`.
- **주의:** `startconditions.xml`은 키 방식이 아니라 문자열을 직접 바꿨기 때문에 **게임 언어를 영어로 바꿔도 한국어로 나온다.** 배포 전에 키 방식으로 바꿀 수 있는지 검토하고, 안 되면 README에 명시.
- Data XML은 원래 파일이 탭/공백 들여쓰기가 섞여 있으므로 **정규식 기반 최소 치환**으로 패치하고 ElementTree로 재저장하지 않는다(포맷 전체가 바뀜).

### 2-4. `Managed/Assembly-CSharp.dll` — IL 바이트 패치 (버전 종속)
- 파일 크기 동일(6,761,984바이트), **79바이트가 8개 구역에서 변경**.
  | 오프셋 | 변경 바이트 수 | 비고 |
  |---|---|---|
  | `0x180` | 1 | PE 헤더(.text 섹션 크기) |
  | `0x143464` | 2 | 메서드 호출 토큰 교체 |
  | `0x1436fc` | 2 | 메서드 호출 토큰 교체 |
  | `0x143b82` | 2 | 메서드 호출 토큰 교체 |
  | `0x143c0f` | 2 | 메서드 호출 토큰 교체 |
  | `0x171d0a` | 47 | 메서드 본문 교체 |
  | `0x3923d4` | 3 | 메타데이터 |
  | `0x672528` | 20 | 새 메서드 본문 추가(빈 영역에 기록) |
- **변경 의도는 문서화되지 않았다(미확인).** 추정: 하드코딩 문자열을 로컬라이즈 함수로 우회. 배포 전 dnSpy/ILSpy로 원본과 비교해 의도를 README에 적을 것.
- 배포 형식: `patch/stationeers/Assembly-CSharp.patch.json` = `[{offset, original_hex, patched_hex}]`. 적용 시 **각 오프셋의 원래 바이트가 일치할 때만** 쓰기.
- 대안(권장): 바이트 패치 대신 BepInEx + Harmony 플러그인으로 같은 동작을 구현하면 게임 업데이트에도 덜 깨진다.

### 2-5. `level1` — 씬 문자열 직접 교체 (버전 종속)
- 크기 동일, 39바이트 변경(오프셋 약 `7936744`~`8283549` 구간).
- 씬 안에 박혀 있던 UI 문자열을 한국어로 교체(예: `난이도`). → **영어로 바꿔도 한국어로 보임.**
- 문자열 길이 필드까지 바뀌므로 반드시 원본 바이트 검증 후 적용.

### 2-6. `resources.assets` — 변경 내용 미확인 ⚠️
- 크기가 20바이트 늘었고(479,046,524 → 479,046,544) 에셋 재패킹으로 파일 대부분의 오프셋이 이동했다.
- 한글 폰트 `font_hangul_b`(한글 11,172자)는 **원본에도 이미 있었으므로** 폰트 추가는 아니다. 무엇이 바뀌었는지는 확인하지 못했다.
- 480MB 파일이라 바이트 diff 배포는 비현실적. 배포 전 UnityPy로 원본/패치본의 객체 단위 diff를 떠서 **바뀐 객체만 재현하는 스크립트**로 만들 것. 확인 전까지는 배포 대상에서 제외하고 영향 여부를 테스트.

### 2-7. 폰트 관련 사실
- 한글: `font_hangul_b`가 한글 음절 11,172자 전체 포함 → 한글은 깨지지 않음.
- 한글 폰트에 없는 기호: 가운뎃점 `·` 등. 번역에서 `·`는 모두 제거했다. 새 번역에도 쓰지 말 것.
- `° × – ‘ ’ …` 는 영어판에서도 쓰이는 기호라 보조 폰트로 표시된다고 판단(게임 화면에서는 미검증).

---

## 3. Turing Complete — 적용해야 하는 패치 전체 목록

경로 기준: `...\steamapps\common\Turing Complete\`

### 3-1. 번역 파일
| 파일 | 내용 |
|---|---|
| `translations/Korean.txt` | 한국어 번역 (2,028항목) |
| `translations/Swedish.txt` | **`Korean.txt`와 바이트 단위로 동일해야 함** |

- 게임이 한국어 슬롯을 따로 인식하지 않아서 **스웨덴어 슬롯을 한국어로 대체**하는 방식이다. 두 파일은 항상 같이 갱신.
- 원본 `Swedish.txt` MD5: `0be64eff87242717057458421bb82454` (언패치 시 복원용).

### 3-2. `Turing Complete.exe` — 언어 메뉴 이름 바이트 패치
> 아래 오프셋은 기존 패치 기록. 새 패처는 오프셋이 아니라 0-2장의 시그니처 치환을 쓴다.

- 오프셋 `0x6A62C8`(10진 6,972,104)부터 17바이트:
  - 원래: `Svenska (3% done)` (ASCII 17바이트)
  - 변경: `한국어(Korean)` (UTF-8 17바이트)
- 길이가 정확히 같아야 한다. 다른 문구로 바꿀 때도 UTF-8 **17바이트** 유지.
- 적용 전 원래 17바이트가 `Svenska (3% done)`인지 확인.

### 3-3. 폰트 교체
| 파일 | 원본 | 교체본 |
|---|---|---|
| `asset/font/NoroshiCode_Regular.ttf` | 403,564B, 한글 0자 | 2,866,904B, 한글 11,172자 |
| `asset/font/NoroshiCode_Bold.ttf` | 344,472B, 한글 0자 | 2,808,024B, 한글 11,172자 |

- 교체 폰트의 이름 테이블에는 `Honoka55`, `IBM Corp.` 저작권만 있다. **합쳐 넣은 한글 글리프의 출처 폰트와 라이선스가 기록되어 있지 않다(미확인).**
  - OFL 등 재배포 가능한 폰트에서 왔는지 확인하고, OFL이면 폰트 이름 변경(Reserved Font Name 규정) 여부와 `OFL.txt` 동봉 필요.
  - 확인이 안 되면 폰트 파일은 배포하지 말고, 사용자가 직접 병합하는 스크립트(fontTools)로 대체.

### 3-4. 번역 파일 형식 (Codex가 파일을 고칠 때 반드시 지킬 규칙)
- 구조:
  ```
  === 원본/파일/경로 ===

  $<ID>* <번역문>

  $<ID>* <번역문>
  ```
- `$ID*` 뒤 **첫 글자 1개(공백 또는 줄바꿈)는 구분자**이며 본문이 아니다.
  - 본문이 줄바꿈으로 시작하면: `$ID*` + `\n` + `\n본문...` → 즉 `$ID*` 다음에 빈 줄 하나.
  - 본문 끝의 공백은 의미가 있다(예: `$53037516781370* 저장 충돌: ` 끝 공백 유지).
- 줄바꿈 LF, UTF-8, BOM 없음.
- 영어 원문: `translations/_ids_and_english.txt` (형식 `$ID* ID 원문`). 줄 끝의 `# com_...` 주석은 원문이 아니다.

---

## 4. 번역 리뷰 규칙 (Codex 리뷰 체크리스트)

### 4-1. 깨지면 게임 오류가 나는 것
- [ ] 태그·변수 **개수·내용·순서 보존**
  - Stationeers: `{THING:키}`, `{LINK:키;표시문구}`, `{GAS:..}`, `{KEY:..}`, `{LOCAL:..}`, `{0}`, `<color=..>`, `</color>`, `\n`, `/n`, `#VAR1#`
    - `{LINK:키;표시문구}`·`{THING:키;표시문구}`는 **세미콜론 뒤 표시문구만** 번역 가능, 키는 절대 불변.
    - `{HEADER:문구}`, `{COLORRED:문구}`는 안의 문구만 번역 가능.
  - Turing Complete: `[color=#..]`, `[/color]`, `[b]`, `[large]`, `[box]`, `[center]`, `[left]`, `[T]`, `[F]`, `[Z]`, `[image=".."]`, `%a %b %c %value %adr`, `{중괄호 변수}`
- [ ] XML 특수문자 이스케이프(`&amp;`, `&lt;`) 유지, XML 파싱 통과
- [ ] Stationeers 키 집합이 `english.xml`과 동일(현재 9,492개 일치)
- [ ] Turing Complete ID 집합이 `_ids_and_english.txt`와 동일(현재 2,028개 일치), `Swedish.txt == Korean.txt`
- [ ] 코드 블록·정렬된 표(어셈블리, 16진수 표, 연산자 표)의 열 정렬 유지

### 4-2. 폰트·문자
- [ ] 사용 가능 문자: 한글, ASCII, 원문에 이미 있는 기호(`° × – ‘ ’ … ≤ ≥ ≠ ≈ π`), 원문의 아이콘 문자(TC `U+E85D`, `U+F2DB`)
- [ ] 금지: `·`(가운뎃점), `ㆍ`, 전각 문자, `「」`, `“”`, 이모지

### 4-3. 품질 규칙
- 설명·안내문: "~합니다/~하세요"체. 버튼·라벨·항목명: 명사형.
- **자리표시자 뒤 조사**
  - 이름을 아는 `{THING:X}`: 용어집의 한국어 이름 받침에 맞춤(예: `케이블 코일 (강화)` → 를, `주괴 (강철)` → 을).
  - 값을 알 수 없는 `{LOCAL:..}`, `{0}`, `%a`, `{value}`: 조사가 필요 없는 구조로 쓴다. `이(가)`, `을(를)`, `(으)로` 병기 금지.
- Turing Complete 오류 메시지 형식 통일:
  - `X는 {실제값} 값이 아니라 {기대값} 값이어야 합니다.`
  - 기대값만 있을 때: `X는 {값} 값이어야 합니다.`
  - `%a`/`%b` 이동: `%b의 값을 %a에 옮깁니다.`
- 원문 버그를 번역에서 바로잡은 곳은 유지(예: TC `[center]`→`[/center]`, `[large]` 닫는 태그, Stationeers `WaterWrongTemp`의 짝 없는 `</color>`, `{THING: Screwdriver}`→`{THING:ItemScrewdriver}`).

### 4-4. 확정 용어 (일부)
| 영어 | 한국어 |
|---|---|
| Stationeer | 스테이셔니어 |
| Respawn / Spawn Point / Revive | 부활 / 스폰 지점 / 소생 |
| Launch Mount / Rocket Tower | 발사 거치대 / 발사 타워 |
| Body Bag / Sleeper | 시신 가방 / 수면 캡슐 |
| Logic Writer | 로직 라이터 |
| Payload Bay | 화물칸 |
| Chute Inlet | 물류관 투입구 |
| Volatiles | 휘발성 가스 |
| ODA | 행성 외 개발청 |
| Enceladus / Tyre | 엔셀라두스 / 티레 |
| carry (TC) | 자리올림 |
| cycle (TC) | 틱 |
| custom component (TC) | 사용자 정의 컴포넌트 |

Stationeers 전체 아이템 이름은 `korean.xml`의 `Things` 섹션 `Value`가 기준.

---

## 5. 권장 저장소 구조

```
/
├─ README.md                  # 설치(덮어쓰기)/제거 방법, 대상 버전, 알려진 문제
├─ KOREAN_PATCH_NOTES.md      # 이 문서
├─ LICENSE                    # 번역문·스크립트 라이선스
├─ .gitignore                 # *.dll *.exe *.assets *.resS level* 등
├─ Stationeers/                         # ← 이 폴더가 그대로 릴리스 zip 내용 (게임 폴더 구조)
│  ├─ rocketstation_Data/StreamingAssets/Language/korean*.xml   # 번역 5개
│  └─ 한국어패치_설치방법.txt
├─ Turing Complete/                     # ← 이 폴더가 그대로 릴리스 zip 내용
│  ├─ translations/Korean.txt
│  ├─ translations/Swedish.txt          # Korean.txt와 동일 (CI가 자동 복사·검증)
│  ├─ asset/font/NoroshiCode_*.ttf      # 라이선스 확인 후에만
│  └─ 한국어패치_설치방법.txt
├─ patcher/                             # 선택 패처 (zip에는 빌드 결과물만 포함)
│  ├─ patcher.py                        # 0-2장 "패처가 해야 할 일" 1~9 구현
│  ├─ compat.json                       # 확인된 게임 버전/해시 목록
│  └─ turing-complete/menu_label.json   # 시그니처 "Svenska (" → "한국어(Korean)"
├─ plugin/StationeersKorean/            # BepInEx 플러그인 소스 (C#, Harmony)
│  ├─ StationeersKorean.csproj
│  ├─ Plugin.cs                         # 로컬라이제이션 주입, 이름 치환, 문자열 치환
│  ├─ extra_keys.ko.json                # 기존 english.xml 추가 키 251개의 한국어 값
│  └─ data_names.ko.json                # Data XML 이름 번역
├─ reference/legacy_patch/              # 기존 오프셋 패치 기록(참고용, 배포 금지)
│  ├─ Assembly-CSharp.patch.json        # 8개 구역 오프셋/원래/변경 바이트 → 플러그인 구현 근거
│  └─ level1_strings.json
├─ tools/
│  └─ validate.py                       # 4-1, 4-2 자동 검사 + english.xml 대비 누락 키 출력
└─ .github/workflows/
   ├─ validate.yml                      # PR마다 validate.py 실행
   └─ release.yml                       # 태그 푸시 시 게임 폴더별 zip + 패처 exe 빌드 → Releases 업로드
```

### patcher.py 필수 동작
1. 게임 경로 입력/자동 탐지(Steam `libraryfolders.vdf`).
2. 수정할 모든 파일을 `_korean_patch_backup/<날짜>/`로 백업(이미 있으면 덮어쓰지 않음).
3. 바이너리 패치 대상의 원본 MD5·원래 바이트 확인 → 불일치 시 해당 패치만 건너뛰고 경고.
4. 번역 파일 복사, XML 삽입(멱등), 바이트 패치.
5. 적용 후 XML 파싱·키 개수·`Swedish==Korean` 검증.
6. 게임 실행 중이면 중단.

### validate.py (CI) 검사 항목
- 두 게임 번역 파일의 키/ID 집합이 영어 원문과 일치
- 모든 항목의 태그·변수 multiset이 영어 원문과 일치(원문 버그 수정 예외 목록 허용)
- 금지 문자 검사
- XML well-formed, CRLF(Stationeers)/LF(TC) 확인
- `Swedish.txt`와 `Korean.txt` 동일성

---

## 6. 미확인·배포 전 해결할 것 (TODO)

- [ ] Stationeers에서 BepInEx 5 + Harmony 동작 확인, 게임 자체 모드 로더와 충돌 여부 확인
- [ ] `Assembly-CSharp.dll` 8개 구역 IL 변경의 의도를 dnSpy/ILSpy로 확인 → 플러그인 Harmony 패치로 이식
- [ ] 로컬라이제이션 딕셔너리 로드 메서드 찾기 → `extra_keys.ko.json` 주입 지점 결정
- [ ] `resources.assets` 20바이트 증가의 원인 객체 확인 (필요 없으면 폐기)
- [ ] `level1` 39바이트 변경 문자열 전체 목록 추출 → 플러그인 치환 사전으로 이전
- [ ] 원본 상태(패치 전 백업)로 되돌린 게임 + 새 방식 설치로 전체 동작 테스트
- [ ] `startconditions.xml`, `level1`처럼 **영어 설정에서도 한국어가 보이는 변경**을 키 방식으로 바꿀 수 있는지 검토
- [ ] Turing Complete 교체 폰트의 한글 글리프 출처·라이선스 확인
- [ ] Turing Complete 게임 버전 문자열 확인 후 README에 기록
- [ ] 두 게임 실제 실행 화면에서 `° × – ‘ ’` 표시, 줄바꿈, 긴 문장 잘림 확인
- [ ] Stationeers 워크숍/모드 로더 방식(`StreamingAssets/Language`만 쓰는 순수 번역 모드)으로 분리 배포 가능한지 검토

---

## 7. 이번 검수에서 바뀐 내용 요약 (2026-09-29)

- Stationeers: 149개 항목 수정 — 가운뎃점 22곳 제거, 조사 오류 약 40곳, 오역(Apex, Tyre 등), 용어 통일, 번역투 정리.
- Turing Complete: 143개 항목 수정 — 조사 오류·병기 조사 제거, 오류 메시지 형식 통일, `%a/%b` 설명문 정리, 누락 줄바꿈 1곳·아이콘 2곳 복원, 가운뎃점 3곳 제거.
- 검수 전 파일 백업: 각 게임 폴더 `_korean_backup_before_review2/`.
- 이전 패치 백업: `_korean_patch_backup/`, `_korean_review_backup_20260929/` (원본 바이너리 포함 — 저장소에 올리지 말 것).
- `Stationeers/_translation_review_work/`: 분석용 임시 파일, 삭제 가능.
