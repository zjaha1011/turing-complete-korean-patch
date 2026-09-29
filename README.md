# Turing Complete 한국어 패치

**압축을 풀고 게임 폴더에 복사하면 되는 패치입니다. 설치 프로그램이나 명령어 실행은 필요 없습니다.**

- 대상: Windows Steam판 **2.1.334**
- 패치 날짜: 2026년 9월 29일
- [패치 ZIP 다운로드](https://github.com/zjaha1011/turing-complete-korean-patch/releases/latest)

번역문, 한글 글꼴, 언어 선택 표시 수정이 함께 들어 있습니다. 별도 선행 한글 패치가 필요하지 않습니다. Swedish 언어 칸을 한국어로 사용하는 방식이므로 이 패치를 쓰는 동안 해당 칸은 한국어로 동작합니다.

## 설치 순서

1. **게임을 완전히 종료합니다.**
2. 위의 **패치 ZIP 다운로드**를 열고 **Assets**에서 `turing-complete-korean-patch-2026-09-29.zip`을 받습니다. **Source code** ZIP은 패치 파일이 아닙니다.
3. 받은 ZIP을 **모두 압축 풀기**로 해제합니다.
4. Steam 라이브러리에서 게임을 우클릭하고 **관리 → 로컬 파일 보기**를 누릅니다. 기존 파일로 되돌릴 수 있도록 아래 파일 목록에 해당하는 원본을 먼저 별도 폴더에 복사해 두세요.
5. 압축을 푼 파일 중 **Turing Complete** 폴더 안의 **asset**, **translations**, **Turing Complete.exe**를 모두 게임 설치 폴더에 복사합니다. 같은 파일이 있다는 창이 나오면 **대상 폴더의 파일 덮어쓰기**를 선택합니다. 기존 게임 폴더를 삭제하지 말고 합쳐 넣으세요.
6. 게임을 실행합니다. Settings → General → Language에서 **한국어(Korean)** 또는 **Korean**을 선택합니다. 언어를 변경했다면 게임을 종료한 뒤 다시 실행합니다.

기본 설치 폴더는 `C:\Program Files (x86)\Steam\steamapps\common\Turing Complete`입니다. 파일을 게임 이름의 폴더 안에 한 번 더 중첩해서 넣지 않도록 주의하세요. 예를 들어 `...\Turing Complete\Turing Complete\...` 형태로 넣는 것은 잘못된 위치입니다.

세이브와 진행 데이터는 포함하지 않으며 덮어쓰지 않습니다. 저장소에는 이 안내와 패치 ZIP만 올립니다. 전체 게임은 Steam에서 별도로 설치해야 합니다.

## 복원 방법

게임을 종료한 뒤 미리 복사해 둔 원본 파일을 같은 위치에 덮어쓰면 됩니다. 백업이 없으면 Steam의 **속성 → 설치된 파일 → 게임 파일 무결성 검사**로 원본 게임 파일을 다시 받을 수 있습니다. 단, 패치가 추가한 `Korean.txt` 같은 파일은 검사 후에도 남을 수 있습니다.

## 버전 안내

이 패치는 위 게임 버전에서 검수하고 실행 확인했습니다. 다른 버전에는 맞지 않을 수 있습니다. Steam 업데이트나 무결성 검사 후 패치가 해제되면 해당 게임 버전에 맞는 패치가 필요합니다. 비공식 한국어 패치이며 공식 배포본은 아닙니다.

## 덮어쓰는 파일

아래 경로는 게임 설치 폴더를 기준으로 합니다.

- `translations/Korean.txt`
- `translations/Swedish.txt`
- `Turing Complete.exe`
- `asset/font/NoroshiCode_Regular.ttf`
- `asset/font/NoroshiCode_Bold.ttf`
