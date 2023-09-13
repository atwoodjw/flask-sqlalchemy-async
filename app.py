import asyncio
import os

from flask import Flask, jsonify
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models import db

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
QUERY = "SELECT SLEEP(1)"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)


async def get_async(query, async_session):
    async with async_session() as session:
        results = await session.execute(text(query))

        return [row[0] for row in results.all()]


async def get_async_flask_sqlalchemy(query):
    results = await db.session.execute(text(query))

    return [row[0] for row in results.all()]


@app.route("/")
async def root_route():
    async_engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
    async_session = async_sessionmaker(async_engine)

    results = await asyncio.gather(
        get_async(QUERY, async_session),
        get_async(QUERY, async_session),
        get_async(QUERY, async_session),
        get_async(QUERY, async_session),
        get_async(QUERY, async_session),
    )

    await async_engine.dispose()

    return jsonify(results)


@app.route("/flask-sqlalchemy")
async def flask_sqlalchemy_route():
    results = await asyncio.gather(
        get_async_flask_sqlalchemy(QUERY),
        get_async_flask_sqlalchemy(QUERY),
        get_async_flask_sqlalchemy(QUERY),
        get_async_flask_sqlalchemy(QUERY),
        get_async_flask_sqlalchemy(QUERY),
    )

    return jsonify(results)
