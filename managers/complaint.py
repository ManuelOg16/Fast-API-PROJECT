from db import database
from models import complaint, RoleType, State


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            print(complaint.c.status)
            q = q.where(complaint.c.status == State.pending)
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data, user):
        data = complaint_data.dict()
        print(data)
        data["complainer_id"] = user["id"]
        id_ = await database.execute(complaint.insert().values(**data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(id_):
        await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.approved))

    @staticmethod
    async def reject(id_):
        await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.rejected))
