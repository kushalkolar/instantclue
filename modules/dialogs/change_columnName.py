"""
	""COLUMN NAME CHANGER""
    Instant Clue - Interactive Data Visualization and Analysis.
    Copyright (C) Hendrik Nolte

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""


import tkinter as tk
from tkinter import ttk             
import tkinter.simpledialog as ts
import matplotlib.pyplot as plt
from collections import OrderedDict
from modules.utils import *


class ColumnNameConfigurationPopup(object):
	
	
	def __init__(self,columns,dfClass,sourceTreeView,analyzeClass):
						
		self.entryDict = OrderedDict()
		self.columns = columns 
		self.dfClass = dfClass
		self.analyzeClass = analyzeClass
		self.renamed = True
		
		self.dataTreeview = sourceTreeView
		self.iidList = sourceTreeView.columnsIidSelected
		self.build_toplevel() 
		self.build_widgets() 
		
		
		self.toplevel.wait_window() 
		
	def close(self, event = None):
		'''
		Close toplevel
		'''

		self.toplevel.destroy() 
		
			
	def build_toplevel(self):
	
		'''
		Builds the toplevel to put widgets in 
		'''
        
		popup = tk.Toplevel(bg=MAC_GREY) 
		popup.wm_title('Change column name') 
		popup.bind('<Escape>', lambda event: self.discard_changes()) 
		popup.bind('<Return>', lambda _,entryDict = self.entryDict : self.rename_columns_in_df(entryDict))
		popup.protocol("WM_DELETE_WINDOW", self.discard_changes)
		w=450
		h=100+int(len(self.columns))*33 ##emperically
		self.toplevel = popup
		self.center_popup((w,h))
		
			
	def build_widgets(self):
			
             '''
             Building needed tkinter widgets 
             '''
             
             cont = tk.Frame(self.toplevel,background = MAC_GREY)
             cont.pack(fill='both', expand=True)
             cont.grid_columnconfigure(1,weight=1,minsize=200)
             cont.grid_columnconfigure(0,weight=1,minsize=200)
			
             labelTitle = tk.Label(cont, text = 'Change column name', **titleLabelProperties)
             labelTitle.grid(pady=5,padx=5,sticky=tk.W,columnspan=2)
             
             self.entryDict.clear()
             for n,columnName in enumerate(self.columns): 
             	columnLabel = tk.Label(cont, text = columnName+': ', bg=MAC_GREY)
             	newColumnEntry = ttk.Entry(cont)
             	newColumnEntry.insert('end',columnName)
             	if n == 0:
             		newColumnEntry.focus()
             	
             	self.entryDict[columnName] = newColumnEntry
             	columnLabel.grid(row=n+2,column=0,sticky=tk.E,padx=5, pady=3)
             	CreateToolTip(columnLabel,text=columnName,waittime=800)
             	newColumnEntry.grid(row=n+2, column=1, padx=5, pady=3, columnspan=5, sticky=tk.EW)
             
             renameButton = ttk.Button(cont, text = 'Rename',
             						   command = lambda: self.rename_columns_in_df(self.entryDict),
             						   width = 7)  
             closeButton = ttk.Button(cont, text = 'Close', 
             						   command = self.discard_changes, 
             						   width = 7)
             							
             
             closeButton.grid(row=n+3, column = 1, padx=5, pady=3, sticky=tk.E) 
             renameButton.grid(row = n+3, column = 0, padx=5, pady=3, sticky=tk.W, columnspan=2)
	
	def discard_changes(self):
		'''
		'''
		self.renamed = False 
		self.close()            	
             	
	def rename_columns_in_df(self,entryDict):
		'''
		'''
		renameDict = OrderedDict() 
		columnNamesToChange = []
		iidList = []
		n = 0
		for oldName, entry in entryDict.items():
			entryText = entry.get()
			if entryText != oldName:
				columnNamesToChange.append(oldName)
				renameDict[oldName] = entryText
				iidList.append(self.iidList[n])
			n+=1
		if len(renameDict) == 0:
			self.discard_changes()
			return
			
		columnNotToChange = [col for col in self.dfClass.df_columns if col not in columnNamesToChange]
		
		for oldName,newName in renameDict.items():
			newNameEval = self.dfClass.evaluate_column_name(newName,columnNotToChange,useExact=True)
			columnNotToChange.append(newNameEval)
			renameDict[oldName] = newNameEval
		
		newIIDList = self.dataTreeview.rename_itemText_by_iidList(iidList, list(renameDict.values()))
		self.dfClass.rename_columnNames_in_current_data(renameDict)
		
		self.adjust_columns_in_receiverbox(renameDict)
		
		self.reverseFuncs = {'funcDataR':'rename_columnNames_in_current_data',
							 'argsDataR':{'replaceDict':reverse_dict(renameDict)},
							 'funcTreeR':'rename_itemText_by_iidList',
							 'argsTreeR':{'iidList':newIIDList,'newNameList':list(renameDict.keys())},
							 'description': OrderedDict([('Activity:','Column renaming'),
     						 ('Description:','Column(s) has/have been renamed.'),
     						 ('Column name(s):',get_elements_from_list_as_string(list(entryDict.keys()), maxStringLength = None)),
     						 ('Renamed columns:',get_elements_from_list_as_string(list(renameDict.values()), maxStringLength = None)),
     						 ('Data ID:',self.dfClass.currentDataFile)])}
		self.close()
		
		

	def adjust_columns_in_receiverbox(self,renameDict):
		'''
		If the renamed columns were dragged and dropped in one of receiver boxes
		we need to change the name and deleting/adjustin functions. 
		numerical and cateogrical columns are saved in a dict. values represent the buttons.
		'''
		if self.dfClass.currentDataFile != self.analyzeClass.plt.get_dataID_used_for_last_chart():
			return
		
		numericColumns = list(self.analyzeClass.selectedNumericalColumns.keys())
		categoricalColumns = list(self.analyzeClass.selectedCategories.keys())
		for oldName,newName in renameDict.items():
		
			if oldName in numericColumns:
				button = self.analyzeClass.selectedNumericalColumns[oldName]
				self.analyzeClass.bind_events_to_button_in_receiverbox(newName,button,True)
				del self.analyzeClass.selectedNumericalColumns[oldName]
				self.analyzeClass.selectedNumericalColumns[newName] = button
			
			elif oldName in categoricalColumns:
				
				button = self.analyzeClass.selectedCategories[oldName]
				self.analyzeClass.bind_events_to_button_in_receiverbox(newName,button,False)
				#delete entry
				del self.analyzeClass.selectedCategories[oldName]
				#replace with new name
				self.analyzeClass.selectedCategories[newName] = button
			     				     
		
	def center_popup(self,size):
         	'''
         	Casts the popup in center of screen
         	'''

         	w_screen = self.toplevel.winfo_screenwidth()
         	h_screen = self.toplevel.winfo_screenheight()
         	x = w_screen/2 - size[0]/2
         	y = h_screen/2 - size[1]/2
         	self.toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))  	
	
	