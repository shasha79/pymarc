from pymarc import Record, WriteNeedsRecord


class Writer(object):

    def write(self, record):
        pass

    def close(self):
        pass


class MARCWriter(Writer):
    """
    A class for writing MARC21 records in transmission format.

    Simple usage:

        from pymarc import MARCWriter

        ## pass in a file
        writer = MARCWriter(file('file.dat','w'))
        writer.write(record)

        ## use StringIO if you want to write to a string
        string = StringIO()
        writer = MARCWriter(string)
        writer.write(record)
        print string
    """

    def __init__(self, file_handle, own_file_handle = True):
        """
        You need to pass in a file like object.

        If own_file_handle is True (the default) then the file handle will be
        closed when the writer is closed. Otherwise the file handle will be
        left open.
        """
        super(MARCWriter, self).__init__()
        self.file_handle = file_handle
        self.own_file_handle = own_file_handle

    def write(self, record):
        """
        Writes a record.
        """
        if not isinstance(record, Record):
            raise WriteNeedsRecord
        self.file_handle.write(record.as_marc())

    def close(self):
        """
        Closes the file.

        If own_file_handle is True, also closes the file handle.
        """
        if self.own_file_handle:
            self.file_handle.close()
        self.file_handle = None


class TextWriter(Writer):
    """
    A class for writing records in prettified text MARCMaker format.

    A blank line separates each record.

    Simple usage:

        from pymarc import TextWriter

        ## pass in a file
        writer = TextWriter(open('file.dat','wt'))
        writer.write(record)
        writer.close()

        ## use StringIO if you want to write to a string
        string = StringIO()
        writer = MARCWriter(string, own_file_handle = False)
        writer.write(record)
        writer.close()
        print string
    """

    def __init__(self, file_handle, own_file_handle = True):
        """
        You need to pass in a file like object.

        If own_file_handle is True (the default) then the file handle will be
        closed when the writer is closed. Otherwise the file handle will be
        left open.
        """
        super(TextWriter, self).__init__()
        self.file_handle = file_handle
        self.own_file_handle = own_file_handle
        self.write_count = 0

    def write(self, record):
        """
        Writes a record.
        """
        if not isinstance(record, Record):
            raise WriteNeedsRecord
        if self.write_count > 0:
            self.file_handle.write('\n')
        self.file_handle.write(str(record))
        self.write_count += 1

    def close(self):
        """
        Closes the file.

        If own_file_handle is True, also closes the file handle.
        """
        if self.own_file_handle:
            self.file_handle.close()
        self.file_handle = None
