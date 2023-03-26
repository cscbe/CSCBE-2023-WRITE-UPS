import os
import argparse

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file does not exist!" % arg)
    else:
        return arg

tmp_file = "tmp.txt"
mappings = {
    0x04:"aA", 0x05:"bB", 0x06:"cC", 0x07:"dD", 0x08:"eE", 0x09:"fF",
    0x0A:"gG", 0x0B:"hH", 0x0C:"iI", 0x0D:"jJ", 0x0E:"kK", 0x0F:"lL",
    0x10:"mM", 0x11:"nN", 0x12:"oO", 0x13:"pP", 0x14:"qQ", 0x15:"rR",
    0x16:"sS", 0x17:"tT", 0x18:"uU", 0x19:"vV", 0x1A:"wW", 0x1B:"xX",
    0x1C:"yY", 0x1D:"zZ", 0x1E:"1!", 0x1F:"2@", 0x20:"3#", 0x21:"4$",
    0x22:"5%", 0x23:"6^", 0x24:"7&", 0x25:"8*", 0x26:"9(", 0x27:"0)",
    0x2C:"  ", 0x2D:"-_", 0x2E:"=+", 0x2F:"[{", 0x30:"]}",  0x32:"#~",
    0x33:";:", 0x34:"'\"",  0x36:",<",  0x37:".>"
}

def main(captureFile, tshark):
    if tshark == None:
        tshark = 'tshark'
    os.system(tshark + ' -r ' + captureFile + ' -e usb.capdata -T fields -Y "(usb.urb_type == URB_COMPLETE)" > ' + tmp_file)
    keyData = open(tmp_file, 'r')
    output = ""
    for line in keyData:
        if len(line) > 6:
            shift = int(line[2:3], 16)
            key = int(line[4:6], 16)
            if key in mappings:
                if shift == 2:
                    output += mappings[key][1]
                else:
                    output += mappings[key][0]
    keyData.close()
    os.system('rm ' + tmp_file)
    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parses keys from USB keyboard capture file')
    parser.add_argument('-f', '--file', 
					dest='captureFile', 
					help='Path to the capture file (.pcap)', 
					metavar="FILE", 
					type=lambda x: is_valid_file(parser, x), 
                    required=True)
    parser.add_argument('-t', '--tshark-exec', 
					dest='tshark', 
					help='Path to tshark (defaults to "tshark")', 
					metavar="FILE", 
					type=lambda x: is_valid_file(parser, x), 
                    required=False)
    args = parser.parse_args()
    main(args.captureFile, args.tshark)