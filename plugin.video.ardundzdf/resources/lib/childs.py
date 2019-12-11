# -*- coding: utf-8 -*-
################################################################################
#				childs.py - Teil von Kodi-Addon-ARDundZDF
#		Rahmenmodul für Kinderprg div. Regionalsender von ARD und ZDF
################################################################################
#	Stand: 10.11.2019
#
#	02.11.2019 Migration Python3 Modul future
#	17.11.2019 Migration Python3 Modul kodi_six + manuelle Anpassungen
#	

# Python3-Kompatibilität:
from __future__ import absolute_import		# sucht erst top-level statt im akt. Verz. 
from __future__ import division				# // -> int, / -> float
from __future__ import print_function		# PYTHON2-Statement -> Funktion
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs

# o. Auswirkung auf die unicode-Strings in PYTHON3:
from kodi_six.utils import py2_encode, py2_decode

import os, sys, subprocess
PYTHON2 = sys.version_info.major == 2
PYTHON3 = sys.version_info.major == 3
if PYTHON2:
	from urllib import quote, unquote, quote_plus, unquote_plus, urlencode, urlretrieve
	from urllib2 import Request, urlopen, URLError 
	from urlparse import urljoin, urlparse, urlunparse, urlsplit, parse_qs
elif PYTHON3:
	from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlencode, urljoin, urlparse, urlunparse, urlsplit, parse_qs
	from urllib.request import Request, urlopen, urlretrieve
	from urllib.error import URLError

import  json		
import os, sys
import ssl
import datetime, time
import re				# u.a. Reguläre Ausdrücke
import string

import ardundzdf					# -> ParseMasterM3u, transl_wtag
import resources.lib.util as util	# (util_imports.py)
PLog=util.PLog; home=util.home; check_DataStores=util.check_DataStores;  make_newDataDir=util. make_newDataDir; 
getDirZipped=util.getDirZipped; Dict=util.Dict; name=util.name; ClearUp=util.ClearUp; 
addDir=util.addDir; get_page=util.get_page; img_urlScheme=util.img_urlScheme; 
R=util.R; RLoad=util.RLoad; RSave=util.RSave; GetAttribute=util.GetAttribute; repl_dop=util.repl_dop; 
repl_char=util.repl_char; repl_json_chars=util.repl_json_chars; mystrip=util.mystrip; 
DirectoryNavigator=util.DirectoryNavigator; stringextract=util.stringextract; blockextract=util.blockextract; 
teilstring=util.teilstring; cleanhtml=util.cleanhtml; decode_url=util.decode_url; 
unescape=util.unescape; transl_doubleUTF8=util.transl_doubleUTF8; make_filenames=util.make_filenames; 
transl_umlaute=util.transl_umlaute; transl_json=util.transl_json; humanbytes=util.humanbytes; 
CalculateDuration=util.CalculateDuration; time_translate=util.time_translate; seconds_translate=util.seconds_translate; 
get_keyboard_input=util.get_keyboard_input; transl_wtag=util.transl_wtag; xml2srt=util.xml2srt; 
ReadFavourites=util.ReadFavourites; get_summary_pre=util.get_summary_pre; get_playlist_img=util.get_playlist_img; 
get_startsender=util.get_startsender; PlayVideo=util.PlayVideo; PlayAudio=util.PlayAudio; 



# Globals
ADDON_ID      	= 'plugin.video.ardundzdf'
SETTINGS 		= xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME    	= SETTINGS.getAddonInfo('name')
SETTINGS_LOC  	= SETTINGS.getAddonInfo('profile')
ADDON_PATH    	= SETTINGS.getAddonInfo('path')	# Basis-Pfad Addon
ADDON_VERSION 	= SETTINGS.getAddonInfo('version')
PLUGIN_URL 		= sys.argv[0]				# plugin://plugin.video.ardundzdf/
HANDLE			= int(sys.argv[1])

FANART = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/fanart.jpg')
ICON = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')

USERDATA		= xbmc.translatePath("special://userdata")
ADDON_DATA		= os.path.join("%sardundzdf_data") % USERDATA
DICTSTORE 		= os.path.join("%s/Dict") % ADDON_DATA			# hier nur DICTSTORE genutzt

NAME			= 'ARD und ZDF'
ICON 			= 'icon.png'		# ARD + ZDF
ICON_CHILDS		= 'childs.png'			
ICON_DIR_FOLDER	= "Dir-folder.png"
ICON_MEHR 		= "icon-mehr.png"

BASE_ZDF		= 'http://www.zdf.de'
BASE_KIKA 		= 'http://www.kika.de'
BASE_TIVI 		= 'https://www.zdf.de/kinder'


def Main_childs():
	PLog('Main_childs:')
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)			# Home-Button
		
	fparams="&fparams={'title': '%s'}" % "KIKA"
	addDir(li=li, label= "KIKA", action="dirList", dirID="resources.lib.childs.Main_KIKA", fanart=R('tv-kika.png'), 
		thumb=R(ICON_DIR_FOLDER), fparams=fparams)
		
	fparams="&fparams={'title': '%s'}" % "tivi"
	addDir(li=li, label= "tivi", action="dirList", dirID="resources.lib.childs.Main_TIVI", fanart=R(ICON_CHILDS), 
		thumb=R(ICON_DIR_FOLDER), fparams=fparams)


	xbmcplugin.endOfDirectory(HANDLE)
		
# ----------------------------------------------------------------------			
def Main_KIKA(title):
	PLog('Main_KIKA:')
	
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
		
	title='KIKA Live gucken'
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Kika_Live", fanart=R('tv-kika.png'),
		thumb=R(ICON_DIR_FOLDER), tagline='KIKA TV-Live', fparams=fparams)
	
	title='KiRaKa Live hören'
	fparams="&fparams={}" 
	addDir(li=li, label=title , action="dirList", dirID="resources.lib.childs.Kiraka_Live", fanart=R('tv-kika.png'),
		thumb=R(ICON_DIR_FOLDER), tagline=title, fparams=fparams)
		
	title='Videos und Bilder'
	fparams="&fparams={}" 
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Kika_VideosBuendel", fanart=R('tv-kika.png'),
		thumb=R(ICON_DIR_FOLDER), tagline=title, fparams=fparams)
		
	title='KiKANiNCHEN'	
	fparams="&fparams={}" 
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Kikaninchen_Menu", fanart=R('tv-kika.png'),
		thumb=R(ICON_DIR_FOLDER), tagline='für Kinder 3-6 Jahre', fparams=fparams)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
			
# ----------------------------------------------------------------------			
def Main_TIVI(title):
	PLog('Main_TIVI:')
	
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
			
	title='Sendungen der letzten 7 Tage'
	fparams="&fparams={}" 
	addDir(li=li, label=title , action="dirList", dirID="resources.lib.childs.Tivi_Woche", fanart=R(ICON_CHILDS), 
		thumb=R(ICON_DIR_FOLDER), tagline=title, fparams=fparams)
		
	title='Sendungen 0-9 | A-Z'
	fparams="&fparams={}" 
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Tivi_AZ", fanart=R(ICON_CHILDS), 
		thumb=R(ICON_DIR_FOLDER), tagline=title, fparams=fparams)

	#title='tivi-Tipps'
	#fparams="&fparams={'name': 'tivi-Tipps'}"
	#addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.TiviTip", fanart=R(ICON_CHILDS), 
	#	thumb=R(ICON_DIR_FOLDER), tagline=title, fparams=fparams)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------			
def Kikaninchen_Menu():
	PLog('Kikaninchen_Menu')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	title='Kikaninchen Videos'
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Kikaninchen_Videoseite", fanart=R(ICON_CHILDS), 
		thumb=R(ICON_DIR_FOLDER), tagline='für Kinder 3-6 Jahre', fparams=fparams)
	title='Kikaninchen Singen und Tanzen'
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.KikaninchenLieder", fanart=R(ICON_CHILDS), 
		thumb=R(ICON_DIR_FOLDER), tagline='für Kinder 3-6 Jahre', fparams=fparams)
	title='Kikaninchen Tonschnipsel'
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Tonschnipsel", fanart=R(ICON_CHILDS), 
		thumb=R(ICON_DIR_FOLDER), tagline='für Kinder 3-6 Jahre', fparams=fparams)
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------			

def Kika_Live():
	PLog('Kika_Live')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	import resources.lib.EPG as EPG
	m3u8link = 'https://kikade-lh.akamaihd.net/i/livetvkika_de@450035/master.m3u8'	# neu 07.12.2017
	
	ID = 'KIKA'
	title = 'KIKA TV-Live'
	Merk = ''
	
	rec = EPG.EPG(ID=ID, mode='OnlyNow')		# Daten holen - nur aktuelle Sendung
	PLog(rec)	# bei Bedarf
	if len(rec) == 0:							# EPG-Satz leer?
		title = 'EPG nicht gefunden'
		summ = ''
		tagline = ''
	else:	
		href=rec[1]; img=rec[2]; sname=rec[3]; stime=rec[4]; summ=rec[5]; vonbis=rec[6]
		if img.find('http') == -1:	# Werbebilder today.de hier ohne http://
			img = R('tv-kika.png')
		title 	= sname.replace('JETZT', ID)		# JETZT durch Sender ersetzen
		# sctime 	= "[COLOR red] %s [/COLOR]" % stime			# Darstellung verschlechtert
		# sname 	= sname.replace(stime, sctime)
		tagline = 'Zeit: ' + vonbis
				
	title = unescape(title)
	PLog("title: " + title); PLog(summ)
	title=py2_encode(title); m3u8link=py2_encode(m3u8link);
	img=py2_encode(img); summ=py2_encode(summ);			
	fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s', 'descr': '%s', 'Merk': '%s'}" %\
		(quote(m3u8link), quote(title), quote(img), quote_plus(summ), Merk)
	addDir(li=li, label=title, action="dirList", dirID="SenderLiveResolution", fanart=R('tv-EPG-all.png'), 
		thumb=img, fparams=fparams, summary=summ, tagline=tagline)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
# ----------------------------------------------------------------------			
def Kiraka_Live():
	PLog('Kiraka_Live')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	url	 	= 'https://wdr-edge-101c-dus-dtag-cdn.sslcast.addradio.de/wdr/diemaus/live/mp3/high'
	thumb 	= "https://www1.wdr.de/mediathek/audio/logo-kiraka100~_v-gseagaleriexl.jpg"
	Plot	= ''	
	title = 'KiRaKa Live hören'
	PLog(url)
	PlayAudio(url, title, thumb, Plot)  		# direkt
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
# ----------------------------------------------------------------------
# alle Videos - erst Bündelgruppen, Einzelvideos in Kika_Videos  		
def Kika_VideosBuendel(): 
	PLog('Kika_VideosBuendel:')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	path = 'https://www.kika.de/videos/allevideos/allevideos-buendelgruppen100.html'
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Kika_VideosBuendel:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
	PLog(len(page))	
	buendel = blockextract('teaser teaserIdent', page)	
	PLog(len(buendel))
	
	for s in 	buendel:			
		# PLog(s[0:40])		# bei Bedarf
		href =  BASE_KIKA + stringextract('href=\"', '\"', s)
		img = stringextract('<noscript>', '</noscript>', s).strip()		# Bildinfo separieren
		img_alt = stringextract('alt=\"', '\"', img)	
		img_src = stringextract('src="', '"', img)
		if img_src.startswith('http') == False:
			img_src = BASE_KIKA + img_src
		
		dachzeile = stringextract('<h4 class=\"headline\">', '</h4>', s)		
		headline = stringextract('page=artikel\">', '</a>', dachzeile).strip()	
		stitle = headline
		
		stitle = unescape(stitle); stitle = repl_json_chars(stitle)	
		img_alt = unescape(img_alt); 	
		
		PLog('Satz:')
		PLog(href);PLog(stitle);PLog(img_alt);PLog(img_src)
		href=py2_encode(href); stitle=py2_encode(stitle); img_src=py2_encode(img_src);
		
		if 'KiKA LIVE' in stitle:										# s. Main_KIKA
			continue
		else:				
			fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s'}" %\
				(quote(href), quote(stitle), quote(img_src))
			addDir(li=li, label=stitle, action="dirList", dirID="resources.lib.childs.Kika_Videos", fanart=img_src, 
				thumb=img_src, fparams=fparams, tagline=img_alt)
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
# ----------------------------------------------------------------------
# Kika-Videos eines Bündels aus Kika_VideosBuendel- enthält playerContainer() der Plex-Version
def Kika_Videos(path, title, thumb):
	PLog('Kika_Videos:')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Kika_Videos:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	if page.find('dataURL:') < 0:		  # ohne 'dataURL:' - ohne kein Link zu xml-Seite, also keine Videos.
		msg1 = "Leider kein Video gefunden zu:"
		msg2 = title
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	videos = blockextract('class="av-playerContainer"', page)
	PLog(len(videos))
	for s in videos:					
		href = ref = stringextract('dataURL:\'', '\'}', s)					# Link Videodetails  (..avCustom.xml)
		# PLog(href);   # PLog(s);   # Bei Bedarf
		img = stringextract('<noscript>', '</noscript>', s).strip()			# Bildinfo separieren
		img_alt = stringextract('alt=\"', '\"', img)	
		img_alt = unescape(img_alt)	
		img_src = stringextract('src="', '"', img)
		if img_src.startswith('http') == False:
			img_src = BASE_KIKA + img_src

		stitle = stringextract('title="', '"', s)
		duration = stringextract('icon-duration">', '</span>', s)	
		tagline = duration + ' Minuten'	
		
		stitle = unescape(stitle); stitle = repl_json_chars(stitle)	
		img_alt = unescape(img_alt); 	
			
		PLog('Satz:')		
		PLog(href);PLog(stitle);PLog(img_alt);PLog(img_src);
		PLog(tagline); 
		href=py2_encode(href); stitle=py2_encode(stitle); img_src=py2_encode(img_src); img_alt=py2_encode(img_alt);
		fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s', 'summ': '%s', 'duration': '%s'}" %\
			(quote(href), quote(stitle), quote(img_src), quote(img_alt), quote(duration))
		addDir(li=li, label=stitle, action="dirList", dirID="resources.lib.childs.SingleBeitragKika", fanart=img_src, 
			thumb=img_src, fparams=fparams, tagline=img_alt)
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
					
# ----------------------------------------------------------------------
# Kikaninchen - Seitenliste Sendungsvideos  			
def Kikaninchen_Videoseite():
	PLog('Kikaninchen_Videoseite')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	path = 'https://www.kika.de/kikaninchen/sendungen/videos-kikaninchen-100.html'
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Kikaninchen_Videoseite:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	items = stringextract('class="bundleNaviItem active"', '</span>', page) # Buchstabenblock
	items = blockextract('bundleNaviItem ">', items)		# nur aktive Buchstaben
	
	for s in items:	
		PLog(s)
		seite =  stringextract('title="">', '</a>', s).strip()
		# PLog(seite)
		title = 'Kikaninchen Videos: Seite ' + seite
		tag = 'Seite ' + seite
		# img_src = R('Buchstabe_%s.png' % (seite))			# entf. aus Platzgründen
		img_src = R(ICON_DIR_FOLDER)
		href = BASE_KIKA + stringextract('href="', '"', s)
		
		PLog(href); PLog(title); PLog(img_src)
		href=py2_encode(href); 		
		fparams="&fparams={'path': '%s'}" % (quote(href))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Kikaninchen_Videos", fanart=img_src, 
			thumb=img_src, fparams=fparams, tagline=tag)
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------
# Kikaninchen - Sendungsvideos, mehrere Seiten - ermittelt die Videos
#	zu einer einzelnen (Buchstaben-)Seite
#	zusammengelegt mit 	playerContainer() der Plexversion	
def Kikaninchen_Videos(path):
	PLog('Kikaninchen_Videos')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Kikaninchen_Videos:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	videos =  blockextract('class="av-playerContainer"', page)	# 16 pro Seite
	PLog(len(videos))
	
	for s in videos:					 # stringextract('', '', s)
		href = ref = stringextract('dataURL:\'', '\'}', s)					# Link Videodetails  (..avCustom.xml)
		PLog(href);   # PLog(s);   # Bei Bedarf
		img = stringextract('<noscript>', '</noscript>', s).strip()			# Bildinfo separieren
		img_alt = stringextract('alt="', '"', img)	
		img_alt = unescape(img_alt)	
		img_src = stringextract('src="', '"', img)
		if img_src.startswith('http') == False:
			img_src = BASE_KIKA + img_src
		stitle = stringextract('title="', '"', s)
		stitle = unescape(stitle)	
		duration = stringextract('icon-duration">', '</span>', s)	
		tagline = duration + ' Minuten'	
		
		PLog(href); PLog(stitle); PLog(img_src); PLog(img_alt)
		href=py2_encode(href); 		
		href=py2_encode(href); stitle=py2_encode(stitle); img_src=py2_encode(img_src); img_alt=py2_encode(img_alt);
		fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s', 'summ': '%s', 'duration': '%s'}" %\
			(quote(href), quote(stitle), quote(img_src), quote(img_alt), quote(duration))
		addDir(li=li, label=stitle, action="dirList", dirID="resources.lib.childs.SingleBeitragKika", fanart=img_src, 
			thumb=img_src, fparams=fparams, tagline=tagline)
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
# ----------------------------------------------------------------------			
# 18.06.2017: KikaninchenLieder ersetzt die Kikaninchen Kramkiste (xml-Seite mit mp3-Audioschnipsel, abgeschaltet)
# 	Unterseite 'Singen + Tanzen' von http://www.kikaninchen.de/index.html?page=0
def KikaninchenLieder():	
	PLog('KikaninchenLieder')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	path = 'https://www.kikaninchen.de/kikaninchen/lieder/liederkikaninchen100.json'	
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Kikaninchen_Videos:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
			
	records = page.split('documentCanvasId')
	PLog(len(records))						
	
	for rec in records:
		href = stringextract('avCustomUrl":"', '"', rec)
		if href == '':
			continue					
		img_src = stringextract('urlScheme":"', '**imageVariant**', rec)
		PLog(img_src)
		img_src = 'http://www.kikaninchen.de' + img_src + 'ident.jpg'		# ident = 800x800
		title = stringextract('title":"', '"', rec)
		altText =  stringextract('altText":"', '"', rec)
		titleText =  stringextract('titleText":"', '"', rec)
		summ = ''
		if altText:
			summ = altText
		if summ == '':
			summ = titleText
							
		PLog(href); PLog(title); PLog(img_src); PLog(summ)
		href=py2_encode(href); title=py2_encode(title); img_src=py2_encode(img_src); summ=py2_encode(summ);
		fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s', 'summ': '%s', 'duration': ''}" %\
			(quote(href), quote(title), quote(img_src), quote(summ))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.SingleBeitragKika", fanart=img_src, 
			thumb=img_src, fparams=fparams, tagline=summ)
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------			
# Tonschnipsel aus verschiedenen Seiten
def Tonschnipsel():	
	PLog('Tonschnipsel')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button

	mp3_links =  [
		'kikaninchen = http://www.kikaninchen.de/kikaninchen/teaseraudio320-play.mp3',
		'Gitarre = http://www.kikaninchen.de/static_kkn/global/clickons/sounds/Gitarre_1.mp3',
		'Trompetenaffe =  http://www.kikaninchen.de/static_kkn/global/clickons/sounds/Trompetenaffe.mp3',
		'Frosch winkt = http://www.kikaninchen.de/static_kkn/global/clickons/sounds/Froschwinkt2_01.mp3?1493048916578',
		'Malfrosch =  http://www.kikaninchen.de/static_kkn/global/clickons/sounds/malfrosch1.mp3?1493048916578',
		'Grunz =  http://www.kikaninchen.de/static_kkn/global/clickons/sounds/grunz.mp3?1492871718285',
		'Huhu = http://www.kikaninchen.de/static_kkn/global/clickons/sounds/huhu.mp3?1493022362691',
		'Schnippel = http://www.kikaninchen.de/static_kkn/global/clickons/sounds/schnippel.mp3?1493022362691',
		'Klacker = http://www.kikaninchen.de/static_kkn/global/clickons/sounds/dices.mp3?1492868784119', 
			#Kurzlieder von http://www.kikaninchen.de/kikaninchen/lieder/liederkikaninchen100.json:
		'Lieder	= http://www.kikaninchen.de/kikaninchen/lieder/teaseraudio288-play.mp3',
		'La, la, la = http://www.kikaninchen.de/kikaninchen/lieder/hilfeaudio104-play.mp3',
		'Haha, toll - so viele lustige Lieder = http://www.kikaninchen.de/kikaninchen/lieder/hilfeaudio106-play.mp3',
		'Höre dir Lieder an und singe mit! = http://www.kikaninchen.de/kikaninchen/lieder/hilfeaudio102-play.mp3',
		'Ja, lass uns singen und dazu tanzen! = http://www.kikaninchen.de/kikaninchen/lieder/hilfeaudio100-play.mp3',		
		]
	PLog(len(mp3_links))
	
	for link in mp3_links:
		title = link.split('=')[0].strip()
		url = link.split('=')[1].strip()

		PLog(url);PLog(title);
		thumb=R('radio-podcasts.png')
		fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': ''}" % (quote(url), 
			quote(title), quote(thumb))
		addDir(li=li, label=title, action="dirList", dirID="PlayAudio", fanart=thumb, thumb=thumb, fparams=fparams, 
			summary=title, mediatype='music')
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ######################################################################			
# einzelnes Video - xml-Seite
def SingleBeitragKika(path, title, thumb, summ, duration):
	PLog('SingleBeitragKika: ' + path)
	title_call = title
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in SingleBeitragKika:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	summ1 = stringextract('<broadcastDescription>', '</', page)
	summ2 = stringextract('<topline>', '</', page)
	summ = summ1 + ' ' + summ2
	Plot_par = summ
	
	assets = blockextract('<asset>', page)
	url_m3u8 = stringextract('<adaptiveHttpStreamingRedirectorUrl>', '</', page) # x-mal identisch
	sub_path = ''
	if 'master.m3u8' in url_m3u8:	
		# 04.08.2019 Sofortstart nur noch abhängig von Settings und nicht zusätzlich von  
		#	Param. Merk.
		if SETTINGS.getSetting('pref_video_direct') == 'true': # or Merk == 'true':	# Sofortstart
			PLog('Sofortstart: SingleBeitragKika')
			PLog("Plot_par: " + Plot_par)
			PlayVideo(url=url_m3u8, title=title_call, thumb=thumb, Plot=Plot_par, sub_path=sub_path)
			xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
			
		title = u'[m3u8] Bandbreite und Auflösung automatisch'
		#   "auto"-Button + Ablage master.m3u8:
		li = ardundzdf.ParseMasterM3u(li=li, url_m3u8=url_m3u8, thumb=thumb, title=title, tagline='', descr=Plot_par,
			sub_path='')	
	
	download_list = []		# 2-teilige Liste für Download: 'Titel # url'	
	for s in assets:
		# Log(s)			# bei Bedarf
		frameWidth = stringextract('<frameWidth>', '</frameWidth>', s)	
		frameHeight = stringextract('<frameHeight>', '</frameHeight>', s)
		url_mp4 = stringextract('<progressiveDownloadUrl>', '</', s)
		bitrate =  stringextract('<bitrateVideo>', '</', s)	
		profil =  stringextract('<profileName>', '</', s)	
		resolution = frameWidth + 'x' + frameHeight
									
		title = profil 
		download_list.append(title + '#' + url_mp4)			# Download-Liste füllen	
		tagline	 = Plot_par.replace('||','\n')				# wie m3u8-Formate

		PLog('Satz:')
		PLog(title); PLog(url_mp4); PLog(thumb); PLog(Plot_par);
		title_call=py2_encode(title_call)
		title=py2_encode(title); url_mp4=py2_encode(url_mp4);
		thumb=py2_encode(thumb); Plot_par=py2_encode(Plot_par); 
		fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': '%s', 'Merk': ''}" %\
			(quote_plus(url_mp4), quote_plus(title_call), quote_plus(thumb), 
			quote_plus(Plot_par), quote_plus(sub_path))	
		addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=thumb, thumb=thumb, fparams=fparams, 
			mediatype='video', tagline=summ) 
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------			
def Tivi_Woche():
	PLog('Tivi_Woche')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	wlist = range(0,8)							# tivi zeigt Sendungen für 8 Tage
	now = datetime.datetime.now()
	img_src = R(ICON_DIR_FOLDER)

	for nr in wlist:
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%d.%m.%Y")			# Formate s. man strftime (3)
		punkte = '.'
		iWeekday = ardundzdf.transl_wtag(rdate.strftime("%A"))
		tiviDate = "%s, %s" % (iWeekday, iDate) 	# Bsp. Freitag, 08.09.2017 	
		if nr == 0:
			iWeekday = 'Heute'	
		if nr == 1:
			iWeekday = 'Gestern'	
		
		# Log(iDate); Log(iWeekday); Log(tiviDate)
		#title = ("%10s ..... %10s"% (iWeekday, iDate))	 # Formatierung in Plex ohne Wirkung
		title = iDate + ' | ' + iWeekday	 # Bsp.: 07.07.2016 | Freitag 
		PLog(tiviDate); PLog(title); 
		tiviDate=py2_encode(tiviDate); title=py2_encode(title);		
		fparams="&fparams={'day': '%s', 'title': '%s'}" % (quote(tiviDate), quote(title))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Tivi_Woche_Sendungen", fanart=img_src, 
			thumb=img_src, fparams=fparams, tagline=title)
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------			
def Tivi_Woche_Sendungen(day, title):
	PLog('Tivi_Woche_Sendungen: ' + day)
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
		
	path = 'https://www.zdf.de/kinder/sendung-verpasst' 	# kompl. Woche						
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Tivi_Woche_Sendungen:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	page = stringextract('data-plusbar-title="Sendungen der letzten 7 Tage"', '>Direkt zu ...</h2>', page)
	PLog(len(page))
	day_area = blockextract('class="cluster-title-wrap">', page)	# Sendungsblöcke nach Tagen
	PLog(len(day_area))
	
	for singleday in day_area:			
		# PLog(s)  # bei Bedarf
		page_day =  stringextract('cluster-title"', '</h2>', singleday) # Blank vor leading '>' möglich
		page_day = cleanhtml(page_day)
		page_day = (page_day.replace('(heute)', '').replace('(gestern)', ''))
		page_day = page_day.strip()	
		page_day = page_day.replace('>', '')
		PLog(page_day); #PLog(day);	
		if page_day == day:									# Abgleich Tag
			PLog('found: ' + page_day)
			sendungen = blockextract('class="b-cluster-teaser', singleday)
			PLog(len(sendungen))		
			li = get_tivi_details(li, sendungen, path)	# Sendungsdetails holen				

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------
# Themen- und Sendungstipps von der Leitseite. 
#	14.09.2017: die Tipp-Rubriken verändern sich. Daher nur 1 Button ('tivi-Tipps') im Hauptmenü, der Rest 
#		wird hier dynamisch generiert
#	03.02.2018: Teaser-Videos vorangestellt	
#	11.12.2019 nur noch Einzelvideos auf BASE_TIVI gefunden, key und ID entfallen

#TODO BASE_TIVI behandeln wie ZDF Startseite
def TiviTip(name):					
	PLog('TiviTip: ' + name)		
	
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button

	path = BASE_TIVI			
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in TiviTip:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
	PLog(len(page))
	
	records =  blockextract('class="artdirect">', page)
	if len(records) == 0:	
		msg1 = "Leider kein Video gefunden zu:"
		msg2 = name
		msg3 = path
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, msg3)	
		return li
	
	PLog(len(records))
	li = get_tivi_details(li, sendungen=records, path=BASE_TIVI)		

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------
# Auflistung 0-9 (1 Eintrag), A-Z (einzeln) 			
def Tivi_AZ():
	PLog('Tivi_AZ')
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	azlist = list(string.ascii_uppercase)
	azlist.insert(0, '0-9')

	for element in azlist:	
		# PLog(element)
		button = element
		title = "Sendungen mit " + button
		#img_src = "Buchstabe_%s.png"  % button
		img_src = R(ICON_DIR_FOLDER)
		PLog(img_src)
		button=py2_encode(button); title=py2_encode(title);		
		fparams="&fparams={'name': '%s', 'char': '%s'}" % (quote(title), quote(button))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Tivi_AZ_Sendungen", fanart=img_src, 
			thumb=img_src, fparams=fparams, tagline=title)
 
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ----------------------------------------------------------------------			
# Alle Sendungen, char steuert Auswahl 0-9, A-Z
def Tivi_AZ_Sendungen(name, char=None):	
	PLog('Tivi_AZ_Sendungen'); PLog(char)
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	char_tmp = char
	if char_tmp == '0-9':
		char_tmp = '0+-+9'
	path = 'https://www.zdf.de/kinder/sendungen-a-z?group=%s'	% char_tmp
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Tivi_AZ_Sendungen:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	page = stringextract('class="b-content-teaser-list"', '>Direkt zu ...</h2>', page)
	PLog(len(page))
	sendungen = blockextract('class="artdirect', page)
	PLog(len(sendungen))
	if len(sendungen) == 0:	
		msg1 = "Leider kein Video gefunden zu:"
		msg2 = name
		msg3 = path
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, msg3)	
		return li
	
	li = get_tivi_details(li, sendungen, path)	# Sendungsdetails holen				
							
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
# ----------------------------------------------------------------------			
# ermittelt Sendungsdetails wie href, title, img_src usw.
#	für Tivi_AZ_Sendungen,  Tivi_SinglePage, Tivi_Woche_Sendungen
#	Blocktrenner i.d.R. class="artdirect">
# Kodiversion ohne Beschränkung der Satzzahl
def get_tivi_details(li, sendungen, path):			# path für Abgleich Quelle/Ziel
	PLog('get_tivi_details'); 
	PLog(len(sendungen))
	send_path =  path	# sichern
	
	for s in sendungen:
		multi = True				# steuert Mehrfachergebnisse 
		duration=''; cnt=''; 
			
		if "icon-502_play" in s:	# Kamerasymbol
			multi = False
			duration = stringextract('m-border">', '</dd>', s)	# Bsp. m-border">24 min</dd>
			
		plusbar_url = stringextract('data-plusbar-url="', '"', s)
		plusbar_url  = plusbar_url.replace('https', 'http')   # variert
		path  = send_path.replace('https', 'http')
		PLog(path);PLog(plusbar_url)
		if plusbar_url == '' or plusbar_url == path: # leeren oder rekursiven Satz verwerfen
			continue
		
		img_src = stringextract('data-srcset="', ' ', s)		# 1. Bild
		if img_src.startswith('/'):
			img_src = BASE_ZDF + img_src						# insbes. Fallbackimage ohne Base
		img_alt = 'Bild: ' + stringextract('alt="', '"', s)		# wird tag
		category = stringextract('cat-category">', '</span>', s)
		brand = stringextract('cat-brand">', '</span>', s)
		category = category.strip(); brand = brand.strip(); 	
		
		if u'Beiträge</dd>'	in s:
			cnt = stringextract('teaser-info  m-border">', ' ', s) # nur Zahl holen

		href = BASE_ZDF + stringextract('href="', '"', s)	
		stitle = stringextract('title="', '"', s)
		if category:
			if "ZDFtivi" not in category:
				stitle = "%s | %s"  % (category, stitle)
		if brand:
			stitle = "%s | %s"  % (brand, stitle)
			
		summ = stringextract('itemprop="description">', '<', s)
		if summ == '':
			summ = stringextract('data-plusbar-title="', '"', s)
		summ = summ.strip(); summ = unescape(summ)
		stitle = cleanhtml(stitle)
		stitle = unescape(stitle); stitle = stitle.strip()
		
		PLog('neu:');PLog(multi);PLog(duration);PLog(img_alt);PLog(category);PLog(brand)
		PLog(cnt);PLog(stitle);PLog(summ);PLog(href);PLog(img_src)
		
		if multi:	# Mehrfachseite - wieder hierher
			if cnt:
				stitle = ' %s Beiträge | %s' % (cnt, stitle)
			summ = 'Folgeseiten'				
		
			stitle=py2_encode(stitle); href=py2_encode(href)
			fparams="&fparams={'path': '%s', 'title': '%s'}" %\
				(quote(href), quote(stitle))
			addDir(li=li, label=stitle, action="dirList", dirID="resources.lib.childs.Tivi_SinglePage", fanart=img_src,  
				thumb=img_src, fparams=fparams, summary=summ, tagline=img_alt)					
									
		else:		# direkt zum Beitrag
			if duration:
				stitle = stitle + ' | ' + duration
			stitle=py2_encode(stitle); href=py2_encode(href); 
			img_alt=py2_encode(img_alt); img_src=py2_encode(img_src);	
			fparams="&fparams={'path': '%s', 'title': '%s', 'tagline': '%s', 'thumb': '%s'}" %\
				(quote(href), quote(stitle), quote(img_alt), quote(img_src))
			addDir(li=li, label=stitle, action="dirList", dirID="resources.lib.childs.SingleBeitragTivi", fanart=img_src, 
				thumb=img_src, fparams=fparams, summary=summ, tagline=img_alt)					
					
								
	return li

# ----------------------------------------------------------------------
# 1 oder mehrere Videos / Fotoalben (letztere leider hier nicht gekennzeichnet) 
#	07.09.2017 völlig neu	
# 	ID + key: aus TiviTip, ID='TiviTip', key='tip' (enthält Sendungen-Ausschnitt)
# Kodiversion ohne Beschränkung der Satzzahl
#
def Tivi_SinglePage(title, path, ID=None, key=None):	
	PLog('Funktion Tivi_SinglePage: ' + path); PLog(str(ID)); PLog(key)

	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
		
	if ID == 'TiviTip':
		records = Dict("load", ID)				# records laden
		page = records[int(key)]				# Ausschnitt. Bei Bedarf mit 'data-tracking=' begrenzen
		PLog(page[0:80])	
	else:			
		page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in Tivi_SinglePage:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		 
	PLog(len(page))
					
	# class="artdirect">: 1 oder mehrere Sendungen, Videos + Folgeseiten				
	items = blockextract('class="artdirect', page)
	PLog(len(items))
	sendungen = []
	for item in items:
		if "icon-502_play" in item:				# Videobeiträge filtern
			sendungen.append(item)
	PLog("sendungen: %s " % len(sendungen))
	li = get_tivi_details(li, sendungen, path)	# Sendungsdetails holen				
							
	PLog(len(sendungen))
	if len(sendungen) == 0:	# keine Sendung / kein Ausschnitt vorhanden
		msg1 = 'Oh, ein Problem - kann keine Sendung zu >%s< finden.' % (title)
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, '', '')	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

			
# ----------------------------------------------------------------------			
# ######################################################################			
# Einzelbeitrag mit Url zu den Midianquellen + apiToken (ZDF-entsprechend)
def SingleBeitragTivi(path, title, tagline, thumb):
	PLog('SingleBeitragTivi: ' + path)
	title_call = title
	li = xbmcgui.ListItem()
	li = home(li, ID='Kinderprogramme')			# Home-Button
	
	page, msg = get_page(path)	
	if page == '':	
		msg1 = "Fehler in SingleBeitragKika:"
		msg2 = msg
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, msg2, '')	
		return li
		
	stitle = title											
	summ = stringextract('description" content="', '"', page)	
	img_src = stringextract('image" content="', '"', page)		
	duration =  stringextract('teaser-info m-border">', '</dd>', page)			
	PLog(img_src);PLog(duration)

	profile_url = stringextract('"content": "', '"', page)
	apiToken1 = stringextract('apiToken: \'', '\'', page) 
	apiToken2 = stringextract('"apiToken": "', '"', page)
	sid = stringextract("docId: \'", "\'", page)				# Bereich window.zdfsite
	PLog("profile_url: " + profile_url); 
	PLog('apiToken1: ' + apiToken1); 
	PLog('apiToken2: ' + apiToken2)
	PLog(sid)
	
	# Video-URL's ermitteln -> ZDF-Funktionen im Haupt-PRG:
	formitaeten,duration,geoblock, sub_path = ardundzdf.get_formitaeten(sid, apiToken1, apiToken2)	
	if formitaeten == '':				# get_formitaeten: if videodat == ''		
		msg1 = 'Oh, ein Problem - kann kein Video zu >%s< finden.' % (title)
		xbmcgui.Dialog().ok(ADDON_NAME, msg1, '', '')	
		return li

	only_list = ["h264_aac_ts_http_m3u8_http"]
	li, download_list = ardundzdf.show_formitaeten(li=li, title_call=title_call, formitaeten=formitaeten, tagline=tagline,
		thumb=thumb, only_list=only_list, geoblock=geoblock, sub_path=sub_path)			  
	if 	download_list == '':	# Sofortstart erfolgt, raus
		return	  
		
	if SETTINGS.getSetting('pref_use_downloads'):				# Video-Items erstellen: weitere Formate
		title_oc = "[COLOR blue]weitere Video-Formate und Downloads[/COLOR] | %s" % title
	else:	
		title_oc = u"[COLOR blue]weitere Video-Formate[/COLOR] | %s" % title
	PLog("title_oc: " + title_oc)
		
	PLog(title); PLog(title_oc);  
	if SETTINGS.getSetting('pref_video_direct') == 'false':	# ZDFotherSources nicht bei Sofortstart zeigen
		# li = Parseplaylist(li, videoURL, thumb)	# hier nicht benötigt - das ZDF bietet bereits 3 Auflösungsbereiche
		title=py2_encode(title); tagline=py2_encode(tagline); thumb=py2_encode(thumb);
		fparams="&fparams={'title': '%s', 'tagline': '%s', 'thumb': '%s', 'sid': '%s', 'apiToken1': '%s', 'apiToken2': '%s'}" \
			% (quote(title), quote(tagline), quote(thumb), sid, apiToken1, apiToken2)
		addDir(li=li, label=title_oc, action="dirList", dirID="ZDFotherSources", fanart=thumb, thumb=thumb, fparams=fparams)
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	












