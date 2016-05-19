import urwid
import sys, os
wd = os.getcwd()
sys.path.insert(0, wd+"/scripts")
import markov
import naive_tags
import jumble


###############################################################################
#                                                                             #
#   File: run.py                                                              #
#   This script will start a GUI which runs one of the selected random text   #
#   generation algorithms.                                                    #
#                                                                             #
#   Lots of GUI setup comes from the tutorial                                 #
#   on the urwid website.                                                     #
#   Henry Rizzi && Angela Assante                                             #
#                                                                             #
###############################################################################

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

#use this to deal with choices from the user in the menu
def item_chosen(button):
  #first respond to the choice
    response = urwid.Text([u'You chose ', button.label, u': check gen.txt for output!\n'])
    #then run the selected thing using the button choice
    handle_choices(button.label)
    done = menu_button(u'OK', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def exit_program(button):
    raise urwid.ExitMainLoop()

menu_top = menu(u'Style of Message', [
    sub_menu(u'Cappy', [
        menu_button(u'Cappy Markov Chain', item_chosen),
        menu_button(u'Cappy Naive', item_chosen),
        menu_button(u'Cappy Word Replacement', item_chosen),
    ]),
    sub_menu(u'Wordsmiths', [
        menu_button(u'Wordsmiths Markov Chain', item_chosen),
        menu_button(u'Wordsmiths Naive', item_chosen),
        menu_button(u'Wordsmiths Word Replacement', item_chosen),
    ]),

    sub_menu(u'Outings Club', [
        menu_button(u'Outings Markov Chain', item_chosen),
        menu_button(u'Outings Naive', item_chosen),
        menu_button(u'Outings Word Replacement', item_chosen),
    ]),
])

#basically just a gigantic switch statement to run whatever script is necessary
#  for the desired output
def handle_choices(choice):
  if (choice == 'Cappy Markov Chain'):
    markov.generate_email("data/cleaned/greetings-cappy.txt","data/cleaned/cappy.txt",
        "data/cleaned/closings-cappy.txt","gen.txt",par_min=4,par_max=8,sen_min=4,sen_max=8)
  elif (choice == 'Cappy Naive'):
    naive_tags.replace_and_output("data/naive/cappy.outline", 
        "gen.txt","data/naive/cappy.yaml")
  elif (choice == 'Cappy Word Replacement'):
    markov.generate_email("data/cleaned/greetings-cappy.txt","data/cleaned/cappy.txt",
        "data/cleaned/closings-cappy.txt","gen.txt", replace=True,par_min=4,par_max=8,sen_min=4,sen_max=8)
  elif (choice == 'Wordsmiths Markov Chain'):
    markov.generate_email("data/cleaned/greetings-wordsmiths.txt","data/cleaned/wordsmiths.txt",
        "data/cleaned/closings-wordsmiths.txt","gen.txt",par_min=2,par_max=5,sen_min=2,sen_max=6)
  elif (choice == 'Wordsmiths Naive'):
    naive_tags.replace_and_output("data/naive/wordsmiths.outline",
        "gen.txt", "data/naive/wordsmiths.yaml")
  elif (choice == 'Wordsmiths Word Replacement'):
    markov.generate_email("data/cleaned/greetings-wordsmiths.txt","data/cleaned/wordsmiths.txt",
        "data/cleaned/closings-wordsmiths.txt","gen.txt",replace=True,par_min=2,par_max=5,sen_min=2,sen_max=6)
  elif (choice == 'Outings Markov Chain'):
    markov.generate_email("data/cleaned/greetings-outing.txt","data/cleaned/outing.txt",
        "data/cleaned/closings-outing.txt","gen.txt",par_min=2,par_max=4,sen_min=1,sen_max=4)
  elif (choice == 'Outings Naive'):
    naive_tags.replace_and_output("data/naive/outing.outline",
        "gen.txt", "data/naive/outing.yaml")
  else:
    markov.generate_email("data/cleaned/greetings-outing.txt","data/cleaned/outing.txt",
        "data/cleaned/closings-outing.txt","gen.txt",replace=True,par_min=2,par_max=4,sen_min=1,sen_max=4)
  
class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

if __name__ == "__main__":
  top = CascadingBoxes(menu_top)
  urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
