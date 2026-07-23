import asyncio
import os
import sys

# Ensure backend path is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.core.database import AsyncSessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.hospital import Hospital
from app.models.user import User
from app.models.round import TrainingRound
from app.models.model_registry import GlobalModel
from app.models.audit import AuditLog


async def ensure_postgres_database_exists():
    from app.core.config import settings
    if settings.SQLALCHEMY_DATABASE_URI.startswith("postgresql"):
        try:
            import asyncpg
            user = settings.POSTGRES_USER
            password = settings.POSTGRES_PASSWORD
            host = settings.POSTGRES_SERVER
            port = settings.POSTGRES_PORT
            target_db = settings.POSTGRES_DB

            conn = await asyncpg.connect(user=user, password=password, host=host, port=port, database="postgres")
            try:
                exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", target_db)
                if not exists:
                    print(f"PostgreSQL database '{target_db}' does not exist. Creating database now...")
                    await conn.execute(f'CREATE DATABASE "{target_db}"')
                    print(f"Created PostgreSQL database '{target_db}' successfully!")
            finally:
                await conn.close()
        except Exception as e:
            print(f"PostgreSQL auto-creation note: {e}")


async def seed():
    await ensure_postgres_database_exists()
    print("Initializing Database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        print("Seeding Consortium Hospital Edge Nodes...")
        hospitals_data = [
            {
                "name": "St. Jude Children's Research Hospital",
                "code": "HOSP_STJUDE",
                "dataset_sample_count": 1500,
                "location": "Memphis, TN, USA",
                "status": "ACTIVE"
            },
            {
                "name": "Mayo Clinic Diagnostic Center",
                "code": "HOSP_MAYO",
                "dataset_sample_count": 2200,
                "location": "Rochester, MN, USA",
                "status": "ACTIVE"
            },
            {
                "name": "Johns Hopkins Medicine",
                "code": "HOSP_JOHNS_HOPKINS",
                "dataset_sample_count": 1800,
                "location": "Baltimore, MD, USA",
                "status": "ACTIVE"
            }
        ]

        hospitals = []
        for h_data in hospitals_data:
            h = Hospital(
                name=h_data["name"],
                code=h_data["code"],
                api_key_hash=get_password_hash(f"key_{h_data['code']}"),
                dataset_sample_count=h_data["dataset_sample_count"],
                location=h_data["location"],
                status=h_data["status"],
                is_verified=True
            )
            db.add(h)
            hospitals.append(h)

        await db.commit()

        print("Seeding System Administrator & Consortium Auditor...")
        admin_user = User(
            email="admin@consortium.health",
            password_hash=get_password_hash("AdminPass2026!"),
            full_name="Dr. Sarah Jenkins",
            role="SYSTEM_ADMIN",
            is_active=True
        )
        db.add(admin_user)
        await db.commit()

        print("Seeding Baseline Model & Round #1...")
        round1 = TrainingRound(
            round_number=1,
            status="COMPLETED",
            target_accuracy=0.95,
            min_clients=2,
            participating_clients_count=3,
            current_accuracy=0.885,
            current_loss=0.182
        )
        db.add(round1)
        await db.commit()
        await db.refresh(round1)

        global_m1 = GlobalModel(
            round_id=round1.id,
            version="v1.0.0",
            s3_storage_path="s3://fl-model-registry/global_models/global_v1.1.0.pt",
            accuracy=0.885,
            loss=0.182,
            f1_score=0.871,
            metrics_summary={"total_samples": 5500, "dp_epsilon": 0.45}
        )
        db.add(global_m1)

        audit = AuditLog(
            user_id=admin_user.id,
            action="INITIAL_SEED_COMPLETE",
            resource_type="SYSTEM",
            details={"seeded_hospitals": len(hospitals_data)}
        )
        db.add(audit)

        await db.commit()
        print("✅ Database seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
