from typing import Literal
from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db
from hr_bot_api.models.db import Poll
from hr_bot_api.schemas.models import PollGet, PollGetAll, PollPost
from hr_bot_api.settings import Settings, get_settings
from auth_lib.fastapi import UnionAuth
from hr_bot_api.exceptions import ObjectNotFound



settings: Settings = get_settings()
poll = APIRouter(prefix="/poll", tags=["Poll"])


@poll.post("", response_model=PollGet)
async def create_poll(poll_info: PollPost, user=Depends(UnionAuth())) -> PollGet:
    """
    Создает опросник в базе данных HRBotApi
    Для создания опросника нужно быть авторизованным и scopes
    """

    new_poll = Poll.create(
        session=db.session,
        **poll_info.model_dump(),
        owner_id=user.get('id'),
    )
    return PollGet.model_validate(new_poll)

@poll.get("/{id}", response_model=PollGet)
async def get_poll(id: int) -> PollGet:
    """
    Возвращает комментарий по его ID в базе данных HRBotApi
    """
    poll: Poll = Poll.query(session=db.session).filter(Poll.id == id).one_or_none()
    # Poll.get(id=id, session=db.session)
    if poll is None:
        raise ObjectNotFound(Poll, id)
    
    return PollGet.model_validate(poll)


# @poll.get("", response_model=Union[CommentGetAll, CommentGetAllWithAllInfo, CommentGetAllWithStatus])
@poll.get("", response_model=PollGetAll)
async def get_comments(
    limit: int = 10,
    offset: int = 0,
    lecturer_id: int | None = None,
    owner_id: int | None = None,
    order_by: list[Literal["create_ts"]] = Query(default=[]),
    user=Depends(UnionAuth(scopes=[], auto_error=False, allow_none=True)),
) -> PollGetAll:
    """
    Scopes: `[]`

    `limit` - максимальное количество возвращаемых комментариев

    `offset` -  смещение, определяющее, с какого по порядку комментария начинать выборку.
    Если без смещения возвращается комментарий с условным номером N,
    то при значении offset = X будет возвращаться комментарий с номером N + X

    `order_by` - возможное значение `'create_ts'` - возвращается список комментариев отсортированных по времени создания

    `owner_id` - вернет все комментарии пользователя с конкретным id
    """
    polls = Poll.query(session=db.session).all()
    # if not comments:
    #     raise ObjectNotFound(Comment, 'all')
    # if "rating.comment.review" in [scope['name'] for scope in user.get('session_scopes')]:
    #     result = CommentGetAllWithAllInfo(limit=limit, offset=offset, total=len(comments))
    #     comment_validator = CommentGetWithAllInfo
    # elif user.get('id') == user_id:
    #     result = CommentGetAllWithStatus(limit=limit, offset=offset, total=len(comments))
    #     comment_validator = CommentGetWithStatus
    # else:
    #     result = CommentGetAll(limit=limit, offset=offset, total=len(comments))
    #     comment_validator = CommentGet
    # result.comments = comments
    # if user_id is not None:
    #     result.comments = [comment for comment in result.comments if comment.user_id == user_id]

    # if lecturer_id is not None:
    #     result.comments = [comment for comment in result.comments if comment.lecturer_id == lecturer_id]

    # if unreviewed:
    #     if not user:
    #         raise ForbiddenAction(Comment)
    #     if "rating.comment.review" in [scope['name'] for scope in user.get('session_scopes')]:
    #         result.comments = [comment for comment in result.comments if comment.review_status is ReviewStatus.PENDING]
    #     else:
    #         raise ForbiddenAction(Comment)
    # else:
    #     result.comments = [comment for comment in result.comments if comment.review_status is ReviewStatus.APPROVED]

    # result.comments = result.comments[offset : limit + offset]

    # if "create_ts" in order_by:
    #     result.comments.sort(key=lambda comment: comment.create_ts, reverse=True)
    # result.total = len(result.comments)
    # result.comments = [comment_validator.model_validate(comment) for comment in result.comments]
    # result.comments.sort(key=lambda comment: comment.create_ts, reverse=True)
    return PollGetAll.model_validate(polls)
