import pandas as pd
from IPython.display import display

def highlights_max(s, until=2):
    s1,s2 = s.nlargest(until)
    is_max = s == s1 #s.max()
    is_2max = s == s2 #s.nlargest(2)
    is_min = s == s.min()
    color_cells = []
    for c, _ in enumerate(is_max):
        if is_max[c]:
            color_cells.append( 'background: lightgreen' )
        elif is_2max[c]:
            color_cells.append( 'background: aqua' )
        elif is_min[c]:
            color_cells.append( 'background: coral' )
        else:
            color_cells.append( "")            
    return color_cells

def highlights_min(s, until=2):
    s1,s2 = s.nsmallest(until)
    is_max = s == s1 #s.max()
    is_2max = s == s2 #s.nlargest(2)
    is_min = s == s.max()
    color_cells = []
    for c, _ in enumerate(is_max):
        if is_max[c]:
            color_cells.append( 'background: lightgreen' )
        elif is_2max[c]:
            color_cells.append( 'background: aqua' )
        elif is_min[c]:
            color_cells.append( 'background: coral' )
        else:
            color_cells.append( "")            
    return color_cells
