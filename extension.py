from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.session import Session as _Session
from flask_sqlalchemy.session import _app_ctx_id
from sqlalchemy.ext.asyncio import async_engine_from_config, async_scoped_session, async_sessionmaker


class SQLAlchemy(_SQLAlchemy):
    def _make_engine(self, bind_key, options, app):
        return async_engine_from_config(options, prefix="")

    def _make_session_factory(self, options):
        options.setdefault("class_", _Session)
        options.setdefault("query_cls", self.Query)
        return async_sessionmaker(db=self, **options)

    def _make_scoped_session(self, options):
        scope = options.pop("scopefunc", _app_ctx_id)
        factory = self._make_session_factory(options)
        return async_scoped_session(factory, scope)
