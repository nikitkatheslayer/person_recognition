from db.orm import AsyncORM

async def add_action(user, action, **kwargs):
    is_result = kwargs.get("is_result")
    file_id = kwargs.get("file_id")
    file_ext = kwargs.get("file_ext")
    action_info = kwargs.get("action_info")

    match is_result:
        case True:
            filename = f"{file_id}_detected{file_ext}"
            await AsyncORM.add_action(user, action, filename)
        case False:
            filename = f"{file_id}{file_ext}"
            await AsyncORM.add_action(user, action, filename)
        case None:
            await AsyncORM.add_action(user, action, action_info)

