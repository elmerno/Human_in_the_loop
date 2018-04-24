import requests
import json

# Add Adjust localization to a mission
#task ={"action_type_id" : 8000, "mission_id" : "67f31783-004e-11e8-95bf-f44d306bb564"} 
#resp = requests.post('http://192.168.1.140:8080/v1.0.0/actions', json=task)

#get mission id
resp = requests.get('http://192.168.1.140:8080/v1.0.0/missions')

print resp.json()


#{u'url': u'/v1.0.0/missions/67f31783-004e-11e8-95bf-f44d306bb564', u'guid': u'67f31783-004e-11e8-95bf-f44d306bb564', u'name': u'adjust_localization'}

#{u'url': u'/v1.0.0/missions/3e64e7bf-8d7e-11e7-9193-f44d306bb564', u'guid': u'3e64e7bf-8d7e-11e7-9193-f44d306bb564', u'name': u'getting_pipes'}

#{u'url': u'/v1.0.0/missions/63ce173b-0055-11e8-95bf-f44d306bb564', u'guid': u'63ce173b-0055-11e8-95bf-f44d306bb564', u'name': u'handover_with_mir'}

