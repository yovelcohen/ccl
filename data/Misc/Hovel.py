from io import StringIO
import difflib


class PiecesDiffTool:
    SPECIAL_DIFF_FIELDS = ("requirements", "description", "dateUpdated", "version",)
    TABLE_FMT = '%20s|%50s|%50s'

    @classmethod
    def get_diffs(cls, o1, o2, shortdesc1, shortdesc2):
        table_diffs = []
        all_keys = set(o1.snapshot).union(o2.snapshot).difference(cls.SPECIAL_DIFF_FIELDS)
        for k in all_keys:
            if k not in o1.snapshot or k not in o2.snapshot:
                continue

            v1 = o1.snapshot.get(k)
            v2 = o2.snapshot.get(k)
            if v1 == v2 or (not v1 and not v2):
                continue
            table_diffs.append((k, cls.format_value(k, v1), cls.format_value(k, v2)))

        requirement_diff = []
        description_diff = []
        if 'requirements' in o1.snapshot and 'requirements' in o2.snapshot:
            req1, req2 = [list(cls.requirements_as_texts(o.snapshot['requirements'])) for o in (o1, o2)]
            requirement_diff = difflib.unified_diff(req1, req2,
                                                    shortdesc1, shortdesc2,
                                                    n=5, lineterm='')

        if 'description' in o1.snapshot and 'description' in o2.snapshot:
            description_diff = difflib.unified_diff(o1.snapshot['description'].splitlines(),
                                                    o2.snapshot['description'].splitlines(),
                                                    shortdesc1,
                                                    shortdesc2,
                                                    n=5, lineterm='')

        return table_diffs, requirement_diff, description_diff

    @classmethod
    def shortdesc(cls, o):
        return '%s @ %s' % ((o.editor.first_name or o.editor.email) if o.editor else '?', o.date_created,)

    @classmethod
    def diff(cls, o1, o2):
        shortdesc1, shortdesc2 = [cls.shortdesc(o) for o in (o1, o2)]

        out = StringIO()
        table_diffs, requirement_diff, description_diff = cls.get_diffs(o1, o2, shortdesc1, shortdesc2)
        if table_diffs:
            print(cls.TABLE_FMT % ("Key", "New (%s)" % (shortdesc1,), "Old (%s)" % (shortdesc2,),), file=out)
            print(cls.TABLE_FMT % ("===========", "=========", "==========",), file=out)
            for key, val1, val2 in table_diffs:
                print(cls.TABLE_FMT % (key, val1, val2,), file=out)

        print("\n============\nDescription:\n===========\n", file=out)
        for l in description_diff:
            print(l, file=out)

        print("\n============\nRequirements:\n===========\n", file=out)
        for l in requirement_diff:
            print(l, file=out)

        return out.getvalue()

    @classmethod
    def format_value(cls, key, val):
        if val is None:
            return '(null)'
        pass

    @classmethod
    def requirements_as_texts(cls, requirements):
        for section in requirements:
            yield "=== %s ===" % (section['heading'],)
            for bullet in section.get('bullets', []):
                yield '* %s' % (bullet['text'],)
            yield ''
