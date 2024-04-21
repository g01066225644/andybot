from AndybotMainService.ServiceList import AndyBot
from HelpUtil.DateTime import Datetime as dt
from Services.Fortune import Fortune

# 현재 날짜 조작
# dt.__force__(2024, 4, 10, 6, 10, 11)

print(Fortune.write())

#andy = AndyBot('test', False)
# andy.calendar('', 1)
# if not dt.is_fixed():
    # andy.personal_fortune('', 1)
    # andy.news('', 1)
    # andy.toss('', 1)

