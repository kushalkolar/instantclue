"""
    Readme Instant Clue - Interactive Scientific Data Analysis
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
    
    
    Website : http://www.instantclue.uni-koeln.de
    Original Publication: https://www.nature.com/articles/s41598-018-31154-6    
    For License information check https://opensource.org/licenses
   
   
******************** IMPORTANT NOTE ********************

To make the treeview work you will have to change 
the function 

    def selection in the ttk.py file in the tkinter package folder:
	line 1392
    
    def selection(self, selop=None, items=None):
        """If selop is not specified, returns selected items."""
        if isinstance(items, (str, bytes)):
            items = (items,)
        return self.tk.splitlist(self.tk.call(self._w, "selection", selop, items))

    Dependencies (alphabetic order):
    
    -husl (color palettes)
    -fastcluster
    -matplotlib (https://matplotlib.org/users/license.html)
    -numpy (BSD 3 - https://docs.scipy.org/doc/numpy-1.10.0/license.html)
    -pandas (BSD 3)
    -pandastable (GPL v3 - note: copied in source code, changes are indicated)
    -scikit-learn (BSD 3)
    -scipy (‎BSD-new license - https://www.scipy.org/scipylib/license.html)
    -seaborn (BSD 3)
    -statsmodels (BSD 3 https://github.com/statsmodels/statsmodels/blob/master/			LICENSE.txt)
    -tslearn
    
    Please check the licence of the individual packages before redistribution.
"""



