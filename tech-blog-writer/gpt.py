from openai import OpenAI
client = OpenAI()

# run this on CMD: setx OPENAI_API_KEY "your-api-key-here"

sample_system = "Summarize the provided Korean Sunday preaching script and convert it to Korean daily (from Monday to Saturday) 'Quite Time' material for young Christians (a high school student)."

sample_user = '''
2023년 12월 31일 주일예배
제목 : 하나님이 찾으시는 자들
  (요한복음 4장 23절 ~ 24절) 

말씀 선포 : 우리 다 같이 선포합시다. 하나님은 살아계십니다. 아멘. 2023년 마지막 날, 그리고 마지막 주일예배를 드릴 수 있게 되서 너무나 영광된 일이고 너무 또 감사한 일이다. 믿음으로 보면 우리가 살아내야 
하는 모든 그 삶이 우리의 삶의 전부로서의 현장이잖아요. 그런데 하나님을 믿는 믿음이 여도 그 삶의 질, 삶의 내용의 그 책임이 나의, 사람인 유한한 존재, 내가 하나님 안에서 열심히 살아내는 믿음의 단계가 
있다. 내가 책임지는 삶이에요. 그런데 아무리 하나님을 믿고 하나님을 알아도 
나는 제한적 존재인 육이기 때문에 직면하고, 당면한 매일의, 매 순간에 맞닥뜨리는 그 세상을, 나와의 직접적인 관계인 환경을 우리는 제한적 존재의 모습이기 때문에 초월할 수가 없는 거예요. 그래서 아무리 능력을 받아도 아주 초자연적인 체험과 성령의 은사적인 부분의 표적이 있어도 나, 육이라는 제한적 존재가 살아내야 하는 삶의 믿음의 단계 에서는 믿음, 하나님의 경험적 믿음도 있고, 환경, 더 넓은 의미는 세상, 
이 세상의 영적 의미는 세상을 다스리는 
사단 마귀란 말이죠. 그 영적 존재를 이겨낼 수 없는 두 주인을 섬기는 영적 모습의 이제 영적 상황이다. 라는 거를 알게 되는 거지요. 그런데 성경은 또 다른 믿음의 하나님의 계획 을, 말씀으로 성숙 안에서 보게 되어지는데 그것은 내가 살아내는 삶이 아니라 하나님이 살아주시는 삶, 다시 말해서 하나님께서 책임져 주시는 삶이 성경의 궁극의 믿음이고 이것을 약속하셨다. 라는 것을 말씀하는 거지요. 그래서 어떻게 하면 하나님이 우리 안에서 실제 되어지는, 하나님의 살아주심이 곧 나의 삶이 되어지는, 하나님의 의로우심이 곧 나의 의가 되는, 하나님의 이 놀라운 믿음 을 성경은 너무나 보증으로 우리에게 나타나 보여 주셨으니 이것이 계시로서의 말씀이라는 거예요.
'''

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": sample_system
    },
    {
      "role": "user",
      "content": sample_user
    }
  ],
  temperature=1,
  max_tokens=4096,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response.choices[0].message)