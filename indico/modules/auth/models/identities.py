# This file is part of Indico.
# Copyright (C) 2002 - 2015 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from sqlalchemy.dialects.postgresql import JSON
from werkzeug.datastructures import MultiDict

from indico.core.db import db
from indico.util.passwords import PasswordProperty
from indico.util.string import return_ascii


class Identity(db.Model):
    """Identities of Indico users"""
    __tablename__ = 'identities'
    __table_args__ = (db.UniqueConstraint('provider', 'identifier'),
                      {'schema': 'users'})

    #: the unique id of the identity
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #: the id of the user this identity belongs to
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.users.id'),
        nullable=False
    )
    #: the provider name of the identity
    provider = db.Column(
        db.String,
        nullable=False
    )
    #: the unique identifier of the user within its provider
    identifier = db.Column(
        db.String,
        nullable=False
    )
    #: internal data used by the flask-multiauth system
    multiauth_data = db.Column(
        JSON,
        nullable=False
    )
    #: the user data from the user provider
    _data = db.Column(
        'data',
        JSON,
        nullable=False,
        default={}
    )
    #: the hash of the password in case of a local identity
    password_hash = db.Column(
        db.String
    )
    #: the password of the user in case of a local identity
    password = PasswordProperty('password_hash')

    @property
    def data(self):
        data = MultiDict()
        data.update(self._data)
        return data

    @data.setter
    def data(self, data):
        self._data = dict(data.lists())

    @return_ascii
    def __repr__(self):
        return '<Identity({}, {}, {}, {})>'.format(self.id, self.user_id, self.provider, self.identifier)