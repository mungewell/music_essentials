# TODO: instantiate chord with multiple notes
# TODO: add_note support note string

from .note import Note
from .scale import Scale
from .interval import Interval

class Chord(object):
    """Representation of group of notes that are played together."""

    # Difference in pitch index from the root note in the scale to each note in the chord
    _MAJOR = (2, 4)
    _MINOR = (2, 4)
    
    _CHORD_PATTERNS = {
        'major': _MAJOR,
        'maj': _MAJOR,
        'minor': _MINOR,
        'min': _MINOR
    }

    _CHORD_NUM_SCALE_INDEX = {
        'I' : 0,
        'II' : 1,
        'III': 2,
        'IV': 3,
        'V': 4,
        'VI': 5,
        'VII': 6,
        'VIII': 7}

    def __init__(self, root_note):
        """Create a new Chord.

        Once the Chord has been created, additional notes can be added using 
        :attr:`~music_essentials.chord.Chord.add_note`
        
        Args:
            root_note: :attr:`~music_essentials.note.Note`
                The first note to add to the chord.

        Returns:
            :attr:`~music_essentials.chord.Chord`
                A new chord object, with a single note added.

        Raises:
            `TypeError: <https://docs.python.org/2/library/exceptions.html#exceptions.TypeError>`_
                If anything but an instance of :attr:`~music_essentials.note.Note` is provided for `root_note`.
        
        Examples:
            >>> c = Chord(Note.from_note_string('C4'))
            >>> print(c)
            C4
            >>> c = Chord(Note.from_note_string('C4'))
            >>> c.add_note(Note.from_note_string('E4'))
            >>> print(c)
            C4+E4
            >>> c = Chord(5.5)
            Expected Note for root note, got '5.5'
        """
        if not isinstance(root_note, Note):
            raise TypeError('Expected Note for root note, got \'' + str(root_note) + '\'')

        self.notes = [root_note]

    @classmethod
    def build_chord(cls, tonic_key, chord_number, chord_type):
        """Build a chord.

        Specify the tonic key, the chord number, and the type of chord to build.
        Receive an ordered list of the notes in the chord.

        Args
        ----
            tonic_key : :attr:`~music_essentials.note.Note`
                They key in which the chord should be built

            chord_number : str
                The scale degree to start building the chord on

            chord_type : str
                The tonality of the key to build the cord in. Can be one of:

                * 'major'/'maj': Major tonality.
                * 'minor'/'min': Minor tonality.

        Returns
        -------
            list
                The list of notes in the chord, in ascending order.

        Examples
        --------
            >>> c = Chord.build_chord(Note.from_note_string('C4'), 'I', 'major')
            >>> print(c)
            >>> C4+E4+G4
            >>> c = Chord.build_chord(Note.from_note_string('C4'), 'V', 'major')
            >>> print(c)
            >>> G4+B4+D5
            >>> c = Chord.build_chord(Note.from_note_string('C4'), 'IV', 'minor')
            >>> print(c)
            >>> F4+A4b+C5
        """
        if not isinstance(tonic_key, Note):
            raise TypeError('Expected Note for tonic key, got \'' + str(tonic_key) + '\'')
        if not chord_number in Chord._CHORD_NUM_SCALE_INDEX.keys():
            raise ValueError('Unsupported chord number: ' + str(chord_number))
        if not chord_type in Chord._CHORD_PATTERNS.keys():
            raise ValueError('Unsupported chord type: ' + str(chord_type))

        s = Scale.build_scale(tonic_key, chord_type)
        root_idx = Chord._CHORD_NUM_SCALE_INDEX[chord_number]
        root = s[root_idx]
        cls = Chord(root)
        for index_diff in Chord._CHORD_PATTERNS[chord_type]:
            next_idx = root_idx + index_diff
            octave_diff = 0
            if next_idx > (len(s) - 1):
                next_idx -= len(s) - 1
                octave_diff += 1
            next_note = s[next_idx]
            cls.add_note(Note(next_note.pitch, next_note.octave + octave_diff, next_note.accidental))

        return cls

    def root(self):
        """Get the root (i.e., lowest) note of the chord.
        
        Returns:
            :attr:`~music_essentials.note.Note`
                The lowest note of the chord.
        
        Examples:
            >>> c = Chord(Note.from_note_string('E4'))
            >>> print(c.root())
            E4
            >>> c = Chord(Note.from_note_string('E4'))
            >>> c.add_note(Note.from_note_string('D4'))
            >>> print(c.root())
            D4
        """
        return self.notes[0]

    def add_note(self, new_note):
        """Add another note to the chord.
        
        Args:
            new_note : :attr:`~music_essentials.note.Note`
                The note to add.

        Raises:
            `TypeError: <https://docs.python.org/2/library/exceptions.html#exceptions.TypeError>`_
                If `new_note` is not an instance of :attr:`~music_essentials.note.Note`.

        Examples:
            >>> c = Chord(Note.from_note_string('C4'))
            >>> c.add_note(Note.from_note_string('E4'))
            >>> print(c)
            C4+E4
            >>> c = Chord(Note.from_note_string('G4'))
            >>> c.add_note(Note.from_note_string('E4'))
            >>> c.add_note(Note.from_note_string('D4'))
            >>> print(c)
            D4+E4+G4
        """
        if not isinstance(new_note, Note):
            raise TypeError('Expected Note for new note, got \'' + str(new_note + '\''))

        if new_note < self.root():
            self.notes.insert(0, new_note)
            return

        for i in range(len(self.notes) - 1):
            if (new_note >= self.notes[i]) and (new_note < self.notes[i + 1]):
                self.notes.insert(i + 1, new_note)
                return

        self.notes.append(new_note)
    
    def __str__(self):
        """Get a string representation of the chord.
        
        Returns:
            str
                A string representation of the chord, in the form ``<note_1>+<note_2>+...+<note_n>``.
        """
        out = ''
        for n in self.notes:
            out += n.__str__() + '+'
        out = out [:-1]
        
        return out