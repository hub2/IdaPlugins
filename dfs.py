from idaapi import *
import colorsys
from Queue import Queue
print "DFS by Hubercik, visiting from cursor position..."

COLOR = 0x00
#COLOR = 0xffffff

# current cursor position
ea = ScreenEA()

visited = set()

# Go until no more instructions
def dfs(ea, color):
    while len(idc.GetMnem(ea)):
        print "Entering %x: %s" % (ea,idc.GetDisasm(ea))

        # Check that we did
        visited.add(ea)

        # Calculate color and apply it to the instruction
        RGBcolor = make_color(color)
        print color
        idc.SetColor(ea, 1, RGBcolor)

        # Get all jmp locations from there
        xrefs = list(XrefsFrom(ea))

        # Count next instruction addr
        nexti = ea + idc.ItemSize(ea)

        # Simple check for jmp instructions(is there api to do that?)
        if len(xrefs) != 1 or nexti != xrefs[0].to:
            # Go into xrefs
            for xref in xrefs[::-1]:
                # We don't want to RECURSE into next instr
                # which will be there in case of conditional jump
                # also don't enter visited nodes
                if xref.to == nexti or xref.to in visited:
                    continue
                dfs(xref.to, color+0x7)

        # Check if we've been in the next instr
        if nexti in visited:
            return

        # Move to next instruction
        ea = nexti

def bfs(ea, color):
    visited = set()
    q = Queue()

    q.put(ea)
    while not q.empty():
        ea = q.get()
        color += 2
        while len(idc.GetMnem(ea)) and ea not in visited:
            print "Entering %x: %s" % (ea,idc.GetDisasm(ea))

            # Check that we did
            visited.add(ea)

            # Calculate color and apply it to the instruction
            RGBcolor = make_color(color)
            print color
            idc.SetColor(ea, 1, RGBcolor)

            # Get all jmp locations from there
            xrefs = list(XrefsFrom(ea))

            # Count next instruction addr
            nexti = ea + idc.ItemSize(ea)

            # Simple check for jmp instructions(is there api to do that?)
            if len(xrefs) != 1 or nexti != xrefs[0].to:
                # Go into xrefs
                for xref in xrefs:
                    # We don't want to QUEUE next instr
                    # which will be there in case of conditional jump
                    # also don't enter visited nodes
                    if xref.to == nexti or xref.to in visited:
                        continue
                    q.put(xref.to)

                if len(xrefs) == 1:
                    break

            # Check if we've been in the next instr
            if nexti in visited:
                break

            # Move to next instruction
            ea = nexti



# Function for creating rgb int only from HSV value in int
def make_color(color):
    rgb = colorsys.hsv_to_rgb(float(color)/0xff, 1,1)
    return int(rgb[0]*(256**2) + rgb[1]*256 + rgb[2])

bfs(ea, COLOR)
