
'''
 #AABBCC -> (123,123,123)
    or
  AABBCC -> (123,123,123)
'''
def Hex_to_RGB(hex):
    if len(hex) == 7:
        hex = hex[1:]
    r = int(hex[0:2],16)
    g = int(hex[2:4],16)
    b = int(hex[4:6],16)
    rgb = [r,g,b]
    return rgb
