import json
from typing import Dict, Any

def get_user_context(session, user_id: int) -> Dict[str, Any]:
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user and user.context:
        return json.loads(user.context)
    return {}

def update_user_context(session, user_id: int, new_context: Dict[str, Any]):
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user:
        current_context = get_user_context(session, user_id)
        current_context.update(new_context)
        user.context = json.dumps(current_context)
        session.commit()