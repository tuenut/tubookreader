import sys
# import zerorpc

TITLE = 'TubookReader'

if __name__ == "__main__":
    gui = 'tk'

    if len(sys.argv) > 1:
        if '--gui' in sys.argv[1]:
            gui_argv = sys.argv[1]
            gui_argv = gui_argv.split('=') if '=' in gui_argv else gui_argv.split()
            gui = gui_argv[1]

    if gui == 'tk':
        import frontend_tk as gui
    elif gui == 'wx':
        import frontend_wx as gui
    else:
        exit(1)

    gui.Application()
