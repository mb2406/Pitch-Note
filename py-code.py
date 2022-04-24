from microbit import *

# Setting up paramaters to allow and control MIDI data being sent to PurrData.

def midiNoteOn(chan, n, vel):
    MIDI_NOTE_ON = 0x90
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_ON | chan, n, vel])
    uart.write(msg)

def midiNoteOff(chan, n, vel):
    MIDI_NOTE_OFF = 0x80
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_OFF | chan, n, vel])
    uart.write(msg)

def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

    # Defining variables that are used throughout the code.

Start()
lastA = False
lastB = False
lastC = False
pot = 0
last_pot = False
BUTTON_C_NOTE = False
BUTTON_A_NOTE = False
pot_note = 60
n_note = 60
start = True
n = 800
low_octave = True
med_octave = False
high_octave = False

# Note display parameters.

c_note = Image("08800:" "80000:" "80000:" "80000:" "08800")
cs_note = Image("08808:" "80000:" "80000:" "80000:" "08800")
d_note = Image("88000:" "80800:" "80800:" "80800:" "88000")
ds_note = Image("88008:" "80800:" "80800:" "80800:" "88000")
e_note = Image("88800:" "80000:" "88800:" "80000:" "88800")
f_note = Image("88800:" "80000:" "88800:" "80000:" "80000")
fs_note = Image("88808:" "80000:" "88800:" "80000:" "80000")
g_note = Image("88800:" "80000:" "80888:" "80080:" "88880")
gs_note = Image("88808:" "80000:" "80888:" "80080:" "88880")
a_note = Image("08800:" "80080:" "88880:" "80080:" "80080")
as_note = Image("08808:" "80080:" "88880:" "80080:" "80080")
b_note = Image("88000:" "80800:" "88000:" "80800:" "88000")

# Octave selection display parameters.

low_display = Image("00000:" "80000:" "88888:" "80000:" "00000")
med_display = Image("00000:" "00800:" "88888:" "00800:" "00000")
high_display = Image("00000:" "00008:" "88888:" "00008:" "00000")

# Plays a low C on startup/reset - default octave range is low.

midiNoteOn(0, 48, 127)
display.show(low_display)
sleep(1000)
midiNoteOff(0, 48, 127)
display.show(Image.HAPPY)

# Code which switches octaves on button B press;

while start is True:
    b = button_b.is_pressed()
    if b is True and lastB is False:
        if low_octave is True:         # Checks which octave band it's on.
            display.show(med_display)  # Shows octave display paramater.
            midiNoteOn(0, 60, 127)     # Plays C note in specified octave.
            low_octave = False         # Changes all other octave paramaters
            high_octave = False        # for repeated button press to cycle
            med_octave = True          # through octaves.
            sleep(1000)
            midiNoteOff(0, 60, 127)
        elif med_octave is True:
            display.show(high_display)
            midiNoteOn(0, 72, 127)
            med_octave = False
            low_octave = False
            high_octave = True
            sleep(1000)
            midiNoteOff(0, 72, 127)
        elif high_octave is True:
            display.show(low_display)
            midiNoteOn(0, 48, 127)
            high_octave = False
            med_octave = False
            low_octave = True
            sleep(1000)
            midiNoteOff(0, 48, 127)
    elif b is False and lastB is True:
        display.clear()
    lastB = b

    # Code which plays a random note for 1 second on button A press
    # within the current set octave range.

    a = button_a.is_pressed()

    if a is True:                       # When button A is pressed;
        import random                   # Generate a random integer between
        n = random.randint(48, 59)      # 48 and 59 which determe note values
        if low_octave is True:          # in PurrData.
            n_note = n
        elif med_octave is True:        # Shifts the note up to the selected
            n_note = n+12               # octave by increasing the note
        elif high_octave is True:       # number.
            n_note = n+24

        midiNoteOn(0, n_note, 127)        # Sends note through MIDI to PurrData.
        display.show(Image.MUSIC_QUAVER)  # Displays visual image.
        sleep(1000)                       # Plays back the random note for 1
        midiNoteOff(0, n_note, 127)       # second, then stops.

    pot = pin2.read_analog()
    c = pin1.is_touched()

    # Depending on the location of the potentiometer, both the display
    # and note played when button C is pressed  will change.

    if pot >= 1 and pot <= 85:
        if c is False:              # Only displays note type when button C is not
            display.show(c_note)    # pressed.
        pot_note = 48
    if pot >= 86 and pot <= 170:
        if c is False:
            display.show(cs_note)
        pot_note = 49
    if pot >= 171 and pot <= 255:
        if c is False:
            display.show(d_note)
        pot_note = 50
    if pot >= 256 and pot <= 340:
        if c is False:
            display.show(ds_note)
        pot_note = 51
    if pot >= 341 and pot <= 425:
        if c is False:
            display.show(e_note)
        pot_note = 52
    if pot >= 426 and pot <= 510:
        if c is False:
            display.show(f_note)
        pot_note = 53
    if pot >= 511 and pot <= 595:
        if c is False:
            display.show(fs_note)
        pot_note = 54
    if pot >= 596 and pot <= 680:
        if c is False:
            display.show(g_note)
        pot_note = 55
    if pot >= 681 and pot <= 765:
        if c is False:
            display.show(gs_note)
        pot_note = 56
    if pot >= 766 and pot <= 850:
        if c is False:
            display.show(a_note)
        pot_note = 57
    if pot >= 851 and pot <= 945:
        if c is False:
            display.show(as_note)
        pot_note = 58
    if pot >= 946 and pot <= 1020:
        if c is False:
            display.show(b_note)
        pot_note = 59

    if med_octave is True:               # Note is shifted depending on
        pot_note = pot_note+12           # selected octave.
    if high_octave is True:
        pot_note = pot_note+24

    if last_pot != pot_note:
        BUTTON_C_NOTE = pot_note
    last_pot = pot_note

    # Code which controls what button C does.

    if c is True and lastC is False:        # Inputs note answer and compares
        midiNoteOn(0, BUTTON_C_NOTE, 127)   # value with the randomised note.
        if last_pot == n_note:              # Plays back selected MIDI note.
            display.show(Image.YES)         # If correct note, displays a tick.
        elif last_pot != n_note:
            display.show(Image.NO)          # If wrong note, displays a cross.
    elif c is False and lastC is True:
        midiNoteOff(0, BUTTON_C_NOTE, 127)
        display.clear()

    lastC = c

    sleep(100)
