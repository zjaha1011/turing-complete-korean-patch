# Turing Complete 한국어 패치 v2

현재 v2는 최종 게임 화면 검증을 기다리는 검토본이며 아직 릴리스되지 않았습니다. 기존 v1 ZIP에는 이 문서의 v2 설치 절차를 적용하지 마세요.

**번역과 폰트 폴더를 게임 폴더에 복사하면 한글화가 적용됩니다.** 원본 게임 실행 파일은 ZIP에 포함하지 않습니다.

대상: Windows Steam판 **2.1.334**. [패치 ZIP 다운로드](https://github.com/zjaha1011/turing-complete-korean-patch/releases/tag/v2.0.0)

## 설치 순서

1. 게임을 완전히 종료합니다.
2. 릴리스 Assets에서 `TuringComplete-Korean-v2.zip`을 받아 **게임 밖의 폴더**에 모두 압축을 풉니다.
3. Steam → 관리 → 로컬 파일 보기로 게임 폴더를 엽니다. `translations/Swedish.txt`, 기존 `translations/Korean.txt`가 있다면 그 파일, `asset/font/NoroshiCode_Regular.ttf`, `asset/font/NoroshiCode_Bold.ttf`를 별도 폴더에 백업합니다.
4. ZIP 안의 **Turing Complete 폴더 안에 있는 내용**을 실제 게임 폴더에 복사하고 파일 덮어쓰기를 선택합니다. `translations`와 `asset` 폴더를 모두 복사해야 합니다.
5. 게임 → **옵션 → 일반 → 언어**에서 **Svenska (3% done)**를 선택합니다. 스웨덴어 슬롯을 한국어로 대체하는 방식이므로 메뉴 이름이 Svenska여도 한국어가 나옵니다. 이미 메뉴 이름 보완을 적용했다면 **한국어(Korean)**를 선택합니다.

기본 경로: `C:\Program Files (x86)\Steam\steamapps\common\Turing Complete`

## 선택: 언어 메뉴 이름도 한국어로

게임을 종료한 뒤 압축을 풀어 둔 폴더에서 `KoreanPatcher.cmd --menu-only`를 실행합니다. 아래 공통 설치 도구 설명처럼 Python 3.10 이상이 필요합니다. 선택 기능이므로 실행하지 않아도 기본 번역은 작동합니다.

이 도구는 설치된 실행 파일에서 확인된 `Svenska (3% done)` 문자열 하나만 같은 17바이트 길이의 `한국어(Korean)`으로 바꿉니다. 원본/결과 해시, 문자열 개수와 길이가 맞아야 적용합니다. 모르는 버전, 문자열 중복·누락이면 건너뜁니다. 변경 전 원본 실행 파일은 사용자 PC에만 백업합니다.

## 제거

게임을 종료하고 백업한 번역·폰트를 복원하거나 Steam 무결성 검사를 실행하세요. 직접 추가한 `translations/Korean.txt`는 필요하면 게임 밖으로 옮기세요. 메뉴 이름을 도구로 적용했다면 `--uninstall`로 도구 백업을 복원할 수 있습니다. 세이브·회로 폴더는 건드리지 마세요.

## 폰트

한글 11,172자를 포함하는 **Noroshi Code 공식 원본 폰트**를 사용합니다. 게임이 찾는 파일 이름만 맞추었으며 폰트 파일 내부는 수정하지 않았습니다. OFL 라이선스를 함께 제공합니다. 원래 게임의 별도 아이콘 폰트는 유지합니다.

## 백업과 선택 설치 도구

복사하기 전에 위에서 안내한 파일을 별도 폴더에 백업하세요. 자동 백업을 원하면 수동 복사 대신, **게임 밖에 압축을 풀어 둔 위치**에서 `KoreanPatcher.cmd`를 실행할 수 있습니다. 이 도구에만 Python 3.10 이상이 필요하며, 기본 복사 설치에는 필요하지 않습니다.

도구는 Steam 설치 경로를 찾고, 게임이 실행 중이면 중단합니다. 원본은 게임 폴더의 `_korean_patch_backup/v2-날짜-고유번호/`에 저장하며 기존 백업은 덮어쓰지 않습니다. 결과는 `_korean_patch_state/v2/last-result.json`에 남습니다. 게임 경로를 못 찾으면 아래처럼 지정합니다.

```text
KoreanPatcher.cmd --game-path "실제 게임 설치 폴더"
KoreanPatcher.cmd --repair --game-path "실제 게임 설치 폴더"
KoreanPatcher.cmd --uninstall --game-path "실제 게임 설치 폴더"
```

`--repair`는 번역과 폰트 같은 기본 파일을 다시 설치합니다. 반드시 **새 ZIP을 게임 밖에 다시 풀고** 실행하세요. Steam이 바꾼 원본은 새 백업에 보관합니다. 추가 기능은 확인된 버전에서만 적용합니다. 실행 파일의 언어 메뉴 이름은 복구 모드에서 변경하지 않습니다.

`--uninstall`은 이 도구가 기록한 파일만 복원합니다. 설치 후 다른 프로그램이나 사용자가 바꾼 파일은 건너뜁니다. 수동으로 먼저 덮어쓴 파일은 패처가 원래 파일을 알 수 없으므로 자동 복원 대상이 아닙니다. 이때는 사전 백업 또는 Steam 무결성 검사를 사용하세요.

## 업데이트와 문제 해결

Steam 업데이트·무결성 검사가 번역과 폰트를 원본으로 바꿀 수 있습니다. 게임을 종료한 후 해당 버전용 새 ZIP을 다시 복사하거나 `--repair`를 실행하세요. 미확인 버전의 실행 파일에는 추가 바이너리 패치를 적용하지 않습니다.

이 패치는 비공식 번역입니다. 확인한 버전과 화면은 [검증 기록](COMPATIBILITY.md)에 구분해 적었습니다. 모든 진행 단계와 다른 모드 조합, 미래 업데이트까지 무오류를 보증하지 않습니다. 세이브·회로·설정 초기화 기능은 없습니다.

## 검증과 소스

`validate.py`는 영문 기준 키 목록, 변수·참조·태그, 금지 문자, 줄바꿈과 파일 구성을 검사합니다. 영어 게임 파일 전체는 저장소에 넣지 않고 키·형식 계약과 원본 해시만 보관합니다. 원문 자체의 잘못된 태그/참조를 고친 예외는 `contracts.json`에 키별 이유와 전후 형식을 명시했습니다.

```text
python -X utf8 validate.py
python -X utf8 -m unittest discover -p test_patcher.py -v
python -X utf8 package.py
```

`validate.py --english-dir "설치 게임의 원문 번역 폴더"`로 현재 게임의 새 키/삭제된 키도 비교할 수 있습니다. CI는 번역·패처를 검사하고 ZIP을 만듭니다. `v*` 태그를 푸시하면 같은 검사 후 릴리스를 생성합니다. 폰트·외부 구성요소의 출처는 [THIRD_PARTY.md](THIRD_PARTY.md)를 참고하세요.
