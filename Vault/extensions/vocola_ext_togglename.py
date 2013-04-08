# Vocola function: match.name

### Not in use
def stdio_toggle_name():
    logging.debug("STN start 0")
    try:
        tni = tn()
        logging.debug("STN start 1")
        string = sys.stdin.read()
        (left_code, code_name, right_code) = tni.toggle_name(string)
        # place back in the clipboard
        #logging.debug( "result = |%s|" % plain_name
        sys.stdio.write( left_code+code_name+right_code)
        logging.debug("STN start 2 %s" %repr(ignore_data))
    except Exception, error:
        logging.debug( "STN %s" %(repr(error)))

    return ""

#
def stdio_match_name():
    logging.debug("SMN start")
    try:
        logging.debug( "SMN stdio result = |%s|" % result)
        tni = tn()
        string = sys.stdin.read()
        ignore_data = tni.match_name(string)
        sys.stdio.write(left_code + code_name + right_code)
    except Exception, error:
        logging.debug( "SMN %s" %(repr(error)))

    return ""
###