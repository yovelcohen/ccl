from neomodel import StructuredRel, StringProperty, DateTimeProperty


class MetaRelationshipMixin:
    date_added = DateTimeProperty()
    added = StringProperty(default='model')
    adding_person_id = StringProperty()

    def save(self):
        if self.added != 'model':
            if not self.adding_person_id:
                raise KeyError("if added by a user than they're id must be provided")
        super(MetaRelationshipMixin, self).save()


class CompanyIndustries(StructuredRel, MetaRelationshipMixin):
    pass


class CompanyLocations(StructuredRel, MetaRelationshipMixin):
    type = StringProperty()


class CompanyPieces(StructuredRel, MetaRelationshipMixin):
    pass
