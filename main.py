from splitwise import Splitwise
import config

s = Splitwise(config.consumer_key, config.consumer_secret,
              api_key=config.API_key)

u = s.getCurrentUser()
print(u.getId())
print(u.getFirstName())

