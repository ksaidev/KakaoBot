# KakaoBot
간단하게 요약하자면 https://github.com/pl-Steve28-lq/KakaoLink-For-Python + https://github.com/taejun281/kakaoPy + 알파

## Setup
pip install -r requirements.txt


## How to use

1. python test.py
2. 카카오톡 ID/PW 입력 후 대기
3. 카카오톡 실행 후 보안 인증번호 Passcode에 입력

## Formatter

Recommend formatter : autopep 

## Library
Standard library
User-defined
External

## 사용 예시

자세한 사용예시는 위키를 살펴봐 주세요

    if chat.message == ".삭제":
        await chat.deletemy(chat.attachment['src_logId'])

    if chat.message == "말":
        await chat.sendText("안녕")

    if chat.message[0:2] == "공지":
        self.postText(chat.chatId,0,chat.message[2:],True)

    if chat.type == 18:
        await chat.channel.sendChat("",json.dumps(chat.attachment),18)

    if chat.message == "태그":
        attachment = {'mentions': [{'user_id': chat.authorId, 'at': [1], 'len': 2}]}
        await chat.channel.sendChat("@태그",json.dumps(attachment),1) 

    if chat.message == "샵검색":
        attachment = {'I': '', 'H': 0, 'V': 'image', 'isExpress': True, 'L': r'https://m.search.daum.net/kakao?al=ON&https_on=on&q=%EC%83%B5%EA%B2%80%EC%83%89&va=5A977B44-FE60-476A-9F1D-7827B0B54CDA&w=tot&DA=SH1&rtmaxcoll=IIM', 'R': [{'L': r'https://m.search.daum.net/kakao?w=tot&q=%EC%83%B5%EA%B2%80%EC%83%89&DA=SH1&rtmaxcoll=IIM&SortType=accuracy#&gid=223&pid=333JdFqNLK3YkCU6M9', 'W': '600', 'H': '308', 'I': r'https://search4.kakaocdn.net/argon/600x0_65_wr/5Nag0JKwsb5'}], 'W': 0, 'Q': '샵검색'}
        await chat.channel.sendChat("",json.dumps(attachment),23) 

    if chat.message == "이모티콘":
        print("dfsdfs")
        attachment = {'name': '(이모티콘)', 'path': '4414234.emot_006.webp', 'type': 'image/webp', 's': 0, 'alt': '카카오 이모티콘'}
        await chat.channel.sendChat("",json.dumps(attachment),12) 

    if chat.message == "일정":
        attachment = {"개인정보 떄문에 삭재하였습니다"}
        await chat.channel.sendChat("",json.dumps(attachment),71) 
