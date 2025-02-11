import asyncio
import json
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.word import Word
from app.models.group import Group
from app.db.base import Base, engine, AsyncSessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json_data(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'seed', filename)
    with open(file_path, 'r') as f:
        return json.load(f)

async def seed_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop all tables first
        await conn.run_sync(Base.metadata.create_all)  # Create tables from scratch
    
    try:
        async with AsyncSessionLocal() as session:
            # Create groups
            groups = {
                "adjectives": Group(name="Adjectives", words_count=0),
                "verbs": Group(name="Verbs", words_count=0)
            }
            
            for group in groups.values():
                session.add(group)
            await session.commit()
            
            # Load and add adjectives
            adjectives = load_json_data('data_adjectives.json')
            for adj_data in adjectives:
                word = Word(
                    kanji=adj_data['kanji'],
                    romaji=adj_data['romaji'],
                    english=adj_data['english'],
                    parts=json.dumps(adj_data['parts']),
                    group_id=groups['adjectives'].id
                )
                session.add(word)
                groups['adjectives'].words_count += 1
            
            # Load and add verbs
            verbs = load_json_data('data_verbs.json')
            for verb_data in verbs:
                word = Word(
                    kanji=verb_data['kanji'],
                    romaji=verb_data['romaji'],
                    english=verb_data['english'],
                    parts=json.dumps(verb_data['parts']),
                    group_id=groups['verbs'].id
                )
                session.add(word)
                groups['verbs'].words_count += 1
            
            await session.commit()
            logger.info("Database seeded successfully")
            
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(seed_database())
