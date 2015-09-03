#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  auto_install.py
#  
#  Copyright 2015 samsung <samsung@SAMSUNG-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


def main(args):
    return 0
    
def menu():
  print("--------------- MENU ---------------")
  print("1) Add")
  print("2) Manage Programs")
  print("c) Create batch")
  print("r) Reset file")
  print("q) Quit")
  choice=input("Your choice : ")
  return choice

def write_conf(name_prog, browser_prog, os, silent_prog):
    config = configparser.RawConfigParser()
    config[''+name_prog+'']={'exe':''+browser_prog+'','os':''+os+'','mode':''+silent_prog}
    conf_file = open("conf.ini", "a")
    config.write(conf_file)
    conf_file.close() 

def check_prog(name_prog):
     config = configparser.RawConfigParser()
     config.sections()
     config.read('conf.ini')
     exist = ''+name_prog+'' in config
     return exist
     
def list_prog():
     config = configparser.RawConfigParser()
     config.sections()
     config.read("conf.ini")
     listprog = config.sections()
     print("-------------------------------------------------------------------")
     print("{0:13} | {1:28} | {2:16} | {3:5} |".format("     Name","         File", "   Silent mode", "  OS"))
     print("-------------------------------------------------------------------")
     for prog in listprog:
       print("{0:13} | {1:28} | {2:16} | {3:5} |".format(prog, config[prog]['exe'], config[prog]['mode'], config[prog]['OS']))
       print("-------------------------------------------------------------------")

def del_prog():
    name_prog=input("Can you delete a program ? (Enter the name or q for quit) :")
    if name_prog != "q":
      dfile = open("conf.ini","r")
      list_file = dfile.readlines()
      dfile.close()
      x = 0
      for data in list_file:
       data = data.rstrip('\n') #supprimer le retour à la ligne \n
       if data == "["+name_prog+"]":
        del list_file[x:x+5]
        dfile = open("conf.ini","w")
        dfile.writelines(list_file)
        dfile.close()
       x = x+1
    
def reset_file():
      conf_file = open("conf.ini", "w+")
      conf_file.write("")

def add_prog():
      print("--------------- ADD PROGRAM ---------------")
      name_prog=input("Name : ")
      browser_prog = input("File exe in 'Tools' folder : ")
      os=input("32/64 bits or multiplateform ? (32/64/multi) : ")
      silent_prog=input("Argument for silent mode : ")
      print("------------------------------")
      exist = False
      exist = check_prog(name_prog)
      
      if exist == True:
       print("The program alread exist")
      else: 
       if os == "32" or os == "64" or os == "multi":
        write_conf(name_prog, browser_prog, os, silent_prog)
        print("SUCCESS !! Entry has been added")  
       else:
        print(" /!\ ERROR  /!\ Please retry ")

def create_batch():
	batch = open("setup.bat", "w+") #création du batch
	config = configparser.RawConfigParser()
	config.sections()
	config.read('conf.ini')
	all_prog = config.sections()
	batch.write('@echo off\n')
	batch.write('cd tools\n')
	batch.write('IF "%PROCESSOR_ARCHITECTURE%"=="x86" (set bit=x86) else (set bit=x64)\n')
	batch.write('@echo Setup programs %bit% \n')
	batch.write('IF %bit% EQU x64 (\n')
	
	#tri des logiciels 64 bits
	for prog in all_prog:
		if config[prog]['OS'] == "64" or config[prog]['OS'] == "multi":
			batch.write('	@echo Install '+prog+'\n')
			batch.write("	\""+config[prog]['exe']+"\" "+config[prog]['mode']+"\n")
	batch.write('	) ELSE (\n')
	
	#Tri des logiciels 32 bits 
	for prog in all_prog:
		if config[prog]['OS'] == "32" or config[prog]['OS'] == "multi":
			batch.write('	@echo Install '+prog+'\n')
			batch.write("	\""+config[prog]['exe']+"\" "+config[prog]['mode']+"\n")
	batch.write(')\n')	
	batch.write('pause')
	
if __name__ == '__main__':
    import sys
    import configparser
    import os
      
    if os.path.isdir("tools") is False:
     os.mkdir("tools")
     
    while menu != 'q':  
     choice = menu()
     
     if choice == '1':
      add_prog()
      
     if choice == '2':
      print("")
      print("*************************************************************************")
      print("**************************   MANAGE PROGRAMS   **************************")
      print("*************************************************************************")
      print("")
      list_prog()
      del_prog()
      
      
     if choice == "c":
       create_batch()
       print("*********************   setup.bat has been create   **********************")
       
     
     if choice == "r":
      reset_file()
      print("The file has been reset")
       
    
    sys.exit(main(sys.argv))
     
          
    
