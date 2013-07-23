#!/usr/bin/env python
# -*- coding: utf-8 -*-

class YMReader():  
	'''YMReader - is free redistributable library for work with Yandex Metrics API
	
Author: GrakovNe (Grakov Maksim)
Licence: GNU GPL v 2
Date: 23.07.13

USAGE:
	To work with YMReader you need your ID and Token from Yandex OAuth
	When you get ID and Token you need import library and create object of YMReader with your ID and Token as arguments
	
	EXAMPLE:
			from YMR import *
			new = YMReader("ID","TOKEN")
			
	Then you can work with your Metrics! As you can see it's simply!
	
	How Library can:
		Return the list of your counters at account ( GetCounters(() )
		Return your login Data (ID and Token)
		Return Summary Statistic by today or total statistic ( GetSummary(ID,["Today"|"Total"]) )
		Return list of search phrases in which users come to your site ( GetSearchPhrases() )
		Check YandexMetrics code on your site ( CheckCode(ID) )
		Return load on your site today or total ( GetSiteLoad(ID,["Today"|"Total"]) )
		Return list of links in which users come to your site ( GetLinkSites(ID) )
		
	For examle, let give the number of visitors in http://grakovne.org:
		
			from YMR import *
			new = YMReader("12345678","123456ABCDEFGHIJKLMNOPRQSTUVWXYZ") # This is not correct data, of course
			print new.GetSummary(new.GetCounters()[1]["ID"])
			#That's all :)
		
	CONTACTS:
	
		ICQ: 5628310
		E-MAIL: grakovne@yandex.ru
		Twitter: http://twitter.com/grakovne
		Web: http://grakovne.org
	
	With best wishes from cold Russia
	'''
	
	def __init__(self,id,token):
		self.ID = str(id)
		self.Token = str(token)
		self.LoginStr = "?id=%s&pretty=1&oauth_token=%s" % (id,token) # and making full string from previous dictonary
		self.SummaryStr = "&pretty=1&oauth_token=%s" % (token)
		self.URLPrefix = "http://api-metrika.yandex.ru/" # setting shared for all request prefix
		
		
	def GetLoginData(self):
		return self.ID, self.Token
		
		
	def GetCounters(self): #Getting list of counters on your account
		import urllib as net
		
		try:
			Source =  net.urlopen(self.URLPrefix+"counters/"+self.LoginStr).read()
		except:
			return None
		
		Result=[]
		Sites=[]
		
		while not Source.find('<counter>')==-1: # Splitting all XML response to lists "per site" 
			IDS = Source.find("<counter>")
			IDE = Source.find("</counter>")
			Sites.append(Source[IDS+10:IDE])
			Source = Source[IDE+9:]
												
		for site in Sites:
			IDS = site.find('<site>')
			IDE = site.find('</site>')
			Host = site[IDS+6:IDE]
			IDS = site.find('<id>')
			IDE = site.find('</id>')	
			ID = site[IDS+4:IDE]
			Result.append({"URL":Host,"ID":ID})
		return Result


	def GetSummary(self,ID,Segment="Today"): # Get Summary daily or total activity on site
		import urllib as net
		Result = {}
		
		try:
			Source = net.urlopen(self.URLPrefix+"stat/traffic/summary/?id="+ID+self.SummaryStr).read()
		except:
			return None
																						
		if Segment == "Today": # Different fragments for different segments
			IDS = Source.find('<data count="7">')
			IDE = Source.find("</row>")
		
		if Segment == "Total":
			IDS = Source.find("<totals>")
			IDE = Source.find("</totals>")	
			
		Summary = Source[IDS:IDE]

		IDS = Summary.find("<denial>")+8
		IDE = Summary.find("</denial>")
		Result["Denial"] = Summary[IDS:IDE]
		
		IDS = Summary.find("<visits>")+8
		IDE = Summary.find("</visits>")
		Result["Visits"] = Summary[IDS:IDE]
		
		IDS = Summary.find("<page_views>")+12
		IDE = Summary.find("</page_views>")
		Result["Views"] = Summary[IDS:IDE]	

		IDS = Summary.find("<depth>")+7
		IDE = Summary.find("</depth>")
		Result["Depth"] = Summary[IDS:IDE]	
	
		IDS = Summary.find("<visitors>")+10
		IDE = Summary.find("</visitors>")
		Result["Visitors"] = Summary[IDS:IDE]	
	
		return Result
		
		
	def GetSearchPhrases(self,ID):
		import urllib as net
		List = []
		Result = []
		
		try:
			Source = net.urlopen(self.URLPrefix+"stat/sources/phrases/"+self.LoginStr).read()
		except:
			return None
			
		while not Source.find("<phrase>")==-1:
			IDS = Source.find("<phrase>")
			IDE = Source.find("</phrase>")
			List.append(Source[IDS+8:IDE])
			Source = Source[IDE+9:]
		
		for each in List:
			Result.append(each[9:-3])
		return Result
		
		
	def CheckCode(self,ID):
		import urllib as net
		
		try:
			Source = net.urlopen(self.URLPrefix+"counter/"+ID+"/check/"+self.LoginStr).read()
		except:
			None
			
		IDS = Source.find("<http_msg>")+10
		IDE = Source.find("</http_msg>")
		return Source[IDS:IDE]


	def GetSiteLoad(self,ID,Segment="Today"):
		import urllib as net
		Result = {"Max-RPS-Date":"","Max-Users-Date":"","Max-RPS-Time":"","Max-Users-Time":"","Max-Users":"","Max-RPS":""}
		try:
			Source = net.urlopen(self.URLPrefix+"stat/traffic/load?id="+ID+self.SummaryStr).read()
		except:
			return None
			
		if Segment == "Today":
			IDS = Source.find('<data count="7">')
			IDE = Source.find("</row>")
			
		if Segment == "Total":
			IDS = Source.find("<totals>")
			IDE = Source.find("</totals>")	
		
		Load = Source[IDS:IDE]
		
		IDS = Load.find("<max_rps_date>")+14
		IDE = Load.find("</max_rps_date>")
		Result["Max-RPS-Date"] = Load[IDS:IDE]
		
		
		IDS = Load.find("<max_rps_time>")+14
		IDE = Load.find("</max_rps_time>")
		Result["Max-RPS-Time"] = Load[IDS:IDE]		
		
		
		IDS = Load.find("<max_users_date>")+16
		IDE = Load.find("</max_users_date>")
		Result["Max-Users-Date"] = Load[IDS:IDE]		
		
		IDS = Load.find("<max_users_time>")+16
		IDE = Load.find("</max_users_time>")
		Result["Max-Users-Time"] = Load[IDS:IDE]
		
		IDS = Load.find("<max_rps>")+9
		IDE = Load.find("</max_rps>")
		Result["Max-RPS"] = Load[IDS:IDE]
		
		IDS = Load.find("<max_users>")+11
		IDE = Load.find("</max_users>")
		Result["Max-Users"] = Load[IDS:IDE]
		return Result
		

	def GetLinkSites(self,ID):
		
		Result = []
		Links = []
		import urllib as net
		try:
			Source = net.urlopen(self.URLPrefix+ "stat/sources/sites/?id="+ID+self.SummaryStr).read()
		except:
			return None
			
		while not Source.find("<url>")==-1:
			IDS = Source.find("<url>")+5
			IDE = Source.find("</url>")
			Links.append(Source[IDS:IDE])
			Source = Source[IDE+5:]
			
		for each in Links:
			Result.append(each[9:-3])
		
		return Result
		
