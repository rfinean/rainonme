#
# getprediction.py, 18 Oct 2014
#

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import RequestHandler
import json
from json import loads
from urllib2 import urlopen
from datetime import datetime, date, timedelta

class GetPrediction(RequestHandler):
    def get(self):
        lat = self.request.get('lat')
        lon = self.request.get('lon')
#        lat = 51.508907
#        lon = -0.084054
        logging.info('Forecast for (%sN,%sE)', lat, lon)
        self.response.out.write(rain_prediction(lat, lon))

def download_json(url):
   weather = urlopen(url)
   string = weather.read()
   weather.close()
   return loads(string)

# See: http://www.gamedev.net/topic/489006-2d-distance-from-a-point-to-a-line-segment/
# for details of following calculation
def perp_dist(l_s, A_v, p_vec_lat, p_vec_long):
   t=(l_s['Lat']*p_vec_lat+l_s['Long']*p_vec_long) - A_v
   return t

def blow_weather(cur_lat_long, wind_dir, london_station):
   wind_from=(wind_dir+180) % 360
# degrees to km given by pi*6371/180, about 111km per degree
# assume strations within 55km, so 0.5 degree
   max_add_lonf=0.5
# Now calculate latitude offset for each quadrant
   if (wind_from < 90):
      add_long=max_add_long
      add_lat=max_add_long/tan(wind_from*pi/180)
   elif (wind_from < 180):
      add_long=max_add_long
      add_lat=-max_add_long*tan((wind_from-90)*pi/180)
   elif (wind_from < 270):
      add_long=-max_add_long
      add_lat=-max_add_long*tan((wind_from-180)*pi/180)
   else:
      add_long=-max_add_long
      add_lat=max_add_long/tan((wind_from-270)*pi/180)
# End points of line along which the wind blows
   a_lat=cur_lat_long[0]
   a_long=cur_lat_long[1]
   # b_lat=a_lat+add_lat
   # b_long=a_long+add_long
# See: http://www.gamedev.net/topic/489006-2d-distance-from-a-point-to-a-line-segment/
   ab_dist=sqrt(add_lat*add_lat+add_long*add_long)
   p_vec_lat=add_lat/ab_dist
   p_vec_long=add_long/ab_dist
   A_p=a_lat*p_vec_lat+a_long*p_vec_long
# Now Calculate perpendicular distance from every point to this line
   cur_min_station_dist=999
   weather_station=[]
   for l_s in london_station:
      c_dist=perp_dist(l_s, A_p, p_vec_lat, p_vec_long)
      if (c_dist < cur_min_station_dist):
         cur_min_station_dist=c_dist
         weather_station=l_s
   return weather_station

def rain_prediction(cur_lat, cur_lon):

   date_time=date.today()

# Not our actual key, don't want that to appear on github
   our_key='485014baf636a61b'


# Get list of weather stations around us
# Example from wunderground doc
# http://api.wunderground.com/api/485014baf636a61b/geolookup/q/37.776289,-122.395234.json

   loc_station_url=''.join(['http://api.wunderground.com/api/', our_key, '/geolookup/q/', str(cur_lat), ',', str(cur_long), '.json'])

#   print loc_station_url

# station_info=download_json(loc_station_url)
# our_locations=station_info['location']

# Now we have either 50 locations or all locations within 40km
# But all we know is their distance, not their location
# (do wunderground want people to use up their API call budget so they make more money?)

# Save on our daily limit of API calls by reusing data that is unlikely to change

   london_f = open('data/london-station.json')
   london_station=json.load(london_f)
   london_f.close()

# Find closest station to us
   cur_closest=99999
   close_station=[]
   for l_s in london_station:
      s_dist=abs(cur_lat-l_s['Lat'])+abs(cur_long-l_s['Long'])
      if (s_dist < cur_closest):
         cur_closest=s_dist
         close_station=l_s

   # print cur_closest, close_station

# http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KCASANTE9&graphspan=month&month=10&day=1&year=2012&format=1

#   closest_data = ''.join(['http://api.wunderground.com/api/', our_key, '/history_', date_time.strftime('%Y%m%d'), '/q/', l_s['id'], '.json'])

# Find station(s) from where the wind is blowing the rain our way
   # wind_dir=closest_data['wind_dir']

   # rain_from=blow_weather(cur_lat_long, wind_dir, london_station)

#   x,y=[],[]
#
#   data_url = ''.join(['http://api.wunderground.com/api/', our_key, '/history_', date_time.strftime('%Y%m%d'), '/q/TX/Addison.json'])
#   data = download_json(data_url)
#
#   for k in data['history']['observations']:
#      y0 = float(k['pressurem'])
#      if y0 < 0.0:
#         continue
#      else:
#         x.append(x1 + float(k['date']['hour'])+ round((float(k['date']['min'])/60.0),2))
#      y.append(y0)

# Test data
   rain_f = open('data/rainonme.json')
   rain_pred=json.load(rain_f)
   rain_f.close()

# Make the json data a viable javascript assignment!!!
   r_str=''.join(['plotData(', json.dumps(rain_pred), ');'])
   return r_str



application = webapp.WSGIApplication([('/getprediction', GetPrediction),
                                     ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
