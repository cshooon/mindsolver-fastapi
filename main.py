from typing import List

import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from openai import AsyncOpenAI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel
import datetime

app = FastAPI()
load_dotenv('env/.env')

client = AsyncOpenAI(api_key=os.getenv('OPEN_API_KEY'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodayStampList(BaseModel):
    GoogleID: str
    dateTime: str
    stamp: str
    memoLet: str


class UserDto(BaseModel):
    GoogleID: str
    username: str
    age: int
    gender: str
    job: str


class User(BaseModel):
    UserDto: UserDto
    TodayStampList: List[TodayStampList]


@app.post("/diary")
async def test_gpt3(user: User):
    async def make_prompt(age, gender, job, memolet_list):

        d = datetime.datetime.now()
        date = f'{str(d.year % 100):0>2}.{str(d.month):0>2}.{str(d.day):0>2}'
        week = ['월', '화', '수', '목', '금', '토', '일']
        weekday = week[datetime.datetime.now().weekday()]

        let = ''
        for i in range(len(memolet_list)):
            date = memolet_list[i].dateTime.split('T')[0]
            let += f"{i + 1}. {date[:10]} {date[11:16]} {memolet_list[i].memoLet}\n"

        text = f"네가 작성할 일기의 조건은 아래와 같아.\n\
            # 조건 1 : 날짜, 제목, 키워드 5개가 포함된 일기를 작성할 것. 오늘 날짜는 {today_date} {weekday}요일임.\n\
            # 조건 2 : 반드시 아래 \'\'\'로 구분된 내용으로만 일기를 작성할 것. 과도한 추측은 하지 말것. 1.,2.,3.과 같이 구분된 각 내용들은 오늘 하루 있었던 일들이야. 구분된 내용들을 합쳐 하나의 글로 된 일기를 작성해줘. \n\
            # 조건 3 : 일기에 구체적인 시간은 절대 포함하지 마. 그리고 시간의 흐름만 반영해 일기를 과거형으로 써줘. 본문엔 숫자가 들어가선 안됨. 내용 간 개행 구분은 하지 않을 것. \n\
            # 조건 4 : 아래 \'\'\'로 구분된 내용의 글의 말투, 개조식 여부, 줄넘김, 문장부호, 말어미, 사용된 단어의 수준, …, ㅠㅠ와 같은 이모티콘 혹은 인터넷 축약어의 사용여부 등을 분석한 후에 동일한 스타일로 일기를 쓸 것. 이때 분석 결과는 작성하지 않을 것.\n\
            # 조건 5 : 일기의 제목은 [제목]으로 구분해 작성하고, 일기의 키워드도 [키워드]로 구분해 작성할 것. 일기 내용은 [일기]로, 오늘 날짜는 [날짜]로 구분할 것.\n\
            \'\'\'\n{let}\'\'\'"

        return text

    user_data = user.UserDto
    user_data = user.UserDto
    prompt = await make_prompt(user_data.age, user_data.gender, user_data.job,
                               user.TodayStampList)

    async def generator():
        await asyncio.sleep(0.01)
        stream = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": f"너는 {user_data.age}세 {user_data.gender} {user_data.job}의 입장에서 주어진 조건에 따라 일기를 쓰는 assistant야."},
                      {"role": "user", "content": f"너는 몇 개의 조건까지 완벽하게 일기에 적용할 수 있지?"},
                      {"role": "assistant", "content": "저는 주어진 조건에 따라 최대한 완벽하게 일기를 쓰려고 노력하지만,\
                        제한적인 지식과 경험으로 인해 모든 조건을 완벽하게 적용할 수는 없을 수도 있습니다.\
                        그래도 최대한 정확하고 적절한 일기를 쓰는 것을 목표로 노력하고 있습니다."},
                      {"role": "user", "content": "조건이 4개인 경우에는 완벽하게 일기에 적용하도록 해."},
                      {"role": "assistant", "content": "네, 알겠습니다."},
                      {"role": "user", "content": f"{prompt}"}
                      ],
            temperature=0.1,
            stream=True
        )
        async for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    return StreamingResponse(generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=9000)
