# -*- coding: utf-8 -*-
from datetime import datetime
from pynamodb.attributes import (
    MapAttribute, UnicodeAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)
from pynamodb.models import Model

from functions.utils.common import DYNAMO_DB_TABLE_NAME


class BaseModel(Model):

    def to_dict(self):
        ret_dict = {}
        for name, attr in self.get_attributes().items():
            ret_dict[attr.attr_name] = self._attr2obj(getattr(self, name))

        return ret_dict

    def _attr2obj(self, attr):
        if isinstance(attr, set) or isinstance(attr, list):
            _list = []
            for value in attr:
                _list.append(self._attr2obj(value))
            return _list
        elif isinstance(attr, MapAttribute):
            _dict = {}
            for k, v in attr.attribute_values.items():
                _dict[k] = self._attr2obj(v)
            return _dict
        elif isinstance(attr, datetime):
            return attr.isoformat()
        else:
            return attr


class Nest(BaseModel):
    class Meta:
        table_name = DYNAMO_DB_TABLE_NAME

    nestId = UnicodeAttribute(hash_key=True, attr_name='nestId')
    nestComponent = UnicodeAttribute(range_key=True, attr_name='nestComponent')
    name = UnicodeAttribute(attr_name='name')
    owner = UnicodeAttribute(attr_name='owner')
    users = UnicodeSetAttribute(attr_name='users', default=set())
    createdAt = UTCDateTimeAttribute(attr_name='createdAt', default=datetime.now())

    def to_dict(self):
        result = super().to_dict()
        result["stories"] = [story.to_dict() for story in self.get_stories()]
        return(result)

    def get_stories(self):
        return(Story.query(self.nestId, Story.nestComponent.startswith('STORY')))


class Story(BaseModel):
    class Meta:
        table_name = DYNAMO_DB_TABLE_NAME

    nestId = UnicodeAttribute(hash_key=True, attr_name='nestId')
    nestComponent = UnicodeAttribute(range_key=True, attr_name='nestComponent')
    title = UnicodeAttribute(attr_name='title')
    owner = UnicodeAttribute(attr_name='owner', null=True)
    description = UnicodeAttribute(attr_name='description', null=True)
    status = UnicodeAttribute(attr_name='status', default='IDEA')
    createdAt = UTCDateTimeAttribute(attr_name='createdAt', default=datetime.now())

    def to_dict(self):
        result = super().to_dict()
        result["storyId"] = self.nestComponent.split('.')[-1]
        return(result)
